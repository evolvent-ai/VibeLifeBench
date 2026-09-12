from __future__ import annotations
from ._helpers import *


def s4_review_risk_sources(env) -> bool:
    # The simulated Stage-4 mutation adds reviews for Candidate A and C.
    # Candidate B belongs to later price/payment-risk events and cannot replace
    # the current review objects.
    return (
        tool_stage(env, 4, "review_platform", None, (C.MER_A,))
        and tool_stage(env, 4, "review_platform", None, (C.MER_C,))
        and review_has(env, C.MER_A, ("video", "south gate", "entrance"))
        and review_has(env, C.MER_C, ("east gate", "construction", "property management"))
    )


def s4_risk_page_update(env) -> bool:
    return (
        s4_review_risk_sources(env)
        and stage_record_persisted(
            env,
            4,
            [
                ("North Shore Garden", C.LIST_A),
                ("Yunqi Court", C.LIST_C),
                ("video", "entrance"),
                ("construction", "lighting", "property management"),
                ("risk", "pending verification", "review", "confirmation"),
            ],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s4_review_risk_sources", s4_review_risk_sources, 1.5),
    ("s4_risk_page_update", s4_risk_page_update, 1.25),
]
