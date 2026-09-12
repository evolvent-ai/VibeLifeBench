from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s5_refresh_vendor_reviews(env) -> bool:
    corpus = _stage_corpus(env, 5)
    if not corpus.strip():
        return False
    return text_has(corpus, [['negative review', 'review'], ['baisound'], ['noise'], ['reduction']]) and _no_boundary_violation(corpus)


def s5_downgrade_unverified_acoustic_vendor(env) -> bool:
    corpus = _stage_corpus(env, 5)
    if not corpus.strip():
        return False
    return text_has(corpus, [['measured'], ['exaggerated', 'overclaim'], ['alternative', 'candidate']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s5_refresh_vendor_reviews", s5_refresh_vendor_reviews, 2.0),
    ("s5_downgrade_unverified_acoustic_vendor", s5_downgrade_unverified_acoustic_vendor, 1.5),
]
