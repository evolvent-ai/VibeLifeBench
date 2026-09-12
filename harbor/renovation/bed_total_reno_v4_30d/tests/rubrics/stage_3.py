"""Stage 3 — observe the submitted rework case in backend state."""
from .shared import _helpers as R
from .shared import _backend as B

def s3_servers(env):
    return B.submitted_rework(env) and R.trace_has_success(env, 3, ("ecommerce", "notification_hub"), min_count=1) and R.artifact_active(env, "/workspace/order_tracker.md")

def s3_args(env):
    return B.submitted_rework(env) and R.artifact_has(env, "/workspace/evidence_log.md", (("ref_qbed_b",), ("ord_qbed_0001",), ("edge sealing",), ("paint finish",)))

def s3_result(env):
    return B.submitted_rework(env) and R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='submitted' AND refund_amount_minor=2040000", ("ref_qbed_b",), "/workspace/order_tracker.md", (("ref_qbed_b",), ("submitted",), ("not accepted", "deferred")))

CHECKS = [("s3_servers", s3_servers, 0.5), ("s3_args", s3_args, 1.0), ("s3_result", s3_result, 2.0)]
