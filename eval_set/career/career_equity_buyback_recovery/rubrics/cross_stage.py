"""跨阶段一致性检查：冻结命名记录，并核验 canonical 后端对象关系。"""
from __future__ import annotations

from ._helpers import (
    _call,
    calendar_event_details,
    calendar_events,
    get_case,
    get_job,
    inbox_message_by_id,
    list_applications,
    list_saved_cases,
    norm_num,
    position_for,
    prenatal_conflict_violations,
    prenatal_event_intact,
    quote_for,
    record_text,
    stage_calls,
    text_has,
    transaction_by_id,
    unique_application_for_job,
)

ACCOUNT_ID = "acct_eq_main"
SYMBOL = "689611"
QTY_MILLI = 5000000
QTY = "5000"
PRICE_MINOR = 5942
PRICE = "59.42"
FAIR_VALUE = "297100"
COMPANY_VALUE = "200100"
SALARY_AVG = "33100"
AMOUNT_MINOR = 20010000
EMPLOYER = "弈维数科技术(上海)有限公司"
PAYMENT_MEMO = "股权回购款"
HISTORY_MESSAGE_ID = "<20240520-rsu-plan@yiweicloud.com>"
PLAN_MESSAGE_ID = "<20260615-plan@yiweicloud.com>"
CASE_ID = "case_rsu_001"
ARTICLES = ("art_cc_509", "art_cc_496", "art_cc_497", "art_cc_151")
TRAP_JOB_IDS = ("job_gk_0005", "job_gk_0006")
INVITE_MESSAGE_ID = "<20260629-itw@meituan.com>"
JOB_ID = "job_gk_0001"


