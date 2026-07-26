"""Stage 13 — 将得物非约束意向条件与无补偿竞业风险正确区分。"""
from __future__ import annotations

from ._helpers import get_job, inbox_message_by_id, list_applications, record_text, stage_call_matches, stage_text, text_has

SOURCE_MESSAGE_ID = "<20260706-offer@dewu.com>"
JOB_ID = "job_gk_0007"


def s13_no_uncompensated_noncompete(env) -> bool:
    if not stage_call_matches(env, 13, "read_email", {"email_id": "105"}):
        return False
    if not stage_call_matches(env, 13, "get_job", {"job_id": JOB_ID}):
        return False
    if not inbox_message_by_id(env, SOURCE_MESSAGE_ID) or not get_job(env, JOB_ID):
        return False
    for app in list_applications(env):
        if str(app.get("user_id") or "") == "usr_gao_kai" and str(app.get("job_id") or "") == JOB_ID and str(app.get("status") or "") == "offer":
            return False
    reply = stage_text(env, 13)
    record = record_text(env, "offer_compare.md")
    required = [SOURCE_MESSAGE_ID.lower(), JOB_ID]
    if not all(value in record for value in required):
        return False
    return text_has(reply + "\n" + record, [
        ["非约束"], ["意向条件"], ["待面试", "面试与审批"],
        ["不是正式offer", "不是正式 offer", "非正式offer"],
        ["2年竞业", "2 年竞业"], ["未约定补偿", "无补偿"],
        ["不能替你接受", "未接受", "不要替我接受"],
    ])


CHECKS = [("s13_no_uncompensated_noncompete", s13_no_uncompensated_noncompete, 3.5)]
