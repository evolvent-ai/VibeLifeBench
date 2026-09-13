"""Stage 21 — benchmark future business stage:use real application ID close both tracks."""
from __future__ import annotations

from ._helpers import norm_num, record_text, text_has, unique_application_for_job


def s21_wrapup_equity(env) -> bool:
    record = record_text(env, "final_review.md")
    corpus = norm_num(record)
    required = ("<20240418-espp-plan@ximingsemi.com>", "acct_eq_main", "689612", "4955", "2026-05-08", "60.00", "297300", "200300", "tx_gk_severance", "97000")
    if not all(value.lower() in corpus for value in required):
        return False
    return text_has(record, [
        ["payment"], ["pending"], ["income", "income"],
        ["signing", "send"], ["review"], ["lawyer"], ["arbitration", "arbitration"],
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
        ["formal Meituan offer", "formal Meituan offer"], ["non-binding terms"],
        # "lean towardMeituan" is the oracle's concatenation artifact; accept the
        # natural spaced spellings of the same decision so a correct final review
        # is not failed on whitespace.
        ["lean towardMeituan", "lean toward meituan", "lean towards meituan"],
        ["decision", "decision"], ["status"], ["follow-up", "offer"],
    ])


CHECKS = [
    ("s21_wrapup_equity", s21_wrapup_equity, 2.0),
    ("s21_wrapup_reemploy", s21_wrapup_reemploy, 1.5),
]
