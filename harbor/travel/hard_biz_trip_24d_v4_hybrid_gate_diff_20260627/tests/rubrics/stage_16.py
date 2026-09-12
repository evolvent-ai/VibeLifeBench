"""Stage 16: extended stay - create refundable lodging for July 20, 2026."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _any, _stage_corpus, _agent_used_tool_with_args, _agent_booked_hotel,
    _workspace_file_text, _hotel_reservations_text, _agent_tool_call_text,
    _hotel_extension_reservations, _text_has_backend_hotel_extension_amount,
)


def s16_extended_hotel(env) -> bool:
    """Agent searched, booked, priced, and persisted the authorized extra night."""
    text = _stage_corpus(env, 16)
    searched_primary = (
        _agent_used_tool_with_args(env, "hotel_booking", "search_hotels", ["roppongi"], stage=16)
        or _agent_used_tool_with_args(env, "hotel_booking", "search_hotels", ["roppongi"], stage=16)
        or _agent_used_tool_with_args(env, "hotel_booking", "get_room_availability", ["hotel_roppongi_biz"], stage=16)
    )
    searched_fallback = (
        _agent_used_tool_with_args(env, "hotel_booking", "search_hotels", ["narita"], stage=16)
        or _agent_used_tool_with_args(env, "hotel_booking", "search_hotels", ["narita"], stage=16)
        or _agent_used_tool_with_args(env, "hotel_booking", "get_room_availability", ["hotel_narita_transit"], stage=16)
    )
    checked_exact_night = (
        _agent_used_tool_with_args(env, "hotel_booking", "get_room_availability", ["2026-07-20", "2026-07-21"], stage=16)
        or _agent_used_tool_with_args(env, "hotel_booking", "get_room_availability", ["2026-07-20"], stage=16)
    )
    persisted_text = (
        text + "\n" +
        _workspace_file_text(env, "/workspace/itinerary.md") + "\n" +
        _workspace_file_text(env, "/workspace/budget.md") + "\n" +
        _hotel_reservations_text(env) + "\n" +
        _agent_tool_call_text(env, stage=16)
    ).lower()
    has_hotel = _any(persisted_text, ["hotel_roppongi_biz", "roppongi", "roppongi business hotel", "hotel_narita_transit", "narita", "narita airport"])
    has_reservation = (
        _agent_booked_hotel(env)
        and _agent_used_tool_with_args(env, "hotel_booking", "create_reservation", [], stage=16)
        and bool(_hotel_extension_reservations(env))
    )
    has_extension_cost = _text_has_backend_hotel_extension_amount(env, persisted_text)
    has_budget_boundary = _any(persisted_text, ["budget", "not exceed", "within budget", "refundable", "cancellable"])
    ok = (searched_primary or searched_fallback) and checked_exact_night and has_hotel and has_reservation and has_extension_cost and has_budget_boundary
    logger.info(
        f"s16_extend: primary={searched_primary} fallback={searched_fallback} night={checked_exact_night} "
        f"hotel={has_hotel} reservation={has_reservation} cost={has_extension_cost} budget={has_budget_boundary} -> {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [
    ("s16_extended_hotel", s16_extended_hotel, 2.0),
]
