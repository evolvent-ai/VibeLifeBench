"""Stage 9 — retain the rejected/supplement-needed flooring claim state."""
from .shared import _helpers as R
from .shared import _helpers as H

def s9_servers(env):
    return H.claim(env, "rejected", 2418000) and H.notification(env, "ntf_qflr_b2", ("ref_qflr_b", "rejected")) and (R.trace_has_success(env, 9, ("ecommerce", "notification_hub"), min_count=1) and R.artifact_active(env, "/workspace/evidence_log.md"))

def s9_args(env):
    return H.claim(env, "rejected", 2418000) and (R.artifact_has(env, "/workspace/evidence_log.md", (("ref_qflr_b",), ("ntf_qflr_b2", "supplementation"))))

def s9_result(env):
    return R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected'", ("ref_qflr_b",), "/workspace/evidence_log.md", (("measurement points",), ("moisture content",), ("two-meter straightedge", "flatness"), ("pressure test",), ("rejected", "supplementation needed")))

CHECKS = [("s9_servers", s9_servers, 0.5), ("s9_args", s9_args, 0.5), ("s9_result", s9_result, 2.5)]
