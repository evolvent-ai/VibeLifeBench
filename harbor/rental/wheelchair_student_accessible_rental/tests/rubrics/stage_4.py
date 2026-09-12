from __future__ import annotations
from ._helpers import *


def s4_review_risk_sources(env) -> bool:
    # Stage 4 mutates reviews for Candidate A (Luogui Jiayuan) and Candidate C
    # (Yunqi Court).  Candidate B belongs to later risk events and must not stand in
    # for the current event object.
    return (
        stage_review_checked(env, 4, "a", [("ramp",), ("lobby", "elevator"), ("evening", "at night", "e-bike")])
        and stage_review_checked(env, 4, "c", [("entrance", "ramp", "step-free"), ("elevator", "maintenance", "maintenance"), ("bathroom", "turning space", "on-site")])
        and stage_record_persisted(
            env,
            4,
            [
                ("Luogui Jiayuan", C.LIST_A),
                ("Yunqi Court", C.LIST_C),
                ("review", "resident"),
                ("elevator",),
                ("ramp",),
                ("on-site", "verification", "measurement", "confirmation"),
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
                ("Luogui Jiayuan", C.LIST_A),
                ("Yunqi Court", C.LIST_C),
                ("evening", "ramp", "entrance"),
                ("elevator", "maintenance", "maintenance"),
                ("bathroom", "doorway width", "on-site"),
                ("risk", "pending verification", "confirmation"),
            ],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and no_forbidden_side_effects(env)
    )


CHECKS = [
    ('s4_review_risk_sources', s4_review_risk_sources, 1.5),
    ('s4_risk_page_update', s4_risk_page_update, 1.25),
]
