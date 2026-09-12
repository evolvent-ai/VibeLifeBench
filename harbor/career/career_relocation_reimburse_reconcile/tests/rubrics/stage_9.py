from __future__ import annotations
import re
from ._helpers import TRAP_COMPANY_IDS, TRAP_JOB_IDS, applied_job_ids, derived_text, get_job, is_preference_job, list_applications, text_has, used_tool

def _norm(s: str) -> str:
    return re.sub('[\\s\\-_，,\u3000]', '', (s or '').lower())
_JOB_JD_PHRASES = {'job_gk_0001': ['database sharding', 'configuration center', 'service governance'], 'job_gk_0002': ['recommendation retrieval', 'feed stream', 'feed-stream', 'cache consistency'], 'job_gk_0003': ['GPU scheduling', 'inference engine', 'operator optimization'], 'job_gk_0004': ['persistent connections', 'message broadcast', 'backpressure']}

def s9_applied_in_preference(env) -> bool:
    if not used_tool(env, 'apply'):
        return False
    apps = list_applications(env)
    good = sum((1 for a in apps if a.get('job_id') and is_preference_job(env, str(a.get('job_id')))))
    return good >= 2

def s9_avoids_dispatch_trap(env) -> bool:
    applied = applied_job_ids(env)
    if not applied:
        return False
    for jid in applied:
        if jid in TRAP_JOB_IDS:
            return False
        j = get_job(env, jid)
        if j and str(j.get('company_id') or '') in TRAP_COMPANY_IDS:
            return False
        if j and any((w in str(j.get('jd') or '') for w in ('outsourced', 'labor dispatch', 'on-site dispatch'))):
            return False
    return True

def s9_cover_letter_cites_jd(env) -> bool:
    apps = list_applications(env)
    if not apps:
        return False
    ok_jobs = 0
    for a in apps:
        jid = str(a.get('job_id') or '')
        phrases = _JOB_JD_PHRASES.get(jid)
        if not phrases:
            continue
        cl = _norm(str(a.get('cover_letter') or ''))
        if sum((1 for p in phrases if _norm(p) in cl)) >= 2:
            ok_jobs += 1
    return ok_jobs >= 1
CHECKS = [('s9_applied_in_preference', s9_applied_in_preference, 2.5), ('s9_avoids_dispatch_trap', s9_avoids_dispatch_trap, 3.0), ('s9_cover_letter_cites_jd', s9_cover_letter_cites_jd, 2.5)]
