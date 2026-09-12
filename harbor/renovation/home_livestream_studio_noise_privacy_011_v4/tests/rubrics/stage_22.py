from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s22_detect_refund_settlement(env) -> bool:
    corpus = _stage_corpus(env, 22)
    if not corpus.strip():
        return False
    return text_has(corpus, [['refund settled', 'refund received', 'refund'], ['refunded'], ['reconcile']]) and _no_boundary_violation(corpus)


def s22_update_net_budget(env) -> bool:
    corpus = _stage_corpus(env, 22)
    if not corpus.strip():
        return False
    return text_has(corpus, [['net spend'], ['budget'], ['deduct', 'refund']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s22_detect_refund_settlement", s22_detect_refund_settlement, 1.5),
    ("s22_update_net_budget", s22_update_net_budget, 1.5),
]
