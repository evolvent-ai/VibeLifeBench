"""Stage 24 checker: notification — aircraft change, reselect seat."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _stage_tools,
    _stage_text,
    _tool_called_in_stage,
    _call,
    _flatten_text,
    _any,
)


def s24_checked_booking(env) -> bool:
    """Stage 24 called get_booking or list_bookings AND response text shows awareness of aircraft change / seat invalidation."""
    tool_ok = _tool_called_in_stage(env, 24, ["get_booking", "list_bookings"])
    text = _stage_text(env, 24)
    understands = _any(text, ["aircraft type", "change", "aircraft change", "seat", "seat selection", "invalid", "reselect"])
    ok = tool_ok and understands
    logger.info(f"s24_checked_booking: tool_ok={tool_ok} understands={understands} -> {ok}")
    return ok


def s24_selected_seat(env) -> bool:
    """Stage 24 called select_seat AND backend booking has a seat assigned."""
    # get_seat_map is read-only; only check_in can persist the seat assignment.
    select_tool = _tool_called_in_stage(env, 24, ["check_in"])

    # list_bookings returns summaries without seat detail; resolve every PNR.
    r = _call(env, "flight_booking", "list_bookings", email="liming@company.com")
    bookings = []
    if isinstance(r, list):
        bookings = [b for b in r if isinstance(b, dict)]
    elif isinstance(r, dict):
        bookings = [b for b in (r.get("bookings") or r.get("pnrs") or []) if isinstance(b, dict)]

    has_seat = False
    for b in bookings:
        pnr = b.get("pnr")
        if not pnr:
            continue
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr)
        segments = detail.get("segments") if isinstance(detail, dict) else []
        if any(
            isinstance(segment, dict)
            and any(isinstance(seat, dict) and bool(seat.get("seat")) for seat in segment.get("seats") or [])
            for segment in segments or []
        ):
            has_seat = True
            break

    ok = select_tool and has_seat
    logger.info(f"s24_selected_seat: select_tool={select_tool}, has_seat={has_seat}")
    return ok


CHECKS = [
    ("s24_checked_booking", s24_checked_booking, 1.25),
    ("s24_selected_seat", s24_selected_seat, 2.0),
]
