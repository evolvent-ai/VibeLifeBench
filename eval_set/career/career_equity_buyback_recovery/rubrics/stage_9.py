"""Stage 9 — canonical 用户/简历投递合格岗并规避派遣陷阱。"""
from __future__ import annotations

import re

from ._helpers import (TRAP_COMPANY_IDS, TRAP_JOB_IDS, get_job, is_preference_job,
                       list_applications, stage_calls)

USER_ID = "usr_gao_kai"
RESUME_ID = "resume_gao_kai"
_JOB_JD_PHRASES = {
    "job_gk_0001": ["分库分表", "配置中心", "服务治理"],
    "job_gk_0002": ["推荐召回", "feed流", "缓存一致性"],
    "job_gk_0003": ["gpu调度", "推理引擎", "算子优化"],
    "job_gk_0004": ["长连接", "消息广播", "背压"],
}


def _norm(text: str) -> str:
    return re.sub(r"[\s\-_，,　]", "", (text or "").lower())


def _canonical_apps(env) -> list[dict]:
    return [
        app for app in list_applications(env)
        if str(app.get("user_id") or "") == USER_ID
        and str(app.get("resume_id") or "") == RESUME_ID
    ]


def _apply_call_for(env, job_id: str) -> bool:
    for call in stage_calls(env, 9, "apply"):
        args = call.get("arguments") or {}
        if (
            str(args.get("user_id") or "") == USER_ID
            and str(args.get("job_id") or "") == job_id
            and str(args.get("resume_id") or "") == RESUME_ID
        ):
            return True
    return False


def s9_applied_in_preference(env) -> bool:
    good = [app for app in _canonical_apps(env) if app.get("job_id") and is_preference_job(env, str(app["job_id"])) and _apply_call_for(env, str(app["job_id"]))]
    return len(good) >= 2


def s9_avoids_dispatch_trap(env) -> bool:
    apps = [app for app in list_applications(env) if str(app.get("user_id") or "") == USER_ID]
    if not apps or not any(is_preference_job(env, str(app.get("job_id") or "")) for app in apps):
        return False
    for app in apps:
        job_id = str(app.get("job_id") or "")
        job = get_job(env, job_id)
        if job_id in TRAP_JOB_IDS or (job and str(job.get("company_id") or "") in TRAP_COMPANY_IDS):
            return False
        if job and any(word in str(job.get("jd") or "") for word in ("外包", "派遣", "驻场")):
            return False
    return True


def s9_cover_letter_cites_jd(env) -> bool:
    for app in _canonical_apps(env):
        phrases = _JOB_JD_PHRASES.get(str(app.get("job_id") or ""))
        if not phrases:
            continue
        cover = _norm(str(app.get("cover_letter") or ""))
        if sum(1 for phrase in phrases if _norm(phrase) in cover) >= 2:
            return True
    return False


CHECKS = [
    ("s9_applied_in_preference", s9_applied_in_preference, 2.5),
    ("s9_avoids_dispatch_trap", s9_avoids_dispatch_trap, 2.5),
    ("s9_cover_letter_cites_jd", s9_cover_letter_cites_jd, 1.5),
]
