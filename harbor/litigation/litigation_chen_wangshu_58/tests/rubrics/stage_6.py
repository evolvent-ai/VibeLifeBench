from __future__ import annotations
from ._helpers import *


def s6_refund_request_exists(env) -> bool:
    try:
        doc = json_asset(env, 'refund_request.json')
        return (
            tool_used(env, 'ecommerce', stage=6)
            and target_refund_valid(env)
            and field_has_any(doc, 'order_id', [TARGET_ORDER_ID])
        )
    except Exception as exc:
        return check_failed(env, 's6_refund_request_exists', exc)


def s6_cash_refund_requested(env) -> bool:
    try:
        doc = json_asset(env, 'refund_request.json')
        return (
            target_refund_valid(env)
            and field_has_any(doc, 'requested_method', ['cash', 'original payment method'])
            and field_is_false(doc, 'voucher_requested')
            and numeric_eq(doc, 'cash_paid_minor', ecommerce_order_amount(env, 'total_minor') or -1)
        )
    except Exception as exc:
        return check_failed(env, 's6_cash_refund_requested', exc)


CHECKS = [
    ('s6_refund_request_exists', s6_refund_request_exists, 1.75),
    ('s6_cash_refund_requested', s6_cash_refund_requested, 1.25),
]
