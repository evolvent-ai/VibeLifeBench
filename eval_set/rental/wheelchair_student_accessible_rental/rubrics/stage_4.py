from __future__ import annotations
from ._helpers import *


def s4_review_risk_sources(env) -> bool:
    # Stage 4 mutates reviews for Candidate A (珞桂家园) and Candidate C
    # (云栖苑).  Candidate B belongs to later risk events and must not stand in
    # for the current event object.
    return (
        stage_review_checked(env, 4, "a", [("坡道",), ("门厅", "电梯"), ("晚间", "夜间", "电动车")])
        and stage_review_checked(env, 4, "c", [("入口", "坡道", "无台阶"), ("电梯", "保养", "维护"), ("卫生间", "回转", "现场")])
        and stage_record_persisted(
            env,
            4,
            [
                ("珞桂家园", C.LIST_A),
                ("云栖苑", C.LIST_C),
                ("评价", "住户"),
                ("电梯",),
                ("坡道",),
                ("现场", "核验", "测量", "确认"),
            ],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
    )


def s4_risk_page_update(env) -> bool:
    return (
        s4_review_risk_sources(env)
        and stage_record_persisted(
            env,
            4,
            [
                ("珞桂家园", C.LIST_A),
                ("云栖苑", C.LIST_C),
                ("晚间", "坡道", "入口"),
                ("电梯", "维护", "保养"),
                ("卫生间", "门宽", "现场"),
                ("风险", "待核验", "确认"),
            ],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and no_forbidden_side_effects(env)
    )


CHECKS = [
    ('s4_review_risk_sources', s4_review_risk_sources, 1.5),
    ('s4_risk_page_update', s4_risk_page_update, 1.25),
]
