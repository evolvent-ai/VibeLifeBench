"""Stage 13: identify the uncompensated noncompete risk."""
from __future__ import annotations
from ._helpers import NONCOMPETE_JOB_ID, get_job, has_offer_binding_statement, sent_to_recruiter_text, stage_or_corpus, successful_tool_trace_text, text_has, used_tool


def s13_no_uncompensated_noncompete(env) -> bool:
    if has_offer_binding_statement(sent_to_recruiter_text(env, ["dewu", "Dewu"])):
        return False
    job = get_job(env, NONCOMPETE_JOB_ID) or {}
    jd = str(job.get("jd") or "")
    backend_risk = text_has(jd, [["noncompete"], ["two years", "2 years"], ["uncompensated", "uncompensated", "no compensation"]])
    read_full = used_tool(env, "get_job", stage=13, server="job_board", arg_substr=NONCOMPETE_JOB_ID)
    trace = successful_tool_trace_text(env, stage=13, name_contains="get_job")
    trace_bound = NONCOMPETE_JOB_ID in trace and text_has(trace, [["noncompete"], ["uncompensated", "uncompensated", "no compensation"]])
    if not (backend_risk and read_full and trace_bound):
        return False
    text = stage_or_corpus(env, 13)
    return bool(text.strip()) and text_has(text, [["noncompete"], ["uncompensated", "no compensation", "noncompete", "missing compensation", "no consideration"]])


CHECKS = [("s13_no_uncompensated_noncompete", s13_no_uncompensated_noncompete, 5.0)]
