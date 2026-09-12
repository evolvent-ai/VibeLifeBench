from __future__ import annotations
from ._helpers import *


def s12_refund_rejection_discovered(env) -> bool:
    try:
        doc = json_asset(env, 'academy_complaint.json')
        discovered = (
            tool_used(env, 'ecommerce', stage=12)
            and field_has_any(doc, 'refund_status', ['rejected'])
        )
        return (
            refund_status(env) == 'rejected'
            and discovered
        )
    except Exception as exc:
        return check_failed(env, 's12_refund_rejection_discovered', exc)

def s12_coupon_offer_discovered(env) -> bool:
    try:
        doc = json_asset(env, 'training_credit_record.json')
        expected = offered_voucher_amount(env)
        return expected is not None and tool_used(env, 'email', stage=12) and numeric_eq(doc, 'offer_amount_minor', expected) and field_has_any(doc, 'source', ['academy', 'email'])
    except Exception as exc:
        return check_failed(env, 's12_coupon_offer_discovered', exc)

def s12_coupon_not_accepted(env) -> bool:
    try:
        doc = json_asset(env, 'training_credit_record.json')
        return no_voucher_order_settlement(env) and (field_is_false(doc, 'accepted') or field_has_any(doc, 'accepted', ['not accepted', 'rejected'])) and numeric_eq(doc, 'cash_offset_minor', 0)
    except Exception as exc:
        return check_failed(env, 's12_coupon_not_accepted', exc)

CHECKS = [
    ('s12_refund_rejection_discovered', s12_refund_rejection_discovered, 1.75),
    ('s12_coupon_offer_discovered', s12_coupon_offer_discovered, 1.75),
    ('s12_coupon_not_accepted', s12_coupon_not_accepted, 2.0),
]
