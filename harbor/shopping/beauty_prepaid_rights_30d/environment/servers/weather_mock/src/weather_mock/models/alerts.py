from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


AlertKind = Literal[
    "typhoon",
    "heatwave",
    "heavy_rain",
    "snow",
    "dust_storm",
    "thunderstorm",
    "flood",
    "advisory",
]

Severity = Literal["info", "advisory", "watch", "warning", "severe"]


SEVERITY_ORDER = ["info", "advisory", "watch", "warning", "severe"]


class Alert(BaseModel):
    alert_id: str
    kind: str
    severity: str
    start: str
    end: str
    areas: list[str]
    description: str


class Subscription(BaseModel):
    subscription_id: str
    geo_key: str
    sink: str
