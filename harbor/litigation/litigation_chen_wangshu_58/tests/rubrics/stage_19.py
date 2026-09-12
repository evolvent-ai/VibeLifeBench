from __future__ import annotations
from ._helpers import *


def s19_reserved_offer_remains_unaccepted(env) -> bool:
    try:
        doc = json_asset(env, 'training_credit_record.json')
        return (
            tool_used(env, 'ecommerce', stage=19)
            and order_voucher_reserved_without_acceptance(env)
            and numeric_eq(doc, 'cash_offset_minor', 0)
            and (field_is_false(doc, 'accepted') or field_has_any(doc, 'accepted', ['not accepted', 'awaiting confirmation']))
        )
    except Exception as exc:
        return check_failed(env, 's19_reserved_offer_remains_unaccepted', exc)


CHECKS = [('s19_reserved_offer_remains_unaccepted', s19_reserved_offer_remains_unaccepted, 1.75)]
