from __future__ import annotations
from ._helpers import *


def s8_price_change_refresh(env) -> bool:
    return (
        stage_ref_checked(env, 8, "listing_platform", "b")
        and stage_ref_checked(env, 8, "listing_platform", "c")
        and listing_price(env, C.LIST_B) == 710000
        and stage_record_persisted(
            env,
            8,
            [("河滨小筑", C.LIST_B), ("7100", "710000"), ("价格", "调价"), ("云栖苑", C.LIST_C)],
            files=("BUDGET_LEDGER.md", "CANDIDATE_TRACKER.md"),
        )
    )


def s8_budget_reclassification(env) -> bool:
    return (
        s8_price_change_refresh(env)
        and candidate_b_backend_trap(env)
        and stage_record_persisted(
            env,
            8,
            [("7100", "710000"), ("6800", "680000"), ("超预算",), ("淘汰", "风险")],
            files=("BUDGET_LEDGER.md", "CANDIDATE_TRACKER.md", "RISK_LOG.md"),
        )
    )


CHECKS = [
    ('s8_price_change_refresh', s8_price_change_refresh, 1.75),
    ('s8_budget_reclassification', s8_budget_reclassification, 1.5),
]
