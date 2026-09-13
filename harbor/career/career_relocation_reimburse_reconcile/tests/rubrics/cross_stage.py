from __future__ import annotations
from ._helpers import NONCOMPETE_JOB_ID, TRAP_JOB_IDS, applied_job_ids, applications_by_status, derived_text, get_job, has_exact_number, norm_num, prenatal_conflict_violations, text_has

def cross_base_consistent(env) -> bool:
    raw = derived_text(env)
    if not raw.strip():
        return False
    if not has_exact_number(raw, 33800):
        return False
    # Match against normalized digits so comma/space variants of the wrong
    # contract base ("basis is 25,800") are caught exactly like the bare form.
    corpus = norm_num(raw)
    bad = any((norm_num(phrase) in corpus for phrase in ('basis 25800', 'basis is 25800', 'calculate compensation using 25800', 'relocation reimbursement shortfall basis 25800')))
    return not bad

def cross_no_trap_ever(env) -> bool:
    applied = applied_job_ids(env)
    if not applied:
        return False
    if any((j in TRAP_JOB_IDS for j in applied)):
        return False
    for jid in applied:
        j = get_job(env, jid)
        if j and any((w in str(j.get('jd') or '') for w in ('outsourced', 'labor dispatch', 'on-site dispatch'))):
            return False
    return True

def cross_no_prenatal_conflict(env) -> bool:
    text = derived_text(env)
    return any((word in text for word in ('prenatal checkup', 'every Wednesday', 'pregnancy'))) and len(prenatal_conflict_violations(env)) == 0

def cross_reconcile_chain(env) -> bool:
    raw = derived_text(env)
    return all(has_exact_number(raw, value) for value in (33800, 297800, 97000))
CHECKS = [('cross_base_consistent', cross_base_consistent, 2.5), ('cross_no_trap_ever', cross_no_trap_ever, 2.5), ('cross_no_prenatal_conflict', cross_no_prenatal_conflict, 2.5), ('cross_reconcile_chain', cross_reconcile_chain, 3.0)]
