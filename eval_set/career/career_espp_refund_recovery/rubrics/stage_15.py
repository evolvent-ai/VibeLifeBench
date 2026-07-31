"""Stage 15 — 动态绑定美团岗位对应的真实 application ID 与 JD 准备。"""
from __future__ import annotations

from ._helpers import get_job, record_text, stage_call_matches, unique_application_for_job

JOB_ID = "job_gk_0001"
PHRASES = ("分库分表", "配置中心", "服务治理", "一致性事务", "全链路压测")


def s15_prep_from_jd(env) -> bool:
    if not stage_call_matches(env, 15, "get_job", {"job_id": JOB_ID}) or not get_job(env, JOB_ID):
        return False
    app = unique_application_for_job(env, JOB_ID, {"interview", "offer"})
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "interview_prep.md")
    if JOB_ID not in record or app_id not in record:
        return False
    return sum(1 for phrase in PHRASES if phrase.lower() in record) >= 3


CHECKS = [("s15_prep_from_jd", s15_prep_from_jd, 1.5)]
