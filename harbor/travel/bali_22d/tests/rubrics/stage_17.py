"""Stage 17: verify the upgraded Ubud storm was checked and persisted."""
from __future__ import annotations

from .shared._helpers import _call, _tool_call_matches, workspace_file_content


def s17_ubud_storm_state_verified(env) -> bool:
    called_alerts = _tool_call_matches(
        env, "weather", "get_alerts", lambda a: "bali_ubud" in str(a.get("geo") or "").lower(), stage=17
    )
    called_forecast = _tool_call_matches(
        env, "weather", "get_forecast_daily", lambda a: "bali_ubud" in str(a.get("geo") or "").lower() and int(a.get("days") or 0) >= 3, stage=17
    )
    alerts = _call(env, "weather", "get_alerts", geo="bali_ubud")
    blob = str(alerts).lower()
    return bool(called_alerts and called_forecast and "alert_storm_ubud" in blob and "80-120mm" in blob)


def s17_storm_risk_persisted(env) -> bool:
    text = (
        workspace_file_content(env, "/workspace/risk_register.md")
        + "\n"
        + workspace_file_content(env, "/workspace/itinerary.md")
        + "\n"
        + workspace_file_content(env, "/workspace/HEARTBEAT.md")
    ).lower()
    return (
        "2026-06-20" in text
        and any(x in text for x in ("80-120", "storm", "storm"))
        and any(x in text for x in ("flood", "flood", "road closure", "road closure"))
        and any(x in text for x in ("owner", "owner"))
        and any(x in text for x in ("next review", "next check", "next check"))
    )


CHECKS = [
    ("s17_ubud_storm_state_verified", s17_ubud_storm_state_verified, 1.25),
    ("s17_storm_risk_persisted", s17_storm_risk_persisted, 1.25),
]
