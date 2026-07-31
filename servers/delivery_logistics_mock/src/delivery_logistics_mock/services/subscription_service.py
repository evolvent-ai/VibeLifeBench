"""SubscriptionService — manage status notification subscriptions."""
import logging
import sqlite3

from ..backends.db import next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import BadArgError, SubscriptionNotFoundError
from ..utils.ids import subscription_id as make_sub_id
from ._common import fetch_shipment_row

logger = logging.getLogger(__name__)

VALID_CHANNELS = ("email", "sms", "webhook")


class SubscriptionService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def subscribe_status(self, tracking_no: str, channel: str, target: str) -> dict:
        if channel not in VALID_CHANNELS:
            raise BadArgError(f"channel must be one of {VALID_CHANNELS}, got {channel!r}")
        if not target or not isinstance(target, str):
            raise BadArgError("target must be a non-empty string")
        row = fetch_shipment_row(self.conn, tracking_no=tracking_no)

        seq = next_counter(self.conn, "subscription_seq")
        sub_id = make_sub_id(seq)
        now = now_iso_z()
        self.conn.execute(
            "INSERT INTO status_subscriptions ("
            "subscription_id, shipment_id, channel, target, active, created_at"
            ") VALUES (?, ?, ?, ?, 1, ?)",
            (sub_id, row["shipment_id"], channel, target, now),
        )
        return {
            "subscription_id": sub_id,
            "shipment_id": row["shipment_id"],
            "tracking_no": tracking_no,
            "channel": channel,
            "target": target,
            "active": True,
            "created_at": now,
        }

    def unsubscribe(self, subscription_id: str) -> dict:
        if not subscription_id or not isinstance(subscription_id, str):
            raise BadArgError("subscription_id must be a non-empty string")
        row = self.conn.execute(
            "SELECT * FROM status_subscriptions WHERE subscription_id = ?",
            (subscription_id,),
        ).fetchone()
        if not row:
            raise SubscriptionNotFoundError(f"subscription not found: {subscription_id}")
        if int(row["active"]) == 0:
            return {
                "subscription_id": subscription_id,
                "active": False,
                "already_inactive": True,
            }
        self.conn.execute(
            "UPDATE status_subscriptions SET active = 0 WHERE subscription_id = ?",
            (subscription_id,),
        )
        return {
            "subscription_id": subscription_id,
            "shipment_id": row["shipment_id"],
            "active": False,
            "deactivated_at": now_iso_z(),
        }
