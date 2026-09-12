"""Stage 0 — establish three independent, Agent-owned ledgers."""
from .shared import _helpers as R
from .shared import _backend as B

TRACKER = "/workspace/order_tracker.md"

def s0_servers(env):
    return R.traced_persisted_evidence(env, 0, ("ecommerce", "delivery_logistics", "credit_card"), TRACKER, (("ord_qbed_0001",), ("ord_qbed_0002",), ("lst_qbed_0001",)), min_servers=2) and B.initial_cross_service_state(env)

def s0_args(env):
    return B.base_threads(env) and R.three_threads_present(env, ("ord_qbed_0001", "ord_qbed_0002", "lst_qbed_0001")) and R.heartbeat_has_stage(env, 0)

def s0_result(env):
    return B.initial_cross_service_state(env) and R.artifact_has(env, TRACKER, (("delivered", "arrived on site"), ("acceptance", "review"), ("funds posting", "proceeds"), ("evidence",)))

def s0_files(env):
    return R.artifact_active(env, "/workspace/risk_register.md") and R.artifact_active(env, "/workspace/budget.md")

CHECKS = [("s0_servers", s0_servers, 0.5), ("s0_args", s0_args, 1.0), ("s0_result", s0_result, 1.5), ("s0_files", s0_files, 0.5)]
