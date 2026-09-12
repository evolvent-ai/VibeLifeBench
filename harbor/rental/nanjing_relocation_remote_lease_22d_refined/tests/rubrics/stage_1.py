"""Stage 1 — capture requirements: budget / commute anchor / whole-unit."""
from __future__ import annotations
from ._helpers import file_has, has_any, stage_corpus

def s1_capture_requirements(env) -> bool:
    corpus = stage_corpus(env, 1)
    if not corpus.strip():
        return False
    budget = has_any(corpus, ['4200', '420000', 'budget'])
    commute = has_any(corpus, ['commute', 'Software Avenue', '40 minutes', 'metro'])
    whole = has_any(corpus, ['entire-unit rental', 'one-bedroom', 'two-bedroom', 'one-bedroom', 'two-bedroom', 'one- or two-bedroom'])
    durable = file_has(env, 'candidates.md', ['4200', 'commute', 'entire-unit rental'], minimum=2) or file_has(env, 'audit_journal.md', ['4200', 'Software Avenue', 'entire-unit rental'], minimum=2)
    return budget and commute and whole and durable
CHECKS = [('s1_capture_requirements', s1_capture_requirements, 1.4910394265232976)]
