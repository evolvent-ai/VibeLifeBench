from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Flight:
    flight_no: str
    origin: str
    dest: str
    depart_dt: str          # ISO-8601 with offset
    arrive_dt: str
    equipment: str
    base_price: float
    currency: str
    carrier: str


@dataclass
class FareBucket:
    flight_no: str
    date: str               # YYYY-MM-DD
    cabin: str
    price: float
    seats_remaining: int


@dataclass
class SegmentRef:
    segment_idx: int
    flight_no: str
    origin: str
    destination: str
    depart_dt: str
    arrive_dt: str
    cabin: str
    equipment: str
