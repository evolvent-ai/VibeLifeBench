"""Stage 15: reread the Meituan JD and create a position-specific checklist."""
from __future__ import annotations

from ._helpers import derived_text, get_job, stage_write_used, text_has, trace_result_text, used_tool

_MEITUAN_JOB_ID = "jb-4vxnibjsgwrdx"
_TERMS = ("sharding", "idempotency compensation", "capacity governance", "end-to-end load testing", "distributed transactions", "hot traffic", "incident review", "java", "spring cloud")


def s15_prep_from_jd(env) -> bool:
    if not used_tool(env, "get_job", stage=15, arg_substr=_MEITUAN_JOB_ID):
        return False
    job = get_job(env, _MEITUAN_JOB_ID) or {}
    source = " ".join(str(job.get(k) or "").lower() for k in ("jd", "requirements", "tags"))
    backend_terms = {term for term in _TERMS if term in source}
    trace = trace_result_text(env, 15, "get_job")
    if _MEITUAN_JOB_ID not in trace or len(backend_terms) < 3:
        return False
    corpus = derived_text(env)
    hits = sum(1 for term in backend_terms if term in corpus)
    prep_shape = text_has(corpus, [["preparation", "checklist", "review"], ["case", "review", "plan"]])
    return stage_write_used(env, 15) and hits >= 3 and prep_shape


CHECKS = [("s15_prep_from_jd", s15_prep_from_jd, 2.5)]
