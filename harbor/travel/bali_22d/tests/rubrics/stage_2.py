"""Stage 2: preserve the equipment-swap seating constraint durably."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import workspace_file_content


def s2_aisle_requirement_persisted(env) -> bool:
    """GA835/B738 re-seat work records an aisle requirement for Wang Meilin."""
    text = (
        workspace_file_content(env, "/workspace/itinerary.md")
        + "\n"
        + workspace_file_content(env, "/workspace/risk_register.md")
        + "\n"
        + workspace_file_content(env, "/workspace/HEARTBEAT.md")
    ).lower()
    has_object = "ga835" in text and any(x in text for x in ("b738", "737-800", "equipment", "equipment type"))
    has_traveler = any(x in text for x in ("wang meilin", "Meilin")) and any(
        x in text for x in ("pregnan", " pregnancy")
    )
    has_seat = any(x in text for x in ("aisle", "aisle", "aisle"))
    has_open_state = any(x in text for x in ("pending", "pending", "next action", "next action"))
    result = bool(has_object and has_traveler and has_seat and has_open_state)
    logger.info("s2_aisle_requirement_persisted: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s2_aisle_requirement_persisted", s2_aisle_requirement_persisted, 2.0)]
