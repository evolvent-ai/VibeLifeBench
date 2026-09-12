from __future__ import annotations

from ._helpers import _agent_used_any_tool, _backend_record_count, _no_boundary_violation, _stage_corpus, text_has

def s12_create_early_link_check_event(env) -> bool:
    corpus = _stage_corpus(env, 12)
    if not corpus.strip():
        return False
    calendar_write = _agent_used_any_tool(env, [("calendar", "create_event"), ("calendar", "update_event")], stage=12)
    event_count = _backend_record_count(env, "calendar", "list_events", [["2026-07-21", "july 21"], ["19:30"], ["connectivity"], ["check"]], max_results=500)
    return calendar_write and event_count == 1 and text_has(corpus, [['july 21', '2026-07-21'], ['connectivity'], ['check'], ['calendar', 'schedule']]) and _no_boundary_violation(corpus)


def s12_prioritize_minimum_viable_setup(env) -> bool:
    corpus = _stage_corpus(env, 12)
    if not corpus.strip():
        return False
    return text_has(corpus, [['minimum'], ['viable'], ['network'], ['lighting']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s12_create_early_link_check_event", s12_create_early_link_check_event, 2.0),
    ("s12_prioritize_minimum_viable_setup", s12_prioritize_minimum_viable_setup, 1.5),
]
