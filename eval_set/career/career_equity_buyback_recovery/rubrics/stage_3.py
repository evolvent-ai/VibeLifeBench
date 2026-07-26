"""Stage 3 — 绑定历史计划邮件、民法典条文和脱敏案例。"""
from __future__ import annotations

from ._helpers import list_saved_cases, record_text, stage_call_matches, text_has

ARTICLES = ("art_cc_509", "art_cc_496", "art_cc_497", "art_cc_151")
CASE_ID = "case_rsu_001"
HISTORY_MESSAGE_ID = "<20240520-rsu-plan@yiweicloud.com>"


def s3_legal_tool_used(env) -> bool:
    if not all(stage_call_matches(env, 3, "get_article", {"article_id": aid}) for aid in ARTICLES):
        return False
    if not stage_call_matches(env, 3, "get_case", {"case_id": CASE_ID}):
        return False
    if not stage_call_matches(env, 3, "save_case", {"case_id": CASE_ID, "user_id": "usr_gao_kai"}):
        return False
    saved = list_saved_cases(env)
    return any(str(row.get("case_id") or "") == CASE_ID and str(row.get("user_id") or "usr_gao_kai") == "usr_gao_kai" for row in saved)


def s3_contract_legal_basis(env) -> bool:
    record = record_text(env, "legal_analysis.md")
    required = [HISTORY_MESSAGE_ID, CASE_ID, *ARTICLES]
    if not all(value.lower() in record for value in required):
        return False
    return text_has(record, [
        ["已归属"], ["基准日"], ["市场收盘价", "市场价"],
        ["适用边界"], ["并非所有", "不是所有", "非自动统一", "不当然"],
    ])


CHECKS = [
    ("s3_legal_tool_used", s3_legal_tool_used, 1.0),
    ("s3_contract_legal_basis", s3_contract_legal_basis, 2.5),
]
