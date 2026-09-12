from __future__ import annotations
from ._helpers import derived_text, norm_num, text_has, used_tool

def s1_notice_logged(env) -> bool:
    read_ok = used_tool(env, 'read_email') or used_tool(env, 'get_email')
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    basis = text_has(corpus, [['Article', 'termination', 'art40', 'Unlawful', 'restructuring', 'adjustment', 'role restructuring']])
    last_day = '2026-06-30' in corpus or '6-30' in corpus or 'June 30' in corpus or ('30 June' in corpus) or ('0630' in norm_num(corpus))
    return read_ok and basis and last_day
CHECKS = [('s1_notice_logged', s1_notice_logged, 3.5)]
