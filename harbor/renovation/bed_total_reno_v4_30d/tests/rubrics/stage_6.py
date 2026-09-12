"""Stage 6 — classify the imported-hinge transaction without premature dispute."""
from .shared import _helpers as R
from .shared import _backend as B

def s6_servers(env):
    return B.fx_sources(env) and R.trace_has_success(env, 6, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/budget.md")

def s6_args(env):
    return B.fx_sources(env) and R.artifact_has(env, "/workspace/evidence_log.md", (("ntf_qbed_fx", "imported hinges"), ("card_qbed_01", "credit card")))

def s6_result(env):
    return B.fx_sources(env) and R.backend_and_artifact(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qbed_fx",), "/workspace/budget.md", (("foreign currency", "original currency"), ("pending verification", "pending"), ("not refunded", "not disputed")))

CHECKS = [("s6_servers", s6_servers, 0.5), ("s6_args", s6_args, 0.5), ("s6_result", s6_result, 1.5)]
