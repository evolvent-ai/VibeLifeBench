from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ReservationNight:
    date: str
    rate_plan_row_id: int
    nightly_price: int


@dataclass
class SpecialRequest:
    ticket_id: str
    reservation_id: str
    text: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class Reservation:
    reservation_id: str
    confirmation_code: str
    user_id: str
    hotel_id: str
    check_in: str
    check_out: str
    room_type: str
    flavor: str
    status: str
    total_charged: int
    currency: str
    refundable: bool
    refundable_until: Optional[str]
    created_at: str
    updated_at: str
    guest_profile: dict = field(default_factory=dict)
    payment_method_id: str = ""
    nights: List[ReservationNight] = field(default_factory=list)
    special_requests_json: dict = field(default_factory=dict)
