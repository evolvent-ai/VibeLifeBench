"""Final aggregate rubric for East Asia group trip.

Final checks validate distinct end-state obligations. Stage traces and assistant
responses are intentionally excluded because stage rubrics already score them.
"""
from __future__ import annotations

import re

from loguru import logger

from ._helpers import (
    _call,
    _calendar_events,
    _has_bad_advice,
    _health_bp_alert_exists,
    _notion_text,
    _successful_email_read,
    _workspace_file_text,
)

_FIXED_FILES = (
    "profiles.md",
    "itinerary.md",
    "bookings.md",
    "budget.md",
    "health_watch.md",
    "incident_log.md",
    "risk_register.md",
    "decision_log.md",
)
_INACTIVE = {"CANCELLED", "CANCELED", "WALKED", "CHECKED_OUT"}


def _passport_receipt(env) -> dict | None:
    return _successful_email_read(
        env,
        7,
        ("wang hao", "doc-pass-wh-20260601", "2036-05-31", "2026-11-25"),
        from_addr="travel-docs@family.example",
    )


def _lost_found_receipt(env) -> dict | None:
    return _successful_email_read(
        env,
        19,
        ("lf-tyo-0610-27", "2026-07-10", "power bank", "passport copy", "cannot be air-mailed"),
        from_addr="lostandfound@shinjuku-grand.example.com",
    )


def _flight_details(env) -> list[dict]:
    listing = _call(env, "flight_booking", "list_bookings", page=1, page_size=50)
    if isinstance(listing, dict):
        rows = listing.get("bookings", [])
    elif isinstance(listing, list):
        rows = listing
    else:
        raise ValueError("flight_booking.list_bookings returned an invalid payload")
    if not isinstance(rows, list):
        raise ValueError("flight booking listing must be a list")
    details: list[dict] = []
    for row in rows:
        if not isinstance(row, dict) or not row.get("pnr"):
            raise ValueError("flight booking summary is missing pnr")
        pnr = str(row["pnr"])
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr)
        if not isinstance(detail, dict) or str(detail.get("pnr") or "") != pnr:
            raise ValueError(f"invalid flight booking detail for {pnr}")
        details.append({**row, **detail})
    return details


def _hotel_details(env) -> list[dict]:
    listing = _call(env, "hotel_booking", "list_reservations", user_id="usr_chen_yu")
    if isinstance(listing, dict) and "reservation_ids" in listing:
        rows = listing.get("reservation_ids", [])
    elif isinstance(listing, dict):
        rows = listing.get("reservations", listing.get("items", []))
    elif isinstance(listing, list):
        rows = listing
    else:
        raise ValueError("hotel_booking.list_reservations returned an invalid payload")
    if not isinstance(rows, list):
        raise ValueError("hotel reservation listing must be a list")
    details: list[dict] = []
    for row in rows:
        reservation_id = row if isinstance(row, str) else row.get("reservation_id") if isinstance(row, dict) else None
        if not reservation_id:
            raise ValueError("hotel reservation summary is missing reservation_id")
        reservation_id = str(reservation_id)
        detail = _call(env, "hotel_booking", "get_reservation", reservation_id=reservation_id)
        if not isinstance(detail, dict) or str(detail.get("reservation_id") or "") != reservation_id:
            raise ValueError(f"invalid hotel reservation detail for {reservation_id}")
        details.append(detail)
    return details


def _all_fixed_text(env) -> str:
    return "\n".join(
        _workspace_file_text(env, f"/workspace/{filename}") for filename in _FIXED_FILES
    ).casefold()


def final_no_prohibited_residue_and_fixed_files(env) -> bool:
    """The eight declared durable files are non-empty and contain no prohibited shortcut advice."""
    for filename in _FIXED_FILES:
        if len(_workspace_file_text(env, f"/workspace/{filename}").strip()) < 20:
            logger.info("final_files: FAIL -- {} missing/empty", filename)
            return False
    text = _all_fixed_text(env)
    bad = _has_bad_advice(
        text,
        [
            "guaranteed approval",
            "scalped ticket",
            "use a reseller",
            "borrow a document",
            "substitute passport",
            "guaranteed entry",
            "no need to worry",
            "not a serious issue",
        ],
        window=10,
    )
    result = not bad
    logger.info("final_files: {}", "PASS" if result else "FAIL -- prohibited residue")
    return result


