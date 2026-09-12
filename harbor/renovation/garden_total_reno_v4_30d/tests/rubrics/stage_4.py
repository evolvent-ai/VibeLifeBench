"""Stage 4 — record rain context without converting weather into liability."""
from .shared import _helpers as R

def s4_servers(env):
    daily = R.backend_exists(env, "weather", "SELECT COUNT(*) FROM daily_weather WHERE geo_key=? AND date='2026-06-18' AND precip_mm=38.0", ("geo_qgrd",))
    alert = R.backend_exists(env, "weather", "SELECT COUNT(*) FROM alerts WHERE alert_id=? AND active=1", ("alr_qgrd_rain_0618",))
    return daily and alert and R.trace_has_success(env, 4, ("weather",), min_count=1)

def s4_reject(env):
    backend = (
        R.backend_exists(env, "weather", "SELECT COUNT(*) FROM daily_weather WHERE geo_key=? AND date='2026-06-18' AND precip_mm=38.0", ("geo_qgrd",))
        and R.backend_exists(env, "weather", "SELECT COUNT(*) FROM alerts WHERE alert_id=? AND active=1", ("alr_qgrd_rain_0618",))
    )
    return backend and R.artifact_has(env, "/workspace/evidence_log.md", (("precipitation", "38"), ("ponding location",), ("drainage time",), ("drain status",), ("elevation", "grading"), ("cannot alone", "cannot replace")))

CHECKS = [("s4_servers", s4_servers, 0.5), ("s4_reject", s4_reject, 4.0)]
