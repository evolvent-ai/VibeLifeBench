"""Derived health alerts.

SAFETY: this service is purely descriptive. It flags readings that fall
outside a *typical* range with neutral wording (e.g. "above typical range").
It NEVER produces a medical diagnosis, severity grade, or any
medication/treatment advice. See SPEC.md §Safety.
"""
import logging
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadValueError
from ._metric_meta import TYPICAL_RANGES

logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_health_alerts(self, user_id: str, limit: int = 50) -> List[dict]:
        """Scan recorded metrics and return descriptive out-of-typical-range
        flags, newest first. Non-diagnostic; informational only."""
        if not user_id:
            raise BadValueError("user_id is required")
        if limit is None or limit < 1:
            raise BadValueError("limit must be >= 1")
        if limit > 200:
            limit = 200

        ranged_types = [t for t, rng in TYPICAL_RANGES.items() if rng is not None]
        placeholders = ", ".join("?" for _ in ranged_types)
        rows = self.conn.execute(
            f"""
            SELECT * FROM metrics
            WHERE user_id = ? AND type IN ({placeholders})
            ORDER BY recorded_at DESC, metric_id DESC
            """,
            (user_id, *ranged_types),
        ).fetchall()

        alerts: List[dict] = []
        for r in rows:
            low, high = TYPICAL_RANGES[r["type"]]
            value = float(r["value"])
            position: Optional[str] = None
            if value < low:
                position = "below_typical_range"
            elif value > high:
                position = "above_typical_range"
            if position is None:
                continue
            alerts.append({
                "metric_id": r["metric_id"],
                "type": r["type"],
                "value": value,
                "value_text": r["value_text"],
                "unit": r["unit"],
                "recorded_at": r["recorded_at"],
                "typical_low": low,
                "typical_high": high,
                "flag": position,
                "note": (
                    f"{r['type']} reading of {r['value_text'] or value} {r['unit']} "
                    f"is {position.replace('_', ' ')} ({low}-{high} {r['unit']}). "
                    f"Informational only; not a diagnosis."
                ),
            })
            if len(alerts) >= limit:
                break
        return alerts
