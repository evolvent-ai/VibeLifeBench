"""Transit planning: snap, direct + one-transfer itineraries."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ..backends.sqlite_backend import SqliteBackend
from ..utils.distance import haversine_m
from ..utils.time_utils import parse_iso, city_tz, to_iso

logger = logging.getLogger(__name__)


# Interchange stop IDs — must match the seeded transit_stops.stop_id values.
# (Seed uses ``ts_shin_osaka`` not ``ts_shin_osaka_sta``; ``ts_shibuya_sta``
# not ``ts_shibuya``; ``ts_umeda`` not ``ts_umeda_sta``.)
INTERCHANGE_STOP_IDS = {
    "ts_tokyo_sta",
    "ts_shin_osaka",
    "ts_kyoto_sta",
    "ts_shibuya_sta",
    "ts_umeda",
    "ts_nagoya",
}

# Station incidents bump itinerary duration by this much (per SPEC §5.2:
# "adds 15–40 min to transfers at that stop" — we take the midpoint).
STATION_INCIDENT_DELAY_MIN = 25


class TransitService:
    def __init__(self, backend: SqliteBackend, geocode_service):
        self.backend = backend
        self.geocode = geocode_service

    # ------------------------------------------------------------------
    def plan(self, origin_str: str, dest_str: str, depart_at_iso: str) -> Any:
        origin = self.geocode.resolve(origin_str)
        dest = self.geocode.resolve(dest_str)
        if origin is None or dest is None:
            return {"error": "ZERO_RESULTS", "code": "ZERO_RESULTS"}

        o_stop = self._snap(origin["lat"], origin["lng"], max_m=1500)
        d_stop = self._snap(dest["lat"], dest["lng"], max_m=1500)
        if o_stop is None or d_stop is None:
            return {"error": "NO_TRANSIT_NEARBY", "code": "NO_TRANSIT_NEARBY"}

        depart_dt = parse_iso(depart_at_iso)

        direct = self._direct_itineraries(o_stop, d_stop, depart_dt)
        transfer = self._transfer_itineraries(o_stop, d_stop, depart_dt)

        all_options: List[dict] = direct + transfer

        # Drop suspended lines/stops and apply station-incident penalties.
        kept: List[dict] = []
        dropped_disruptions: List[dict] = []
        for it in all_options:
            blocked = False
            for leg in it["legs"]:
                for ev in self._line_suspensions(leg["line"]["line_id"]):
                    if _overlaps(leg["depart"], leg["arrive"], ev["start_dt"], ev["end_dt"]):
                        blocked = True
                        dropped_disruptions.append({
                            "event_id": ev["event_id"],
                            "kind": "line_suspended",
                            "line_id": leg["line"]["line_id"],
                            "window": {"start": ev["start_dt"], "end": ev["end_dt"]},
                            "note": ev["note"],
                        })
                        break
                if blocked:
                    break
                # Stop-level delays add alert + duration penalty.
                for ev in self._stop_delays([leg["origin_stop_id"], leg["dest_stop_id"]]):
                    if _overlaps(leg["depart"], leg["arrive"], ev["start_dt"], ev["end_dt"]):
                        self._apply_station_penalty(leg, it, ev)
            if not blocked:
                kept.append(it)

        kept.sort(key=lambda x: x["legs"][-1]["arrive"])
        trimmed = kept[:3]

        if not trimmed and dropped_disruptions:
            # Deduplicate disruptions.
            seen = set()
            uniq = []
            for d in dropped_disruptions:
                if d["event_id"] in seen:
                    continue
                seen.add(d["event_id"])
                uniq.append(d)
            return {"itineraries": [], "disruptions": uniq}

        return trimmed

    # Expose for directions_service
    def plan_and_unwrap(self, *args, **kwargs):
        r = self.plan(*args, **kwargs)
        if isinstance(r, dict):
            return []
        return r

    # ------------------------------------------------------------------
    def _snap(self, lat: float, lng: float, max_m: float = 1500) -> Optional[dict]:
        best = None
        best_d = float("inf")
        for s in self.backend.list_transit_stops():
            d = haversine_m((lat, lng), (s["lat"], s["lng"]))
            if d < best_d:
                best_d = d
                best = s
        if best is None or best_d > max_m:
            return None
        return {
            "stop_id": best["stop_id"],
            "name": best["name"],
            "lat": best["lat"],
            "lng": best["lng"],
            "city": best["city"],
            "distance_m": int(round(best_d)),
        }

    def _colocated_stops(self, stop: dict, radius_m: float = 200.0) -> List[dict]:
        """Return the snapped stop plus any other stops co-located within radius_m.

        Major Japanese stations (e.g. Kyoto Station Shinkansen platforms vs JR
        Kyoto Line platforms, or Umeda/Osaka-Umeda/Higashi-Umeda) are modelled
        as sibling stops at nearly-identical lat/lng. The snapper picks one
        arbitrarily; transit planning should consider all of them so Shinkansen
        itineraries aren't missed just because the snap landed on a JR-only
        sibling. We default to 200 m which covers Umeda-cluster offsets.
        """
        out: List[dict] = [stop]
        sid = stop["stop_id"]
        for s in self.backend.list_transit_stops():
            if s["stop_id"] == sid:
                continue
            if haversine_m((stop["lat"], stop["lng"]), (s["lat"], s["lng"])) <= radius_m:
                out.append({
                    "stop_id": s["stop_id"],
                    "name": s["name"],
                    "lat": s["lat"],
                    "lng": s["lng"],
                    "city": s["city"],
                    "distance_m": stop.get("distance_m", 0),
                })
        return out

    # ------------------------------------------------------------------
    def _direct_itineraries(self, o_stop: dict, d_stop: dict,
                            depart_dt: datetime) -> List[dict]:
        out = []
        seen_depart = set()
        for o_cand in self._colocated_stops(o_stop):
            for d_cand in self._colocated_stops(d_stop):
                lines_o = self.backend.lines_serving_stop(o_cand["stop_id"])
                lines_d_set = set(
                    (r["line_id"], r["direction"])
                    for r in self.backend.lines_serving_stop(d_cand["stop_id"])
                )
                for r in lines_o:
                    key = (r["line_id"], r["direction"])
                    if key not in lines_d_set:
                        continue
                    iti = self._build_leg(r["line_id"], r["direction"], o_cand, d_cand, depart_dt)
                    if iti and iti["legs"][0]["depart"] not in seen_depart:
                        out.append(iti)
                        seen_depart.add(iti["legs"][0]["depart"])
        return out

    def _transfer_itineraries(self, o_stop: dict, d_stop: dict,
                              depart_dt: datetime) -> List[dict]:
        """One-transfer itineraries via known interchange stops.

        Both the origin and destination are expanded to their co-located
        sibling clusters (Kyoto Shinkansen platforms + Kyoto JR, Umeda cluster,
        etc.), so that e.g. Shibuya (Yamanote) → transfer → Kyoto (JR) routes
        are discoverable even when the snap picked a sibling platform.
        """
        o_cluster = self._colocated_stops(o_stop)
        d_cluster = self._colocated_stops(d_stop)

        lines_o = set()
        for cand in o_cluster:
            lines_o.update(
                (r["line_id"], r["direction"])
                for r in self.backend.lines_serving_stop(cand["stop_id"])
            )
        lines_d = set()
        for cand in d_cluster:
            lines_d.update(
                (r["line_id"], r["direction"])
                for r in self.backend.lines_serving_stop(cand["stop_id"])
            )

        out: List[dict] = []
        seen_sig: set = set()

        for xc in INTERCHANGE_STOP_IDS:
            xc_row = self.backend.get_transit_stop(xc)
            if xc_row is None:
                continue
            xc_stop_base = {
                "stop_id": xc_row["stop_id"],
                "name": xc_row["name"],
                "lat": xc_row["lat"],
                "lng": xc_row["lng"],
                "city": xc_row["city"],
            }
            xc_cluster = self._colocated_stops(xc_stop_base)
            xc_lines = set()
            for c in xc_cluster:
                xc_lines.update(
                    (r["line_id"], r["direction"])
                    for r in self.backend.lines_serving_stop(c["stop_id"])
                )

            # Leg 1 options: any origin-cluster stop + any xc-cluster stop on a common line.
            leg1_options: List[Tuple[dict, dict, str, str]] = []
            for o_cand in o_cluster:
                o_cand_lines = {
                    (r["line_id"], r["direction"])
                    for r in self.backend.lines_serving_stop(o_cand["stop_id"])
                }
                for xc_cand in xc_cluster:
                    xc_cand_lines = {
                        (r["line_id"], r["direction"])
                        for r in self.backend.lines_serving_stop(xc_cand["stop_id"])
                    }
                    for (line_id, direction) in (o_cand_lines & xc_cand_lines):
                        leg1 = self._build_leg(line_id, direction, o_cand, xc_cand, depart_dt)
                        if leg1:
                            leg1_options.append((o_cand, xc_cand, line_id, direction))

            for (o_cand, xc_cand1, line1_id, dir1) in leg1_options:
                leg1 = self._build_leg(line1_id, dir1, o_cand, xc_cand1, depart_dt)
                if not leg1:
                    continue
                transfer_start = parse_iso(leg1["legs"][-1]["arrive"]) + timedelta(minutes=5)
                for xc_cand2 in xc_cluster:
                    xc_cand2_lines = {
                        (r["line_id"], r["direction"])
                        for r in self.backend.lines_serving_stop(xc_cand2["stop_id"])
                    }
                    for d_cand in d_cluster:
                        d_cand_lines = {
                            (r["line_id"], r["direction"])
                            for r in self.backend.lines_serving_stop(d_cand["stop_id"])
                        }
                        for (line2_id, dir2) in (xc_cand2_lines & d_cand_lines):
                            if line2_id == line1_id:
                                continue  # same line → not a transfer
                            leg2 = self._build_leg(line2_id, dir2, xc_cand2, d_cand, transfer_start)
                            if not leg2:
                                continue

                            sig = (line1_id, dir1, leg1["legs"][0]["depart"],
                                   line2_id, dir2, leg2["legs"][-1]["arrive"])
                            if sig in seen_sig:
                                continue
                            seen_sig.add(sig)

                            total_duration = _iso_duration_s(
                                leg1["legs"][0]["depart"],
                                leg2["legs"][-1]["arrive"],
                            )
                            out.append({
                                "route_id": _stable_route_id(
                                    line1_id, line2_id, leg1["legs"][0]["depart"],
                                ),
                                "total_duration_s": total_duration,
                                "total_distance_m": leg1["total_distance_m"] + leg2["total_distance_m"],
                                "legs": leg1["legs"] + leg2["legs"],
                                "alerts": [],
                            })
        return out

    # ------------------------------------------------------------------
    def _build_leg(self, line_id: str, direction: str,
                   origin_stop: dict, dest_stop: dict,
                   depart_after: datetime) -> Optional[dict]:
        line = self.backend.get_transit_line(line_id)
        if line is None:
            return None

        schedule = self.backend.line_schedule(line_id, direction)
        if not schedule:
            return None

        tz = city_tz(origin_stop.get("city", "Tokyo"))

        origin_rows = sorted(
            [s for s in schedule if s["stop_id"] == origin_stop["stop_id"]],
            key=lambda r: r["time"],
        )
        dest_rows = [s for s in schedule if s["stop_id"] == dest_stop["stop_id"]]
        if not origin_rows or not dest_rows:
            return None

        o_seq = origin_rows[0]["stop_seq"]
        d_seq = dest_rows[0]["stop_seq"]
        if d_seq <= o_seq:
            return None

        # Segment minutes between the two stops on this line, using stop_seq
        try:
            segments = json.loads(line["segment_minutes_json"] or "[]")
        except json.JSONDecodeError:
            segments = []
        if segments:
            minutes_between = sum(segments[o_seq - 1:d_seq - 1])
        else:
            # Fallback: approximate
            minutes_between = max(5, (d_seq - o_seq) * 10)
        if minutes_between <= 0:
            minutes_between = max(5, (d_seq - o_seq) * 10)

        depart_date = depart_after.date()
        depart_hm = depart_after.strftime("%H:%M")

        candidates: List[Tuple[str, int]] = []  # (time_hm, date_offset)
        for r in origin_rows:
            if r["time"] >= depart_hm:
                candidates.append((r["time"], 0))
        for r in origin_rows:
            candidates.append((r["time"], 1))

        if not candidates:
            return None

        t_hm, day_off = candidates[0]
        dep_dt = datetime(depart_date.year, depart_date.month, depart_date.day,
                          int(t_hm[:2]), int(t_hm[3:]), tzinfo=tz) + timedelta(days=day_off)
        arr_dt = dep_dt + timedelta(minutes=minutes_between)

        distance_m = self._line_segment_distance(line, o_seq, d_seq)
        if distance_m <= 0:
            distance_m = int(haversine_m(
                (origin_stop["lat"], origin_stop["lng"]),
                (dest_stop["lat"], dest_stop["lng"]),
            ))

        # Stop list for the leg (names only) — derive from the schedule rows
        stop_seq_map = {}
        for s in schedule:
            stop_seq_map.setdefault(s["stop_seq"], s["stop_id"])
        name_by_stop = {r["stop_id"]: r["name"] for r in self.backend.list_transit_stops()}
        between = [
            name_by_stop.get(stop_seq_map[seq], stop_seq_map[seq])
            for seq in sorted(stop_seq_map)
            if o_seq <= seq <= d_seq
        ]
        if not between:
            between = [origin_stop["name"], dest_stop["name"]]

        return {
            "route_id": f"rt_{line_id}_{dep_dt.strftime('%H%M')}",
            "total_duration_s": int((arr_dt - dep_dt).total_seconds()),
            "total_distance_m": int(distance_m),
            "legs": [{
                "line": {
                    "line_id": line_id,
                    "name": line["name"],
                    "mode": line["mode"],
                },
                "operator": line["operator"],
                "stops": between,
                "depart": to_iso(dep_dt),
                "arrive": to_iso(arr_dt),
                "platform": str((o_seq % 14) + 1),
                "headsign": between[-1],
                "origin_stop_id": origin_stop["stop_id"],
                "dest_stop_id": dest_stop["stop_id"],
            }],
            "alerts": [],
        }

    # ------------------------------------------------------------------
    def _line_segment_distance(self, line_row, seq_from: int, seq_to: int) -> int:
        seg_json = line_row["segment_minutes_json"]
        try:
            segments = json.loads(seg_json or "[]")
        except json.JSONDecodeError:
            segments = []
        if not segments or seq_from >= seq_to:
            return 0
        mode = line_row["mode"]
        if mode == "shinkansen":
            kmh = 250.0
        elif mode == "subway":
            kmh = 35.0
        else:
            kmh = 60.0
        minutes = sum(segments[seq_from - 1:seq_to - 1])
        return int(round(kmh * 1000.0 * minutes / 60.0))

    def _line_suspensions(self, line_id: str) -> List[dict]:
        return [
            {
                "event_id": ev["event_id"],
                "start_dt": ev["start_dt"],
                "end_dt": ev["end_dt"],
                "kind": ev["kind"],
                "note": ev["note"],
            }
            for ev in self.backend.list_transit_events(only_active=True)
            if ev["kind"] == "suspended" and ev["line_id"] == line_id
        ]

    def _stop_delays(self, stop_ids: List[str]) -> List[dict]:
        out = []
        for ev in self.backend.list_transit_events(only_active=True):
            if ev["kind"] == "delayed" and ev["stop_id"] in stop_ids:
                out.append({
                    "event_id": ev["event_id"],
                    "stop_id": ev["stop_id"],
                    "start_dt": ev["start_dt"],
                    "end_dt": ev["end_dt"],
                    "note": ev["note"],
                })
        return out

    # ------------------------------------------------------------------
    def _apply_station_penalty(self, leg: dict, it: dict, ev: dict) -> None:
        """Attach station-incident alert + bump leg/itinerary arrival time.

        SPEC §5.2 requires station incidents to delay transfers by 15-40 min.
        We encode that as a deterministic +25 min bump applied to the first
        affected leg's arrival and propagated into the itinerary total.
        """
        # Skip duplicate alerts for the same event.
        existing = {a.get("event_id") for a in leg.get("alerts", []) or []}
        if ev["event_id"] in existing:
            return

        leg.setdefault("alerts", []).append({
            "event_id": ev["event_id"],
            "kind": "station_incident",
            "stop_id": ev["stop_id"],
            "note": ev["note"],
            "delay_minutes": STATION_INCIDENT_DELAY_MIN,
        })
        it["alerts"] = it.get("alerts", []) + [{
            "event_id": ev["event_id"],
            "kind": "station_incident",
            "note": ev["note"],
            "delay_minutes": STATION_INCIDENT_DELAY_MIN,
        }]

        # Bump arrival time of this leg and all subsequent legs; grow totals.
        delay = timedelta(minutes=STATION_INCIDENT_DELAY_MIN)
        legs = it["legs"]
        try:
            affected_idx = legs.index(leg)
        except ValueError:
            affected_idx = 0
        for i in range(affected_idx, len(legs)):
            cur = legs[i]
            cur["arrive"] = to_iso(parse_iso(cur["arrive"]) + delay)
            if i > affected_idx:
                cur["depart"] = to_iso(parse_iso(cur["depart"]) + delay)
        it["total_duration_s"] = int(it.get("total_duration_s", 0)) + int(delay.total_seconds())


# ---------------------------------------------------------------------------
def _overlaps(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    try:
        a0 = parse_iso(a_start)
        a1 = parse_iso(a_end)
        b0 = parse_iso(b_start)
        b1 = parse_iso(b_end)
    except Exception:
        return False
    return a0 <= b1 and b0 <= a1


def _iso_duration_s(a: str, b: str) -> int:
    return int((parse_iso(b) - parse_iso(a)).total_seconds())


def _stable_route_id(line1: str, line2: str, depart_iso: str) -> str:
    hhmm = depart_iso[-8:-3].replace(":", "")
    return f"rt_{line1}_{line2}_{hhmm}"
