from __future__ import annotations
from ._helpers import derived_text, text_has

def s7_quiet_monitor(env) -> bool:
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    # A seed plan alone is not evidence that monitoring was performed.  Require
    # both a reemployment/role subject and an explicit monitoring action.
    return text_has(corpus, [['role', 'application', 'job-search', 'reemployment'], ['monitoring', 'tracking']])
CHECKS = [('s7_quiet_monitor', s7_quiet_monitor, 1.5)]
