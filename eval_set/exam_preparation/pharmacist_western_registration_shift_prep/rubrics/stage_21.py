from __future__ import annotations

from ._helpers import (
    official_status_seen,
    payment_status_stage21,
    persistent_record,
    successful_result_contains,
)


def r35_payment_status_refreshed(env) -> bool:
    return bool(
        official_status_seen(env, "approved_unpaid", "western_pharmacist", "24400")
        and successful_result_contains(
            env,
            "notification_hub",
            None,
            21,
            "approved_unpaid",
            "western_pharmacist",
            "24400",
        )
    )


def r36_exam_fee_payment_verified(env) -> bool:
    return payment_status_stage21(env)


# Compatibility for older local callers; CHECKS uses the corrected ID/name.
def r36_exam_fee_paid_authorized(env) -> bool:
    return r36_exam_fee_payment_verified(env)


def r37_budget_ledger_payment(env) -> bool:
    return bool(
        payment_status_stage21(env)
        and persistent_record(env, 21, "244", "paid", "收据", min_hits=2)
    )


CHECKS = [
    ("r35_payment_status_refreshed", r35_payment_status_refreshed, 1.5),
    ("r36_exam_fee_payment_verified", r36_exam_fee_payment_verified, 2.0),
    ("r37_budget_ledger_payment", r37_budget_ledger_payment, 1.5),
]
