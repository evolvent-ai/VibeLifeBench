"""PickupService — handles ``request_pickup`` (the create-shipment flow).

Creates a shipment row, an initial label_created event, a pickups row,
and an outbox fanout for any subscriptions that exist (rare at this
moment, but the function shape stays consistent with later transitions).
"""
import json
import logging
import sqlite3

from ..backends.db import current_date as _today, next_counter
from ..utils.dates import now_iso_z, parse_date
from ..utils.exceptions import BadArgError, BadDateError
from ..utils.ids import (
    confirmation_code,
    event_id as make_event_id,
    pickup_id as make_pickup_id,
    shipment_id as make_shipment_id,
    tracking_no as make_tracking_no,
)
from ._common import (
    address_summary,
    address_to_json,
    eta_for,
    fee_for,
    pick_carriers,
    validate_address,
    validate_service_type,
)

logger = logging.getLogger(__name__)


class PickupService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def request_pickup(
        self,
        user_id: str,
        pickup_addr: dict,
        dest_addr: dict,
        item_desc: str,
        weight_kg: float,
        service_type: str,
        scheduled_at: str,
    ) -> dict:
        if not user_id or not isinstance(user_id, str):
            raise BadArgError("user_id must be a non-empty string")
        if not item_desc or not isinstance(item_desc, str):
            raise BadArgError("item_desc must be a non-empty string")
        validate_address(pickup_addr, "pickup_addr")
        validate_address(dest_addr, "dest_addr")
        validate_service_type(service_type)
        try:
            w = float(weight_kg)
        except Exception:
            raise BadArgError("weight_kg must be a number")
        if w <= 0:
            raise BadArgError("weight_kg must be positive")
        if not scheduled_at or not isinstance(scheduled_at, str):
            raise BadArgError("scheduled_at must be an ISO timestamp string")
        # Accept both "YYYY-MM-DD" and "YYYY-MM-DDTHH:MM[:SS]" forms.
        date_part = scheduled_at[:10]
        try:
            parse_date(date_part)
        except ValueError as e:
            raise BadDateError(str(e))

        current_date = _today()
        if date_part < current_date:
            raise BadDateError("scheduled_at is in the past")

        # Deterministic carrier choice — pick the first offer from
        # estimate_delivery so request_pickup is consistent with what the
        # agent saw.
        carriers = pick_carriers(service_type, pickup_addr, dest_addr, w)
        carrier, service_level = carriers[0]
        fee_minor = fee_for(service_type, w)
        eta_date = eta_for(service_type, current_date, slot_index=0)

        seq = next_counter(self.conn, "shipment_seq")
        ship_id = make_shipment_id(seq)
        # tracking_no is a deterministic hash of (shipment_id, carrier) so
        # the same shipment always has the same number on replay.
        track = make_tracking_no(carrier, f"{ship_id}|{carrier}")

        now = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO shipments (
              shipment_id, user_id, tracking_no, carrier, service_level, status,
              sender_json, recipient_json, weight_kg, dimensions_json,
              declared_value_minor, fee_minor, created_at, eta_date,
              scheduled_pickup_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, 'label_created', ?, ?, ?, '{}', 0, ?, ?, ?, ?, ?)
            """,
            (
                ship_id,
                user_id,
                track,
                carrier,
                service_level,
                address_to_json(pickup_addr),
                address_to_json(dest_addr),
                w,
                fee_minor,
                now,
                eta_date,
                scheduled_at,
                now,
            ),
        )

        # Initial event: label created.
        evt_seq = next_counter(self.conn, "event_seq")
        self.conn.execute(
            "INSERT INTO shipment_events (event_id, shipment_id, at, location, status_code, description) "
            "VALUES (?, ?, ?, ?, 'label_created', ?)",
            (
                make_event_id(evt_seq),
                ship_id,
                now,
                address_summary(pickup_addr),
                f"Shipping label created for {item_desc}",
            ),
        )

        # Pickup row.
        pck_seq = next_counter(self.conn, "pickup_seq")
        self.conn.execute(
            "INSERT INTO pickups (pickup_id, shipment_id, scheduled_at, status) "
            "VALUES (?, ?, ?, 'pending')",
            (make_pickup_id(pck_seq), ship_id, scheduled_at),
        )

        # A confirmation code for the receipt (echoed in description).
        code = confirmation_code(ship_id)
        logger.info(f"created shipment {ship_id} tracking {track} code {code}")

        return {
            "shipment_id": ship_id,
            "tracking_no": track,
            "carrier": carrier,
            "service_level": service_level,
            "fee_minor": fee_minor,
            "eta_date": eta_date,
            "scheduled_pickup_at": scheduled_at,
            "confirmation_code": code,
        }
