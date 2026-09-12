"""Stage 1 — persist cross-service state distinctions."""
from .shared import _helpers as R
from .shared import _backend as B

def s1_servers(env):
    return R.traced_persisted_evidence(env, 1, ("ecommerce", "delivery_logistics", "credit_card", "listing_platform"), "/workspace/order_tracker.md", (("marketplace", "order"), ("delivery", "arriving on site"), ("listing", "active")), min_servers=3) and B.initial_cross_service_state(env)

def s1_args(env):
    return B.base_threads(env) and B.base_delivery(env) and R.three_threads_present(env, ("ord_qbed_0001", "ord_qbed_0002", "lst_qbed_0001"))

def s1_result(env):
    return B.initial_cross_service_state(env) and R.artifact_has(env, "/workspace/budget.md", (("paid_minor",), ("resale_received_minor",), ("not received", "0"))) and R.heartbeat_has_stage(env, 1)

CHECKS = [("s1_servers", s1_servers, 0.5), ("s1_args", s1_args, 0.5), ("s1_result", s1_result, 1.0)]
