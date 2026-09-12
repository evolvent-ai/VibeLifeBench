from __future__ import annotations

from ._helpers import _tool_call_results, _workspace_file_text, text_has


def s17_weather_monitor(env) -> bool:
    kyoto_results = _tool_call_results(
        env, ["weather__get_forecast_daily"], lambda a: str(a.get("geo") or "").lower() == "kyoto" and int(a.get("days") or 0) >= 14, 17
    )
    nara_results = _tool_call_results(
        env, ["weather__get_forecast_daily"], lambda a: str(a.get("geo") or "").lower() == "nara" and int(a.get("days") or 0) >= 14, 17
    )
    kyoto_ok = any(isinstance(rows, list) and any(row.get("date") == "2026-10-15" and row.get("precip_prob") == 0.72 for row in rows if isinstance(row, dict)) for rows in kyoto_results)
    nara_ok = any(isinstance(rows, list) and any(row.get("date") == "2026-10-17" and row.get("precip_prob") == 0.62 for row in rows if isinstance(row, dict)) for rows in nara_results)
    return bool(kyoto_ok and nara_ok)


def s17_weather_risk_is_durable(env) -> bool:
    text = _workspace_file_text(env, "risk_register.md") + "\n" + _workspace_file_text(env, "trip_plan.md")
    return bool(text_has(text, [["2026-10-15"], ["kyoto", "Kyoto"], ["rain", "rainfall"], ["step-free", "accessibility", "mobility"], ["next review", "next review date"]]))


CHECKS = [
    ("s17_weather_monitor", s17_weather_monitor, 1.25),
    ("s17_weather_risk_is_durable", s17_weather_risk_is_durable, 1.25),
]