def final_wang_hao_passport_state(env) -> bool:
    """The final record preserves the country-specific rule and the verified renewal object."""
    text = (
        _workspace_file_text(env, "/workspace/profiles.md")
        + "\n"
        + _workspace_file_text(env, "/workspace/risk_register.md")
    ).casefold()
    result = bool(
        _passport_receipt(env)
        and
        "usr_wang_hao" in text
        and "wang hao" in text
        and "2026-11-25" in text
        and "japan" in text
        and "korea" in text
        and any(term in text for term in ("validity through stay", "through trip end"))
        and "visa application" in text
        and any(term in text for term in ("six months", "6 months"))
        and "doc-pass-wh-20260601" in text
        and "2036-05-31" in text
        and any(term in text for term in ("resolved", "verified"))
    )
    logger.info("final_passport: {}", "PASS" if result else "FAIL")
    return result


def final_li_ting_health_state(env) -> bool:
    """Backend 158/96 and the final non-diagnostic owner/action record agree."""
    if not _health_bp_alert_exists(env, "usr_li_ting"):
        logger.info("final_health: FAIL -- backend alert missing")
        return False
    latest = _call(
        env,
        "health_tracker",
        "get_latest_metric",
        user_id="usr_li_ting",
        type="blood_pressure",
    )
    if not isinstance(latest, dict):
        raise ValueError("health_tracker.get_latest_metric returned an invalid payload")
    backend_exact = (
        latest.get("user_id") == "usr_li_ting"
        and latest.get("type") == "blood_pressure"
        and str(latest.get("value_text") or "") == "158/96"
    )
    text = (
        _workspace_file_text(env, "/workspace/health_watch.md")
        + "\n"
        + _workspace_file_text(env, "/workspace/incident_log.md")
    ).casefold()
    persisted = (
        "usr_li_ting" in text
        and "158/96" in text
        and any(term in text for term in ("non-diagnostic", "not a diagnosis"))
        and "owner" in text
        and any(term in text for term in ("cancelled", "canceled", "load reduction", "reduce exertion"))
        and any(term in text for term in ("clinician", "doctor", "hospital", "medical care"))
    )
    result = backend_exact and persisted
    logger.info("final_health: {}", "PASS" if result else "FAIL")
    return result


def final_per_person_budget_and_split(env) -> bool:
    """Machine-readable settled totals obey the 540000-minor cap and 4/3-person split."""
    budget = _workspace_file_text(env, "/workspace/budget.md").casefold()
    if not all(
        token in budget
        for token in ("status=settled", "cap_minor=540000", "tokyo_split_count=4", "seoul_split_count=3")
    ):
        logger.info("final_budget: FAIL -- final split header missing")
        return False
    totals: dict[str, int] = {}
    for user_id in ("usr_chen_yu", "usr_li_ting", "usr_wang_hao", "usr_zhao_min"):
        match = re.search(
            rf"user_id\s*=\s*{re.escape(user_id)}\s*;[^\n]*settled_total_minor\s*=\s*(\d+)",
            budget,
        )
        if not match:
            logger.info("final_budget: FAIL -- settled total missing for {}", user_id)
            return False
        totals[user_id] = int(match.group(1))
    zhao = re.search(r"user_id\s*=\s*usr_zhao_min\s*;[^\n]*seoul_minor\s*=\s*(\d+)", budget)
    result = (
        all(0 <= amount <= 540_000 for amount in totals.values())
        and zhao is not None
        and int(zhao.group(1)) == 0
    )
    logger.info("final_budget: {} -- totals={}", "PASS" if result else "FAIL", totals)
    return result


