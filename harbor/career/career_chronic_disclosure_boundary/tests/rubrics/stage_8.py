"""Stage 8: recommend traceable reemployment positions in the target scope."""
from __future__ import annotations

from ._helpers import (derived_text, get_job, is_preference_job, search_jobs,
                       stage_write_used, successful_stage_calls, text_has, used_tool)


def s8_search_done(env) -> bool:
    if not used_tool(env, "search_jobs", stage=8):
        return False
    result_ids: set[str] = set()
    for call in successful_stage_calls(env, 8, "search_jobs"):
        result = call.get("result")
        if isinstance(result, dict):
            rows = result.get("items") or result.get("jobs") or result.get("results") or []
        else:
            rows = result
        for row in rows or []:
            if isinstance(row, dict) and row.get("job_id"):
                result_ids.add(str(row["job_id"]))
    backend_rows = search_jobs(env)
    backend_ids = {
        str(row.get("job_id") or row.get("id") or "")
        for row in backend_rows
        if isinstance(row, dict) and (row.get("job_id") or row.get("id"))
    }
    if not backend_ids:
        return False
    result_ids &= backend_ids
    valid = []
    for jid in result_ids:
        job = get_job(env, jid) or {}
        if job.get("job_id") and str(job.get("status") or "").lower() == "open" and is_preference_job(env, jid):
            valid.append(jid)
    corpus = derived_text(env)
    object_bound = sum(1 for jid in valid if jid.lower() in corpus.lower()) >= 3
    reasons = text_has(corpus, [["fit", "match", "recommendation", "experience", "technical", "direction"], ["employed", "directly-employed", "employment"]])
    return len(valid) >= 3 and object_bound and reasons and stage_write_used(env, 8)


CHECKS = [("s8_search_done", s8_search_done, 2.5)]
