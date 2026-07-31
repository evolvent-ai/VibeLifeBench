"""Traffic multiplier + estimate."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Iterable, List, Optional, Tuple

from ..backends.sqlite_backend import SqliteBackend
from ..utils.distance import haversine_m
from ..utils.time_utils import parse_iso, city_tz, current_sim_datetime

logger = logging.getLogger(__name__)


# Road polyline endpoints must be within this radius (metres) of either the
# route origin OR the route destination for an intercity road to count as
# "touching" the route. Anything farther away (e.g. a Hanshin closure while
# driving Tokyo→Nagoya) is not on the route.
INTERCITY_TOUCH_RADIUS_M = 60_000.0


class TrafficService:
    def __init__(self, backend: SqliteBackend):
        self.backend = backend

    # ------------------------------------------------------------------
    def current_multiplier(
        self,
        city: str,
        at: datetime,
        *,
        intercity: bool = False,
        origin: Optional[dict] = None,
        dest: Optional[dict] = None,
    ) -> Tuple[float, List[dict]]:
        """Return ``(multiplier, [active_incidents])`` for a driving route.

        Components:
          - ``hour_of_day_curve(city, local_time)``   → [0.0 .. 0.4]
          - active road events *intersecting the route* → sum magnitudes
          - ``weekday_factor``                        → [0.0 .. 0.15]

        The route-intersection check replaces the older "every active event
        in the origin city" heuristic, which wrongly folded every active
        road event into intercity routes (SPEC §3.8 / review §2).
        """
        mult = 1.0
        mult += self._hour_curve(city, at)
        mult += self._weekday_factor(city, at)

        origin_city = (origin or {}).get("city", "")
        dest_city = (dest or {}).get("city", "")
        origin_pt: Optional[Tuple[float, float]] = None
        dest_pt: Optional[Tuple[float, float]] = None
        if origin and "lat" in origin and "lng" in origin:
            origin_pt = (float(origin["lat"]), float(origin["lng"]))
        if dest and "lat" in dest and "lng" in dest:
            dest_pt = (float(dest["lat"]), float(dest["lng"]))

        incidents: List[dict] = []
        for ev in self.backend.list_road_events(only_active=True):
            road = self.backend.get_road(ev["road_id"])
            if road is None:
                continue
            if not self._road_touches_route(
                road,
                city=city,
                intercity=intercity,
                origin_city=origin_city,
                dest_city=dest_city,
                origin_pt=origin_pt,
                dest_pt=dest_pt,
            ):
                continue
            mult += float(ev["magnitude"] or 0.3)
            incidents.append({
                "event_id": ev["event_id"],
                "kind": ev["kind"],
                "road_name": road["name"],
            })
        return mult, incidents

    # ------------------------------------------------------------------
    def estimate(self, origin: dict, dest: dict, base_distance_m: int,
                 base_duration_s: int, depart_at_iso: str | None,
                 current_date_iso: str) -> dict:
        city = origin.get("city") or dest.get("city") or "Tokyo"
        tz = city_tz(city)
        if depart_at_iso:
            dt = parse_iso(depart_at_iso)
        else:
            dt = current_sim_datetime(current_date_iso, "09:00", tz)
        intercity = (origin.get("city") or "") != (dest.get("city") or "") and bool(origin.get("city"))
        mult, incidents = self.current_multiplier(
            city, dt,
            intercity=intercity,
            origin=origin,
            dest=dest,
        )
        with_traffic = int(round(base_duration_s * mult))
        return {
            "origin": origin.get("formatted", ""),
            "destination": dest.get("formatted", ""),
            "distance_m": int(base_distance_m),
            "normal_duration_s": int(base_duration_s),
            "with_traffic_duration_s": with_traffic,
            "severity": self._severity(mult),
            "active_incidents": incidents,
        }

    # ------------------------------------------------------------------
    def _road_touches_route(
        self,
        road,
        *,
        city: str,
        intercity: bool,
        origin_city: str,
        dest_city: str,
        origin_pt: Optional[Tuple[float, float]],
        dest_pt: Optional[Tuple[float, float]],
    ) -> bool:
        road_city = (road["city"] or "").strip()
        rc_lower = road_city.lower()
        is_intercity_road = rc_lower == "intercity"

        # Within-city drive: require road to match the driving city.
        if not intercity:
            return rc_lower == (city or "").lower()

        # Intercity drive: road must either be explicitly intercity, or must
        # match one of the endpoint cities AND its polyline must be near that
        # endpoint (so a Hanshin loop closure in Osaka doesn't poison a
        # Tokyo→Nagoya route just because Osaka sits between them on a map).
        if not is_intercity_road:
            if road_city not in {origin_city, dest_city}:
                return False

        # For both intercity-flagged roads and endpoint-matching local roads,
        # require polyline proximity to at least one endpoint.
        if origin_pt is None and dest_pt is None:
            return True

        try:
            geom = json.loads(road["geom_json"] or "[]")
        except json.JSONDecodeError:
            geom = []
        if not geom:
            return True  # No geometry → fall back to city match only.

        nearest = float("inf")
        for pt in geom:
            p = (float(pt[0]), float(pt[1]))
            if origin_pt is not None:
                nearest = min(nearest, haversine_m(origin_pt, p))
            if dest_pt is not None:
                nearest = min(nearest, haversine_m(dest_pt, p))
        return nearest <= INTERCITY_TOUCH_RADIUS_M

    # ------------------------------------------------------------------
    @staticmethod
    def _severity(mult: float) -> str:
        if mult < 1.10:
            return "light"
        if mult < 1.30:
            return "moderate"
        if mult < 1.60:
            return "heavy"
        return "severe"

    @staticmethod
    def _hour_curve(city: str, at: datetime) -> float:
        city_l = (city or "").lower()
        hm = at.hour + at.minute / 60.0
        if city_l in ("tokyo", "osaka"):
            return _bump(hm, peaks=[(8.0, 0.35), (18.5, 0.40)], width=2.0)
        if city_l in ("kyoto", "nara"):
            return _bump(hm, peaks=[(9.0, 0.18), (18.0, 0.20)], width=2.5)
        if city_l == "hakone":
            return _bump(hm, peaks=[(10.0, 0.05)], width=3.0)
        if city_l == "shanghai":
            return _bump(hm, peaks=[(8.5, 0.35), (18.0, 0.35)], width=2.0)
        return 0.0

    @staticmethod
    def _weekday_factor(city: str, at: datetime) -> float:
        city_l = (city or "").lower()
        if city_l not in ("tokyo", "osaka"):
            return 0.0
        if at.weekday() <= 4:
            return 0.05
        return 0.0


def _bump(hm: float, peaks: Iterable[Tuple[float, float]], width: float = 2.0) -> float:
    """Piecewise triangular bump summed across peaks."""
    total = 0.0
    for (peak_hm, peak_val) in peaks:
        d = abs(hm - peak_hm)
        if d >= width:
            continue
        total += peak_val * (1.0 - d / width)
    return max(0.0, total)
