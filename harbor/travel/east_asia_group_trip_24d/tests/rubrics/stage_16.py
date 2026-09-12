"""Stage 16: exact Korea advisory recheck and durable route response."""
from __future__ import annotations

from ._helpers import _call, _tool_calls, _workspace_file_text


def s16_kr_level3_rechecked(env) -> bool:
    queried = any(
        str(call.get("name") or "").lower().replace("-", "_").endswith("get_advisory")
        and (call.get("arguments") or {}).get("country_code") == "KR"
        for call in _tool_calls(env, 16)
    )
    if not queried:
        return False
    advisory = _call(env, "visa_and_advisory", "get_advisory", country_code="KR")
    if not isinstance(advisory, dict):
        raise ValueError("visa_and_advisory.get_advisory returned an invalid payload")
    text = str(advisory.get("text") or "").casefold()
    return (
        advisory.get("country_code") == "KR"
        and advisory.get("level") == 3
        and "seoul" in text
        and "social unrest" in text
        and "avoid" in text
    )


def s16_route_and_risk_response_persisted(env) -> bool:
    risk = _workspace_file_text(env, "/workspace/risk_register.md").casefold()
    itinerary = _workspace_file_text(env, "/workspace/itinerary.md").casefold()
    return (
        "kr" in risk
        and "level 3" in risk
        and "social unrest" in risk
        and "owner" in risk
        and "next review" in risk
        and "avoid demonstrations" in risk
        and "2026-06-08" in itinerary
        and "seoul" in itinerary
        and "route changed" in itinerary
        and "indoor fallback" in itinerary
        and "hotel-return" in itinerary
    )


CHECKS = [
    ("s16_kr_level3_rechecked", s16_kr_level3_rechecked, 1.0),
    ("s16_route_and_risk_response_persisted", s16_route_and_risk_response_persisted, 1.0),
]
