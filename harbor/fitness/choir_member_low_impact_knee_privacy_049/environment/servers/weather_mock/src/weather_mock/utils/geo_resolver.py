from __future__ import annotations

import math
from typing import Any

from .exceptions import InvalidGeo


_ALIASES: dict[str, str] = {
    "tokyo": "tokyo_city",
    "tokyo_city": "tokyo_city",
    "tokyo haneda": "tokyo_hnd",
    "tokyo-haneda": "tokyo_hnd",
    "haneda": "tokyo_hnd",
    "hnd": "tokyo_hnd",
    "tokyo narita": "tokyo_nrt",
    "tokyo-narita": "tokyo_nrt",
    "narita": "tokyo_nrt",
    "nrt": "tokyo_nrt",
    "hakone": "hakone",
    "kyoto": "kyoto_city",
    "kyoto_city": "kyoto_city",
    "osaka": "osaka_city",
    "osaka_city": "osaka_city",
    "osaka kansai": "osaka_kix",
    "osaka kansai intl": "osaka_kix",
    "kansai": "osaka_kix",
    "kix": "osaka_kix",
    "nara": "nara",
    "shanghai": "shanghai",
    "shanghai_city": "shanghai",
    "shanghai pudong": "shanghai_pvg",
    "shanghai pudong intl": "shanghai_pvg",
    "pudong": "shanghai_pvg",
    "pvg": "shanghai_pvg",
}


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    c = 2 * math.asin(min(1.0, math.sqrt(a)))
    return r * c


def resolve_geo(
    geo: Any,
    locations: list[dict],
    max_km: float = 50.0,
) -> dict | None:
    """Resolve ``geo`` (string name or {lat,lng}) to a locations row.

    Returns the matching row dict or None when nothing within ``max_km`` is
    seeded. Raises InvalidGeo on bad input shape.
    """
    by_key = {row["geo_key"]: row for row in locations}
    by_city = {row["city"].lower(): row for row in locations}

    if isinstance(geo, str):
        needle = geo.strip().lower()
        if needle in by_key:
            return by_key[needle]
        if needle in _ALIASES and _ALIASES[needle] in by_key:
            return by_key[_ALIASES[needle]]
        if needle in by_city:
            return by_city[needle]
        return None

    if isinstance(geo, dict):
        lat = geo.get("lat")
        lng = geo.get("lng")
        if lat is None and "latitude" in geo:
            lat = geo["latitude"]
        if lng is None and "longitude" in geo:
            lng = geo["longitude"]
        if lat is None or lng is None:
            raise InvalidGeo("geo dict must contain lat/lng")
        best = None
        best_d = float("inf")
        for row in locations:
            d = _haversine_km(float(lat), float(lng), row["lat"], row["lng"])
            if d < best_d:
                best_d = d
                best = row
        if best is None or best_d > max_km:
            return None
        return best

    raise InvalidGeo("geo must be a string city name or {lat,lng} dict")
