from __future__ import annotations
from ._helpers import derived_text, text_has, used_tool

def s15_prep_from_jd(env) -> bool:
    read_job = used_tool(env, 'get_job')
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    phrases = ['database sharding', 'configuration center', 'service governance', 'end-to-end', 'consistent transactions', 'high concurrency']
    hits = sum((1 for p in phrases if p in corpus))
    return read_job and hits >= 2
CHECKS = [('s15_prep_from_jd', s15_prep_from_jd, 2.5)]
