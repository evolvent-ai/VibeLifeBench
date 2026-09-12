"""Stage 8: search and persist suitable Shanghai roles."""
from __future__ import annotations
import re
from ._helpers import derived_text, get_job, search_jobs, used_tool

_JOB_ID_RE = re.compile(r"\bjb-[a-z2-7]{13}\b")


def s8_search_done(env) -> bool:
    if not used_tool(env, "search_jobs", stage=8, server="job_board"):
        return False
    searched = {str(row.get("job_id") or "") for row in search_jobs(env, city="Shanghai", category="backend", experience="5-10", limit=100, sort="newest")}
    ids = sorted(set(_JOB_ID_RE.findall(derived_text(env))))
    good = 0
    for job_id in ids:
        if job_id not in searched:
            continue
        job = get_job(env, job_id) or {}
        category = (str(job.get("category") or "") + " " + str(job.get("title") or "")).lower()
        if str(job.get("city") or "").lower() == "shanghai" and str(job.get("status") or "open").lower() == "open" and any(term in category for term in ("backend", "platform")):
            good += 1
    return good >= 3


CHECKS = [("s8_search_done", s8_search_done, 2.5)]
