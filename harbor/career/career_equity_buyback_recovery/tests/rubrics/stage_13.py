"""Stage 13 — treat Dewunon-binding indicative termswithno compensationnon-competerisk correctly."""
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
        ["non-binding"], ["indicative"], ["interview pending", "interview approval pending"],
        ["not a formal offer"],
        ["two-year"], ["no compensation specified", "no compensation"],
        ["cannot accept for you", "not accepted", "do not accept for me"],
    ])


CHECKS = [("s13_no_uncompensated_noncompete", s13_no_uncompensated_noncompete, 3.5)]
