from __future__ import annotations
from ._helpers import *


def s20_reserved_coupon_rechecked(env) -> bool:
    try:
        doc = json_asset(env, 'training_credit_record.json')
        return (
            tool_used(env, 'ecommerce', stage=20)
            and tool_used(env, 'email', stage=20)
            and order_voucher_reserved_without_acceptance(env)
            and bool(voucher_followup_email(env))
            and field_has_any(doc, 'reserved_status', ['reserved but not accepted', 'not accepted'])
        )
    except Exception as exc:
        return check_failed(env, 's20_reserved_coupon_rechecked', exc)


def s20_reserved_not_accepted(env) -> bool:
    try:
        doc = json_asset(env, 'training_credit_record.json')
        status_recorded = field_is_false(doc, 'accepted') or field_has_any(doc, 'accepted', ['not accepted', 'rejected'])
        return order_voucher_reserved_without_acceptance(env) and bool(voucher_followup_email(env)) and status_recorded
    except Exception as exc:
        return check_failed(env, 's20_reserved_not_accepted', exc)


CHECKS = [
    ('s20_reserved_coupon_rechecked', s20_reserved_coupon_rechecked, 1.5),
    ('s20_reserved_not_accepted', s20_reserved_not_accepted, 2.0),
]
