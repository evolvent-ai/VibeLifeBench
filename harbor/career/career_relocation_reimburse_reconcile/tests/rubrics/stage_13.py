from __future__ import annotations
from ._helpers import NONCOMPETE_JOB_ID, applications_by_status, derived_text, stage_or_corpus, text_has

def s13_no_uncompensated_noncompete(env) -> bool:
    by_status = applications_by_status(env)
    for a in by_status.get('offer', []) + by_status.get('accepted', []):
        if str(a.get('job_id')) == NONCOMPETE_JOB_ID:
            return False
    text = stage_or_corpus(env, 13)
    if not text.strip():
        return False
    noncompete = text_has(text, [['non-compete']])
    no_comp = text_has(text, [['without compensation', 'no compensation', 'compensation not stipulated', 'no non-compete compensation', 'compensation unpaid', 'missing compensation', 'no compensation provision', 'compensation was not paid', 'without consideration']])
    return noncompete and no_comp
CHECKS = [('s13_no_uncompensated_noncompete', s13_no_uncompensated_noncompete, 5.0)]
