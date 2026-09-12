"""Stage 14: require a reservation-bound mold request, bounded health communication, and exact calendar update."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _agent_responses, _tool_call_matches, list_hotel_reservations, search_calendar_events


def _stay_and_request(env) -> tuple[dict, dict] | None:
    for reservation in list_hotel_reservations(env):
        check_in = str(reservation.get("check_in") or "")[:10]
        check_out = str(reservation.get("check_out") or "")[:10]
        if not (check_in <= "2026-06-11" < check_out):
            continue
        for request in reservation.get("special_requests") or []:
            if not isinstance(request, dict):
                continue
            text = str(request.get("text") or "").casefold()
            if any(x in text for x in ("mold", "mold", "musty", "musty smell")) and any(
                x in text for x in ("room change", "dry room", "inspect")
            ) and request.get("ticket_id"):
                return reservation, request
    return None


def s14_room_change_requested(env) -> bool:
    match = _stay_and_request(env)
    if not match:
        logger.info("s14_room_change_requested: FAIL -- no reservation-bound request")
        return False
    reservation, _request = match
    reservation_id = str(reservation.get("reservation_id") or "")
    called = _tool_call_matches(
        env,
        "hotel_booking",
        "submit_special_request",
        lambda a: str(a.get("reservation_id") or "") == reservation_id
        and any(x in str(a.get("text") or "").casefold() for x in ("mold", "mold", "musty")),
        stage=14,
    )
    result = bool(called)
    logger.info("s14_room_change_requested: {}", "PASS" if result else "FAIL")
    return result


def s14_mold_health_risk_communicated(env) -> bool:
    resp = _agent_responses(env, 14).casefold()
    specific = any(x in resp for x in ("respiratory", "respiratory", "allerg", "allergy", "spore"))
    pregnancy = any(x in resp for x in ("pregnan", " pregnancy", "Meilin", "meilin"))
    boundary = any(x in resp for x in ("doctor", "doctor", "clinician", "seek care", "seek care"))
    no_diagnosis = not any(x in resp for x in ("definitely caused", "definitely caused", "definitely harmful", "diagnosis"))
    result = bool(resp and specific and pregnancy and boundary and no_diagnosis)
    logger.info("s14_mold_health_risk_communicated: {}", "PASS" if result else "FAIL")
    return result


def s14_calendar_updated(env) -> bool:
    match = _stay_and_request(env)
    if not match:
        return False
    reservation, request = match
    reservation_id = str(reservation.get("reservation_id") or "").casefold()
    ticket_id = str(request.get("ticket_id") or "").casefold()
    for query in (reservation_id, ticket_id):
        for event in search_calendar_events(env, query):
            body = " ".join(str(event.get(k) or "") for k in ("summary", "title", "description", "notes")).casefold()
            start = str(event.get("start") or event.get("start_dt") or "")[:10]
            if start == "2026-06-11" and reservation_id in body and ticket_id in body and any(
                x in body for x in ("mold", "mold", "room change")
            ):
                logger.info("s14_calendar_updated: PASS")
                return True
    logger.info("s14_calendar_updated: FAIL")
    return False


CHECKS = [
    ("s14_room_change_requested", s14_room_change_requested, 3.0),
    ("s14_mold_health_risk_communicated", s14_mold_health_risk_communicated, 2.5),
    ("s14_calendar_updated", s14_calendar_updated, 2.0),
]
