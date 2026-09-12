"""Stage 15 — dynamically bindMeituanrolecorrespondingreal application ID with JD preparation."""
from __future__ import annotations

from ._helpers import get_job, record_text, stage_call_matches, unique_application_for_job

JOB_ID = "job_gk_0001"
PHRASES = ("database sharding", "configuration center", "service governance", "consistency transaction", "end-to-end load testing")


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
