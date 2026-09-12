from __future__ import annotations
from ._helpers import *

def r28_exam_seat_update(env) -> bool:
    try:
        text = _agent_reply(env, 16) + "\n" + _trace_text(env, 16, 16) + "\n" + wfile(env, "CONTROL_CENTER.md")
        return (
            _stage_trace_all(env, 16, [["email", "mail"], ["read_email", "search_emails", "get_emails"]])
            and any_has(text, ["A2-031", "Pudong Graduate Admissions", "room", "seat"])
            and any_has(text, ["admission", "ticket", "identity", "card", "2B", "45"])
            and _workspace_file_has(env, "CONTROL_CENTER.md", [["room", "seat"], ["admission", "ticket", "identity", "card", "2B"]])
            and _notion_has(env, [["A2-031", "Pudong Graduate Admissions"], ["admission", "ticket", "identity", "card", "2B"], ["45", "early"]])
        )
    except Exception:
        return False

CHECKS = [
    ("r28_exam_seat_update", r28_exam_seat_update, 2.0),
]
