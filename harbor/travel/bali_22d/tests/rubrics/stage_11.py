"""Stage 11: reconcile live confirmations without sending a noisy update."""
from __future__ import annotations

import re

from loguru import logger

from .shared._helpers import _agent_responses, _call, _tool_call_matches, list_flight_bookings, list_hotel_reservations


def _sentence_count(text: str) -> int:
    normalized = re.sub(
        r"\b(?:mr|mrs|ms|dr|prof|e\.g|i\.e)\.",
        lambda match: match.group(0).replace(".", ""),
        text,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"(?<=\d)\.(?=\d)", "", normalized)
    return len([part for part in re.split(r"[.!?。！？]+", normalized) if part.strip()])


def s11_max_3_sentences_to_user(env) -> bool:
    resp = _agent_responses(env, 11).strip()
    sentence_count = _sentence_count(resp)
    concise = len(resp) <= 500 and 1 <= sentence_count <= 3
    flights = _tool_call_matches(env, "flight_booking", "list_bookings", lambda _a: True, stage=11)
    hotels = _tool_call_matches(env, "hotel_booking", "list_reservations", lambda _a: True, stage=11)
    inbox = any(
        _tool_call_matches(env, "email", tool, lambda _a: True, stage=11)
        for tool in ("get_emails", "search_emails")
    )
    live_flights = list_flight_bookings(env)
    live_hotels = list_hotel_reservations(env)
    email_result = _call(env, "email", "search_emails", query="Bali", folder="INBOX", page=1, page_size=20)
    email_rows = email_result.get("emails", email_result.get("messages", [])) if isinstance(email_result, dict) else email_result
    flight_state = any(
        str(item.get("status") or "").upper() == "TICKETED"
        and item.get("pnr")
        and item.get("total_paid")
        for item in live_flights
    )
    hotel_state = any(
        str(item.get("status") or "").upper() in {"CONFIRMED", "MODIFIED"}
        and item.get("reservation_id")
        and item.get("total_charged")
        for item in live_hotels
    )
    inbox_state = isinstance(email_rows, list) and bool(email_rows)
    result = bool(concise and flights and hotels and inbox and flight_state and hotel_state and inbox_state)
    logger.info(
        "s11_reconciled_and_concise: {} -- chars={} sentences={} calls={}/{}/{} state={}/{}/{}",
        "PASS" if result else "FAIL",
        len(resp), sentence_count, flights, hotels, inbox, flight_state, hotel_state, inbox_state,
    )
    return result


CHECKS = [("s11_max_3_sentences_to_user", s11_max_3_sentences_to_user, 2.0)]
