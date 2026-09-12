from __future__ import annotations

from ._helpers import _agent_used_any_tool, _backend_record_count, _no_boundary_violation, _stage_corpus, text_has

def s18_schedule_silent_light_test(env) -> bool:
    corpus = _stage_corpus(env, 18)
    if not corpus.strip():
        return False
    calendar_write = _agent_used_any_tool(env, [("calendar", "create_event"), ("calendar", "update_event")], stage=18)
    event_count = _backend_record_count(env, "calendar", "list_events", [["quiet", "silent"], ["test", "debug"], ["lighting"]], max_results=500)
    return calendar_write and event_count == 1 and text_has(corpus, [['quiet', 'silent'], ['test', 'debug'], ['lighting']]) and _no_boundary_violation(corpus)


def s18_update_link_check_checklist(env) -> bool:
    corpus = _stage_corpus(env, 18)
    if not corpus.strip():
        return False
    return text_has(corpus, [['network'], ['backdrop', 'background'], ['checklist']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s18_schedule_silent_light_test", s18_schedule_silent_light_test, 1.5),
    ("s18_update_link_check_checklist", s18_update_link_check_checklist, 1.5),
]
