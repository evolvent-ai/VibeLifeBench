"""Places: nearby search + text search + details."""

from __future__ import annotations

import json
import logging
from typing import List, Optional

from ..backends.sqlite_backend import SqliteBackend
from ..utils.distance import haversine_m
from ..utils.validators import validate_category, clamp

logger = logging.getLogger(__name__)


# Category aliases → canonical category
CATEGORY_ALIAS = {
    "ramen": "restaurant",
    "noodles": "restaurant",
    "sushi": "restaurant",
    "kaiseki": "restaurant",
    "food": "restaurant",
    "dining": "restaurant",
    "izakaya": "restaurant",
    "shrine": "shrine",
    "shrines": "shrine",
    "temple": "temple",
    "temples": "temple",
    "museum": "museum",
    "museums": "museum",
    "galleries": "museum",
    "gallery": "museum",
    "train": "station",
    "subway": "station",
    "metro": "station",
    "station": "station",
    "airport": "airport",
    "airports": "airport",
    "hotels": "hotel",
    "ryokan": "hotel",
    "lodging": "hotel",
    "hotel": "hotel",
    "park": "park",
    "parks": "park",
    "garden": "park",
    "shop": "shopping",
    "shopping": "shopping",
    "market": "shopping",
    "viewpoint": "viewpoint",
    "scenic": "viewpoint",
    "observation": "viewpoint",
    # Medical aliases — stage 17 "nearest clinic" etc.
    "clinic": "clinic",
    "clinics": "clinic",
    "hospital": "hospital",
    "hospitals": "hospital",
    "er": "hospital",
    "medical": "clinic",
    "urgent": "clinic",
    "pharmacy": "pharmacy",
    "pharmacies": "pharmacy",
    "drugstore": "pharmacy",
    "attraction": "attraction",
    "attractions": "attraction",
    "sightseeing": "attraction",
}


class PlacesService:
    def __init__(self, backend: SqliteBackend):
        self.backend = backend

    # ------------------------------------------------------------------
    def search(self, query: str, geo: Optional[dict] = None,
               radius_m: int = 5000, category: Optional[str] = None,
               limit: int = 10) -> List[dict]:
        if query is None or not isinstance(query, str):
            raise ValueError("query is required")
        limit = clamp(int(limit or 10), 1, 50)
        radius_m = int(radius_m or 5000)

        q = query.strip().lower()
        cat = validate_category(category) if category else None
        # Try to infer category from query words if not explicitly given
        if cat is None:
            for tok in q.split():
                if tok in CATEGORY_ALIAS:
                    cat = CATEGORY_ALIAS[tok]
                    break

        rows = self.backend.list_places()
        candidates = []
        for row in rows:
            name_l = row["name"].lower()
            if cat and row["category"] != cat:
                # Allow also if alias resolves to same canonical cat
                pass
            # Text match
            matches_text = (
                not q or
                q in name_l or
                any(tok in name_l for tok in q.split()) or
                (cat and row["category"] == cat)
            )
            if cat and row["category"] != cat:
                # Must match category if specified
                continue
            if not matches_text:
                continue
            candidates.append(row)

        # Apply geo filter + sort
        enriched = []
        if geo and isinstance(geo, dict) and "lat" in geo and "lng" in geo:
            center = (float(geo["lat"]), float(geo["lng"]))
            for row in candidates:
                d = haversine_m(center, (row["lat"], row["lng"]))
                if d <= radius_m:
                    enriched.append((d, row))
            enriched.sort(key=lambda x: (x[0], x[1]["place_id"]))
        else:
            for row in candidates:
                enriched.append((None, row))
            enriched.sort(key=lambda x: (
                -1 * (x[1]["rating"] if x[1]["rating"] is not None else 0.0),
                x[1]["name"],
                x[1]["place_id"],
            ))

        results = []
        for (d, row) in enriched[:limit]:
            item = {
                "place_id": row["place_id"],
                "name": row["name"],
                "geo": {"lat": row["lat"], "lng": row["lng"]},
                "category": row["category"],
                "rating": row["rating"],
                "price_level": row["price_level"],
            }
            if d is not None:
                item["distance_m"] = int(round(d))
            results.append(item)
        return results

    # ------------------------------------------------------------------
    def details(self, place_id: str) -> dict:
        row = self.backend.get_place(place_id)
        if row is None:
            return {"error": "NOT_FOUND", "code": "NOT_FOUND"}

        hours = row["hours_json"]
        if hours:
            try:
                hours = json.loads(hours)
            except json.JSONDecodeError:
                hours = None

        reviews = [
            {
                "author": r["author"],
                "rating": r["rating"],
                "text": r["text"],
                "time": r["time"],
            }
            for r in self.backend.list_place_reviews(place_id)
        ]

        # Alerts: look for active transit/road events touching this place
        alerts = self._collect_alerts(row)

        resp = {
            "place_id": row["place_id"],
            "name": row["name"],
            "category": row["category"],
            "geo": {"lat": row["lat"], "lng": row["lng"]},
            "formatted": row["formatted"],
            "country": row["country"],
            "city": row["city"],
            "rating": row["rating"],
            "price_level": row["price_level"],
            "phone": row["phone"],
            "website": row["website"],
            "opening_hours": hours,
            "reviews_sample": reviews,
        }
        if alerts:
            resp["alerts"] = alerts
        return resp

    # ------------------------------------------------------------------
    def _collect_alerts(self, place_row) -> List[dict]:
        """Collect active events that *touch* this specific place.

        SPEC §3.4 says "active transit or road event touching it" — we require
        geometric proximity, not just a city-name match, so that a Gion road
        closure doesn't light up every Tokyo POI the way the earlier
        city-equality heuristic did.
        """
        alerts: List[dict] = []
        place_pt = (place_row["lat"], place_row["lng"])

        # transit events: if the place doubles as a stop, or is close to one
        for ev in self.backend.list_transit_events(only_active=True):
            matched = False
            if ev["stop_id"]:
                stop = self.backend.get_transit_stop(ev["stop_id"])
                if stop is not None:
                    d = haversine_m(place_pt, (stop["lat"], stop["lng"]))
                    if d < 300:
                        matched = True
            if matched:
                alerts.append({
                    "event_id": ev["event_id"],
                    "kind": f"transit_{ev['kind']}",
                    "note": ev["note"],
                    "window": {"start": ev["start_dt"], "end": ev["end_dt"]},
                })

        # road events: only attach if the road polyline passes within ~2 km of
        # the place (so "touching" actually means touching, spec §3.4).
        TOUCH_RADIUS_M = 2000
        for ev in self.backend.list_road_events(only_active=True):
            road = self.backend.get_road(ev["road_id"])
            if road is None:
                continue
            try:
                geom = json.loads(road["geom_json"] or "[]")
            except json.JSONDecodeError:
                geom = []
            if not geom:
                continue
            nearest_m = min(
                (haversine_m(place_pt, (float(pt[0]), float(pt[1]))) for pt in geom),
                default=float("inf"),
            )
            if nearest_m > TOUCH_RADIUS_M:
                continue
            alerts.append({
                "event_id": ev["event_id"],
                "kind": f"road_{ev['kind']}",
                "note": ev["note"],
                "window": {"start": ev["start_dt"], "end": ev["end_dt"]},
                "nearest_m": int(round(nearest_m)),
            })
        return alerts
