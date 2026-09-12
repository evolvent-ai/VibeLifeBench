from __future__ import annotations

from ._helpers import health_metric_has, stage_record


def chk_s01_health_fields(env) -> bool:
    observed = (
        health_metric_has(env, "sleep_minutes", ({"value": 366}, {"value_text": "baseline_sleep_minutes=366; source=wearable_7d_summary; status=complete"}, {"recorded_at": "2026-09-02T08:05:00+08:00"}))
        and health_metric_has(env, "steps", ({"value": 7640}, {"recorded_at": "2026-09-02T08:06:00+08:00"}))
        and health_metric_has(env, "heart_rate", ({"value": 63}, {"recorded_at": "2026-09-02T08:07:00+08:00"}))
        and health_metric_has(env, "score", ({"value": 2}, {"value_text": "baseline_edema_score=2; exertion_level=4; fatigue_level=5; self_reported_after_duty=true"}, {"recorded_at": "2026-09-02T08:08:00+08:00"}))
    )
    recorded = stage_record(
        env,
        "risk_log.md",
        1,
        (("sleep",), ("swelling",), ("rpe",), ("fatigue",), ("steps",)),
        ("Evidence/source", "Risk level", "Load/change", "Review threshold", "Status"),
    )
    return observed and recorded


CHECKS = [("chk_s01_health_fields", chk_s01_health_fields, 1.5)]
