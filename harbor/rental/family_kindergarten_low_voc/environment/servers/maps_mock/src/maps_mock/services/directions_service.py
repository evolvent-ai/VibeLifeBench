"""Directions across driving/walking/bicycling/transit modes."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ..backends.sqlite_backend import SqliteBackend
from ..utils.distance import haversine_m, tortuosity_for_mode, speed_mps
from ..utils.validators import validate_mode
from ..utils.time_utils import parse_iso, city_tz, current_sim_datetime

logger = logging.getLogger(__name__)

# v3: no sim clock. When the agent does not specify ``depart_at``, fall back
# to a fixed reference so traffic/transit lookups remain deterministic.
_DEFAULT_DEPART_DATE = "2026-05-01"


class DirectionsService:
    def __init__(
        self,
        backend: SqliteBackend,
        geocode_service,
        traffic_service,
        transit_service,
    ):
        self.backend = backend
        self.geocode = geocode_service
        self.traffic = traffic_service
        self.transit = transit_service

    # ------------------------------------------------------------------
    def directions(self, origin_str: str, dest_str: str, mode: str = "driving",
                   depart_at: Optional[str] = None) -> dict:
        mode = validate_mode(mode)
        origin = self.geocode.resolve(origin_str)
        dest = self.geocode.resolve(dest_str)
        if origin is None or dest is None:
            return {"status": "ZERO_RESULTS",
                    "error": "could not resolve origin or destination",
                    "code": "ZERO_RESULTS"}

        city = origin.get("city") or "Tokyo"
        tz = city_tz(city)
        depart_dt = parse_iso(depart_at) if depart_at else current_sim_datetime(_DEFAULT_DEPART_DATE, "09:00", tz)

        if mode == "transit":
            itineraries = self.transit.plan(origin_str, dest_str, depart_dt.isoformat(timespec="seconds"))
            if isinstance(itineraries, dict) and itineraries.get("error"):
                return {"status": "ZERO_RESULTS", **itineraries}
            if isinstance(itineraries, dict) and "itineraries" in itineraries:
                # Only disruption payload remains — expose as zero-results + disruptions
                return {
                    "status": "ZERO_RESULTS",
                    "routes": [],
                    "disruptions": itineraries.get("disruptions", []),
                }
            if not itineraries:
                return {"status": "ZERO_RESULTS", "routes": []}

            routes = []
            for it in itineraries:
                legs = self._transit_legs_with_walk(it, origin, dest)
                routes.append({
                    "summary": self._transit_summary(it),
                    "distance_m": int(it["total_distance_m"]),
                    "duration_s": int(it["total_duration_s"]),
                    "mode": "transit",
                    "legs": legs,
                    "warnings": [a.get("note", "") for a in it.get("alerts", [])],
                })
            return {"status": "OK", "routes": routes}

        # --- driving / walking / bicycling --------------------------------
        straight_m = haversine_m((origin["lat"], origin["lng"]), (dest["lat"], dest["lng"]))
        intercity = (origin.get("city") or "") != (dest.get("city") or "") and bool(origin.get("city"))
        distance_m = int(round(straight_m * tortuosity_for_mode(mode)))
        duration_s = int(round(distance_m / max(speed_mps(mode, intercity), 0.1)))

        warnings: List[str] = []
        duration_in_traffic_s: Optional[int] = None
        if mode == "driving":
            mult, incidents = self.traffic.current_multiplier(
                origin.get("city") or "Tokyo", depart_dt,
                intercity=intercity,
                origin=origin,
                dest=dest,
            )
            duration_in_traffic_s = int(round(duration_s * mult))
            for inc in incidents:
                warnings.append(f"{inc['kind']} on {inc['road_name']}")

        steps = self._surface_steps(origin, dest, distance_m, duration_s, mode)

        route = {
            "summary": self._surface_summary(origin, dest, mode),
            "distance_m": distance_m,
            "duration_s": duration_s,
            "mode": mode,
            "legs": [{
                "origin": {
                    "place_id": origin["place_id"],
                    "formatted": origin["formatted"],
                },
                "dest": {
                    "place_id": dest["place_id"],
                    "formatted": dest["formatted"],
                },
                "distance_m": distance_m,
                "duration_s": duration_s,
                "steps": steps,
            }],
            "warnings": warnings,
        }
        if duration_in_traffic_s is not None:
            route["duration_in_traffic_s"] = duration_in_traffic_s
        return {"status": "OK", "routes": [route]}

    # ------------------------------------------------------------------
    def distance_matrix(self, origins: List[str], dests: List[str],
                        mode: str = "driving") -> dict:
        mode = validate_mode(mode)
        if not origins or not dests:
            return {"status": "INVALID_REQUEST",
                    "error": "origins and dests required", "code": "INVALID_REQUEST"}
        if len(origins) > 25 or len(dests) > 25:
            return {"status": "INVALID_REQUEST",
                    "error": "at most 25 origins and 25 dests",
                    "code": "INVALID_REQUEST"}
        if len(origins) * len(dests) > 100:
            return {"status": "INVALID_REQUEST",
                    "error": "|origins| * |dests| must be <= 100",
                    "code": "INVALID_REQUEST"}

        # Resolve once
        resolved_o = [self.geocode.resolve(s) for s in origins]
        resolved_d = [self.geocode.resolve(s) for s in dests]

        current_date = _DEFAULT_DEPART_DATE

        origin_addresses = [r["formatted"] if r else "<unresolved>" for r in resolved_o]
        dest_addresses = [r["formatted"] if r else "<unresolved>" for r in resolved_d]

        rows = []
        for (o, o_str) in zip(resolved_o, origins):
            elements = []
            for (d, d_str) in zip(resolved_d, dests):
                if o is None or d is None:
                    elements.append({"status": "NOT_FOUND"})
                    continue
                intercity = (o.get("city") or "") != (d.get("city") or "")
                if mode == "transit":
                    # Delegate to the transit planner so shinkansen/subway timings
                    # are consistent with `directions(mode=transit)` (SPEC §3.6).
                    depart_dt = current_sim_datetime(
                        current_date, "09:00",
                        city_tz(o.get("city") or "Tokyo"),
                    )
                    plan = self.transit.plan(o_str, d_str, depart_dt.isoformat(timespec="seconds"))
                    if isinstance(plan, list) and plan:
                        best = min(plan, key=lambda it: int(it.get("total_duration_s", 1 << 30)))
                        elements.append({
                            "status": "OK",
                            "distance_m": int(best.get("total_distance_m", 0)),
                            "duration_s": int(best.get("total_duration_s", 0)),
                        })
                    else:
                        elements.append({"status": "ZERO_RESULTS"})
                    continue

                straight_m = haversine_m((o["lat"], o["lng"]), (d["lat"], d["lng"]))
                dist = int(round(straight_m * tortuosity_for_mode(mode)))
                dur = int(round(dist / max(speed_mps(mode, intercity), 0.1)))
                element = {"status": "OK", "distance_m": dist, "duration_s": dur}
                if mode == "driving":
                    depart_dt = current_sim_datetime(current_date, "09:00",
                                                     city_tz(o.get("city") or "Tokyo"))
                    mult, _ = self.traffic.current_multiplier(
                        o.get("city") or "Tokyo", depart_dt,
                        intercity=intercity,
                        origin=o,
                        dest=d,
                    )
                    element["duration_in_traffic_s"] = int(round(dur * mult))
                elements.append(element)
            rows.append({"elements": elements})

        return {
            "status": "OK",
            "origin_addresses": origin_addresses,
            "destination_addresses": dest_addresses,
            "rows": rows,
        }

    # ------------------------------------------------------------------
    @staticmethod
    def _surface_summary(origin: dict, dest: dict, mode: str) -> str:
        return f"{mode.capitalize()}: {origin['formatted'].split(',')[0]} → {dest['formatted'].split(',')[0]}"

    @staticmethod
    def _surface_steps(origin: dict, dest: dict, distance_m: int,
                       duration_s: int, mode: str) -> List[Dict[str, Any]]:
        # 3 synthetic steps: depart, cruise, arrive
        dep = int(distance_m * 0.1)
        cruise = int(distance_m * 0.8)
        arr = distance_m - dep - cruise
        dep_t = int(duration_s * 0.1)
        cru_t = int(duration_s * 0.8)
        arr_t = duration_s - dep_t - cru_t
        verb = {
            "driving": "Drive",
            "walking": "Walk",
            "bicycling": "Cycle",
            "transit": "Travel",
        }.get(mode, "Head")
        origin_short = origin["formatted"].split(",")[0]
        dest_short = dest["formatted"].split(",")[0]
        return [
            {"instruction": f"Depart {origin_short}",
             "distance_m": dep, "duration_s": dep_t},
            {"instruction": f"{verb} toward {dest_short}",
             "distance_m": cruise, "duration_s": cru_t},
            {"instruction": f"Arrive at {dest_short}",
             "distance_m": arr, "duration_s": arr_t},
        ]

    @staticmethod
    def _transit_steps(leg: dict) -> List[Dict[str, Any]]:
        stops = leg["stops"]
        line_name = leg["line"]["name"]
        n = len(stops)
        total_s = max(1, _iso_duration_s(leg["depart"], leg["arrive"]))
        return [
            {"instruction": f"BOARD {line_name} at {stops[0]}",
             "distance_m": 0, "duration_s": 30, "mode": "transit"},
            {"instruction": f"RIDE {n - 1} stops",
             "distance_m": 0, "duration_s": total_s - 60, "mode": "transit"},
            {"instruction": f"ALIGHT at {stops[-1]}",
             "distance_m": 0, "duration_s": 30, "mode": "transit"},
        ]

    def _transit_legs_with_walk(self, it: dict, origin: dict, dest: dict) -> List[Dict[str, Any]]:
        """Build legs list for a transit itinerary, bookended by WALK legs.

        SPEC §3.5 requires transit directions to include explicit walk segments
        connecting the caller's origin/destination to the first and last stops.
        """
        legs: List[Dict[str, Any]] = []
        transit_legs = it.get("legs") or []

        first_stop_id = transit_legs[0].get("origin_stop_id") if transit_legs else None
        last_stop_id = transit_legs[-1].get("dest_stop_id") if transit_legs else None
        first_stop = self.backend.get_transit_stop(first_stop_id) if first_stop_id else None
        last_stop = self.backend.get_transit_stop(last_stop_id) if last_stop_id else None

        # Pre-leg WALK from origin coords to the boarding stop.
        if first_stop is not None:
            walk_m = int(round(haversine_m(
                (origin["lat"], origin["lng"]),
                (first_stop["lat"], first_stop["lng"]),
            )))
            if walk_m > 10:
                walk_s = max(30, int(round(walk_m / 1.3)))  # ~1.3 m/s
                legs.append({
                    "origin": {"formatted": origin["formatted"]},
                    "dest":   {"formatted": first_stop["name"]},
                    "distance_m": walk_m,
                    "duration_s": walk_s,
                    "mode": "walking",
                    "steps": [{
                        "instruction": f"WALK to {first_stop['name']}",
                        "distance_m": walk_m,
                        "duration_s": walk_s,
                        "mode": "walking",
                    }],
                })

        for leg in transit_legs:
            legs.append({
                "origin": {"formatted": leg["stops"][0]},
                "dest":   {"formatted": leg["stops"][-1]},
                "distance_m": int(it.get("total_distance_m", 0) // max(1, len(transit_legs))),
                "duration_s": self._leg_duration_s(leg),
                "mode": "transit",
                "line": leg.get("line"),
                "steps": self._transit_steps(leg),
            })

        if last_stop is not None:
            walk_m = int(round(haversine_m(
                (last_stop["lat"], last_stop["lng"]),
                (dest["lat"], dest["lng"]),
            )))
            if walk_m > 10:
                walk_s = max(30, int(round(walk_m / 1.3)))
                legs.append({
                    "origin": {"formatted": last_stop["name"]},
                    "dest":   {"formatted": dest["formatted"]},
                    "distance_m": walk_m,
                    "duration_s": walk_s,
                    "mode": "walking",
                    "steps": [{
                        "instruction": f"WALK to {dest['formatted'].split(',')[0]}",
                        "distance_m": walk_m,
                        "duration_s": walk_s,
                        "mode": "walking",
                    }],
                })
        return legs

    @staticmethod
    def _leg_duration_s(leg: dict) -> int:
        return _iso_duration_s(leg["depart"], leg["arrive"])

    @staticmethod
    def _transit_summary(it: dict) -> str:
        if not it.get("legs"):
            return "Transit"
        head = it["legs"][0]
        tail = it["legs"][-1]
        return f"{head['line']['name']} {head['stops'][0]} → {tail['stops'][-1]}"


def _iso_duration_s(a: str, b: str) -> int:
    da = parse_iso(a)
    db = parse_iso(b)
    return int((db - da).total_seconds())
