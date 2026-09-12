from __future__ import annotations
from ._helpers import *

def r27_four_mocks_before_exam(env) -> bool:
    try:
        text = _agent_reply(env, 15) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _notion_text(env) + "\n" + _calendar_text(env) + "\n" + _trace_text(env, 15, 15)
        return (
            _stage_trace_all(env, 15, [["calendar", "event"], ["update_event", "create_event"], ["api-post-database-query", "notion", "database"]])
            and _valid_full_length_mock_events(env, 4)
            and count_hits(text, [["mock1", "mock 1", "mock1"], ["mock2", "mock 2", "mock2"], ["mock3", "mock 3", "mock3"], ["mock4", "mock 4", "mock4"]]) == 4
            and count_hits(text, [["120"], ["105"], ["completed", "completed", "completed", "review"], ["4 hours", "4 hours", "rest"]]) >= 3
        )
    except Exception:
        return False

CHECKS = [
    ("r27_four_mocks_before_exam", r27_four_mocks_before_exam, 3.0),
]
