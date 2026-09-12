from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Amenity:
    key: str
    status: Optional[str] = None


@dataclass
class Hotel:
    hotel_id: str
    name: str
    city: str
    district: Optional[str]
    geo_lat: float
    geo_lng: float
    star_rating: int
    user_rating: float
    user_rating_count: int
    amenities: List[str] = field(default_factory=list)
    address: dict = field(default_factory=dict)
    policies: dict = field(default_factory=dict)
    description: Optional[str] = None
    capacity_estimate: int = 20


@dataclass
class RatePlan:
    rate_plan_row_id: int
    hotel_id: str
    date: str
    room_type: str
    flavor: str
    nightly_price: int
    base_price: int
    currency: str
    inventory_remaining: int
    inventory_capacity: int
    cancellation_policy: str
    refundable_until: Optional[str]
    breakfast_included: bool
    max_occupancy: int
