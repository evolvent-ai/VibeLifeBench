from __future__ import annotations
from ._helpers import *


def s21_refund_state_second_recheck(env) -> bool:
    try:
        doc = json_asset(env, 'academy_complaint.json')
        return (
            tool_used(env, 'ecommerce', stage=21)
            and tool_used(env, 'email', stage=21)
            and refund_status(env) == 'rejected'
            and order_voucher_reserved_without_acceptance(env)
            and bool(voucher_followup_email(env))
            and field_has_any(doc, 'refund_status', ['rejected'])
            and (numeric_eq(doc, 'refresh_stage', 21) or field_has_any(doc, 'refresh_stage', ['21', 'second recheck']))
        )
    except Exception as exc:
        return check_failed(env, 's21_refund_state_second_recheck', exc)


def s21_complaint_tracker_updated(env) -> bool:
    try:
        doc = json_asset(env, 'academy_complaint.json')
        return (
            refund_status(env) == 'rejected'
            and order_voucher_reserved_without_acceptance(env)
            and bool(voucher_followup_email(env))
            and field_has_any(doc, 'next_action', ['supplement evidence', 'complaint', 'small claims', 'confirmation'])
            and field_is_true(doc, 'cash_refund_still_requested')
        )
    except Exception as exc:
        return check_failed(env, 's21_complaint_tracker_updated', exc)


CHECKS = [
    ('s21_refund_state_second_recheck', s21_refund_state_second_recheck, 1.5),
    ('s21_complaint_tracker_updated', s21_complaint_tracker_updated, 1.25),
]
