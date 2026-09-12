"""Stage 15: user asks book hotel."""
from __future__ import annotations
from loguru import logger
from ._helpers import _tool_called_in_stage, _hotel_reservations, _hotel_covers_summit


def s15_booked_hotel(env) -> bool:
    """Stage 15 called book_hotel AND backend has a San Francisco hotel reservation covering the summit window."""
    tool_ok = _tool_called_in_stage(env, 15, ["create_reservation"])  # real hotel_booking tool (was phantom book_hotel)
    if not tool_ok:
        logger.info("s15_booked_hotel: tool_ok=False -> False")
        return False
    hotels = _hotel_reservations(env)
    has_sf = any(_hotel_covers_summit(h) for h in hotels)
    ok = tool_ok and has_sf
    logger.info(f"s15_booked_hotel: tool_ok={tool_ok} covers_summit={has_sf} -> {ok}")
    return ok


def s15_hotel_dates(env) -> bool:
    """DEPRECATED: merged into s15_booked_hotel."""
    return True


CHECKS = [
    ("s15_booked_hotel", s15_booked_hotel, 2.0),
]
