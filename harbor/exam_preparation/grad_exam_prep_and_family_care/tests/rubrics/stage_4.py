from __future__ import annotations
from ._helpers import *

def r10_mock1_score_recorded(env) -> bool:
    try:
        text = _agent_reply(env, 4) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _notion_text(env) + "\n" + _trace_text(env, 4, 4)
        return (
            _stage_trace_all(env, 4, [["api-", "notion", "database", "block"], ["update", "patch", "query", "post"]])
            and count_hits(text, [["mock 1", "mock1", "mock1"], ["120"], ["series"], ["multivariable function", "multivariable", "differentiation"]]) == 4
            and _stage_trace_all(env, 4, [["calendar", "event"], ["create_event", "update_event"]])
            and _calendar_event_count(env, [["series"], ["incorrect", "problems", "review", "review"]]) >= 1
            and _calendar_event_count(env, [["multivariable function", "multivariable", "differentiation"], ["incorrect", "problems", "review", "review"]]) >= 1
            and calendar_has_no_long_study_blocks(env)
        )
    except Exception:
        return False

CHECKS = [
    ("r10_mock1_score_recorded", r10_mock1_score_recorded, 2.0),
]
