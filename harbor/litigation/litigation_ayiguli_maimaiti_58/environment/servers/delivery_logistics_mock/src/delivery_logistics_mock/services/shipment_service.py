"""Shipment lifecycle: detail, estimate, reschedule, change address, cancel."""
import json
import logging
import sqlite3
from typing import Optional

from ..backends.db import current_date as _today, next_counter
from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    BadArgError,
    BadDateError,
    CancelTooLateError,
    InTransitLockedError,
    InvalidStatusForOpError,
)
from ..utils.ids import confirmation_code, event_id as make_event_id
from ._common import (
    address_summary,
    address_to_json,
    eta_for,
    fanout_to_subscriptions,
    fee_for,
    fetch_shipment_row,
    pick_carriers,
    validate_address,
    validate_service_type,
)

logger = logging.getLogger(__name__)

VALID_TIME_WINDOWS = ("morning", "afternoon", "evening", "anytime")
LOCKED_STATUSES_FOR_ADDR = ("in_transit", "out_for_delivery", "delivered",
                            "exception", "returned", "cancelled")
LOCKED_STATUSES_FOR_CANCEL = ("in_transit", "out_for_delivery", "delivered",
                              "exception", "returned", "cancelled")
RESCHEDULE_ALLOWED = ("in_transit", "out_for_delivery", "exception")


def _shipment_dict(conn: sqlite3.Connection, row: sqlite3.Row) -> dict:
    sender = json.loads(row["sender_json"])
    recipient = json.loads(row["recipient_json"])
    dims = json.loads(row["dimensions_json"]) if row["dimensions_json"] else {}
    events = conn.execute(
        "SELECT at, location, status_code, description FROM shipment_events "
        "WHERE shipment_id = ? ORDER BY at ASC, event_id ASC",
        (row["shipment_id"],),
    ).fetchall()
    subs = conn.execute(
        "SELECT subscription_id, channel, target, active FROM status_subscriptions "
        "WHERE shipment_id = ? ORDER BY created_at ASC",
        (row["shipment_id"],),
    ).fetchall()
    return {
        "shipment_id": row["shipment_id"],
        "user_id": row["user_id"],
        "tracking_no": row["tracking_no"],
        "carrier": row["carrier"],
        "service_level": row["service_level"],
        "status": row["status"],
        "sender": sender,
        "recipient": recipient,
        "weight_kg": float(row["weight_kg"]),
        "dimensions": dims,
        "declared_value_minor": int(row["declared_value_minor"]),
        "fee_minor": int(row["fee_minor"]),
        "created_at": row["created_at"],
        "eta_date": row["eta_date"],
        "scheduled_pickup_at": row["scheduled_pickup_at"],
        "origin": address_summary(sender),
        "destination": address_summary(recipient),
        "cancel_reason": row["cancel_reason"],
        "events": [
            {
                "at": e["at"],
                "location": e["location"],
                "status_code": e["status_code"],
                "description": e["description"],
            }
            for e in events
        ],
        "subscriptions": [
            {
                "subscription_id": s["subscription_id"],
                "channel": s["channel"],
                "target": s["target"],
                "active": bool(s["active"]),
            }
            for s in subs
        ],
    }


def _insert_event(
    conn: sqlite3.Connection,
    shipment_id: str,
    at: str,
    location: str,
    status_code: str,
    description: str,
) -> None:
    seq = next_counter(conn, "event_seq")
    conn.execute(
        "INSERT INTO shipment_events (event_id, shipment_id, at, location, status_code, description) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (make_event_id(seq), shipment_id, at, location, status_code, description),
    )


