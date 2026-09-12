"""Stage 20: archive and remaining deadlines."""
from __future__ import annotations
from ._helpers import _assistant_calendar_text, _food_journal_text

def s20_archive_notion(env) -> bool:
    text = _food_journal_text(env)
    return bool(text) and any(k in text for k in ("archive", "case index", "materials index")) and sum(k in text for k in ("evidence", "testing report", "order", "medical records")) >= 2 and sum(k in text for k in ("first instance", "judgment", "second instance", "appeal")) >= 2

def s20_deadlines_tracked(env) -> bool:
    text = _assistant_calendar_text(env)
    return text is not None and any(k in text for k in ("second instance", "appellee", "appeal")) and any(k in text for k in ("defense", "evidence submission", "respond to the case")) and any(k in text for k in ("deadline", "cutoff", "15 days"))
CHECKS = [("s20_persisted_case_archive", s20_archive_notion, 0.5), ("s20_remaining_deadlines_tracked", s20_deadlines_tracked, 0.5)]

