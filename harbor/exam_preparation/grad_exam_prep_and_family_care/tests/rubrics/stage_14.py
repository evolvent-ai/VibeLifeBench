from __future__ import annotations
from ._helpers import *

def r26_prune_confirmation_reply(env) -> bool:
    try:
        text = _agent_reply(env, 14) + "\n" + _calendar_text(env) + "\n" + wfile(env, "CONTROL_CENTER.md")
        return (
            _stage_trace_all(env, 14, [["calendar", "event"], ["update_event", "delete_event", "create_event"]])
            and _stage_reply_has(env, 14, [["English", "politics", "low priority", "compress"], ["Math", "main line"], ["evening", "do not overfill", "rest"]])
            and _calendar_has(env, [["Math", "incorrect", "problems", "mock"], ["rest", "buffer", "do not overfill"]])
            and _notion_has(env, [["English", "politics", "compress"], ["Math", "main line"], ["evening", "do not overfill", "rest"]])
            and any_has(text, ["confirm", "execute this way", "updated"])
        )
    except Exception:
        return False

CHECKS = [
    ("r26_prune_confirmation_reply", r26_prune_confirmation_reply, 1.0),
]
