"""Stage 11 — update three evidence-backed drainage alternatives."""
from .shared import _helpers as R


def s11_decision(env):
    survey = R.backend_exists(env, "email", "SELECT COUNT(*) FROM messages WHERE message_id=? AND body_text LIKE ? AND body_text LIKE ?", ("<20260625.1750.47ac@inspect.example>", "%24-point elevation grid%", "%finished-surface elevation difference at connection%"))
    marker = R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_emptying_marker", "%markers_min%"))
    queried = R.trace_has_success(env, 11, ("email", "notification_hub"), min_count=2)
    options = R.artifact_has(env, "/workspace/gear_plan.md", (("surface diversion channel",), ("localized pavement removal",), ("third party",), ("grading",), ("drainage-channel connection",), ("rain test",), ("nursery stock",), ("light wiring",), ("net cost", "net_cost_minor"), ("duration",)))
    decision = R.artifact_has(env, "/workspace/decision_log.md", (("recommendation",), ("authorization", "final confirmation"), ("third party", "measurement")))
    return survey and marker and queried and options and decision


CHECKS = [("s11_decision", s11_decision, 4.0)]
