"""Stage 15: the post-arrival Ubud plan must be person-, date-, and distance-specific."""
from __future__ import annotations

import re

from loguru import logger

from .shared._helpers import workspace_file_content


def s15_daily_walking_under_3km(env) -> bool:
    text = (workspace_file_content(env, "/workspace/itinerary.md") + "\n" + workspace_file_content(env, "/workspace/risk_register.md")).casefold()
    person = any(x in text for x in ("liu fang",))
    dates = "2026-06-22" in text and any(x in text for x in ("2026-06-23", "2026-06-24", "2026-06-25"))
    cap_patterns = (
        r"(?:daily\s+walking|walking|daily)\s+(?:total|cap|limit)\s*(?:is|:|=)?\s*(?:<=|≤|under|at most|no more than|max(?:imum)?(?: of)?)?\s*3(?:\.0+)?\s*km(?:\s*(?:/|per)\s*day)?",
        r"(?:<=|≤|under|at most|no more than|max(?:imum)?(?: of)?)\s*3(?:\.0+)?\s*km(?:\s*(?:/|per)\s*day)?",
        r"\b3(?:\.0+)?\s*km\s*(?:/|per)\s*day\b",
    )
    stated_totals = [
        float(value)
        for value in re.findall(
            r"(?:daily\s+walking|walking|daily)\s+(?:total|cap|limit)[^\d]{0,24}(\d+(?:\.\d+)?)\s*km",
            text,
        )
    ]
    cap = any(re.search(pattern, text) for pattern in cap_patterns) and not any(value > 3 for value in stated_totals)
    measured = any(x in text for x in ("0.4 km", "0.4km")) and any(x in text for x in ("total", "total", "running total"))
    choices = "ceking" in text and any(x in text for x in ("taman ayun", "ubud royal palace", "palace"))
    rejection = "tegallalang" in text and any(x in text for x in ("avoid", "skip", "skip", "cancel", "stairs"))
    result = bool(person and dates and cap and measured and choices and rejection)
    logger.info("s15_daily_walking_under_3km: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s15_daily_walking_under_3km", s15_daily_walking_under_3km, 2.0)]
