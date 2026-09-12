"""Stage 19: second-instance deadlines and scope."""
from __future__ import annotations
from ._helpers import _assistant_calendar_text, _food_journal_text

def s19_appeal_deadlines_calendar(env) -> bool:
    text = _assistant_calendar_text(env)
    return text is not None and any(k in text for k in ("second instance", "appellee", "appeal")) and any(k in text for k in ("defense", "respond to the case", "evidence submission")) and any(k in text for k in ("deadline", "cutoff", "15 days", "2026-07"))

def s19_second_instance_diff(env) -> bool:
    text = _food_journal_text(env)
    return text is not None and any(k in text for k in ("within the appeal claims", "scope of appeal claims", "scope of second-instance review")) and any(k in text for k in ("testing report", "evidence index", "supplementary evidence", "first-instance evidence")) and any(k in text for k in ("litigation fee", "fees", "prepay"))
CHECKS = [("s19_assistant_appeal_deadlines_calendar", s19_appeal_deadlines_calendar, 0.5), ("s19_persisted_second_instance_plan", s19_second_instance_diff, 0.5)]

