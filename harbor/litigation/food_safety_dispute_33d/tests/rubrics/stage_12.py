"""Stage 12: hearing calendar and originals checklist."""
from __future__ import annotations
from ._helpers import _assistant_calendar_text, _food_journal_text

def s12_hearing_in_calendar(env) -> bool:
    text = _assistant_calendar_text(env)
    return text is not None and any(k in text for k in ("trial hearing", "hearing", "pre-hearing")) and any(k in text for k in ("2026-06-12", "06-12"))

def s12_bring_originals(env) -> bool:
    journal, calendar = _food_journal_text(env), _assistant_calendar_text(env)
    return journal is not None and calendar is not None and any(k in journal for k in ("original evidence", "originals", "identity document")) and any(k in journal for k in ("food samples", "food at issue", "infant formula", "tea substitute")) and any(k in journal for k in ("testing materials", "testing report", "submit for testing")) and any(k in calendar for k in ("trial hearing", "hearing", "pre-hearing")) and any(k in calendar for k in ("2026-06-12", "06-12"))
CHECKS = [("s12_assistant_hearing_calendar", s12_hearing_in_calendar, 0.5), ("s12_persisted_originals_checklist", s12_bring_originals, 0.5)]

