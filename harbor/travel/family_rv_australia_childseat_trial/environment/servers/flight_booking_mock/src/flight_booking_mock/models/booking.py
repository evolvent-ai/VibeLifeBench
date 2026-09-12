from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Passenger:
    type: str                  # ADT|CHD|INF
    given_name: str
    family_name: str
    dob: str
    passport_no: Optional[str] = None
    nationality: Optional[str] = None
    frequent_flyer: Optional[dict[str, str]] = None


@dataclass
class SeatAssignment:
    pnr: str
    segment_idx: int
    pax_idx: int
    seat: str
    checked_in: bool = False
    boarding_pass_id: Optional[str] = None


@dataclass
class Booking:
    pnr: str
    user_id: Optional[str]
    offer_id: str
    status: str                # TICKETED|HOLD|CANCELLED|CHANGED
    paid_amount: float
    currency: str
    created_at: str
    segments: list[dict[str, Any]] = field(default_factory=list)
    passengers: list[dict[str, Any]] = field(default_factory=list)
    contact: dict[str, str] = field(default_factory=dict)
    history: list[dict[str, str]] = field(default_factory=list)
