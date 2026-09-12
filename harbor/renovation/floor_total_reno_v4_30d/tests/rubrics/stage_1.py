"""Stage 1 — persist cross-service flooring state distinctions."""
from .shared import _helpers as R
from .shared import _helpers as H

def s1_servers(env):
    return H.initial_core(env) and H.layer_notice(env) and (R.traced_persisted_evidence(env, 1, ("ecommerce", "delivery_logistics", "credit_card", "listing_platform"), "/workspace/order_tracker.md", (("marketplace", "order"), ("logistics", "arrived on site"), ("listing", "display")), min_servers=3))

def s1_args(env):
    return R.three_threads_present(env, ("ord_qflr_0001", "ord_qflr_0002", "lst_qflr_0001"))

def s1_result(env):
    return H.initial_core(env) and H.layer_notice(env) and (R.artifact_has(env, "/workspace/budget.md", (("paid_minor",), ("resale_received_minor",), ("not posted", "0"))) and R.heartbeat_has_stage(env, 1))

CHECKS = [("s1_servers", s1_servers, 0.5), ("s1_args", s1_args, 0.5), ("s1_result", s1_result, 1.0)]
