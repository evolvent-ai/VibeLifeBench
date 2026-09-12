from __future__ import annotations

from ._helpers import _call_json, _tool_call_matches, _workspace_file_text, text_has


def s23_exact_rechecks(env) -> bool:
    return _tool_call_matches(env, ["weather__get_forecast_daily"], lambda a: str(a.get("geo", "")).lower() == "kyoto" and int(a.get("days") or 0) >= 2, 23) and _tool_call_matches(env, ["rail_booking__get_train_status"], lambda a: a.get("train_no") == "A1738" and a.get("date") == "2026-10-16", 23)


def s23_backend_weather_and_rail(env) -> bool:
    rechecked = s23_exact_rechecks(env)
    weather = _call_json(env, "weather", "get_forecast_daily", geo="kyoto", days=2)
    rail = _call_json(env, "rail_booking", "get_train_status", train_no="A1738", date="2026-10-16")
    rows = (weather.get("daily") or weather.get("forecast") or []) if isinstance(weather, dict) else []
    backend = any(x.get("date") == "2026-10-15" and x.get("condition") == "heavy_rain" and float(x.get("precip_prob", 0)) == 0.9 and float(x.get("precip_mm", 0)) == 28.0 and float(x.get("wind_kmh", 0)) == 18.0 for x in rows) and isinstance(rail, dict) and rail.get("train_no") == "A1738" and rail.get("date") == "2026-10-16" and rail.get("status") == "DELAYED" and rail.get("delay_min") == 35
    durable = text_has(_workspace_file_text(env, "trip_plan.md"), [["2026-10-15"], ["heavy_rain", "heavy rain"], ["28"], ["a1738"], ["35"]])
    return bool(rechecked and backend and durable)


def s23_plan_has_object_specific_recovery(env) -> bool:
    text = _workspace_file_text(env, "trip_plan.md")
    return text_has(text, [["2026-10-15"], ["heavy_rain", "heavy rain"], ["0.9", "90%"], ["indoor", "museum", "tea", "itinerary", "places", "ceremony"], ["a1738"], ["35"], ["buffer", "time"], ["owner", "responsible"], ["next review", "review"]])


CHECKS = [("s23_exact_rechecks", s23_exact_rechecks, 0.5), ("s23_backend_weather_and_rail", s23_backend_weather_and_rail, 1.0), ("s23_plan_has_object_specific_recovery", s23_plan_has_object_specific_recovery, 0.5)]
