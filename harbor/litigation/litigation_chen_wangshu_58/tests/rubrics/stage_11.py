from __future__ import annotations
from ._helpers import *


def s11_learning_offer_indexed_without_acceptance(env) -> bool:
    try:
        doc = json_asset(env, 'training_credit_record.json')
        expected = offered_voucher_amount(env)
        return (
            expected is not None
            and
            tool_used(env, 'email', stage=11)
            and numeric_eq(doc, 'offer_amount_minor', expected)
            and (field_is_false(doc, 'accepted') or field_has_any(doc, 'accepted', ['not accepted', 'awaiting confirmation']))
            and numeric_eq(doc, 'cash_offset_minor', 0)
        )
    except Exception as exc:
        return check_failed(env, 's11_learning_offer_indexed_without_acceptance', exc)


CHECKS = [('s11_learning_offer_indexed_without_acceptance', s11_learning_offer_indexed_without_acceptance, 1.75)]
