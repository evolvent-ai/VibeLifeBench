"""Stage 11 — update three evidence-backed remediation alternatives."""
from .shared import _helpers as R
from .shared import _backend as B


def s11_decision(env):
    return B.rejected_rework(env) and B.inspection_report(env) and R.artifact_has(env, "/workspace/gear_plan.md", (("original contractor",), ("independently certified contractor", "third party"), ("termination", "self-managed"), ("opening and inspection",), ("schedule",), ("net cost", "net_cost_minor"), ("indoor air",), ("warranty",))) and R.artifact_has(env, "/workspace/decision_log.md", (("recommendation",), ("authorization", "final confirmation"), ("independent site record", "third party")))


CHECKS = [("s11_decision", s11_decision, 4.0)]
