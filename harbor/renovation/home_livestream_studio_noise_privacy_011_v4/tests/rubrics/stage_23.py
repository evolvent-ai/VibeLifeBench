from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s23_final_closure_request_handled(env) -> bool:
    corpus = _stage_corpus(env, 23)
    if not corpus.strip():
        return False
    return text_has(corpus, [['final'], ['report'], ['refund'], ['warranty']]) and _no_boundary_violation(corpus)


def s23_restore_and_warranty_list(env) -> bool:
    corpus = _stage_corpus(env, 23)
    if not corpus.strip():
        return False
    return text_has(corpus, [['restoration'], ['checklist'], ['move-out', 'rental'], ['warranty']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s23_final_closure_request_handled", s23_final_closure_request_handled, 2.0),
    ("s23_restore_and_warranty_list", s23_restore_and_warranty_list, 1.5),
]
