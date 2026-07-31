"""Distance / speed helpers. Deterministic, no external deps."""

import math
from typing import Tuple

_EARTH_R_M = 6_371_000.0


def haversine_m(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Great-circle distance between two (lat, lng) points in metres."""
    lat1, lng1 = a
    lat2, lng2 = b
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lng2 - lng1)
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2) ** 2
    return 2 * _EARTH_R_M * math.asin(math.sqrt(h))


def tortuosity_for_mode(mode: str) -> float:
    """Straight-line → road-distance multiplier."""
    return {
        "driving": 1.30,
        "bicycling": 1.25,
        "walking": 1.15,
        "transit": 1.20,
    }.get(mode, 1.30)


def speed_mps(mode: str, intercity: bool) -> float:
    """Approximate travel speed (m/s) for non-transit modes."""
    if mode == "driving":
        kmh = 90.0 if intercity else 40.0
    elif mode == "bicycling":
        kmh = 15.0
    elif mode == "walking":
        kmh = 5.0
    else:
        kmh = 40.0
    return kmh * 1000.0 / 3600.0
