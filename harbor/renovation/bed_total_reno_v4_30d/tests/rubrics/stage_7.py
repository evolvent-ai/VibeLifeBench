"""Stage 7 — compare the contractor's partial offer against complete scopes."""
from .shared import _helpers as R
from .shared import _backend as B

def s7_servers(env):
    return B.offer_sources(env) and R.trace_has_success(env, 7, ("notification_hub",), min_count=1) and R.artifact_active(env, "/workspace/gear_plan.md")

def s7_args(env):
    return B.offer_sources(env) and R.backend_and_artifact(env, "notification_hub", "SELECT COUNT(*) FROM notifications WHERE notification_id=?", ("ntf_qbed_cp",), "/workspace/gear_plan.md", (("localized paint touch-up",), ("wall-side edge sealing",)))

def s7_result(env):
    return B.offer_sources(env) and R.artifact_has(env, "/workspace/gear_plan.md", (("original contractor",), ("third party",), ("termination", "self-managed"), ("schedule",), ("net cost", "net_cost_minor"), ("indoor air",), ("warranty",)))

CHECKS = [("s7_servers", s7_servers, 0.5), ("s7_args", s7_args, 0.5), ("s7_result", s7_result, 1.0)]
