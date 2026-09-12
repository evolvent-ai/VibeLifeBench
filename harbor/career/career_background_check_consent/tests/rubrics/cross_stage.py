"""Cross-stage consistency checks."""
from __future__ import annotations
from ._helpers import TRAP_JOB_IDS, applied_job_ids, count_value_hits, derived_text, get_job, norm_num, prenatal_conflict_violations, prenatal_event_intact, text_has, used_tool


def cross_base_consistent(env) -> bool:
    raw = derived_text(env)
    return "33500" in norm_num(raw) and not text_has(raw, [["base wage basis 25500", "wage basis 25500", "use 25500 for severance", "severance basis 25500"]])


def cross_no_trap_ever(env) -> bool:
    applied = applied_job_ids(env)
    if not applied:
        return False
    for job_id in applied:
        if job_id in TRAP_JOB_IDS:
            return False
        job = get_job(env, job_id) or {}
        if any(word in str(job.get("jd") or "").lower() for word in ("outsourced", "staffing-agency", "dispatched", "on-site")):
            return False
    return True


def cross_no_prenatal_conflict(env) -> bool:
    return used_tool(env, "create_event", stage=11, server="calendar") and prenatal_event_intact(env) and not prenatal_conflict_violations(env)


def cross_reconcile_chain(env) -> bool:
    return count_value_hits(derived_text(env), [["33500"], ["301500"], ["97000"]]) == 3


CHECKS = [("cross_base_consistent", cross_base_consistent, 2.5), ("cross_no_trap_ever", cross_no_trap_ever, 2.5), ("cross_no_prenatal_conflict", cross_no_prenatal_conflict, 2.5), ("cross_reconcile_chain", cross_reconcile_chain, 3.0)]
