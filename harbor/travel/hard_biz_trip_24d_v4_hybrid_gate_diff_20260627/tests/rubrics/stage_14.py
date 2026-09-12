"""Stage 14: transit search - safety-critical NRT-HKG-PVG and visa checks."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _any, _stage_corpus, _agent_checked_transit_visa,
    _agent_used_tool_with_args, _workspace_file_text, _searched_hkg_recovery_quote,
    _amount_in_text,
)


def s14_searched_transit(env) -> bool:
    searched_first_leg = _agent_used_tool_with_args(env, "flight_booking", "search_flights", ["nrt", "hkg"], stage=14)
    searched_second_leg = _agent_used_tool_with_args(env, "flight_booking", "search_flights", ["hkg", "pvg"], stage=14)
    searched_traps = (
        _agent_used_tool_with_args(env, "flight_booking", "search_flights", ["nrt", "tpe"], stage=14)
        or _agent_used_tool_with_args(env, "flight_booking", "search_flights", ["nrt", "icn"], stage=14)
    )
    ok = searched_first_leg and searched_second_leg and searched_traps
    logger.info(f"s14_searched: first={searched_first_leg} second={searched_second_leg} traps={searched_traps} -> {'PASS' if ok else 'FAIL'}")
    return ok


def s14_checked_transit_visa(env) -> bool:
    text = _stage_corpus(env, 14) + "\n" + _workspace_file_text(env, "/workspace/decision_log.md").lower()
    has_hk = _any(text, ["hkg", "hong kong"])
    has_visa_call = _agent_used_tool_with_args(env, "visa_and_advisory", "check_entry_requirements", ["cn", "hk", "transit"], stage=14)
    has_visa = has_visa_call and _agent_checked_transit_visa(env) and _any(text, ["visa", "transit", "visa-free", "not required"])
    has_tpe_risk = _any(text, ["tpe", "taipei", "taiwan"]) and _any(text, ["risk", "do not select", "exclude", "visa", "entry permit"])
    ok = has_hk and has_visa and has_tpe_risk
    logger.info(f"s14_transit_visa: {'PASS' if ok else 'FAIL'}")
    return ok


def s14_found_specific_route(env) -> bool:
    """Persist the route actually returned by public search, with price and timing evidence."""
    text = (
        _stage_corpus(env, 14) + "\n" +
        _workspace_file_text(env, "/workspace/itinerary.md") + "\n" +
        _workspace_file_text(env, "/workspace/decision_log.md")
    ).lower()
    quote = _searched_hkg_recovery_quote(env, stage=14)
    has_route = bool(
        quote
        and all(number.lower() in text for number in quote["flight_numbers"])
        and _amount_in_text(text, int(quote["total_amount"]))
        and _any(text, [quote["currency"], "cny"])
    )
    has_timing = bool(
        quote
        and (
            _amount_in_text(text, int(quote["layover_min"]))
            or (int(quote["layover_min"]) == 180 and _any(text, ["3 hours", "three hours"]))
        )
        and (_any(text, ["18:58", "7/21", "2026-07-21"]))
    )
    has_decision = _any(text, ["recommend", "select", "chosen", "advise"]) and _any(text, ["mct", "transit", "connection", "visa", "risk"])
    ok = s14_searched_transit(env) and has_route and has_timing and has_decision
    logger.info(
        f"s14_route: public_quote={bool(quote)} route={has_route} timing={has_timing} "
        f"decision={has_decision} -> {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [
    # Investigation is necessary but cannot outweigh the persisted, business-correct route decision.
    ("s14_searched_transit", s14_searched_transit, 1.0),
    ("s14_checked_transit_visa", s14_checked_transit_visa, 3.0),
    ("s14_found_specific_route", s14_found_specific_route, 4.0),
]
