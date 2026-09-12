"""Cross-stage rubric -- checks spanning the entire trip. Strict: 30% target pass rate."""
from __future__ import annotations

import re
from .shared._helpers import (
    compute_total_spend_cny,
    list_hotel_reservations,
    list_flight_bookings,
    search_calendar_events,
    notion_page_text,
    workspace_file_content,
    _call,
    _tool_calls,
)
from loguru import logger


def spend_under_45k_hard(env) -> bool:
    """Provider-backed spend plus the visible insurance/VOA costs stays <= 45000."""
    backend = compute_total_spend_cny(env)
    if backend <= 0:
        logger.info("cross_spend: FAIL -- no spend data")
        return False
    total = backend + 4040.0 + (1_500_000.0 / 2200.0)
    if total <= 45000:
        logger.info(f"cross_spend: PASS -- all_in={total:.2f} CNY")
        return True
    logger.info(f"cross_spend: FAIL -- all_in={total:.2f} CNY > 45000")
    return False


def all_hotels_have_ac_and_fridge(env) -> bool:
    """Every active trip hotel has cooling, humidity control, and medicine storage."""
    reservations = list_hotel_reservations(env)
    active = [r for r in reservations
              if (r.get("status") or "").upper() not in ("CANCELLED", "CANCELED")]
    if not active:
        logger.info("cross_ac_fridge: FAIL -- no active reservations")
        return False
    for r in active:
        hotel_id = r.get("hotel_id") or r.get("property_id")
        if not hotel_id:
            logger.info("cross_ac_fridge: FAIL -- missing hotel_id")
            return False
        details = _call(env, "hotel_booking", "get_hotel_details", hotel_id=hotel_id)
        if not details:
            logger.info(f"cross_ac_fridge: FAIL -- cannot get details for {hotel_id}")
            return False
        amenities = details.get("amenities") or details.get("facilities") or []
        if isinstance(amenities, str):
            amenities = [amenities]
        amenities_lower = [a.lower() for a in amenities]
        all_text = " ".join(amenities_lower)
        has_ac = ("air" in all_text and "condition" in all_text) or "ac" in amenities_lower or "a/c" in amenities_lower
        has_fridge = any(w in all_text for w in ["fridge", "refrigerator", "minibar", "minifridge"])
        has_humidity = any(w in all_text for w in ["dehumidifier", "humidity_control", "humidity control"])
        if not has_ac:
            logger.info(f"cross_ac_fridge: FAIL -- {hotel_id} lacks AC")
            return False
        if not has_fridge:
            logger.info(f"cross_ac_fridge: FAIL -- {hotel_id} lacks fridge")
            return False
        if not has_humidity:
            logger.info(f"cross_ac_fridge: FAIL -- {hotel_id} lacks humidity control")
            return False
    logger.info("cross_ac_fridge_humidity: PASS")
    return True


def _calendar_event_text(event: dict) -> str:
    return " ".join(
        str(event.get(key) or "")
        for key in ("summary", "title", "description", "notes", "location")
    ).casefold()


def _calendar_event_date(event: dict) -> str:
    start = event.get("start") or event.get("start_dt") or event.get("start_time") or ""
    if isinstance(start, dict):
        start = start.get("dateTime") or start.get("date") or ""
    return str(start)[:10]


def _booking_has_exact_calendar_event(env, identifier: str, expected_date: str) -> bool:
    if not identifier or not expected_date:
        return False
    needle = identifier.casefold()
    for event in search_calendar_events(env, identifier):
        if needle not in _calendar_event_text(event):
            continue
        if _calendar_event_date(event) == expected_date:
            return True
    return False


def calendar_notion_sync(env) -> bool:
    """Every active booking is synchronized across calendar, Notion, and register."""
    flights = [
        booking
        for booking in list_flight_bookings(env)
        if str(booking.get("status") or "").upper() not in {"CANCELLED", "CANCELED"}
    ]
    hotels = [
        reservation
        for reservation in list_hotel_reservations(env)
        if str(reservation.get("status") or "").upper() not in {"CANCELLED", "CANCELED"}
    ]
    if not flights and not hotels:
        logger.info("cross_cal_sync: FAIL -- no active bookings")
        return False

    missing: list[str] = []
    notion = notion_page_text(env).casefold()
    register = workspace_file_content(env, "/workspace/booking_register.md").casefold()
    for booking in flights:
        pnr = str(booking.get("pnr") or "").strip()
        segments = booking.get("segments") or []
        first_segment = segments[0] if isinstance(segments, list) and segments else {}
        depart = str(
            (first_segment.get("depart_dt") or first_segment.get("departure_time") or "")
            if isinstance(first_segment, dict)
            else ""
        )[:10]
        if not _booking_has_exact_calendar_event(env, pnr, depart):
            missing.append(f"flight:{pnr or '<missing-id>'}@{depart or '<missing-date>'}")
        if pnr.casefold() not in notion or pnr.casefold() not in register or depart not in register:
            missing.append(f"flight-durable:{pnr or '<missing-id>'}")

    for reservation in hotels:
        reservation_id = str(reservation.get("reservation_id") or "").strip()
        check_in = str(
            reservation.get("check_in")
            or reservation.get("checkin")
            or reservation.get("check_in_date")
            or ""
        )[:10]
        if not _booking_has_exact_calendar_event(env, reservation_id, check_in):
            missing.append(
                f"hotel:{reservation_id or '<missing-id>'}@{check_in or '<missing-date>'}"
            )
        if reservation_id.casefold() not in notion or reservation_id.casefold() not in register or check_in not in register:
            missing.append(f"hotel-durable:{reservation_id or '<missing-id>'}")

    if missing:
        logger.info("cross_cal_sync: FAIL -- missing exact booking events: {}", missing)
        return False
    logger.info(
        "cross_cal_sync: PASS -- exact ID/date events for {} flights and {} hotels",
        len(flights),
        len(hotels),
    )
    return True


