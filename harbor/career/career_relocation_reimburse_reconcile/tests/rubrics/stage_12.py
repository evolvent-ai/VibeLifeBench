from __future__ import annotations
from ._helpers import applications_by_status, derived_text, text_has, used_tool

def s12_status_synced(env) -> bool:
    if not used_tool(env, 'list_applications', stage=12):
        if not used_tool(env, 'list_applications'):
            return False
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    return text_has(corpus, [['viewed', 'viewed-alternative-21', 'reviewed', 'interview-alternative-22', 'progress', 'advanced', 'scheduled', 'rejection', 'rejection-alternative-23', 'statuses']])
CHECKS = [('s12_status_synced', s12_status_synced, 2.5)]
