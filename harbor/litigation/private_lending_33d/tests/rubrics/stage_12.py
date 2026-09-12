"""Stage 12: CJK_5F00_CJK_5EAD_CJK_901A_CJK_77E5_ — CJK_68C0_CJK_67E5_CJK_534F_CJK_4F5C_CJK_8005_CJK_81EA_CJK_884C_CJK_6301_CJK_4E45_CJK_5316_CJK_7684_CJK_5EAD_CJK_524D_CJK_5B89_CJK_6392_。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text


def s12_hearing_on_calendar(env) -> bool:
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_hearing = any(key in text for key in ("CJK_5F00_CJK_5EAD_", "CJK_5EAD_CJK_5BA1_", "CJK_5EAD_CJK_524D_"))
    has_date = any(key in text for key in ("2026-06-12", "06-12", "6CJK_6708_12"))
    return has_hearing and has_date


def s12_brings_originals(env) -> bool:
    journal = _journal_text(env)
    calendar = _assistant_calendar_text(env)
    if journal is None or calendar is None:
        return False  # required evidence unavailable -> fail closed
    has_id = any(key in journal for key in ("CJK_8EAB_CJK_4EFD_CJK_8BC1_", "CJK_8BC1_CJK_4EF6_"))
    has_note = any(key in journal for key in ("CJK_501F_CJK_6761_CJK_539F_CJK_4EF6_", "CJK_501F_CJK_6761_", "CJK_8BC1_CJK_636E_CJK_539F_CJK_4EF6_"))
    has_bank = any(key in journal for key in ("CJK_8F6C_CJK_8D26_CJK_56DE_CJK_5355_", "CJK_94F6_CJK_884C_CJK_6D41_CJK_6C34_", "CJK_7535_CJK_5B50_CJK_56DE_CJK_5355_"))
    has_chat = any(key in journal for key in ("CJK_5FAE_CJK_4FE1_CJK_8BB0_CJK_5F55_", "CJK_50AC_CJK_6536_CJK_8BB0_CJK_5F55_", "CJK_8FD8_CJK_6B3E_CJK_8BB0_CJK_5F55_"))
    has_hearing_calendar = (
        any(key in calendar for key in ("CJK_5F00_CJK_5EAD_", "CJK_5EAD_CJK_5BA1_", "CJK_5EAD_CJK_524D_"))
        and any(key in calendar for key in ("2026-06-12", "06-12", "6CJK_6708_12"))
    )
    return has_id and has_note and has_bank and has_chat and has_hearing_calendar


CHECKS = [
    ("s12_assistant_hearing_calendar", s12_hearing_on_calendar, 0.5),
    ("s12_persisted_originals_checklist", s12_brings_originals, 0.5),
]
