"""Offer repricing service."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..backends.sqlite_backend import SQLiteBackend
from ..utils import timewin
from ..utils.exceptions import FlightBookingError


def _wall_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class PricingService:
    def __init__(self, backend: SQLiteBackend) -> None:
        self.backend = backend

    def price_offer(self, offer_id: str) -> dict[str, Any]:
        row = self.backend.get_offer(offer_id)
        if not row:
            raise FlightBookingError("offer_not_found", offer_id)

        payload = json.loads(row["payload_json"])
        prev_total = float(payload["total_price"]["amount"])
        currency = payload["total_price"]["currency"]
        paid_pax = int(payload.get("paid_pax") or 1)
        cabin = payload.get("cabin") or "ECONOMY"

        per_leg_total = 0.0
        for seg in payload["segments"]:
            date = timewin.dt_date(seg["depart_dt"])
            bucket = self.backend.get_fare_bucket(seg["flight_no"], date, cabin)
            if not bucket or bucket["seats_remaining"] <= 0:
                raise FlightBookingError(
                    "inventory_gone",
                    f"{seg['flight_no']} {cabin} on {date} sold out",
                )
            per_leg_total += float(bucket["price"])

        new_total = round(per_leg_total * max(1, paid_pax), 2)
        priced_at = _wall_now_iso()
        guarantee_until = timewin.add_minutes(priced_at, 10)
        self.backend.set_offer_pricing(offer_id, new_total, priced_at, guarantee_until)

        change_pct = 0.0 if prev_total == 0 else round(
            (new_total - prev_total) / prev_total * 100, 4)
        return {
            "offer_id": offer_id,
            "priced_total": {"amount": new_total, "currency": currency},
            "previous_total": {"amount": prev_total, "currency": currency},
            "price_changed": new_total != prev_total,
            "change_percent": change_pct,
            "priced_at": priced_at,
            "price_guarantee_until": guarantee_until,
        }
