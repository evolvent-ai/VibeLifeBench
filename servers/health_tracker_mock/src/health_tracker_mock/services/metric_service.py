"""Metric logging + querying: log/get/latest/summary.

Units by type: weight=g, steps=count, heart_rate=bpm, sleep_minutes=min,
blood_pressure=mmHg (numeric value = systolic), body_fat=percent.
"""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import add_days, date_of, parse_date, parse_ts
from ..utils.exceptions import (
    BadPeriodError,
    BadTypeError,
    BadValueError,
    MetricNotFoundError,
)
from ..utils.ids import metric_id as make_metric_id
from ._metric_meta import DEFAULT_UNITS, METRIC_TYPES

logger = logging.getLogger(__name__)

VALID_PERIODS = ("week", "month")


def _row_to_metric(r: sqlite3.Row) -> dict:
    return {
        "metric_id": r["metric_id"],
        "user_id": r["user_id"],
        "type": r["type"],
        "value": float(r["value"]),
        "value_text": r["value_text"],
        "unit": r["unit"],
        "recorded_at": r["recorded_at"],
    }


class MetricService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def _check_type(self, type_: str) -> None:
        if type_ not in METRIC_TYPES:
            raise BadTypeError(f"type must be one of {METRIC_TYPES}")

    # ---- write -----------------------------------------------------------
    def log_metric(
        self,
        user_id: str,
        type_: str,
        value: float,
        recorded_at: str,
        unit: Optional[str] = None,
        value_text: Optional[str] = None,
    ) -> dict:
        if not user_id:
            raise BadValueError("user_id is required")
        self._check_type(type_)
        if value is None:
            raise BadValueError("value is required")
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise BadValueError(f"value must be numeric, got {value!r}")
        parse_ts(recorded_at)  # validates ISO timestamp
        resolved_unit = unit or DEFAULT_UNITS[type_]

        seq = next_counter(self.conn, "metric_seq")
        mid = make_metric_id(seq)
        self.conn.execute(
            """
            INSERT INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (mid, user_id, type_, value, value_text, resolved_unit, recorded_at),
        )
        row = self.conn.execute(
            "SELECT * FROM metrics WHERE metric_id = ?", (mid,)
        ).fetchone()
        return _row_to_metric(row)

    # ---- read ------------------------------------------------------------
    def get_metrics(
        self,
        user_id: str,
        type_: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 100,
    ) -> List[dict]:
        if not user_id:
            raise BadValueError("user_id is required")
        self._check_type(type_)
        if limit is None or limit < 1:
            raise BadValueError("limit must be >= 1")
        if limit > 1000:
            limit = 1000
        if since:
            parse_date(since)
        if until:
            parse_date(until)

        sql = [
            "SELECT * FROM metrics WHERE user_id = ? AND type = ?"
        ]
        args: List = [user_id, type_]
        if since:
            sql.append("AND substr(recorded_at, 1, 10) >= ?")
            args.append(since)
        if until:
            sql.append("AND substr(recorded_at, 1, 10) <= ?")
            args.append(until)
        sql.append("ORDER BY recorded_at DESC, metric_id DESC LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [_row_to_metric(r) for r in rows]

    def get_latest_metric(self, user_id: str, type_: str) -> dict:
        if not user_id:
            raise BadValueError("user_id is required")
        self._check_type(type_)
        row = self.conn.execute(
            """
            SELECT * FROM metrics WHERE user_id = ? AND type = ?
            ORDER BY recorded_at DESC, metric_id DESC LIMIT 1
            """,
            (user_id, type_),
        ).fetchone()
        if not row:
            raise MetricNotFoundError(
                f"no {type_} readings for user {user_id}"
            )
        return _row_to_metric(row)

    def get_metric_summary(self, user_id: str, type_: str, period: str) -> dict:
        """min/max/avg/first/last + trend over the trailing window ending at the
        latest reading. ``period`` ∈ {week (7d), month (30d)}."""
        if not user_id:
            raise BadValueError("user_id is required")
        self._check_type(type_)
        if period not in VALID_PERIODS:
            raise BadPeriodError(f"period must be one of {VALID_PERIODS}")
        span_days = 7 if period == "week" else 30

        latest = self.conn.execute(
            """
            SELECT recorded_at FROM metrics WHERE user_id = ? AND type = ?
            ORDER BY recorded_at DESC, metric_id DESC LIMIT 1
            """,
            (user_id, type_),
        ).fetchone()
        if not latest:
            return {
                "user_id": user_id,
                "type": type_,
                "period": period,
                "count": 0,
                "min": None,
                "max": None,
                "avg": None,
                "first": None,
                "last": None,
                "trend": None,
            }

        end_date = date_of(latest["recorded_at"])
        start_date = add_days(end_date, -(span_days - 1))
        rows = self.conn.execute(
            """
            SELECT value, unit, recorded_at FROM metrics
            WHERE user_id = ? AND type = ?
              AND substr(recorded_at, 1, 10) >= ?
              AND substr(recorded_at, 1, 10) <= ?
            ORDER BY recorded_at ASC, metric_id ASC
            """,
            (user_id, type_, start_date, end_date),
        ).fetchall()

        values = [float(r["value"]) for r in rows]
        unit = rows[0]["unit"] if rows else DEFAULT_UNITS[type_]
        first_v, last_v = values[0], values[-1]
        delta = round(last_v - first_v, 4)
        if delta > 0:
            trend = "up"
        elif delta < 0:
            trend = "down"
        else:
            trend = "flat"
        return {
            "user_id": user_id,
            "type": type_,
            "period": period,
            "window_start": start_date,
            "window_end": end_date,
            "unit": unit,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": round(sum(values) / len(values), 2),
            "first": first_v,
            "last": last_v,
            "delta": delta,
            "trend": trend,
        }
