"""Stage 18: arrival home - initial expense-report draft."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _amount_in_text, _any, _stage_corpus, _workspace_file_nonempty, _workspace_file_text,
    _text_has_backend_flight_amounts, _text_has_backend_hotel_amounts,
)


def s18_expense_report(env) -> bool:
    """Agent produced a concrete report whose booking totals match live backends."""
    text = (
        _stage_corpus(env, 18) + "\n" +
        _workspace_file_text(env, "/workspace/budget.md") + "\n" +
        _workspace_file_text(env, "/workspace/evidence_log.md")
    ).lower()
    has_categories = all(x in text for x in ["flight", "accommodation", "registration", "insurance"])
    has_currency = _any(text, ["cny"]) and _any(text, ["jpy"])
    has_backend_flight_amounts = _text_has_backend_flight_amounts(env, text)
    has_backend_hotel_amounts = _text_has_backend_hotel_amounts(env, text)
    has_disclosed_fixed_items = all(
        _amount_in_text(text, amount) for amount in [1200, 800]
    )
    has_status = _any(text, ["paid", "settled", "actual"]) and _any(text, ["pending", "pending refund", "not received"])
    has_evidence = _any(text, ["supporting document", "invoice", "order", "receipt", "reservation", "booking"]) and _any(text, ["missing", "to be supplemented"])
    has_reimburse_scope = _any(text, ["reimbursement", "company", "reimbursable"]) and _any(text, ["self-funded", "personal", "non-reimbursable", "excluded"])
    has_report = has_categories and has_currency and has_backend_flight_amounts and has_backend_hotel_amounts and has_disclosed_fixed_items and has_status and has_evidence and has_reimburse_scope
    persisted = _workspace_file_nonempty(env, "/workspace/budget.md") and _workspace_file_nonempty(env, "/workspace/evidence_log.md")
    ok = has_report and persisted
    logger.info(
        f"s18_report: report={has_report} flight_backend={has_backend_flight_amounts} "
        f"hotel_backend={has_backend_hotel_amounts} persist={persisted} -> {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [
    ("s18_expense_report", s18_expense_report, 2.0),
]
