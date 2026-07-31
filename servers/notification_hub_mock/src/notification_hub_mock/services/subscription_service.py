"""Cross-platform subscriptions: list / get / create / update / lifecycle."""
import json
import logging
import sqlite3
from typing import Any, List, Optional, Union

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    BadArgError,
    BadTypeError,
    SubscriptionNotFoundError,
)
from ..utils.ids import subscription_id as make_subscription_id
from ._common import subscription_row

logger = logging.getLogger(__name__)

VALID_TYPES = (
    "price_drop", "restock", "policy_update",
    "new_content", "price_target", "keyword",
)
VALID_STATUS = ("active", "paused", "deleted")


class SubscriptionService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list / get ------------------------------------------------------
    def list_subscriptions(
        self, user_id: str, status: Optional[str] = None
    ) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        if status is not None and status not in VALID_STATUS:
            raise BadArgError(f"status must be one of {VALID_STATUS}")
        sql = ["SELECT * FROM subscriptions WHERE user_id = ?"]
        args: List = [user_id]
        if status:
            sql.append("AND status = ?")
            args.append(status)
        else:
            sql.append("AND status != 'deleted'")
        sql.append("ORDER BY created_at ASC, subscription_id ASC")
        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [subscription_row(r) for r in rows]

    def get_subscription(self, subscription_id: str) -> dict:
        return subscription_row(self._fetch(subscription_id))

    # ---- create ----------------------------------------------------------
    def create_subscription(
        self,
        user_id: str,
        source: str,
        type: str,
        target: str,
        condition_json: Optional[Union[str, dict]] = None,
    ) -> dict:
        if not user_id or not source or not target:
            raise BadArgError("user_id, source, target are all required")
        if type not in VALID_TYPES:
            raise BadTypeError(f"type must be one of {VALID_TYPES}")
        cond = self._normalize_condition(condition_json)
        seq = next_counter(self.conn, "subscription_seq")
        new_id = make_subscription_id(seq)
        ts = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO subscriptions
              (subscription_id, user_id, source, type, target, condition_json,
               status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
            """,
            (new_id, user_id, source, type, target, cond, ts, ts),
        )
        return subscription_row(self._fetch(new_id))

    # ---- update ----------------------------------------------------------
    def update_subscription(
        self,
        subscription_id: str,
        target: Optional[str] = None,
        condition_json: Optional[Union[str, dict]] = None,
        source: Optional[str] = None,
    ) -> dict:
        self._fetch(subscription_id)  # raises if missing
        sets: List[str] = []
        args: List = []
        if target is not None:
            sets.append("target = ?")
            args.append(target)
        if source is not None:
            sets.append("source = ?")
            args.append(source)
        if condition_json is not None:
            sets.append("condition_json = ?")
            args.append(self._normalize_condition(condition_json))
        if not sets:
            raise BadArgError(
                "at least one of target, source, condition_json must be set"
            )
        sets.append("updated_at = ?")
        args.append(now_iso_z())
        args.append(subscription_id)
        self.conn.execute(
            f"UPDATE subscriptions SET {', '.join(sets)} WHERE subscription_id = ?",
            args,
        )
        return subscription_row(self._fetch(subscription_id))

    # ---- lifecycle -------------------------------------------------------
    def pause_subscription(self, subscription_id: str) -> dict:
        return self._set_status(subscription_id, "paused")

    def resume_subscription(self, subscription_id: str) -> dict:
        return self._set_status(subscription_id, "active")

    def delete_subscription(self, subscription_id: str) -> dict:
        return self._set_status(subscription_id, "deleted")

    # ---- internals -------------------------------------------------------
    def _set_status(self, subscription_id: str, status: str) -> dict:
        self._fetch(subscription_id)
        self.conn.execute(
            "UPDATE subscriptions SET status = ?, updated_at = ? "
            "WHERE subscription_id = ?",
            (status, now_iso_z(), subscription_id),
        )
        return subscription_row(self._fetch(subscription_id))

    def _fetch(self, subscription_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM subscriptions WHERE subscription_id = ?",
            (subscription_id,),
        ).fetchone()
        if not row:
            raise SubscriptionNotFoundError(
                f"subscription not found: {subscription_id}"
            )
        return row

    @staticmethod
    def _normalize_condition(
        condition_json: Optional[Union[str, dict]]
    ) -> Optional[str]:
        """Validate condition_json and store canonical JSON text.

        Accepts either a JSON string or an already-parsed object/dict (MCP
        clients sometimes coerce JSON-looking strings into objects before the
        call reaches the server).
        """
        if condition_json is None:
            return None
        obj: Any
        if isinstance(condition_json, str):
            try:
                obj = json.loads(condition_json)
            except (ValueError, TypeError) as e:
                raise BadArgError(f"condition_json must be valid JSON: {e}")
        else:
            obj = condition_json
        return json.dumps(obj, ensure_ascii=False)
