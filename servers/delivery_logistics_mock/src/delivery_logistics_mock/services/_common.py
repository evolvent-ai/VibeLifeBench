"""Shared helpers used by multiple services."""
import json
import sqlite3
from typing import Optional

from ..utils.dates import add_days
from ..utils.exceptions import BadAddressError, BadServiceTypeError, ShipmentNotFoundError
from ..utils.ids import stable_hash_int

VALID_SERVICE_TYPES = ("standard", "express", "same_day")

# Carrier roster — keyed by service type. Each entry: (carrier, service_level).
CARRIER_POOL = {
    "same_day": [
        ("SF Express", "SF Same-Day"),
        ("JD Logistics", "JD Express City"),
    ],
    "express": [
        ("SF Express", "SF Standard Express"),
        ("JD Logistics", "JD Express"),
        ("ZTO Express", "ZTO Express Plus"),
    ],
    "standard": [
        ("ZTO Express", "ZTO Standard"),
        ("JD Logistics", "JD Standard"),
        ("YTO", "YTO Standard"),
        ("STO", "STO Standard"),
    ],
}

# Fee model (in 分). Base fee + per-kg. Tuned so small parcels are
# ~10-30 CNY express, ~6-15 CNY standard.
SERVICE_FEE_BASE_MINOR = {
    "same_day": 2500,    # 25 CNY base
    "express": 1200,     # 12 CNY base
    "standard": 600,     # 6 CNY base
}
SERVICE_FEE_PER_KG_MINOR = {
    "same_day": 800,     # 8 CNY/kg
    "express": 500,      # 5 CNY/kg
    "standard": 200,     # 2 CNY/kg
}

# Default ETA offsets (days) per service type and carrier slot.
DEFAULT_ETA_DAYS = {
    "same_day": 0,
    "express": 2,
    "standard": 4,
}


def validate_service_type(service_type: str) -> None:
    if service_type not in VALID_SERVICE_TYPES:
        raise BadServiceTypeError(
            f"service_type must be one of {VALID_SERVICE_TYPES}, got {service_type!r}"
        )


def validate_address(addr: dict, label: str = "address") -> None:
    if not isinstance(addr, dict):
        raise BadAddressError(f"{label} must be an object")
    for field in ("recipient", "phone", "province", "city", "district", "detail"):
        if not addr.get(field):
            raise BadAddressError(f"{label}.{field} is required")


def address_to_json(addr: dict) -> str:
    """Stable JSON serialization for an address dict (CJK-safe)."""
    return json.dumps(addr, ensure_ascii=False, sort_keys=True)


def address_summary(addr: dict) -> str:
    parts = [addr.get("province", ""), addr.get("city", ""), addr.get("district", "")]
    return "".join(p for p in parts if p)


def fee_for(service_type: str, weight_kg: float) -> int:
    base = SERVICE_FEE_BASE_MINOR[service_type]
    per_kg = SERVICE_FEE_PER_KG_MINOR[service_type]
    weight = max(0.1, float(weight_kg))
    # Round up to nearest 0.1kg for billing realism.
    billable_kg_tenths = int(weight * 10 + 0.999)
    return base + (per_kg * billable_kg_tenths) // 10


def pick_carriers(service_type: str, origin: dict, dest: dict, weight_kg: float) -> list:
    """Deterministically choose 2-3 carrier offers for the given route.

    Hash on the route + service so identical inputs always return the same
    ordered carrier list. ETA shifts slightly per carrier slot.
    """
    pool = CARRIER_POOL[service_type]
    route_hash = stable_hash_int(
        service_type,
        origin.get("city", ""),
        origin.get("district", ""),
        dest.get("city", ""),
        dest.get("district", ""),
        f"{weight_kg:.2f}",
    )
    # Rotate the pool by route hash so different routes get different orderings.
    rot = route_hash % len(pool)
    rotated = pool[rot:] + pool[:rot]
    return rotated[: min(3, len(rotated))]


def eta_for(service_type: str, current_date: str, slot_index: int = 0) -> str:
    base_days = DEFAULT_ETA_DAYS[service_type]
    # Standard carriers in slots 1+ trail by 1 day, express trails by half.
    extra = 0
    if service_type == "standard" and slot_index > 0:
        extra = slot_index  # 0, 1, 2 days extra
    elif service_type == "express" and slot_index > 1:
        extra = 1
    return add_days(current_date, base_days + extra)


def fetch_shipment_row(conn: sqlite3.Connection, *, shipment_id: Optional[str] = None,
                      tracking_no: Optional[str] = None) -> sqlite3.Row:
    """Look up a shipment by id or tracking number; raise SHIPMENT_NOT_FOUND."""
    if shipment_id:
        row = conn.execute(
            "SELECT * FROM shipments WHERE shipment_id = ?", (shipment_id,)
        ).fetchone()
    elif tracking_no:
        row = conn.execute(
            "SELECT * FROM shipments WHERE tracking_no = ?", (tracking_no,)
        ).fetchone()
    else:
        raise ShipmentNotFoundError("either shipment_id or tracking_no required")
    if not row:
        key = shipment_id or tracking_no
        raise ShipmentNotFoundError(f"shipment not found: {key}")
    return row


def fanout_to_subscriptions(
    conn: sqlite3.Connection,
    shipment_id: str,
    event_payload: dict,
    queued_at: str,
) -> int:
    """Queue one notification row per active subscription for the shipment.

    Returns the number of subscriptions queued. Called from the
    pickup/cancel/reschedule/change-address flows.
    """
    subs = conn.execute(
        "SELECT subscription_id FROM status_subscriptions "
        "WHERE shipment_id = ? AND active = 1",
        (shipment_id,),
    ).fetchall()
    payload_json = json.dumps(event_payload, ensure_ascii=False, sort_keys=True)
    for s in subs:
        conn.execute(
            "INSERT INTO notifications_outbox (subscription_id, payload_json, queued_at) "
            "VALUES (?, ?, ?)",
            (s["subscription_id"], payload_json, queued_at),
        )
    return len(subs)
