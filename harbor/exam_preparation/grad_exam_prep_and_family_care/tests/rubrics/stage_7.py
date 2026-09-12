from __future__ import annotations
from ._helpers import *

def r16_reschedule_reply(env) -> bool:
    try:
        text = _agent_reply(env, 7) + "\n" + _calendar_text(env)
        return (
            _stage_reply_has(env, 7, [["11-29", "11 month29", "29day"], ["follow-up", "Calendar"], ["4 hours", "4 hours", "rest", "continuous", "study"]])
            and _calendar_has(env, [["2026-11-29", "11-29"], ["follow-up", "Ms. Li", "knee"]])
            and any_has(text, ["recorded", "updated", "rescheduled", "confirm"])
        )
    except Exception:
        return False

CHECKS = [
    ("r16_reschedule_reply", r16_reschedule_reply, 1.0),
]
