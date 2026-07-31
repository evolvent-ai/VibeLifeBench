from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class FlightStatus:
    flight_no: str
    date: str
    status: str                # SCHEDULED|DELAYED|BOARDING|DEPARTED|ARRIVED|CANCELLED|DIVERTED
    actual_depart: Optional[str]
    actual_arrive: Optional[str]
    gate: Optional[str]
    terminal: Optional[str]
    delay_min: int
    last_updated: str


@dataclass
class StatusSubscription:
    sub_id: str
    flight_no: str
    date: str
    sink: str
    webhook_url: Optional[str]
    created_at: str


@dataclass
class Notification:
    id: Optional[int]
    created_at: str
    channel: str
    payload: dict
