"""Stage 11 — update three evidence-backed flooring alternatives."""
from .shared import _helpers as R
from .shared import _helpers as H

def s11_decision(env):
    return H.claim(env, "rejected", 2418000) and H.duplicate_tx(env) and H.notification(env, "ntf_qflr_cp", ("missing_tests",)) and (R.artifact_has(env, "/workspace/gear_plan.md", (("original contractor",), ("localized rework",), ("independent third party",), ("moisture content",), ("two-meter straightedge", "flatness"), ("doorway elevation difference",), ("expansion joints",), ("pressure test",), ("net cost", "net_cost_minor"), ("schedule",))) and R.artifact_has(env, "/workspace/decision_log.md", (("recommendation",), ("authorization", "final confirmation"), ("independent third party", "measurement"))))

CHECKS = [("s11_decision", s11_decision, 4.0)]
