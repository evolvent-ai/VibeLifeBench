"""Stage 12: packing safeguards must be structured, assigned, and ready by departure."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _tool_call_matches, list_flight_bookings, workspace_file_content


def _packing_text(env) -> str:
    return (workspace_file_content(env, "/workspace/HEARTBEAT.md") + "\n" + workspace_file_content(env, "/workspace/risk_register.md") + "\n" + workspace_file_content(env, "/workspace/itinerary.md")).casefold()


def _structured(text: str, terms: tuple[str, ...]) -> bool:
    return any(x in text for x in terms) and any(x in text for x in ("owner", "owner")) and any(
        x in text for x in ("packed", "ready", "done")
    ) and any(x in text for x in ("2026-06-09", "2026-06-10", "departure"))


def _priority_boarding_reminder(text: str) -> bool:
    return any(x in text for x in ("priority boarding", "pre-boarding", "priority board", "priority boarding")) and any(
        x in text for x in ("airline", "gate", "airline", "gate")
    ) and any(x in text for x in ("ask", "check", "request", "confirm", "ask", "confirm", "request")) and any(
        x in text for x in ("owner", "owner")
    ) and any(x in text for x in ("2026-06-09", "2026-06-10", "departure"))


def _outbound_checked_in(env) -> bool:
    for booking in list_flight_bookings(env):
        pnr = str(booking.get("pnr") or "").strip()
        passengers = booking.get("passengers")
        if not pnr or not isinstance(passengers, list) or not passengers:
            continue
        for segment in booking.get("segments") or []:
            if not isinstance(segment, dict):
                continue
            segment_idx = int(segment.get("segment_idx") or 0)
            if not (
                str(segment.get("flight_no") or "").replace(" ", "").upper() == "GA835"
                and str(segment.get("origin") or "").upper() == "PVG"
                and str(segment.get("destination") or segment.get("dest") or "").upper() == "DPS"
                and str(segment.get("depart_dt") or "")[:10] == "2026-06-10"
            ):
                continue
            history_ok = any(
                isinstance(item, dict)
                and str(item.get("event") or "").upper() == "CHECKED_IN"
                and f"segment={segment_idx}" in str(item.get("detail") or "")
                for item in booking.get("history") or []
            )
            called = _tool_call_matches(
                env,
                "flight_booking",
                "check_in",
                lambda a: str(a.get("pnr") or "") == pnr
                and int(a.get("segment_idx") or 0) == segment_idx
                and (
                    a.get("pax_indices") is None
                    or set(a.get("pax_indices") or []) == set(range(len(passengers)))
                ),
                stage=12,
            )
            if history_ok and called:
                return True
    return False


def s12_prenatal_doc_in_packing(env) -> bool:
    text = _packing_text(env)
    result = _structured(text, ("prenatal", " pregnancy", "ob report", "obstetric")) and _priority_boarding_reminder(text) and _outbound_checked_in(env)
    logger.info("s12_prenatal_doc_in_packing: {}", "PASS" if result else "FAIL")
    return result


def s12_mosquito_repellent_in_packing(env) -> bool:
    text = _packing_text(env)
    result = _structured(text, ("deet", "repellent", "repellent", "mosquito")) and any(
        x in text for x in ("long sleeve", "long sleeve", "mosquito", "mosquito net", "air-conditioned", "air-conditioned")
    )
    logger.info("s12_mosquito_repellent_in_packing: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [
    ("s12_prenatal_doc_in_packing", s12_prenatal_doc_in_packing, 2.0),
    ("s12_mosquito_repellent_in_packing", s12_mosquito_repellent_in_packing, 2.0),
]
