from __future__ import annotations

from ._helpers import _agent_used_any_tool, _backend_record_count, _no_boundary_violation, _stage_corpus, text_has

def s10_detect_split_shipment(env) -> bool:
    corpus = _stage_corpus(env, 10)
    if not corpus.strip():
        return False
    return text_has(corpus, [['split'], ['delay'], ['key light']]) and _no_boundary_violation(corpus)


def s10_replan_installation_calendar(env) -> bool:
    corpus = _stage_corpus(env, 10)
    if not corpus.strip():
        return False
    calendar_write = _agent_used_any_tool(env, [("calendar", "create_event"), ("calendar", "update_event")], stage=10)
    event_count = _backend_record_count(env, "calendar", "list_events", [["2026-07-21", "july 21"], ["minimum"], ["viable"]], max_results=500)
    return calendar_write and event_count == 1 and text_has(corpus, [['reschedule', 'replan'], ['july 21', '2026-07-21'], ['minimum'], ['viable']]) and _no_boundary_violation(corpus)


CHECKS = [
    ("s10_detect_split_shipment", s10_detect_split_shipment, 2.0),
    ("s10_replan_installation_calendar", s10_replan_installation_calendar, 1.5),
]
