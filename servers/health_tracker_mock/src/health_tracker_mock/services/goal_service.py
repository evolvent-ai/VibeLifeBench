"""Health goal management + progress computation.

A goal is a target on a metric or workout-derived quantity over a period.
``direction`` decides whether more is better (``at_least`` — e.g. weekly run
distance) or less is better (``at_most`` — e.g. target weight).

Progress is computed descriptively from logged data. The server never gives
medical advice — it only reports numbers (see SPEC.md §Safety).
"""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import add_days, parse_date
from ..utils.exceptions import BadPeriodError, BadValueError, GoalNotFoundError
from ..utils.ids import goal_id as make_goal_id

logger = logging.getLogger(__name__)

VALID_PERIODS = ("day", "week", "month", "once")
VALID_DIRECTIONS = ("at_least", "at_most")
VALID_STATUSES = ("active", "achieved", "abandoned")


def _row_to_goal(r: sqlite3.Row) -> dict:
    return {
        "goal_id": r["goal_id"],
        "user_id": r["user_id"],
        "type": r["type"],
        "target": float(r["target"]),
        "unit": r["unit"],
        "period": r["period"],
        "direction": r["direction"],
        "start_date": r["start_date"],
        "status": r["status"],
    }


class GoalService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def set_goal(
        self,
        user_id: str,
        type_: str,
        target: float,
        period: str,
        unit: Optional[str] = None,
        direction: str = "at_least",
        start_date: Optional[str] = None,
    ) -> dict:
        if not user_id:
            raise BadValueError("user_id is required")
        if not type_:
            raise BadValueError("type is required (e.g. weight, run_distance, steps)")
        if target is None:
            raise BadValueError("target is required")
        try:
            target = float(target)
        except (TypeError, ValueError):
            raise BadValueError(f"target must be numeric, got {target!r}")
        if period not in VALID_PERIODS:
            raise BadPeriodError(f"period must be one of {VALID_PERIODS}")
        if direction not in VALID_DIRECTIONS:
            raise BadValueError(f"direction must be one of {VALID_DIRECTIONS}")
        if start_date:
            parse_date(start_date)
        resolved_unit = unit or ""

        seq = next_counter(self.conn, "goal_seq")
        gid = make_goal_id(seq)
        self.conn.execute(
            """
            INSERT INTO goals (goal_id, user_id, type, target, unit, period, direction, start_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """,
            (gid, user_id, type_, target, resolved_unit, period, direction, start_date or "1970-01-01"),
        )
        row = self.conn.execute(
            "SELECT * FROM goals WHERE goal_id = ?", (gid,)
        ).fetchone()
        return _row_to_goal(row)

    def get_goals(self, user_id: str, status: Optional[str] = None) -> List[dict]:
        if not user_id:
            raise BadValueError("user_id is required")
        if status is not None and status not in VALID_STATUSES:
            raise BadValueError(f"status must be one of {VALID_STATUSES}")
        if status:
            rows = self.conn.execute(
                "SELECT * FROM goals WHERE user_id = ? AND status = ? "
                "ORDER BY start_date DESC, goal_id DESC",
                (user_id, status),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM goals WHERE user_id = ? "
                "ORDER BY start_date DESC, goal_id DESC",
                (user_id,),
            ).fetchall()
        return [_row_to_goal(r) for r in rows]

    def get_goal_progress(self, user_id: str, goal_id: str) -> dict:
        """Descriptive progress for a goal over its current period window.

        For ``run_distance`` / ``distance`` goals we sum workout distance; for
        ``steps`` goals we sum the daily-latest steps readings; for ``weight`` /
        ``body_fat`` goals we take the latest metric reading. Returns the raw
        numbers and a boolean ``on_track`` — no advice, no diagnosis.
        """
        if not user_id:
            raise BadValueError("user_id is required")
        row = self.conn.execute(
            "SELECT * FROM goals WHERE goal_id = ? AND user_id = ?",
            (goal_id, user_id),
        ).fetchone()
        if not row:
            raise GoalNotFoundError(
                f"goal not found for user {user_id}: {goal_id}"
            )
        goal = _row_to_goal(row)

        window_start, window_end = self._window(goal["period"], goal["start_date"])
        current = self._measure(user_id, goal, window_start, window_end)
        target = goal["target"]

        if current is None:
            pct = 0.0
            on_track = False
        elif goal["direction"] == "at_least":
            pct = round(100.0 * current / target, 1) if target else 0.0
            on_track = current >= target
        else:  # at_most — lower is better
            on_track = current <= target
            pct = round(100.0 * target / current, 1) if current else 0.0

        return {
            "goal_id": goal["goal_id"],
            "user_id": user_id,
            "type": goal["type"],
            "direction": goal["direction"],
            "period": goal["period"],
            "target": target,
            "unit": goal["unit"],
            "current": current,
            "window_start": window_start,
            "window_end": window_end,
            "percent_of_target": pct,
            "on_track": on_track,
            "status": goal["status"],
        }

    # ---- helpers ---------------------------------------------------------
    def _window(self, period: str, start_date: str):
        """Return the (start, end) date window the progress is measured over.

        The window's end is the latest dated data point for the user across
        metrics+workouts (the server has no clock), and its start is end minus
        the period span. For ``once`` the window spans from the goal start_date
        to the latest data point.
        """
        latest = self.conn.execute(
            """
            SELECT MAX(d) AS d FROM (
              SELECT MAX(substr(recorded_at,1,10)) AS d FROM metrics
              UNION ALL
              SELECT MAX(substr(started_at,1,10)) AS d FROM workouts
            )
            """
        ).fetchone()
        end = latest["d"] if latest and latest["d"] else start_date
        if period == "day":
            return end, end
        if period == "week":
            return add_days(end, -6), end
        if period == "month":
            return add_days(end, -29), end
        # once
        return start_date, end

    def _measure(self, user_id: str, goal: dict, start: str, end: str):
        t = goal["type"].lower()
        if "distance" in t or t in ("run", "running", "cycling"):
            row = self.conn.execute(
                """
                SELECT COALESCE(SUM(distance_m), 0) AS s FROM workouts
                WHERE user_id = ? AND substr(started_at,1,10) >= ?
                  AND substr(started_at,1,10) <= ?
                """,
                (user_id, start, end),
            ).fetchone()
            return float(row["s"])
        if t == "steps":
            rows = self.conn.execute(
                """
                SELECT substr(recorded_at,1,10) AS d, MAX(value) AS v FROM metrics
                WHERE user_id = ? AND type = 'steps'
                  AND substr(recorded_at,1,10) >= ? AND substr(recorded_at,1,10) <= ?
                GROUP BY d
                """,
                (user_id, start, end),
            ).fetchall()
            return float(sum(float(r["v"]) for r in rows))
        if t in ("weight", "body_fat", "heart_rate", "blood_pressure", "sleep_minutes"):
            row = self.conn.execute(
                """
                SELECT value FROM metrics
                WHERE user_id = ? AND type = ?
                  AND substr(recorded_at,1,10) <= ?
                ORDER BY recorded_at DESC, metric_id DESC LIMIT 1
                """,
                (user_id, t, end),
            ).fetchone()
            return float(row["value"]) if row else None
        # workout-count style goal (e.g. type='workouts')
        row = self.conn.execute(
            """
            SELECT COUNT(*) AS c FROM workouts
            WHERE user_id = ? AND substr(started_at,1,10) >= ?
              AND substr(started_at,1,10) <= ?
            """,
            (user_id, start, end),
        ).fetchone()
        return float(row["c"])