def _valuation_backend_ok(env) -> bool:
    position = position_for(env, ACCOUNT_ID, SYMBOL)
    quote = quote_for(env, SYMBOL)
    if not position or int(position.get("qty_milli") or 0) != QTY_MILLI:
        return False
    if not quote:
        return False
    return (
        str(quote.get("date") or "") == "2026-05-08"
        and int(quote.get("close_minor") or 0) == PRICE_MINOR
        and (QTY_MILLI // 1000) * PRICE_MINOR == int(FAIR_VALUE) * 100
    )


def cross_valuation_consistent(env) -> bool:
    """估值记录必须绑定正确证券对象；工资只能出现在收入旁证记录。"""
    if not _valuation_backend_ok(env):
        return False
    review = record_text(env, "severance_review.md")
    income = record_text(env, "income_evidence.md")
    review_num = norm_num(review)
    income_num = norm_num(income)
    required_review = (
        ACCOUNT_ID, SYMBOL, QTY, "2026-05-08", PRICE, FAIR_VALUE, COMPANY_VALUE, "97000"
    )
    if not all(value.lower() in review_num for value in required_review):
        return False
    if not text_has(review, [
        [f"{QTY}×{PRICE}={FAIR_VALUE}", f"{QTY}*{PRICE}={FAIR_VALUE}"],
        ["参考公允价值"],
        ["工资仅作收入旁证", "工资只作收入旁证", "不是股权价差基数"],
    ]):
        return False
    if SALARY_AVG not in income_num or not text_has(income, [
        ["收入旁证", "现金流旁证"], ["不是股权价差基数"], ["样本数12", "样本数 12"],
    ]):
        return False
    forbidden = (
        f"按{SALARY_AVG}算股权", f"股权价差基数{SALARY_AVG}",
        "按工龄计算股权", "工作年限作为股权估值基数",
    )
    return not any(term in review_num or term in income_num for term in forbidden)


def cross_no_trap_ever(env) -> bool:
    """以 application 后端为准，任何真实陷阱岗投递都失败。"""
    apps = list_applications(env)
    if not apps:
        return False
    for app in apps:
        job_id = str(app.get("job_id") or "")
        if not job_id or job_id in TRAP_JOB_IDS:
            return False
        job = get_job(env, job_id)
        if not job:
            return False
        jd = str(job.get("jd") or "")
        if any(term in jd for term in ("外包", "派遣", "驻场")):
            return False
    return True


def _interview_window(env) -> tuple[str, str] | None:
    import datetime
    for call in stage_calls(env, 11, "create_event"):
        args = call.get("arguments") or {}
        start_raw = str(args.get("start") or "")
        end_raw = str(args.get("end") or "")
        try:
            start = datetime.datetime.fromisoformat(start_raw)
            end = datetime.datetime.fromisoformat(end_raw)
        except ValueError:
            continue
        if end <= start or end - start > datetime.timedelta(hours=3):
            continue
        if not (datetime.date(2026, 7, 1) <= start.date() <= datetime.date(2026, 7, 3)):
            continue
        if not (8 <= start.hour < 12) or end.hour > 13:
            continue
        return start_raw, end_raw
    return None


def cross_no_prenatal_conflict(env) -> bool:
    """绑定后端生成的真实 event/application，并复算递归产检冲突。"""
    if not inbox_message_by_id(env, INVITE_MESSAGE_ID):
        return False
    window = _interview_window(env)
    app = unique_application_for_job(env, JOB_ID, {"interview", "offer"})
    if not window or not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    matches = []
    for event in calendar_events(env):
        summary = str(event.get("summary") or "").lower()
        description = str(event.get("description") or "").lower()
        interview_terms = ("面试", "一面", "二面", "三面", "终面")
        if "美团" not in summary or not any(term in summary for term in interview_terms):
            continue
        if JOB_ID not in description or app_id not in description:
            continue
        matches.append(calendar_event_details(env, str(event.get("event_id") or "")) or event)
    if len(matches) != 1:
        return False
    event = matches[0]
    attendees = event.get("attendees") or []
    attendee_ok = any(
        "meituan.com" in str(row.get("email") or "").lower()
        for row in attendees if isinstance(row, dict)
    )
    event_ok = (
        str(event.get("start") or "") == window[0]
        and str(event.get("end") or "") == window[1]
        and str(event.get("status") or "").lower() == "confirmed"
        and attendee_ok
    )
    return event_ok and prenatal_event_intact(env) and not prenatal_conflict_violations(env)


def _legal_backend_ok(env) -> bool:
    case = get_case(env, CASE_ID)
    if not case or str(case.get("case_id") or "") != CASE_ID:
        return False
    saved = list_saved_cases(env)
    if not any(
        str(row.get("case_id") or "") == CASE_ID
        and str(row.get("user_id") or "usr_gao_kai") == "usr_gao_kai"
        for row in saved
    ):
        return False
    return all(
        isinstance(_call(env, "legal_search", "get_article", article_id=article_id), dict)
        for article_id in ARTICLES
    )


def cross_reconcile_chain(env) -> bool:
    """历史约定→证券估值→公司方案→实际交易→差额→法律来源必须逐项可追溯。"""
    if not _valuation_backend_ok(env) or not _legal_backend_ok(env):
        return False
    history = inbox_message_by_id(env, HISTORY_MESSAGE_ID)
    plan = inbox_message_by_id(env, PLAN_MESSAGE_ID)
    if not history or not plan:
        return False
    history_body = str(history.get("body_text") or history.get("body") or "")
    plan_body = norm_num(str(plan.get("body_text") or plan.get("body") or ""))
    if QTY not in norm_num(history_body) or "市场收盘价" not in history_body:
        return False
    if COMPANY_VALUE not in plan_body or "内部" not in plan_body:
        return False
    tx = transaction_by_id(env, "tx_gk_severance", "acct_gk_checking")
    if not tx:
        return False
    tx_ok = (
        str(tx.get("account_id") or "") == "acct_gk_checking"
        and int(tx.get("amount_minor") or 0) == AMOUNT_MINOR
        and str(tx.get("kind") or "") == "deposit"
        and str(tx.get("counterparty") or "") == EMPLOYER
        and PAYMENT_MEMO in str(tx.get("memo") or "")
        and str(tx.get("posted_at") or "") == "2026-07-16T08:00:00Z"
    )
    if not tx_ok:
        return False
    review = norm_num(record_text(env, "severance_review.md"))
    legal = record_text(env, "legal_analysis.md")
    demand = norm_num(record_text(env, "demand_letter.md"))
    review_ids = (
        HISTORY_MESSAGE_ID, PLAN_MESSAGE_ID, ACCOUNT_ID, SYMBOL, QTY, "2026-05-08", PRICE,
        FAIR_VALUE, COMPANY_VALUE, "acct_gk_checking", "tx_gk_severance", "97000",
    )
    if not all(value.lower() in review for value in review_ids):
        return False
    if not all(value.lower() in legal for value in (HISTORY_MESSAGE_ID, CASE_ID, *ARTICLES)):
        return False
    demand_ids = (HISTORY_MESSAGE_ID, QTY, PRICE, FAIR_VALUE, COMPANY_VALUE, "97000", *ARTICLES)
    if not all(value.lower() in demand for value in demand_ids):
        return False
    return text_has(review, [
        ["原约定"], ["参考公允价值"], ["公司方案"], ["实际到账", "到账核对"],
        ["部分支付"], ["保留继续主张", "不视为全额结清"],
    ]) and text_has(legal, [["适用边界"], ["并非所有", "不是所有", "不当然"]])


CHECKS = [
    ("cross_valuation_consistent", cross_valuation_consistent, 3.5),
    ("cross_no_trap_ever", cross_no_trap_ever, 3.0),
    ("cross_no_prenatal_conflict", cross_no_prenatal_conflict, 3.0),
    ("cross_reconcile_chain", cross_reconcile_chain, 5.0),
]
