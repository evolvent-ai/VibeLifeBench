from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Address:
    recipient: str
    phone: str
    province: str
    city: str
    district: str
    detail: str
    postal_code: Optional[str] = None


@dataclass
class ShipmentEvent:
    at: str  # ISO timestamp
    location: str
    status_code: str
    description: str


@dataclass
class Shipment:
    shipment_id: str
    user_id: str
    tracking_no: str
    carrier: str
    service_level: str
    status: str
    sender: Address
    recipient: Address
    weight_kg: float
    declared_value_minor: int
    fee_minor: int
    created_at: str
    eta_date: str
    scheduled_pickup_at: Optional[str] = None
    events: List[ShipmentEvent] = field(default_factory=list)
