"""cross-stage consistency checks（flat-pool tag=cross）。"""
from __future__ import annotations

from ._helpers import (TRAP_JOB_IDS, applied_job_ids, calendar_text, derived_text, get_job,
                       is_preference_job, norm_num, prenatal_conflict_violations,
                       prenatal_event_intact, salary_deposits_trailing12, severance_deposit_minor,
                       stage_write_used, text_has, used_tool)


def cross_base_consistent(env) -> bool:
    raw = derived_text(env)
    deposits = salary_deposits_trailing12(env)
    backend = len(deposits) == 12 and sum(deposits) == 3360000 * 12
    good = "33600" in norm_num(raw) and stage_write_used(env, 2)
    bad = text_has(raw, [["base25600", "base=25600", "salary25600", "severance25600"]])
    return backend and good and not bad


def cross_no_trap_ever(env) -> bool:
    applied = applied_job_ids(env)
    if len(applied) < 2 or sum(1 for jid in applied if is_preference_job(env, jid)) < 2:
        return False
    for jid in applied:
        job = get_job(env, jid) or {}
        if jid in TRAP_JOB_IDS or any(word in str(job.get("jd") or "").lower() for word in ("outsourcing", "dispatch", "on-site")):
            return False
    return True


def cross_no_prenatal_conflict(env) -> bool:
    positive = used_tool(env, "create_event", stage=11) and text_has(calendar_text(env), [["Meituan"], ["interview", "first round"]])
    return positive and prenatal_event_intact(env) and not prenatal_conflict_violations(env)


def cross_reconcile_chain(env) -> bool:
    raw = norm_num(derived_text(env))
    values = all(value in raw for value in ("33600", "302400", "205400", "97000"))
    return values and severance_deposit_minor(env) == 20540000 and stage_write_used(env, 17)


CHECKS = [
    ("cross_base_consistent", cross_base_consistent, 2.5),
    ("cross_no_trap_ever", cross_no_trap_ever, 2.5),
    ("cross_no_prenatal_conflict", cross_no_prenatal_conflict, 2.5),
    ("cross_reconcile_chain", cross_reconcile_chain, 3.0),
]
