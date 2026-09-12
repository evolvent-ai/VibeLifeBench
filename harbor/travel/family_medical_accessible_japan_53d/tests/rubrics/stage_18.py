from __future__ import annotations

from ._helpers import _call_json, _tool_call_matches, _workspace_file_text, text_has


def s18_weather_itinerary_change(env) -> bool:
    alert_call = _tool_call_matches(
        env,
        ["weather__get_alerts"],
        lambda a: str(a.get("geo") or "").lower() == "kyoto",
        stage=18,
    )
    nara_call = _tool_call_matches(
        env,
        ["weather__get_forecast_daily"],
        lambda a: str(a.get("geo") or "").lower() == "nara" and int(a.get("days") or 0) >= 14,
        stage=18,
    )
    alert = str(_call_json(env, "weather", "get_alerts", geo="kyoto")).lower()
    plan = _workspace_file_text(env, "trip_plan.md") + "\n" + _workspace_file_text(env, "decision_log.md")
    durable = text_has(
        plan,
        [["2026-10-15"], ["kyoto", "Kyoto"], ["wx_kyoto_jma_orange_20261015"], ["indoor", "indoor activity"], ["status", "state"], ["evidence", "supporting evidence"]],
    )
    return bool(alert_call and nara_call and "wx_kyoto_jma_orange_20261015" in alert and "orange" in alert and durable)


CHECKS = [("s18_weather_itinerary_change", s18_weather_itinerary_change, 2.0)]
