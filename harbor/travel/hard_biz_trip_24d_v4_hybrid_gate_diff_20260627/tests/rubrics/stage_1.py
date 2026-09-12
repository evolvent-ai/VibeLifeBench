"""Stage 1: flight search - persist compared facts and refund boundary."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _amount_in_text, _any, _agent_used_tool_with_args, _successful_tool_results,
    _workspace_file_text,
)


def _verified_offer_fact(env, flight_no: str) -> tuple[int, str] | None:
    for result in _successful_tool_results(env, "flight_booking", "get_flight_offer", stage=1):
        if not isinstance(result, dict):
            continue
        segments = result.get("segments") or []
        if not any(isinstance(seg, dict) and str(seg.get("flight_no") or "").upper() == flight_no for seg in segments):
            continue
        if not any(
            isinstance(seg, dict)
            and isinstance(seg.get("fare_rules"), dict)
            and seg["fare_rules"].get("refundable") is True
            and seg["fare_rules"].get("changeable") is True
            for seg in segments
        ):
            continue
        price = result.get("total_price")
        if not isinstance(price, dict) or not isinstance(price.get("amount"), (int, float)):
            continue
        return int(price["amount"]), str(price.get("currency") or "").upper()
    return None

def s1_must_name_flights(env) -> bool:
    """Must identify the actual outbound/return pair and refund boundary."""
    text = (
        _workspace_file_text(env, "/workspace/decision_log.md") + "\n" +
        _workspace_file_text(env, "/workspace/itinerary.md")
    ).lower()
    has_outbound = _any(text, ["mu523"])
    has_return = _any(text, ["mu524"])
    outbound_fact = _verified_offer_fact(env, "MU523")
    return_fact = _verified_offer_fact(env, "MU524")
    has_prices = (
        outbound_fact is not None
        and return_fact is not None
        and outbound_fact[1] == "CNY"
        and return_fact[1] == "CNY"
        and _amount_in_text(text, outbound_fact[0])
        and _amount_in_text(text, return_fact[0])
        and _any(text, ["cny"])
    )
    has_refund = _any(text, ["refundable", "changeable", "flex", "approval"])
    ok = has_outbound and has_return and has_prices and has_refund
    logger.info(f"s1_must: outbound={has_outbound} return={has_return} prices={has_prices} refund={has_refund} -> {ok}")
    return ok

def s1_tool_used(env) -> bool:
    searched_out = _agent_used_tool_with_args(env, "flight_booking", "search_flights", ["pvg", "nrt"], stage=1)
    searched_return = _agent_used_tool_with_args(env, "flight_booking", "search_flights", ["nrt", "pvg"], stage=1)
    ok = searched_out and searched_return
    logger.info(f"s1_tool: {ok}")
    return ok

CHECKS = [
    ("s1_must_name_flights", s1_must_name_flights, 2.5),
    ("s1_tool_used", s1_tool_used, 1.0),
]
