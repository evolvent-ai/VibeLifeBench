from __future__ import annotations
from ._helpers import *


def s4_review_risk_sources(env) -> bool:
    # The simulated Stage-4 mutation adds reviews for Candidate A and C.
    # Candidate B belongs to later price/payment-risk events and cannot replace
    # the current review objects.
    return (
        tool_stage(env, 4, "review_platform", None, (C.MER_A,))
        and tool_stage(env, 4, "review_platform", None, (C.MER_C,))
        and review_has(env, C.MER_A, ("视频", "南门", "入口"))
        and review_has(env, C.MER_C, ("东门", "施工", "物业"))
    )


def s4_risk_page_update(env) -> bool:
    return (
        s4_review_risk_sources(env)
        and stage_record_persisted(
            env,
            4,
            [
                ("北岸花园", C.LIST_A),
                ("云栖苑", C.LIST_C),
                ("视频", "入口"),
                ("施工", "照明", "物业"),
                ("风险", "待核验", "复核", "确认"),
            ],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s4_review_risk_sources", s4_review_risk_sources, 1.5),
    ("s4_risk_page_update", s4_risk_page_update, 1.25),
]
