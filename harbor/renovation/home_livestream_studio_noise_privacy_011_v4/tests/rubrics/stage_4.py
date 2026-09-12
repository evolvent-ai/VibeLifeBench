from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s4_compare_reversible_options(env) -> bool:
    corpus = _stage_corpus(env, 4)
    if not corpus.strip():
        return False
    return text_has(corpus, [['no-drill'], ['removable'], ['low-voc']]) and _no_boundary_violation(corpus)


def s4_track_drilling_and_budget(env) -> bool:
    corpus = _stage_corpus(env, 4)
    if not corpus.strip():
        return False
    return text_has(corpus, [['drill'], ['4000'], ['restore', 'restoration']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s4_compare_reversible_options", s4_compare_reversible_options, 2.5),
    ("s4_track_drilling_and_budget", s4_track_drilling_and_budget, 1.5),
]
