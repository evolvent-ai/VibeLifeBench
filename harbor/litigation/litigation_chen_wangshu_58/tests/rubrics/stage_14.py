from __future__ import annotations
from ._helpers import *


def s14_installment_fees_refreshed(env) -> bool:
    try:
        doc = json_asset(env, 'installment_dispute.json')
        expected = installment_fee_total(env)
        return (
            tool_used(env, 'credit_card', stage=14)
            and expected > 0
            and numeric_eq(doc, 'fee_total_minor', expected)
        )
    except Exception as exc:
        return check_failed(env, 's14_installment_fees_refreshed', exc)


CHECKS = [('s14_installment_fees_refreshed', s14_installment_fees_refreshed, 1.75)]
