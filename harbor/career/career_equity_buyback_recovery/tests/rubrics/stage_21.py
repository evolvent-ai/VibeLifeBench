"""Stage 21 — benchmark future business stage:use real application ID close both tracks."""
from __future__ import annotations

from ._helpers import has_values, record_text, text_has, unique_application_for_job


def s21_wrapup_equity(env) -> bool:
    record = record_text(env, "final_review.md")
    required = ("<20240520-rsu-plan@yiweicloud.com>", "acct_eq_main", "689611", "5000", "2026-05-08", "59.42", "297100", "200100", "tx_gk_severance", "97000")
    if not has_values(record, *required):
        return False
    return text_has(record, [
        ["payment"], ["unsettled"], ["salary only as income support"],
        ["unauthorizedsigning", "unauthorizedsend"], ["continue negotiation"], ["consult a lawyer"], ["arbitration", "litigation"],
    ])


def s21_wrapup_reemploy(env) -> bool:
    app = unique_application_for_job(env, "job_gk_0001", {"offer"})
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "final_review.md")
    required = (app_id, "job_gk_0001", "<20260706-offer@dewu.com>")
    if not all(value.lower() in record for value in required):
        return False
    return text_has(record, [
        ["formal Meituan offer"], ["indicative"],
        ["lean toward Meituan"], ["you decide", "whether to accept you decide"], ["unresolved"], ["continue follow-up", "reply to the offer"],
    ])


CHECKS = [
    ("s21_wrapup_equity", s21_wrapup_equity, 2.0),
    ("s21_wrapup_reemploy", s21_wrapup_reemploy, 1.5),
]
