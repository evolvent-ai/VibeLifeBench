"""Stage 9: read each real JD, tailor cover letters, and avoid dispatch traps."""
from __future__ import annotations

import re
from ._helpers import (TRAP_COMPANY_IDS, TRAP_JOB_IDS, applied_job_ids, get_job,
                       is_preference_job, list_applications, successful_stage_calls, used_tool)

_TECH_TERMS = (
    "java", "go", "spring cloud", "sharding", "transaction", "idempotency", "capacity", "load",
    "cache consistency", "message queue", "observability", "orders", "inventory", "marketing", "hot products", "e-commerce peak",
    "kubernetes", "gpu", "inference framework", "netty", "backpressure", "message ordering", "high concurrency", "redis", "kafka",
    "mysql", "rules engine", "workflow", "data governance", "API gateway", "oauth", "time-series data", "distributed systems",
)


def _norm(value: str) -> str:
    return re.sub(r"[\s\-_，,。；;（）()]", "", (value or "").lower())


def _job_terms(job: dict) -> set[str]:
    source = _norm(" ".join(str(job.get(k) or "") for k in ("tags", "jd", "requirements")))
    return {term for term in _TECH_TERMS if _norm(term) in source}


def _stage_job_ids(env, needle: str) -> set[str]:
    ids: set[str] = set()
    for call in successful_stage_calls(env, 9, needle):
        args = call.get("arguments") or {}
        result = call.get("result") or {}
        jid = args.get("job_id") or (result.get("job_id") if isinstance(result, dict) else None)
        if jid:
            ids.add(str(jid))
    return ids


def s9_applied_in_preference(env) -> bool:
    if not used_tool(env, "apply_job", stage=9):
        return False
    applied_stage = _stage_job_ids(env, "apply_job")
    apps = [a for a in list_applications(env) if str(a.get("job_id") or "") in applied_stage]
    return len({str(a.get("job_id")) for a in apps if a.get("job_id") and is_preference_job(env, str(a.get("job_id")))}) >= 2


def s9_avoids_dispatch_trap(env) -> bool:
    applied = applied_job_ids(env)
    if len(applied) < 2:
        return False
    for jid in applied:
        job = get_job(env, jid) or {}
        if jid in TRAP_JOB_IDS or str(job.get("company_id") or "") in TRAP_COMPANY_IDS:
            return False
        if any(word in str(job.get("jd") or "") for word in ("outsourcing", "dispatch", "on-site")):
            return False
    return True


def s9_cover_letter_cites_jd(env) -> bool:
    read_stage = _stage_job_ids(env, "get_job")
    applied_stage = _stage_job_ids(env, "apply_job")
    qualifying_letters: list[str] = []
    for app in list_applications(env):
        jid = str(app.get("job_id") or "")
        if jid not in read_stage or jid not in applied_stage:
            continue
        job = get_job(env, jid) or {}
        terms = _job_terms(job)
        cover = _norm(str(app.get("cover_letter") or ""))
        if sum(1 for term in terms if _norm(term) in cover) >= 2:
            qualifying_letters.append(cover)
    return len(qualifying_letters) >= 2 and len(set(qualifying_letters)) == len(qualifying_letters)


CHECKS = [
    ("s9_applied_in_preference", s9_applied_in_preference, 2.5),
    ("s9_avoids_dispatch_trap", s9_avoids_dispatch_trap, 3.0),
    ("s9_cover_letter_cites_jd", s9_cover_letter_cites_jd, 2.5),
]
