from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LatLng:
    lat: float
    lng: float

    def as_dict(self) -> dict:
        return {"lat": self.lat, "lng": self.lng}


@dataclass
class BBox:
    south: float
    west: float
    north: float
    east: float


@dataclass
class Place:
    place_id: str
    name: str
    category: str
    lat: float
    lng: float
    country: str
    city: str
    rating: Optional[float] = None
    price_level: Optional[int] = None
    hours_json: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    formatted: Optional[str] = None


@dataclass
class Step:
    instruction: str
    distance_m: int
    duration_s: int

    def as_dict(self) -> dict:
        return {
            "instruction": self.instruction,
            "distance_m": self.distance_m,
            "duration_s": self.duration_s,
        }


@dataclass
class Leg:
    origin: dict
    dest: dict
    distance_m: int
    duration_s: int
    steps: List[Step] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "origin": self.origin,
            "dest": self.dest,
            "distance_m": self.distance_m,
            "duration_s": self.duration_s,
            "steps": [s.as_dict() for s in self.steps],
        }


@dataclass
class Route:
    summary: str
    distance_m: int
    duration_s: int
    mode: str
    legs: List[Leg] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration_in_traffic_s: Optional[int] = None

    def as_dict(self) -> dict:
        d = {
            "summary": self.summary,
            "distance_m": self.distance_m,
            "duration_s": self.duration_s,
            "mode": self.mode,
            "legs": [leg.as_dict() for leg in self.legs],
            "warnings": list(self.warnings),
        }
        if self.duration_in_traffic_s is not None:
            d["duration_in_traffic_s"] = self.duration_in_traffic_s
        return d