def budget_tracked_every_5_stages(env) -> bool:
    """Expense state has object-bound, dated running totals across the trip."""
    notion_text = notion_page_text(env).lower()
    expense_content = ""
    for fname in ("expense_summary.md", "budget.md", "expenses.md", "spending.md"):
        content = workspace_file_content(env, f"/workspace/{fname}")
        if content:
            expense_content += "\n" + content.lower()
    all_text = notion_text + "\n" + expense_content
    total_pattern = r'(?:running total|total|sum|total|total|running total)[\s\S]{0,30}[\d,]+(?:\.\d+)?'
    matches = re.findall(total_pattern, all_text)
    dates = set(re.findall(r"2026-\d{2}-\d{2}", all_text))
    booking_refs = len(set(re.findall(r"(?:mock-[a-z0-9]+|res_[a-z0-9_-]+|hb-[a-z0-9-]+|ti-q-20260602)", all_text)))
    if len(matches) >= 4 and len(dates) >= 4 and booking_refs >= 4:
        logger.info(f"cross_budget_tracked: PASS -- totals={len(matches)} dates={len(dates)} refs={booking_refs}")
        return True
    logger.info(f"cross_budget_tracked: FAIL -- totals={len(matches)} dates={len(dates)} refs={booking_refs}")
    return False


def _mother_booking_offer(booking: dict) -> str | None:
    passengers = booking.get("passengers")
    if not isinstance(passengers, list):
        raise ValueError(f"booking {booking.get('pnr')} has invalid passengers")
    has_liu_fang = any(
        isinstance(passenger, dict)
        and (
            (
                str(passenger.get("given_name") or "").strip().casefold() == "liu"
                and str(passenger.get("family_name") or "").strip().casefold() == "fang"
            )
            or str(passenger.get("name") or passenger.get("full_name") or "")
            .strip()
            .casefold()
            in {"liu fang"}
        )
        for passenger in passengers
    )
    if not has_liu_fang or str(booking.get("status") or "").upper() != "TICKETED":
        return None

    segments = booking.get("segments")
    if not isinstance(segments, list):
        raise ValueError(f"booking {booking.get('pnr')} has invalid segments")
    matching_segment = any(
        isinstance(segment, dict)
        and str(segment.get("flight_no") or "").upper() == "GA837"
        and str(segment.get("origin") or "").upper() == "PVG"
        and str(segment.get("destination") or segment.get("dest") or "").upper() == "DPS"
        and str(segment.get("depart_dt") or "")[:10] == "2026-06-22"
        and str(segment.get("arrive_dt") or "")[:10] == "2026-06-22"
        for segment in segments
    )
    if not matching_segment:
        return None

    history = booking.get("history")
    if not isinstance(history, list):
        raise ValueError(f"booking {booking.get('pnr')} has invalid history")
    for event in history:
        if not isinstance(event, dict):
            raise ValueError(f"booking {booking.get('pnr')} has invalid history event")
        match = re.search(r"(?:^|\s)offer=([^\s]+)", str(event.get("detail") or ""))
        if match:
            return match.group(1)
    return None


def _matching_booking_calls(env, offer_id: str) -> list[tuple[int, dict]]:
    matches: list[tuple[int, dict]] = []
    for stage in range(24):
        for call in _tool_calls(env, stage):
            name = str(call.get("name") or "").lower().replace("-", "_")
            arguments = call.get("arguments") or {}
            if (
                name.endswith("create_booking")
                and arguments.get("offer_id") == offer_id
                and arguments.get("hold") is False
            ):
                matches.append((stage, call))
    return matches


def mother_flight_only_after_passport(env) -> bool:
    """GA837 is ticketed once, after the stage-16 passport-resolution evidence."""
    matching: list[tuple[dict, str]] = []
    for booking in list_flight_bookings(env):
        offer_id = _mother_booking_offer(booking)
        if offer_id:
            matching.append((booking, offer_id))
    if len(matching) != 1:
        logger.info("cross_mother_flight: FAIL -- expected one exact Liu Fang GA837 booking")
        return False

    booking, offer_id = matching[0]
    calls = _matching_booking_calls(env, offer_id)
    if len(calls) != 1 or calls[0][0] < 16:
        logger.info(
            "cross_mother_flight: FAIL -- matching create_booking must occur once at stage >=16"
        )
        return False

    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    register = workspace_file_content(env, "/workspace/booking_register.md").casefold()
    resolution_ok = (
        any(name in risk for name in ("liu fang",))
        and "2026-12-03" in risk
        and "2036-06-14" in risk
        and "doc-pass-lf-20260616" in risk
        and any(word in risk for word in ("verified", "resolved"))
    )
    booking_ok = (
        str(booking.get("pnr") or "").casefold() in register
        and "ga837" in register
        and "pvg-dps" in register
        and "2026-06-22" in register
        and any(name in register for name in ("liu fang",))
        and "ticketed" in register
        and "doc-pass-lf-20260616" in register
    )
    result = resolution_ok and booking_ok
    logger.info("cross_mother_flight: {}", "PASS" if result else "FAIL -- durable state missing")
    return result


CHECKS = [
    ("spend_under_45k_hard", spend_under_45k_hard, 4.0),
    ("all_hotels_have_ac_and_fridge", all_hotels_have_ac_and_fridge, 3.0),
    ("calendar_notion_sync", calendar_notion_sync, 2.5),
    ("budget_tracked_every_5_stages", budget_tracked_every_5_stages, 2.0),
    ("mother_flight_only_after_passport", mother_flight_only_after_passport, 3.0),
]
