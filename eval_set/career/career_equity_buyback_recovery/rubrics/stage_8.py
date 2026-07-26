"""Stage 8 — 按上海后端/平台范围搜索并记录真实候选对象。"""
from __future__ import annotations

import re

from ._helpers import get_job, record_text, stage_calls


def _search_scope_ok(env) -> bool:
    for call in stage_calls(env, 8, "search_jobs") + stage_calls(env, 8, "recommend_jobs"):
        args = call.get("arguments") or {}
        city = str(args.get("city") or args.get("location") or "")
        category = str(args.get("category") or args.get("query") or args.get("keyword") or "").lower()
        if city == "上海" and any(word in category for word in ("backend", "后端", "平台")):
            return True
    return False


def s8_search_done(env) -> bool:
    if not _search_scope_ok(env):
        return False
    record = record_text(env, "job_tracker.md")
    job_ids = sorted(set(re.findall(r"job_gk_\d{4}", record)))
    eligible = []
    for job_id in job_ids:
        job = get_job(env, job_id)
        if not job:
            continue
        city = str(job.get("city") or "")
        category = (str(job.get("category") or "") + str(job.get("title") or "")).lower()
        if city == "上海" and any(word in category for word in ("backend", "后端", "平台")):
            eligible.append(job_id)
    return len(set(eligible)) >= 3 and "来源" in record and "下一步" in record


CHECKS = [("s8_search_done", s8_search_done, 1.5)]
