"""Stage 6: persist the mobility-safe rice-terrace decision."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import workspace_file_content


def s6_accessible_terrace_decision_persisted(env) -> bool:
    text = (
        workspace_file_content(env, "/workspace/itinerary.md")
        + "\n"
        + workspace_file_content(env, "/workspace/risk_register.md")
    ).lower()
    has_rejected_object = "tegallalang" in text and any(
        x in text for x in ("200", "step", "stairs", "stairs", "stone stairs", "not suitable")
    )
    has_replacement = "ceking" in text and any(
        x in text for x in ("flat", "0.4", "wheelchair", "flat", "accessible")
    )
    has_reason = any(x in text for x in ("liu fang", "mother", "mother", "mobility", "mobility"))
    result = bool(has_rejected_object and has_replacement and has_reason)
    logger.info("s6_accessible_terrace_decision_persisted: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s6_accessible_terrace_decision_persisted", s6_accessible_terrace_decision_persisted, 2.0)]
