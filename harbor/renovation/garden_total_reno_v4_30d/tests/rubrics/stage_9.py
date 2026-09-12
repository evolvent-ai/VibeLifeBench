"""Stage 9 — retain the rejected/survey-needed ponding claim state."""
from .shared import _helpers as R


def _stage9_state(env):
    rejected = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected'", ("ref_qgrd_b",))
    notice = R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=? AND payload_json LIKE ?", ("ntf_qgrd_b2", "%rain_observation%"))
    return rejected and notice


def s9_servers(env):
    return R.trace_has_success(env, 9, ("ecommerce", "notification_hub"), min_count=2) and _stage9_state(env) and R.artifact_active(env, "/workspace/evidence_log.md")


def s9_args(env):
    return _stage9_state(env) and R.artifact_has(env, "/workspace/evidence_log.md", (("ref_qgrd_b",), ("ntf_qgrd_b2", "supplement")))


def s9_result(env):
    return R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected'", ("ref_qgrd_b",), "/workspace/evidence_log.md", (("benchmark",), ("grading",), ("connection elevation difference",), ("rain observation", "drainage time"), ("rejected", "to supplement")))


CHECKS = [("s9_servers", s9_servers, 0.5), ("s9_args", s9_args, 0.5), ("s9_result", s9_result, 2.5)]