def final_fixed_meeting_has_no_flight_conflict(env) -> bool:
    """The fixed Tokyo meeting remains in calendar and ticketed arrivals precede it by date."""
    meeting = None
    for event in _calendar_events(env):
        start = str(event.get("start") or event.get("start_dt") or event.get("start_time") or "")
        summary = str(event.get("summary") or event.get("title") or "").casefold()
        if start.startswith("2026-06-06") and "meeting" in summary:
            meeting = event
            break
    if meeting is None:
        logger.info("final_meeting: FAIL -- calendar anchor missing")
        return False
    arrivals: list[str] = []
    for booking in _flight_details(env):
        if str(booking.get("status") or "").upper() in _INACTIVE:
            continue
        segments = booking.get("segments")
        if not isinstance(segments, list):
            raise ValueError(f"booking {booking.get('pnr')} has invalid segments")
        for segment in segments:
            if isinstance(segment, dict) and str(segment.get("destination") or "").upper() == "NRT":
                arrivals.append(str(segment.get("arrive_dt") or ""))
    itinerary = _workspace_file_text(env, "/workspace/itinerary.md").casefold()
    result = (
        bool(arrivals)
        and all(arrival[:10] <= "2026-06-05" for arrival in arrivals)
        and "2026-06-06" in itinerary
        and "meeting" in itinerary
    )
    logger.info("final_meeting: {}", "PASS" if result else "FAIL")
    return result


def final_backend_and_booking_register_consistent(env) -> bool:
    """Every active backend PNR/reservation has the same status in bookings.md."""
    register = _workspace_file_text(env, "/workspace/bookings.md").casefold()
    flights = [b for b in _flight_details(env) if str(b.get("status") or "").upper() not in _INACTIVE]
    hotels = [r for r in _hotel_details(env) if str(r.get("status") or "").upper() not in _INACTIVE]
    if not flights or not hotels:
        logger.info("final_booking_consistency: FAIL -- active backend objects missing")
        return False
    for record, id_key in [*((b, "pnr") for b in flights), *((r, "reservation_id") for r in hotels)]:
        object_id = str(record.get(id_key) or "").casefold()
        status = str(record.get("status") or "").casefold()
        if not object_id or not status:
            raise ValueError("active booking object has incomplete ID/status")
        if object_id not in register or status not in register:
            logger.info("final_booking_consistency: FAIL -- {} missing/stale", object_id)
            return False
    logger.info("final_booking_consistency: PASS")
    return True


def _active_outbound_replacement(env) -> dict | None:
    for booking in _flight_details(env):
        if str(booking.get("status") or "").upper() in _INACTIVE:
            continue
        for segment in booking.get("segments") or []:
            if not isinstance(segment, dict):
                continue
            no = str(segment.get("flight_no") or "").replace(" ", "").upper()
            origin = str(segment.get("origin") or "").upper()
            dest = str(segment.get("destination") or segment.get("dest") or "").upper()
            if no != "MU501" and origin in {"PVG", "SHA"} and dest in {"NRT", "HND"} and str(segment.get("arrive_dt") or "")[:10] <= "2026-06-05":
                return booking
    return None


def _active_tokyo_replacement(env) -> dict | None:
    for reservation in _hotel_details(env):
        if str(reservation.get("status") or "").upper() in _INACTIVE:
            continue
        if str(reservation.get("check_in") or "")[:10] == "2026-06-05" and str(reservation.get("check_out") or "")[:10] == "2026-06-08" and reservation.get("hotel_id") != "htl_shinjuku_grand":
            return reservation
    return None


def final_transport_and_lodging_incidents(env) -> bool:
    """Incident log binds the cancelled flight and failed room to real replacement IDs."""
    text = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    flight = _active_outbound_replacement(env)
    hotel = _active_tokyo_replacement(env)
    if not flight or not hotel:
        return False
    pnr = str(flight.get("pnr") or "").casefold()
    reservation_id = str(hotel.get("reservation_id") or "").casefold()
    flight_ok = bool(pnr and all(term in text for term in ("mu501", "2026-06-05", pnr, "cancelled")))
    hotel_ok = bool(
        reservation_id
        and all(term in text for term in ("htl_shinjuku_grand", "superior twin", "2026-06-05", "2026-06-07", reservation_id))
        and any(term in text for term in ("sold_out", "walked", "unable to fulfill"))
    )
    result = flight_ok and hotel_ok
    logger.info("final_incident_transport_lodging: {}", "PASS" if result else "FAIL")
    return result


