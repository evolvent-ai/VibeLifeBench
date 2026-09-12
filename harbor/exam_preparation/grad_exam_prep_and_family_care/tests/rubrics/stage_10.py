from __future__ import annotations
from ._helpers import *

def r19_confirm_makeup_plan(env) -> bool:
    try:
        text = _agent_reply(env, 10) + "\n" + _calendar_text(env) + "\n" + wfile(env, "CONTROL_CENTER.md")
        return (
            _stage_reply_has(env, 10, [["makeup", "practice", "incorrect", "problems"], ["Sunday", "12-06"], ["4 hours", "two", "sessions", "split"]])
            and _calendar_has(env, [["incorrect", "problems", "makeup", "remediation"], ["rest", "split", "two", "sessions", "4 hours"]])
            and any_has(text, ["confirm", "as requested", "adjusted"])
        )
    except Exception:
        return False

CHECKS = [
    ("r19_confirm_makeup_plan", r19_confirm_makeup_plan, 1.0),
]
