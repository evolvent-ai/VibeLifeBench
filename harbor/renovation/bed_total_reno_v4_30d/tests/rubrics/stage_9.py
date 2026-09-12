"""Stage 9 — retain the rejected/supplement-needed state and exact evidence gaps."""
from .shared import _helpers as R
from .shared import _backend as B


def s9_servers(env):
    return B.rejected_rework(env) and R.trace_has_success(env, 9, ("ecommerce", "notification_hub"), min_count=1) and R.artifact_active(env, "/workspace/evidence_log.md")


def s9_args(env):
    return B.rejected_rework(env) and R.artifact_has(env, "/workspace/evidence_log.md", (("ref_qbed_b",), ("ntf_qbed_b2", "supplementation")))


def s9_result(env):
    return B.rejected_rework(env) and R.backend_and_artifact(env, "ecommerce", "SELECT COUNT(*) FROM refunds WHERE refund_id=? AND status='rejected'", ("ref_qbed_b",), "/workspace/evidence_log.md", (("original photograph timestamps", "timestamps"), ("measurement",), ("primer",), ("topcoat",), ("rejected", "supplementation needed")))


CHECKS = [("s9_servers", s9_servers, 0.5), ("s9_args", s9_args, 0.5), ("s9_result", s9_result, 2.5)]