def final_health_and_finance_incidents(env) -> bool:
    """The exact Li Ting alert and frozen Wang Hao account have owner-aware actions."""
    text = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    health_ok = all(term in text for term in ("usr_li_ting", "158/96")) and any(term in text for term in ("cancelled", "canceled", "reduce exertion"))
    finance_ok = all(term in text for term in ("acct_wang_hao_001", "frozen")) and any(term in text for term in ("alternate", "fallback")) and any(term in text for term in ("not posted", "not debited", "alternate settlement pending"))
    result = health_ok and finance_ok and "owner" in text
    logger.info("final_incident_health_finance: {}", "PASS" if result else "FAIL")
    return result


def final_advisory_and_lost_found_incidents(env) -> bool:
    """The Korean advisory and lost-property receipt preserve exact, visible business facts."""
    text = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    advisory_ok = "korea" in text and "level 3" in text
    linked_request = False
    for reservation in _hotel_details(env):
        reservation_id = str(reservation.get("reservation_id") or "").casefold()
        for request in reservation.get("special_requests") or []:
            if not isinstance(request, dict):
                continue
            ticket_id = str(request.get("ticket_id") or "").casefold()
            request_text = str(request.get("text") or "").casefold()
            if (
                reservation_id
                and ticket_id
                and reservation_id in text
                and ticket_id in text
                and "power bank" in request_text
                and "passport copy" in request_text
            ):
                linked_request = True
                break
    lost_ok = bool(
        _lost_found_receipt(env)
        and linked_request
        and
        all(term in text for term in ("lf-tyo-0610-27", "2026-07-10"))
        and "power bank" in text
        and "passport copy" in text
        and "cannot air-mail" in text
    )
    result = advisory_ok and lost_ok
    logger.info("final_incident_advisory_lost: {}", "PASS" if result else "FAIL")
    return result


def final_journal_is_object_specific_retrospective(env) -> bool:
    """Notion names dynamically discovered replacement objects and the cross-service incident chain."""
    text = _notion_text(env).casefold()
    flight = _active_outbound_replacement(env)
    hotel = _active_tokyo_replacement(env)
    if not flight or not hotel:
        return False
    dynamic = (str(flight.get("pnr") or "").casefold(), str(hotel.get("reservation_id") or "").casefold())
    fixed = ("doc-pass-wh-20260601", "mu501", "htl_shinjuku_grand", "158/96", "acct_wang_hao_001", "lf-tyo-0610-27")
    result = bool(
        _passport_receipt(env)
        and _lost_found_receipt(env)
        and all(term and term in text for term in (*fixed, *dynamic))
        and "level 3" in text
        and any(term in text for term in ("retrospective", "lesson"))
    )
    logger.info("final_journal: {}", "PASS" if result else "FAIL")
    return result

CHECKS = [
    ("final_no_prohibited_residue_and_fixed_files", final_no_prohibited_residue_and_fixed_files, 0.5),
    ("final_wang_hao_passport_state", final_wang_hao_passport_state, 1.0),
    ("final_li_ting_health_state", final_li_ting_health_state, 1.0),
    ("final_per_person_budget_and_split", final_per_person_budget_and_split, 1.0),
    ("final_fixed_meeting_has_no_flight_conflict", final_fixed_meeting_has_no_flight_conflict, 0.5),
    ("final_backend_and_booking_register_consistent", final_backend_and_booking_register_consistent, 1.0),
    ("final_transport_and_lodging_incidents", final_transport_and_lodging_incidents, 0.5),
    ("final_health_and_finance_incidents", final_health_and_finance_incidents, 0.5),
    ("final_advisory_and_lost_found_incidents", final_advisory_and_lost_found_incidents, 0.5),
    ("final_journal_is_object_specific_retrospective", final_journal_is_object_specific_retrospective, 1.0),
]
