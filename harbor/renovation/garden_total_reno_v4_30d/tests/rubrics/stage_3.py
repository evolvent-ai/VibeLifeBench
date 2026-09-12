"""Stage 3 — observe the submitted ponding claim in backend state."""
from .shared import _helpers as R

def s3_servers(env):
    backend = (
        R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='submitted' AND refund_amount_minor=2478000", ("ref_qgrd_b",))
        and R.backend_exists(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qgrd_b1",))
    )
    return backend and R.trace_has_success(env, 3, ("ecommerce", "notification_hub"), min_count=1) and R.artifact_active(env, "/workspace/order_tracker.md")

def s3_args(env):
    backend = R.backend_exists(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND order_id=? AND status='submitted'", ("ref_qgrd_b", "ord_qgrd_0001"))
    return backend and R.artifact_has(env, "/workspace/evidence_log.md", (("ref_qgrd_b",), ("ord_qgrd_0001",), ("ponding",), ("grading", "drainage")))

def s3_result(env):
    return R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='submitted' AND refund_amount_minor=2478000", ("ref_qgrd_b",), "/workspace/order_tracker.md", (("ref_qgrd_b",), ("submitted",), ("not accepted", "pending rain test")))

CHECKS = [("s3_servers", s3_servers, 0.5), ("s3_args", s3_args, 1.0), ("s3_result", s3_result, 2.0)]
