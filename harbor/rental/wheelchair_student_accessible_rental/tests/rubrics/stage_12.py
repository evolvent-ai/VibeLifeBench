from __future__ import annotations
from ._helpers import *


def s12_gate_mutation_recovered(env) -> bool:
    return (
        stage_map_alert_recovered(env, 12, "b", "rd_evt_b_gate")
        and stage_review_checked(env, 12, "b", [("entrance", "west gate"), ("lighting",), ("property management",)])
        and candidate_b_backend_trap(env)
    )


def s12_safety_risk_escalated(env) -> bool:
    return (
        s12_gate_mutation_recovered(env)
        and stage_record_persisted(
            env,
            12,
            [("Riverside Nook", C.LIST_B), ("west gate",), ("entrance",), ("lighting",), ("private transfer", "lock-in fee"), ("risk", "eliminated")],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and no_forbidden_side_effects(env)
    )


CHECKS = [
    ('s12_gate_mutation_recovered', s12_gate_mutation_recovered, 1.75),
    ('s12_safety_risk_escalated', s12_safety_risk_escalated, 2.0),
]