class ShipmentService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    def get_shipment(self, shipment_id: str) -> dict:
        if not shipment_id or not isinstance(shipment_id, str):
            raise BadArgError("shipment_id must be a non-empty string")
        row = fetch_shipment_row(self.conn, shipment_id=shipment_id)
        return _shipment_dict(self.conn, row)

    # ------------------------------------------------------------------
    # Estimate (no DB writes)
    # ------------------------------------------------------------------
    def estimate_delivery(
        self,
        origin_addr: dict,
        dest_addr: dict,
        weight_kg: float,
        service_type: str,
    ) -> dict:
        validate_address(origin_addr, "origin_addr")
        validate_address(dest_addr, "dest_addr")
        validate_service_type(service_type)
        try:
            w = float(weight_kg)
        except Exception:
            raise BadArgError("weight_kg must be a number")
        if w <= 0:
            raise BadArgError("weight_kg must be positive")

        current_date = _today()
        offers = []
        for i, (carrier, service_level) in enumerate(
            pick_carriers(service_type, origin_addr, dest_addr, w)
        ):
            offers.append(
                {
                    "carrier": carrier,
                    "service_level": service_level,
                    "eta_date": eta_for(service_type, current_date, slot_index=i),
                    "fee_minor": fee_for(service_type, w),
                }
            )
        return {
            "service_type": service_type,
            "weight_kg": w,
            "origin": address_summary(origin_addr),
            "destination": address_summary(dest_addr),
            "offers": offers,
        }

    # ------------------------------------------------------------------
    # Reschedule
    # ------------------------------------------------------------------
    def reschedule_delivery(self, tracking_no: str, new_date: str, time_window: str) -> dict:
        if time_window not in VALID_TIME_WINDOWS:
            raise BadArgError(f"time_window must be one of {VALID_TIME_WINDOWS}")
        from ..utils.dates import parse_date
        try:
            parse_date(new_date)
        except ValueError as e:
            raise BadDateError(str(e))

        row = fetch_shipment_row(self.conn, tracking_no=tracking_no)
        if row["status"] not in RESCHEDULE_ALLOWED:
            raise InvalidStatusForOpError(
                f"reschedule not allowed in status {row['status']!r}"
            )
        current_date = _today()
        if new_date < current_date:
            raise BadDateError("new_date is in the past")

        code = confirmation_code(f"{row['shipment_id']}|{new_date}|{time_window}")
        now = now_iso_z()
        self.conn.execute(
            "UPDATE shipments SET eta_date = ?, updated_at = ? WHERE shipment_id = ?",
            (new_date, now, row["shipment_id"]),
        )
        loc = address_summary(json.loads(row["recipient_json"]))
        _insert_event(
            self.conn,
            row["shipment_id"],
            now,
            loc,
            "reschedule",
            f"Delivery rescheduled to {new_date} ({time_window}); ref {code}",
        )
        fanout_to_subscriptions(
            self.conn,
            row["shipment_id"],
            {
                "kind": "reschedule",
                "tracking_no": tracking_no,
                "new_eta_date": new_date,
                "time_window": time_window,
                "confirmation_code": code,
            },
            now,
        )
        return {
            "tracking_no": tracking_no,
            "new_eta_date": new_date,
            "time_window": time_window,
            "confirmation_code": code,
        }

    # ------------------------------------------------------------------
    # Change address
    # ------------------------------------------------------------------
    def change_address(self, tracking_no: str, new_address: dict) -> dict:
        validate_address(new_address, "new_address")
        row = fetch_shipment_row(self.conn, tracking_no=tracking_no)
        if row["status"] in LOCKED_STATUSES_FOR_ADDR:
            raise InTransitLockedError(
                f"address change locked once shipment is {row['status']!r}"
            )
        # Only allowed in label_created or picked_up.
        if row["status"] not in ("label_created", "picked_up"):
            raise InvalidStatusForOpError(
                f"address change not allowed in status {row['status']!r}"
            )

        now = now_iso_z()
        self.conn.execute(
            "UPDATE shipments SET recipient_json = ?, updated_at = ? WHERE shipment_id = ?",
            (address_to_json(new_address), now, row["shipment_id"]),
        )
        _insert_event(
            self.conn,
            row["shipment_id"],
            now,
            address_summary(new_address),
            "address_changed",
            f"Recipient address updated by sender",
        )
        fanout_to_subscriptions(
            self.conn,
            row["shipment_id"],
            {
                "kind": "address_changed",
                "tracking_no": tracking_no,
                "destination": address_summary(new_address),
                "new_eta_date": row["eta_date"],
            },
            now,
        )
        updated = fetch_shipment_row(self.conn, shipment_id=row["shipment_id"])
        return _shipment_dict(self.conn, updated)

    # ------------------------------------------------------------------
    # Cancel
    # ------------------------------------------------------------------
    def cancel_shipment(self, tracking_no: str, reason: str) -> dict:
        if not reason or not isinstance(reason, str):
            raise BadArgError("reason must be a non-empty string")
        row = fetch_shipment_row(self.conn, tracking_no=tracking_no)
        if row["status"] in LOCKED_STATUSES_FOR_CANCEL:
            raise CancelTooLateError(
                f"cannot cancel in status {row['status']!r}"
            )
        if row["status"] not in ("label_created", "picked_up"):
            raise InvalidStatusForOpError(
                f"cancel not allowed in status {row['status']!r}"
            )

        now = now_iso_z()
        self.conn.execute(
            "UPDATE shipments SET status = 'cancelled', cancel_reason = ?, updated_at = ? "
            "WHERE shipment_id = ?",
            (reason, now, row["shipment_id"]),
        )
        # Also mark any pending pickup as cancelled.
        self.conn.execute(
            "UPDATE pickups SET status = 'cancelled' WHERE shipment_id = ? AND status = 'pending'",
            (row["shipment_id"],),
        )
        loc = address_summary(json.loads(row["sender_json"]))
        _insert_event(
            self.conn,
            row["shipment_id"],
            now,
            loc,
            "cancelled",
            f"Shipment cancelled by sender: {reason}",
        )
        fanout_to_subscriptions(
            self.conn,
            row["shipment_id"],
            {
                "kind": "cancelled",
                "tracking_no": tracking_no,
                "reason": reason,
            },
            now,
        )
        return {
            "tracking_no": tracking_no,
            "shipment_id": row["shipment_id"],
            "status": "cancelled",
            "reason": reason,
            "cancelled_at": now,
        }


# Re-exported for admin module use.
insert_event = _insert_event
shipment_dict = _shipment_dict
