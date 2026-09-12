"""Stage 0 — initial information gathering."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _file_read_in_stage,
    _tool_called_in_stage,
    _tool_with_args,
    _has_bad_advice,
    BAD_ADVICE_L1,
    _stage_text,
    _any,
    _has_stage_substance,
)


def s0_read_user_materials(env) -> bool:
    """Agent reads both USER.md and TOOLS.md in stage 0 (must understand user + available tools)."""
    ok_user = _file_read_in_stage(env, 0, "USER.md")
    ok_tools = _file_read_in_stage(env, 0, "TOOLS.md")
    ok = ok_user and ok_tools
    logger.info(f"s0_read_user_materials: user={ok_user} tools={ok_tools} -> {ok}")
    return ok


def s0_searched_flights(env) -> bool:
    """Agent searches flights for PEK/SFO on 3/26 or 3/27 AND checks flight details."""
    searched = _tool_with_args(
        env, 0, ["search_flights"], origin=["PEK"], destination=["SFO"]
    )
    # Use the public mock schema exactly: departure_date is the authoritative date key.
    has_date = _tool_with_args(env, 0, ["search_flights"], departure_date=["2026-03-26", "2026-03-27"])
    has_detail = _tool_called_in_stage(env, 0, ["get_flight_offer", "get_booking", "price_offer"])  # real flight detail tools (was phantom get_flight)
    ok = searched and has_date and has_detail
    logger.info(f"s0_searched_flights: searched={searched} date={has_date} detail={has_detail} -> {ok}")
    return ok


def s0_searched_hotels(env) -> bool:
    """Agent searches hotels in San Francisco covering summit window."""
    searched = _tool_with_args(env, 0, ["search_hotels"], city_or_geo=["San Francisco"])
    has_dates = _tool_with_args(
        env, 0, ["search_hotels"],
        check_in=["2026-03-26", "2026-03-27", "2026-03-28"],
        check_out=["2026-03-30", "2026-03-31", "2026-04-01"],
    )
    ok = searched and has_dates
    logger.info(f"s0_searched_hotels: searched={searched} dates={has_dates} -> {ok}")
    return ok


def s0_queried_health(env) -> bool:
    """Agent checks both health profile and restrictions, and records constraint in response/doc."""
    # Real health_tracker tools (get_health_profile/get_health_restrictions were phantom).
    profile = _tool_called_in_stage(env, 0, ["get_goals", "get_metric_summary", "get_metrics", "get_activity_summary"])
    restrictions = _tool_called_in_stage(env, 0, ["list_health_alerts", "get_goals", "get_goal_progress"])
    text = _stage_text(env, 0)
    # evidence that agent understood the constraint
    understood = _any(
        text,
        ["lumbar spine", "business class", "business", "transit", "stopover", "connecting", "10 hours", "ten hours", "health"],
    )
    ok = profile and restrictions and understood
    logger.info(f"s0_queried_health: profile={profile} restrictions={restrictions} understood={understood} -> {ok}")
    return ok


def s0_queried_visa_and_banking(env) -> bool:
    """Agent checks both visa/passport/EVUS status AND banking/policy status."""
    visa = _tool_called_in_stage(
        env,
        0,
        # Real visa_and_advisory tools (get_passport_info/get_visa_info/get_evus_status were phantom).
        ["list_visa_applications", "get_visa_application", "check_entry_requirements"],
    )
    banking = _tool_called_in_stage(
        env,
        0,
        # Real banking tools (get_account_balance/get_reimbursement_remaining/list_approvals/get_approval were phantom).
        ["get_account", "list_accounts", "list_transactions"],
    )
    ok = visa and banking
    logger.info(f"s0_queried_visa_and_banking: visa={visa} banking={banking} -> {ok}")
    return ok


def s0_no_bad_advice(env) -> bool:
    """Agent response in stage 0 contains no lazy/irresponsible advice."""
    text = _stage_text(env, 0)
    ok = _has_stage_substance(env, 0) and not _has_bad_advice(text, BAD_ADVICE_L1)
    logger.info(f"s0_no_bad_advice: {ok}")
    return ok


CHECKS = [
    ("s0_read_user_materials", s0_read_user_materials, 1.0),
    ("s0_searched_flights", s0_searched_flights, 1.25),
    ("s0_searched_hotels", s0_searched_hotels, 1.25),
    ("s0_queried_health", s0_queried_health, 1.0),
    ("s0_queried_visa_and_banking", s0_queried_visa_and_banking, 1.0),
    ("s0_no_bad_advice", s0_no_bad_advice, 1.0),
]
