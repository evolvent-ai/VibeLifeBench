from __future__ import annotations
from ._helpers import *

def r24_progress_query(env) -> bool:
    try:
        text = _agent_reply(env, 13) + "\n" + _trace_text(env, 13, 13) + "\n" + wfile(env, "CONTROL_CENTER.md")
        return (
            _stage_trace_all(env, 13, [["api-post-database-query", "notion", "database", "database_rows", "properties_json"]])
            and count_hits(text + "\n" + _notion_text(env), [["row_completion", "completion", "completion_rate", "priority", "math_first"], ["50%", "0.4", "40%"], ["three", "days", "3days", "days"]]) == 3
            and _stage_reply_has(env, 13, [["below50%", "50%", "40%", "0.4"], ["three consecutive days", "three", "days", "3days"], ["Math", "main line", "math_first"]])
            and _notion_has(env, [["below50%", "50%", "40%", "0.4"], ["Math", "main line", "math_first"]])
        )
    except Exception:
        return False

def r25_prune_low_priority(env) -> bool:
    try:
        text = _agent_reply(env, 13) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _calendar_text(env) + "\n" + _notion_text(env) + "\n" + _trace_text(env, 13, 14)
        return (
            _stage_trace_all(env, 13, [["calendar", "event"], ["update_event", "delete_event", "create_event"]])
            and count_hits(text, [["Math", "main line", "preserve"], ["evening", "rest", "do not overfill", "buffer"]]) == 2
            and _calendar_event_count(env, [["Math", "main line", "incorrect", "problems", "mock"]]) >= 1
            and _calendar_event_count(env, [["rest", "do not overfill", "buffer", "break"]]) >= 1
        )
    except Exception:
        return False

CHECKS = [
    ("r24_progress_query", r24_progress_query, 3.0),
    ("r25_prune_low_priority", r25_prune_low_priority, 3.0),
]
