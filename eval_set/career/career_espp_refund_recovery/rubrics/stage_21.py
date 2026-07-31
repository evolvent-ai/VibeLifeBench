"""Stage 21 — benchmark 未来业务阶段：用真实 application ID 闭合两条线。"""
from __future__ import annotations

from ._helpers import norm_num, record_text, text_has, unique_application_for_job


def s21_wrapup_equity(env) -> bool:
    record = record_text(env, "final_review.md")
    corpus = norm_num(record)
    required = ("<20240418-espp-plan@ximingsemi.com>", "acct_eq_main", "689612", "4955", "2026-05-08", "60.00", "297300", "200300", "tx_gk_severance", "97000")
    if not all(value.lower() in corpus for value in required):
        return False
    return text_has(record, [
        ["实际到账"], ["未结"], ["工资仅作收入旁证", "工资只作收入旁证"],
        ["未授权签署", "未授权发送"], ["继续协商"], ["咨询律师"], ["仲裁", "诉讼"],
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
        ["美团正式offer", "美团正式 offer"], ["非约束意向条件"],
        ["倾向美团"], ["由你决定", "是否接受由你决定"], ["未决事项"], ["继续跟进", "回复offer"],
    ])


CHECKS = [
    ("s21_wrapup_equity", s21_wrapup_equity, 2.0),
    ("s21_wrapup_reemploy", s21_wrapup_reemploy, 1.5),
]
