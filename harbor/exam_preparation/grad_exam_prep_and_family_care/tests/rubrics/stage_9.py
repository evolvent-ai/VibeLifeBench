from __future__ import annotations
from ._helpers import *

def r17_mock2_score(env) -> bool:
    try:
        text = _agent_reply(env, 9) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _notion_text(env) + "\n" + _trace_text(env, 9, 9)
        return (
            _stage_trace_all(env, 9, [["api-post-database-query", "notion", "database", "database_rows", "properties_json"]])
            and count_hits(text, [["mock 2", "mock2", "mock2", "second", "mock"], ["105"], ["drop", "decline", "remediation", "risk"]]) == 3
            and _notion_has(env, [["mock 2", "mock2", "score", "needs_recovery"], ["105"], ["series", "multivariable function", "incorrect", "problems"], ["remediation", "makeup practice", "risk"]])
        )
    except Exception:
        return False

def r18_add_makeup_study(env) -> bool:
    try:
        text = _agent_reply(env, 9) + "\n" + wfile(env, "CONTROL_CENTER.md") + "\n" + _calendar_text(env) + "\n" + _trace_text(env, 9, 10)
        return (
            _stage_trace_all(env, 9, [["calendar", "event"], ["create_event", "update_event"]])
            and any_has(text, ["incorrect", "problems", "redo", "makeup practice", "remediation"])
            and _calendar_has(env, [["incorrect", "problems", "redo", "makeup practice", "remediation"], ["rest", "split", "4 hours", "4 hours"]])
            and _calendar_event_count(env, [["series"], ["incorrect", "problems", "redo", "makeup practice"]]) >= 1
            and _calendar_event_count(env, [["multivariable function", "multivariable", "differentiation"], ["incorrect", "problems", "redo", "makeup practice"]]) >= 1
            and _stage_reply_has(env, 9, [["105"], ["series", "multivariable function"], ["Sunday", "12-06", "12-06"], ["no more than4 hours", "4 hours", "split"]])
            and calendar_has_no_long_study_blocks(env)
        )
    except Exception:
        return False

CHECKS = [
    ("r17_mock2_score", r17_mock2_score, 3.0),
    ("r18_add_makeup_study", r18_add_makeup_study, 4.0),
]
