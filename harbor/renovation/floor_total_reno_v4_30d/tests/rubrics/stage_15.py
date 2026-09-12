"""Stage 15 — use released weather as a flooring schedule constraint, not a verdict."""
from .shared import _helpers as R
from .shared import _helpers as H

def s15_servers(env):
    return H.weather_window(env) and (R.trace_has_success(env, 15, ("weather", "ecommerce"), min_count=1) and R.artifact_active(env, "/workspace/evidence_log.md"))

def s15_result(env):
    return R.backend_and_artifact(env, "weather", "SELECT COUNT(*) FROM daily_weather WHERE geo_key=? AND date BETWEEN '2026-07-02' AND '2026-07-09'", ("geo_qflr",), "/workspace/decision_log.md", (("July 9", "2026-07-09"), ("flooring installation window",), ("moisture content",), ("weather", "humidity")))

def s15_weather(env):
    return R.backend_exists(env, "weather", "SELECT COUNT(*) FROM alerts WHERE alert_id=? AND active=1", ("alr_qflr_rain_0702",)) and R.artifact_has(env, "/workspace/evidence_log.md", (("weather",), ("on-site reinspection",), ("cannot replace", "not equal to"), ("moisture content", "substrate")))

CHECKS = [("s15_servers", s15_servers, 0.5), ("s15_result", s15_result, 3.0), ("s15_weather", s15_weather, 2.5)]
