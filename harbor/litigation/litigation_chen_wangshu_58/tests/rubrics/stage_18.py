from __future__ import annotations
from ._helpers import *


def s18_cash_paid_component_correct(env) -> bool:
    try:
        doc = json_asset(env, 'refund_calculation.json')
        expected = ecommerce_order_amount(env, 'total_minor')
        return (
            expected is not None
            and
            tool_used(env, 'ecommerce', stage=18)
            and tool_used(env, 'credit_card', stage=18)
            and numeric_eq(doc, 'cash_paid_minor', expected)
        )
    except Exception as exc:
        return check_failed(env, 's18_cash_paid_component_correct', exc)

def s18_original_coupon_separate(env) -> bool:
    try:
        doc = json_asset(env, 'refund_calculation.json')
        expected = ecommerce_order_amount(env, 'discount_minor')
        return expected is not None and numeric_eq(doc, 'original_coupon_minor', expected) and field_is_false(doc, 'original_coupon_cash_claim')
    except Exception as exc:
        return check_failed(env, 's18_original_coupon_separate', exc)

def s18_installment_fee_separate(env) -> bool:
    try:
        doc = json_asset(env, 'refund_calculation.json')
        expected = installment_fee_total(env)
        return expected > 0 and numeric_eq(doc, 'installment charges', expected) and field_has_any(doc, 'installment_fee_category', ['separate', 'credit card', 'separate'])
    except Exception as exc:
        return check_failed(env, 's18_installment_fee_separate', exc)

def s18_voucher_not_cash_component(env) -> bool:
    try:
        doc = json_asset(env, 'refund_calculation.json')
        expected = offered_voucher_amount(env)
        voucher_recorded = expected is not None and numeric_eq(doc, 'learning_voucher_minor', expected)
        zero_cash = numeric_eq(doc, 'learning_voucher_cash_offset_minor', 0)
        return tool_used(env, 'ecommerce', stage=18) and voucher_recorded and zero_cash
    except Exception as exc:
        return check_failed(env, 's18_voucher_not_cash_component', exc)

def s18_deductions_marked_disputed(env) -> bool:
    try:
        doc = json_asset(env, 'refund_calculation.json')
        return (
            refund_status(env) == 'rejected'
            and '现金退款' in ecommerce_order_note(env)
            and field_has_any(doc, 'platform_deduction_status', ['disputed', 'awaiting additional evidence', 'awaiting verification'])
        )
    except Exception as exc:
        return check_failed(env, 's18_deductions_marked_disputed', exc)

CHECKS = [
    ('s18_cash_paid_component_correct', s18_cash_paid_component_correct, 1.75),
    ('s18_original_coupon_separate', s18_original_coupon_separate, 1.5),
    ('s18_installment_fee_separate', s18_installment_fee_separate, 1.5),
    ('s18_voucher_not_cash_component', s18_voucher_not_cash_component, 2.0),
    ('s18_deductions_marked_disputed', s18_deductions_marked_disputed, 1.25),
]
