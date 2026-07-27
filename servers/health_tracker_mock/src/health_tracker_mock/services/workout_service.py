"""Workout logging + querying + per-day activity summary."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import date_of, parse_date, parse_ts
from ..utils.exceptions import BadValueError, WorkoutNotFoundError
from ..utils.ids import workout_id as make_workout_id

logger = logging.getLogger(__name__)


def _row_to_workout(r: sqlite3.Row) -> dict:
    return {
        "workout_id": r["workout_id"],
        "user_id": r["user_id"],
        "type": r["type"],
        "duration_min": int(r["duration_min"]),
        "calories": int(r["calories"]) if r["calories"] is not None else None,
        "distance_m": int(r["distance_m"]) if r["distance_m"] is not None else None,
        "started_at": r["started_at"],
    }


class WorkoutService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- write -----------------------------------------------------------
    def log_workout(
        self,
        user_id: str,
        type_: str,
        duration_min: int,
        started_at: str,
        calories: Optional[int] = None,
        distance_m: Optional[int] = None,
    ) -> dict:
        if not user_id:
            raise BadValueError("user_id is required")
        if not type_:
            raise BadValueError("type is required (e.g. run, gym, cycling, swim, yoga)")
        if duration_min is None or int(duration_min) <= 0:
            raise BadValueError("duration_min must be a positive integer")
        parse_ts(started_at)
        cal = int(calories) if calories is not None else None
        dist = int(distance_m) if distance_m is not None else None
        if cal is not None and cal < 0:
            raise BadValueError("calories must be >= 0")
        if dist is not None and dist < 0:
            raise BadValueError("distance_m must be >= 0")

        seq = next_counter(self.conn, "workout_seq")
        wid = make_workout_id(seq)
        self.conn.execute(
            """
            INSERT INTO workouts (workout_id, user_id, type, duration_min, calories, distance_m, started_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (wid, user_id, type_, int(duration_min), cal, dist, started_at),
        )
        row = self.conn.execute(
            "SELECT * FROM workouts WHERE workout_id = ?", (wid,)
        ).fetchone()
        return _row_to_workout(row)

    # ---- read ------------------------------------------------------------
    def list_workouts(
        self,
        user_id: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 100,
    ) -> List[dict]:
        if not user_id:
            raise BadValueError("user_id is required")
        if limit is None or limit < 1:
            raise BadValueError("limit must be >= 1")
        if limit > 500:
            limit = 500
        if since:
            parse_date(since)
        if until:
            parse_date(until)

        sql = ["SELECT * FROM workouts WHERE user_id = ?"]
        args: List = [user_id]
        if since:
            sql.append("AND substr(started_at, 1, 10) >= ?")
            args.append(since)
        if until:
            sql.append("AND substr(started_at, 1, 10) <= ?")
            args.append(until)
        sql.append("ORDER BY started_at DESC, workout_id DESC LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [_row_to_workout(r) for r in rows]

    def get_workout(self, workout_id: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM workouts WHERE workout_id = ?", (workout_id,)
        ).fetchone()
        if not row:
            raise WorkoutNotFoundError(f"workout not found: {workout_id}")
        return _row_to_workout(row)

    def get_activity_summary(self, user_id: str, date: str) -> dict:
        """Aggregate one calendar day: total steps (latest steps reading that
        day), workouts done, total workout duration/calories/distance."""
        if not user_id:
            raise BadValueError("user_id is required")
        parse_date(date)

        steps_row = self.conn.execute(
            """
            SELECT value FROM metrics
            WHERE user_id = ? AND type = 'steps'
              AND substr(recorded_at, 1, 10) = ?
            ORDER BY recorded_at DESC, metric_id DESC LIMIT 1
            """,
            (user_id, date),
        ).fetchone()
        steps = int(steps_row["value"]) if steps_row else 0

        workouts = self.conn.execute(
            """
            SELECT * FROM workouts
            WHERE user_id = ? AND substr(started_at, 1, 10) = ?
            ORDER BY started_at ASC, workout_id ASC
            """,
            (user_id, date),
        ).fetchall()
        wlist = [_row_to_workout(w) for w in workouts]

        total_active_min = sum(w["duration_min"] for w in wlist)
        total_workout_cal = sum(w["calories"] or 0 for w in wlist)
        total_distance_m = sum(w["distance_m"] or 0 for w in wlist)

        return {
            "user_id": user_id,
            "date": date,
            "steps": steps,
            "workout_count": len(wlist),
            "active_minutes": total_active_min,
            "workout_calories": total_workout_cal,
            "distance_m": total_distance_m,
            "workouts": wlist,
        }
