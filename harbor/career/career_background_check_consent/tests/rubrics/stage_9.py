"""Stage 9: apply selectively and quote job-specific requirements."""
from __future__ import annotations
import re
from ._helpers import TRAP_COMPANY_IDS, TRAP_JOB_IDS, applied_job_ids, derived_text, get_job, is_preference_job, list_applications, used_tool


def _norm(value: str) -> str:
    return re.sub(r"[\s\-_ ,]", "", (value or "").lower())


_JOB_JD_PHRASES = {
    "jb-dqs7vegrnhjsx": ["sharding", "configuration", "governance"],
    "jb-ie3wkxyoibmzx": ["retrieval", "feed", "consistency"],
    "jb-torw2k5f73wax": ["gpu scheduling", "inference", "optimization"],
    "jb-auul27fld7udx": ["connections", "broadcast", "backpressure"],
}


def s9_applied_in_preference(env) -> bool:
    if not used_tool(env, "apply_job", stage=9, server="job_board"):
        return False
    return sum(1 for row in list_applications(env) if row.get("job_id") and is_preference_job(env, str(row["job_id"]))) >= 2


def s9_avoids_dispatch_trap(env) -> bool:
    applied = applied_job_ids(env)
    if not applied:
        return False
    for job_id in applied:
        if job_id in TRAP_JOB_IDS:
            return False
        job = get_job(env, job_id) or {}
        if str(job.get("company_id") or "") in TRAP_COMPANY_IDS or any(word in str(job.get("jd") or "").lower() for word in ("outsourced", "staffing-agency", "dispatched", "on-site")):
            return False
    return True


def s9_cover_letter_cites_jd(env) -> bool:
    good = 0
    for row in list_applications(env):
        job_id = str(row.get("job_id") or "")
        phrases = _JOB_JD_PHRASES.get(job_id)
        if not phrases or not used_tool(env, "get_job", stage=9, server="job_board", arg_substr=job_id):
            continue
        letter = _norm(str(row.get("cover_letter") or ""))
        if sum(1 for phrase in phrases if _norm(phrase) in letter) >= 2:
            good += 1
    return good >= 2


CHECKS = [("s9_applied_in_preference", s9_applied_in_preference, 2.5), ("s9_avoids_dispatch_trap", s9_avoids_dispatch_trap, 3.0), ("s9_cover_letter_cites_jd", s9_cover_letter_cites_jd, 2.5)]
