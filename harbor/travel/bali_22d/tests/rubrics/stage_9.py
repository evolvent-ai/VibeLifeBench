"""Stage 9: verify exact passenger bookings, continuous lodging, facilities, and full committed cost."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _call, _tool_call_matches, compute_total_spend_cny, list_flight_bookings, list_hotel_reservations, workspace_file_content

_TICKETED = {"TICKETED"}
_ACTIVE_HOTEL = {"CONFIRMED", "MODIFIED"}


def _passenger_names(booking: dict) -> set[str]:
    passengers = booking.get("passengers")
    if not isinstance(passengers, list):
        raise ValueError(f"booking {booking.get('pnr')} has invalid passengers")
    out: set[str] = set()
    for passenger in passengers:
        if not isinstance(passenger, dict):
            raise ValueError(f"booking {booking.get('pnr')} has invalid passenger")
        full = str(passenger.get("name") or passenger.get("full_name") or "").strip().casefold()
        if not full:
            full = f"{passenger.get('given_name') or ''} {passenger.get('family_name') or ''}".strip().casefold()
        if full:
            out.add(full)
    return out


def _has_ticketed_segment(booking: dict, *, origin: str, destination: str, departure_date: str, include_mother: bool = False) -> bool:
    if str(booking.get("status") or "").upper() not in _TICKETED:
        return False
    names = _passenger_names(booking)
    has_couple = any(x in names for x in ("chen yu",)) and any(x in names for x in ("wang meilin", "meilin"))
    has_party = has_couple and (
        not include_mother or any(x in names for x in ("liu fang",))
    )
    segments = booking.get("segments")
    if not isinstance(segments, list):
        raise ValueError(f"booking {booking.get('pnr')} has invalid segments")
    segment_ok = any(
        isinstance(segment, dict)
        and str(segment.get("origin") or "").upper() == origin
        and str(segment.get("destination") or segment.get("dest") or "").upper() == destination
        and str(segment.get("depart_dt") or "")[:10] == departure_date
        for segment in segments
    )
    return bool(has_party and segment_ok and booking.get("pnr"))


def _active_trip_reservations(env) -> list[tuple[dict, dict]]:
    active: list[tuple[dict, dict]] = []
    for reservation in list_hotel_reservations(env):
        if str(reservation.get("status") or "").upper() not in _ACTIVE_HOTEL:
            continue
        check_in = str(reservation.get("check_in") or "")[:10]
        check_out = str(reservation.get("check_out") or "")[:10]
        if check_in >= "2026-07-01" or check_out <= "2026-06-10":
            continue
        hotel_id = str(reservation.get("hotel_id") or "").strip()
        details = _call(env, "hotel_booking", "get_hotel_details", hotel_id=hotel_id)
        if not isinstance(details, dict) or str(details.get("hotel_id") or "") != hotel_id:
            raise ValueError(f"invalid hotel details for {hotel_id}")
        active.append((reservation, details))
    return active


def _district(details: dict) -> str:
    address = details.get("address")
    if not isinstance(address, dict):
        raise ValueError(f"hotel {details.get('hotel_id')} has invalid address")
    # Production get_hotel_details exposes the seed district in address.city.
    return str(address.get("district") or address.get("city") or "").strip().casefold()


def _covers(reservations: list[tuple[dict, dict]], start: str, end: str) -> bool:
    cursor = start
    for reservation, _details in sorted(reservations, key=lambda item: str(item[0].get("check_in") or "")):
        check_in = str(reservation.get("check_in") or "")[:10]
        check_out = str(reservation.get("check_out") or "")[:10]
        if check_out <= cursor or check_in > cursor:
            continue
        cursor = max(cursor, check_out)
        if cursor >= end:
            return True
    return False


def _hospital_access_ok(env, details: dict) -> bool:
    address = details.get("address")
    if not isinstance(address, dict):
        raise ValueError(f"hotel {details.get('hotel_id')} has invalid address")
    lat = address.get("geo_lat")
    lng = address.get("geo_lng")
    if lat is None or lng is None:
        raise ValueError(f"hotel {details.get('hotel_id')} lacks coordinates")
    origin = f"{float(lat)},{float(lng)}"
    coord_tokens = (f"{float(lat):.4f}", f"{float(lng):.4f}")
    for hospital_id in ("pl_bimc_kuta", "pl_siloam_bali", "pl_kasih_ibu_ubud"):
        route = _call(env, "maps", "directions", origin=origin, dest=hospital_id, mode="driving")
        routes = route.get("routes") if isinstance(route, dict) else None
        if not isinstance(routes, list) or not routes or not isinstance(routes[0], dict):
            continue
        duration = routes[0].get("duration_in_traffic_s")
        if duration is None:
            duration = routes[0].get("duration_s")
        called = _tool_call_matches(
            env,
            "maps",
            "directions",
            lambda a: str(a.get("dest") or "") == hospital_id
            and all(token in str(a.get("origin") or "") for token in coord_tokens)
            and str(a.get("mode") or "driving").casefold() == "driving",
            stage=9,
        )
        if called and duration is not None and int(duration) <= 1800:
            return True
    return False


def s9_outbound_flight_confirmed(env) -> bool:
    result = any(_has_ticketed_segment(b, origin="PVG", destination="DPS", departure_date="2026-06-10") for b in list_flight_bookings(env))
    logger.info("s9_outbound_flight_confirmed: {}", "PASS" if result else "FAIL")
    return result


def s9_return_flight_confirmed(env) -> bool:
    result = any(_has_ticketed_segment(b, origin="DPS", destination="PVG", departure_date="2026-07-01", include_mother=True) for b in list_flight_bookings(env))
    logger.info("s9_return_flight_confirmed: {}", "PASS" if result else "FAIL")
    return result


def s9_hotel_seminyak_booked(env) -> bool:
    result = any(
        _district(details) == "seminyak"
        and str(reservation.get("check_in") or "")[:10] == "2026-06-10"
        and str(reservation.get("check_out") or "")[:10] >= "2026-06-15"
        for reservation, details in _active_trip_reservations(env)
    )
    logger.info("s9_hotel_seminyak_booked: {}", "PASS" if result else "FAIL")
    return result


def s9_hotel_ubud_booked(env) -> bool:
    active = _active_trip_reservations(env)
    ubud = any(
        _district(details) == "ubud"
        and str(reservation.get("check_in") or "")[:10] <= "2026-06-15"
        and str(reservation.get("check_out") or "")[:10] >= "2026-06-22"
        for reservation, details in active
    )
    result = bool(ubud and _covers(active, "2026-06-10", "2026-07-01"))
    logger.info("s9_hotel_ubud_and_full_chain: {}", "PASS" if result else "FAIL")
    return result


def s9_budget_under_45k(env) -> bool:
    backend = compute_total_spend_cny(env)
    fixed_visible = 4040.0 + (1_500_000.0 / 2200.0)  # insurance quote + three VOA fees
    expense = workspace_file_content(env, "/workspace/expense_summary.md").casefold().replace(",", "")
    fixed_recorded = all(x in expense for x in ("ti-q-20260602", "4040", "1500000", "idr", "voa"))
    result = bool(backend > 0 and backend + fixed_visible <= 45_000 and fixed_recorded)
    logger.info("s9_budget_under_45k: {} -- all_in={:.2f}", "PASS" if result else "FAIL", backend + fixed_visible)
    return result


def s9_all_hotels_have_ac(env) -> bool:
    active = _active_trip_reservations(env)
    if not active:
        return False
    for reservation, details in active:
        amenities = details.get("amenities")
        if not isinstance(amenities, list):
            raise ValueError(f"hotel {details.get('hotel_id')} has invalid amenities")
        normalized = {str(x).strip().casefold().replace("-", "_") for x in amenities}
        ac = bool({"air_conditioning", "ac", "a/c"} & normalized)
        fridge = bool({"minifridge", "minibar", "refrigerator", "fridge"} & normalized)
        humidity = bool({"dehumidifier", "humidity_control"} & normalized)
        if not (ac and fridge and humidity):
            logger.info("s9_all_hotels_have_ac: FAIL -- reservation={} amenities={}", reservation.get("reservation_id"), normalized)
            return False
        if not _hospital_access_ok(env, details):
            logger.info("s9_all_hotels_have_ac: FAIL -- reservation={} has no verified <=30 minute OB/GYN route", reservation.get("reservation_id"))
            return False
    logger.info("s9_all_hotels_have_ac: PASS")
    return True


CHECKS = [
    ("s9_outbound_flight_confirmed", s9_outbound_flight_confirmed, 3.5),
    ("s9_return_flight_confirmed", s9_return_flight_confirmed, 3.5),
    ("s9_hotel_seminyak_booked", s9_hotel_seminyak_booked, 3.0),
    ("s9_hotel_ubud_booked", s9_hotel_ubud_booked, 2.5),
    ("s9_budget_under_45k", s9_budget_under_45k, 3.0),
    ("s9_all_hotels_have_ac", s9_all_hotels_have_ac, 2.5),
]
