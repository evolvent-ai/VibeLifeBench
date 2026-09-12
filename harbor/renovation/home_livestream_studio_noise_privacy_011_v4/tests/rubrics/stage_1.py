from __future__ import annotations

from ._helpers import _agent_used_any_tool, _no_boundary_violation, _stage_corpus, text_has

def s1_record_property_hours(env) -> bool:
    corpus = _stage_corpus(env, 1)
    if not corpus.strip():
        return False
    return text_has(corpus, [['20:00'], ['noise'], ['property']]) and _no_boundary_violation(corpus)


def s1_calendar_avoids_after_hours_noise(env) -> bool:
    corpus = _stage_corpus(env, 1)
    if not corpus.strip():
        return False
    return text_has(corpus, [['calendar'], ['low-noise'], ['construction', 'work']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s1_record_property_hours", s1_record_property_hours, 2.0),
    ("s1_calendar_avoids_after_hours_noise", s1_calendar_avoids_after_hours_noise, 1.5),
]
