from __future__ import annotations
from . import _helpers as h


def _registration_exact(env) -> bool:
    payload = h.notification_payload(env, "registration_status", "registered") or {}
    subjects = payload.get("subjects") or []
    return bool(
        payload.get("payment_status") == "posted"
        and payload.get("amount_minor") == 24400
        and payload.get("exam_date") == "2026-08-16"
        and set(subjects) == {"法律法规与综合能力", "个人理财"}
    )


def r21_no_batch_changed_on_pay(env) -> bool:
    return bool(
        h.tool_used(env, 11, "notification_hub")
        and h.tool_used(env, 11, "calendar")
        and _registration_exact(env)
        and h.calendar_event_match(env, date="2026-08-16", status="confirmed", summary_any=("双科", "银行业"), description_all=("法律法规", "个人理财"))
    )


def r22_payment_confirmed_by_scheduled(env) -> bool:
    return bool(
        h.tool_used(env, 11, "banking")
        and h.tool_used(env, 11, "notification_hub")
        and h.official_exam_fee_payment(env)
        and _registration_exact(env)
    )


def r23_expense_ledger_complete(env) -> bool:
    return bool(
        h.tool_used(env, 11, "banking")
        and h.any_tool(env, 11, ("notion",))
        and h.official_exam_fee_payment(env)
        and h.durable_evidence_contains(
            env, "budget ledger", "budget_ledger.md",
            "24400", "备考账户", "银行业资格考试服务平台", ("恰好一笔", "一次"),
        )
    )


CHECKS = [
    ("r21_no_batch_changed_on_pay", r21_no_batch_changed_on_pay, 1.25),
    ("r22_payment_confirmed_by_scheduled", r22_payment_confirmed_by_scheduled, 1.75),
    ("r23_expense_ledger_complete", r23_expense_ledger_complete, 1.25),
]
