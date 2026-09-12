"""Geocoding (forward + reverse). Token-overlap scoring, haversine NN."""

from __future__ import annotations

import logging
import re
from typing import Optional

from ..backends.sqlite_backend import SqliteBackend
from ..utils.distance import haversine_m

logger = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"[a-z0-9\u3000-\u9fff\u30a0-\u30ff\u3040-\u309f]+", re.UNICODE)


def _tokens(s: str) -> list[str]:
    return _TOKEN_RE.findall((s or "").lower())


class GeocodeService:
    def __init__(self, backend: SqliteBackend):
        self.backend = backend

    # ------------------------------------------------------------------
    def geocode(self, address: str) -> dict:
        if not address or not isinstance(address, str):
            return {"error": "address is required", "code": "INVALID_REQUEST"}

        normalized = " ".join(address.split()).lower()
        tokens = set(_tokens(normalized))

        # "lat,lng" short-circuit
        m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$", address)
        if m:
            return self.reverse_geocode(float(m.group(1)), float(m.group(2)))

        best = None  # (score, row)
        for row in self.backend.list_places():
            name_l = row["name"].lower()
            formatted_l = (row["formatted"] or "").lower()
            # exact-name hit — cap confidence at 1.0
            if name_l == normalized or formatted_l == normalized:
                return self._to_geocode_resp(row, 1.0)

            haystack = f"{row['name']} {row['city']} {row['country']}".lower()
            haystack_tokens = set(_tokens(haystack))
            if not tokens:
                continue
            overlap = tokens & haystack_tokens
            if not overlap:
                continue
            score = len(overlap) / max(len(tokens), 1)
            # Give a small boost if full normalized query is a substring of name
            if normalized and normalized in name_l:
                score = max(score, 0.95)
            if normalized and normalized in formatted_l:
                score = max(score, 0.9)
            if best is None or score > best[0]:
                best = (score, row)

        if best is None or best[0] < 0.5:
            return {"error": "ZERO_RESULTS", "code": "ZERO_RESULTS"}

        score, row = best
        return self._to_geocode_resp(row, round(score, 2))

    def reverse_geocode(self, lat: float, lng: float) -> dict:
        rows = self.backend.list_places()
        if not rows:
            return {
                "place_id": None,
                "formatted": f"{lat}, {lng} (unmapped area)",
                "geo": {"lat": lat, "lng": lng},
                "distance_m": None,
            }
        best_row = None
        best_dist = float("inf")
        for row in rows:
            d = haversine_m((lat, lng), (row["lat"], row["lng"]))
            if d < best_dist:
                best_dist = d
                best_row = row
        if best_row is None or best_dist > 500:
            return {
                "place_id": None,
                "formatted": f"{lat}, {lng} (unmapped area)",
                "geo": {"lat": lat, "lng": lng},
                "distance_m": int(best_dist) if best_row else None,
            }
        return {
            "place_id": best_row["place_id"],
            "formatted": best_row["formatted"],
            "geo": {"lat": best_row["lat"], "lng": best_row["lng"]},
            "distance_m": int(round(best_dist)),
        }

    # ------------------------------------------------------------------
    def resolve(self, anything: str) -> Optional[dict]:
        """Resolve an origin/dest string into a normalized dict.

        Returns {"place_id"|None, "lat", "lng", "formatted", "city", "country"}
        or None if it cannot be resolved.
        """
        if not anything:
            return None
        s = anything.strip()
        # place_id direct hit?
        if s.startswith("pl_"):
            row = self.backend.get_place(s)
            if row is not None:
                return self._to_resolved(row)
        # "lat,lng"
        m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$", s)
        if m:
            rev = self.reverse_geocode(float(m.group(1)), float(m.group(2)))
            if rev.get("place_id"):
                row = self.backend.get_place(rev["place_id"])
                if row is not None:
                    return self._to_resolved(row)
            return {
                "place_id": None,
                "lat": float(m.group(1)),
                "lng": float(m.group(2)),
                "formatted": f"{m.group(1)}, {m.group(2)}",
                "city": "",
                "country": "",
            }
        # fallback: geocode
        g = self.geocode(s)
        if g.get("error"):
            return None
        return {
            "place_id": g["place_id"],
            "lat": g["geo"]["lat"],
            "lng": g["geo"]["lng"],
            "formatted": g["formatted"],
            "city": g.get("city", ""),
            "country": g.get("country", ""),
        }

    # ------------------------------------------------------------------
    @staticmethod
    def _to_geocode_resp(row, confidence: float) -> dict:
        return {
            "place_id": row["place_id"],
            "formatted": row["formatted"],
            "geo": {"lat": row["lat"], "lng": row["lng"]},
            "country": row["country"],
            "city": row["city"],
            "match_confidence": round(float(confidence), 2),
        }

    @staticmethod
    def _to_resolved(row) -> dict:
        return {
            "place_id": row["place_id"],
            "lat": row["lat"],
            "lng": row["lng"],
            "formatted": row["formatted"],
            "city": row["city"],
            "country": row["country"],
        }
