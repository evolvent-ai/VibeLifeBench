"""Stage 15 — use released rainfall forecast as a safe retest constraint."""
from .shared import _helpers as R


def _retest_state(env):
    forecast = R.scalar(env, "weather", "SELECT COUNT(*) FROM daily_weather WHERE geo_key=? AND date IN ('2026-07-02','2026-07-03','2026-07-05','2026-07-07','2026-07-09')", ("geo_qgrd",)) == 5
    alert = R.backend_exists(env, "weather", "SELECT COUNT(*) FROM alerts WHERE alert_id=? AND active=1 AND areas_json LIKE ?", ("alr_qgrd_retest_0703", "%Xi'an%"))
    claim = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected'", ("ref_qgrd_b",))
    return forecast and alert and claim


def s15_servers(env):
    return R.trace_has_success(env, 15, ("weather", "ecommerce"), min_count=2) and _retest_state(env) and R.artifact_active(env, "/workspace/evidence_log.md")


def s15_result(env):
    forecast = R.scalar(env, "weather", "SELECT COUNT(*) FROM daily_weather WHERE geo_key=? AND date IN ('2026-07-02','2026-07-03','2026-07-05','2026-07-07','2026-07-09')", ("geo_qgrd",)) == 5
    return forecast and R.artifact_has(env, "/workspace/decision_log.md", (("July 9", "2026-07-09"), ("retest window", "rain test"), ("grading",), ("connection elevation difference",)))


def s15_weather(env):
    return R.backend_exists(env, "weather", "SELECT COUNT(*) FROM alerts WHERE alert_id=? AND active=1", ("alr_qgrd_retest_0703",)) and R.artifact_has(env, "/workspace/evidence_log.md", (("weather",), ("drainage time",), ("cannot replace", "not equal"), ("nursery-stock protection",), ("outdoor light", "power off")))


CHECKS = [("s15_servers", s15_servers, 0.5), ("s15_result", s15_result, 3.0), ("s15_weather", s15_weather, 2.5)]
