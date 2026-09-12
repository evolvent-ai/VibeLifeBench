"""Stage 3 — observe the submitted leveling claim in backend state."""
from .shared import _helpers as R
from .shared import _helpers as H

def s3_servers(env):
    return H.claim(env, "submitted", 2418000) and H.notification(env, "ntf_qflr_b1", ("ref_qflr_b", "submitted")) and (R.trace_has_success(env, 3, ("ecommerce", "notification_hub"), min_count=1) and R.artifact_active(env, "/workspace/order_tracker.md"))

def s3_args(env):
    return H.claim(env, "submitted", 2418000) and (R.artifact_has(env, "/workspace/evidence_log.md", (("ref_qflr_b",), ("ord_qflr_0001",), ("leveling",), ("hollow spots", "moisture content"))))

def s3_result(env):
    return R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='submitted' AND refund_amount_minor=2418000", ("ref_qflr_b",), "/workspace/order_tracker.md", (("ref_qflr_b",), ("submitted", "submitted"), ("not installed", "deferred")))

CHECKS = [("s3_servers", s3_servers, 0.5), ("s3_args", s3_args, 1.0), ("s3_result", s3_result, 2.0)]
