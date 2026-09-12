from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s0_create_project_board(env) -> bool:
    corpus = _stage_corpus(env, 0)
    if not corpus.strip():
        return False
    return text_has(corpus, [['budget'], ['18000'], ['authorization']]) and _no_boundary_violation(corpus)


def s0_initial_tool_triage(env) -> bool:
    corpus = _stage_corpus(env, 0)
    if not corpus.strip():
        return False
    return text_has(corpus, [['email'], ['calendar'], ['notion']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s0_create_project_board", s0_create_project_board, 2.0),
    ("s0_initial_tool_triage", s0_initial_tool_triage, 1.5),
]
