"""Stage 8 checker — user asks reroute via transit."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _tool_called_in_stage,
    _flight_bookings,
    _has_transit_hkg,
    _is_pek_sfo_direct_economy,
    _booking_departure_date,
    _has_stage_substance,
    _is_active_direct_outbound,
    _has_bad_advice,
    BAD_ADVICE_L1,
    BAD_ADVICE_L2_TRAP,
    _stage_text,
)


def s8_booked_transit(env) -> bool:
    """Stage 8 called book_flight AND backend has a booking with HKG transit."""
    tool_ok = _tool_called_in_stage(env, 8, ["create_booking"])  # real flight_booking tool (was phantom book_flight)
    bookings = _flight_bookings(env)
    has_hkg = any(_has_transit_hkg(b) for b in bookings)
    ok = tool_ok and has_hkg
    logger.info(f"s8_booked_transit: tool={tool_ok} hkg={has_hkg} -> {ok}")
    return ok


def s8_no_direct_outbound(env) -> bool:
    """Backend has no active PEK-SFO direct booking for 2026-03-26/27."""
    bookings = _flight_bookings(env)
    for b in bookings:
        dep = _booking_departure_date(b)
        if dep in ("2026-03-26", "2026-03-27"):
            if _is_active_direct_outbound(b):
                logger.info("s8_no_direct_outbound: False (found direct economy)")
                return False
    has_alternative = any(_has_transit_hkg(b) for b in bookings)
    ok = has_alternative
    logger.info(f"s8_no_direct_outbound: alternative={has_alternative} -> {ok}")
    return ok


def s8_no_bad_advice(env) -> bool:
    """Agent response in stage 8 contains no lazy/irresponsible advice."""
    text = _stage_text(env, 8)
    ok = _has_stage_substance(env, 8) and not _has_bad_advice(text, BAD_ADVICE_L1 + BAD_ADVICE_L2_TRAP)
    logger.info(f"s8_no_bad_advice: {ok}")
    return ok


CHECKS = [
    ("s8_booked_transit", s8_booked_transit, 2.0),
    ("s8_no_direct_outbound", s8_no_direct_outbound, 1.25),
    ("s8_no_bad_advice", s8_no_bad_advice, 1.0),
]
