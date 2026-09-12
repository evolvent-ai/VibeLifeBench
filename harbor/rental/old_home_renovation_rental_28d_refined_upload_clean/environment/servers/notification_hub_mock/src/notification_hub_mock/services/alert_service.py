"""Price alerts: target-price watches on item references."""
import logging
import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadAmountError, BadArgError
from ..utils.ids import alert_id as make_alert_id
from ._common import price_alert_row

logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def create_price_alert(
        self, user_id: str, item_ref: str, target_price_minor: int
    ) -> dict:
        if not user_id or not item_ref:
            raise BadArgError("user_id and item_ref are required")
        if target_price_minor is None or int(target_price_minor) <= 0:
            raise BadAmountError("target_price_minor must be a positive integer")
        seq = next_counter(self.conn, "alert_seq")
        new_id = make_alert_id(seq)
        ts = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO price_alerts
              (alert_id, user_id, item_ref, target_price_minor, currency,
               status, created_at)
            VALUES (?, ?, ?, ?, 'CNY', 'active', ?)
            """,
            (new_id, user_id, item_ref, int(target_price_minor), ts),
        )
        return price_alert_row(self._fetch(new_id))

    def list_price_alerts(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            "SELECT * FROM price_alerts WHERE user_id = ? "
            "ORDER BY created_at ASC, alert_id ASC",
            (user_id,),
        ).fetchall()
        return [price_alert_row(r) for r in rows]

    def _fetch(self, alert_id: str) -> sqlite3.Row:
        return self.conn.execute(
            "SELECT * FROM price_alerts WHERE alert_id = ?", (alert_id,)
        ).fetchone()
