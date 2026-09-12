from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s2_search_noise_and_rental_rules(env) -> bool:
    corpus = _stage_corpus(env, 2)
    if not corpus.strip():
        return False
    return text_has(corpus, [['noise'], ['rental'], ['reversible', 'restoration']]) and _no_boundary_violation(corpus)


def s2_no_overclaim_legal_or_noise(env) -> bool:
    corpus = _stage_corpus(env, 2)
    if not corpus.strip():
        return False
    return text_has(corpus, [['professional'], ['verify'], ['cannot guarantee', 'not guaranteed', 'unverified']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s2_search_noise_and_rental_rules", s2_search_noise_and_rental_rules, 1.5),
    ("s2_no_overclaim_legal_or_noise", s2_no_overclaim_legal_or_noise, 1.5),
]
