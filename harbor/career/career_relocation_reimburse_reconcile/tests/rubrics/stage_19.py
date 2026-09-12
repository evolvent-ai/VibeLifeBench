from __future__ import annotations
from ._helpers import derived_text, text_has

def s19_maintains_state(env) -> bool:
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    # Seed guidance mentions both workstreams. Require a weekly maintenance
    # record so the inherited template cannot satisfy this stage by itself.
    maintained = text_has(corpus, [['weekly state', 'weekly update', 'state maintenance', 'remain current']])
    compensation = text_has(corpus, [['compensation', 'shortfall-alternative-59', 'arbitration-alternative-60', 'negotiated-alternative-61']])
    reemployment = text_has(corpus, [['offer', 'interview-alternative-63', 'application-alternative-64', 'reemployment-alternative-65']])
    return maintained and compensation and reemployment
CHECKS = [('s19_maintains_state', s19_maintains_state, 1.5)]
