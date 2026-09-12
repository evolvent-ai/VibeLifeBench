from __future__ import annotations

from pydantic import BaseModel


class LatLng(BaseModel):
    lat: float
    lng: float


class Location(BaseModel):
    geo_key: str
    city: str
    country: str
    lat: float
    lng: float
    timezone: str
    climate_profile_id: str
    kind: str = "city"


def geo_key(city: str) -> str:
    return city.strip().lower().replace(" ", "_")
