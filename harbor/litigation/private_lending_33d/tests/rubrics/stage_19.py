"""Stage 19: CJK_4E8C_CJK_5BA1_CJK_5E94_CJK_8BC9_CJK_671F_CJK_9650_ — CJK_65E5_CJK_5386_CJK_4E0E_ Notion CJK_53CC_CJK_6301_CJK_4E45_CJK_5316_。"""
from __future__ import annotations

from ._helpers import _assistant_calendar_text, _journal_text


def s19_appeal_deadlines(env) -> bool:
    text = _assistant_calendar_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_second = any(key in text for key in ("CJK_4E8C_CJK_5BA1_", "CJK_88AB_CJK_4E0A_CJK_8BC9_", "CJK_4E0A_CJK_8BC9_"))
    has_response = any(key in text for key in ("CJK_7B54_CJK_8FA9_", "CJK_5E94_CJK_8BC9_", "CJK_4E3E_CJK_8BC1_"))
    has_deadline = any(key in text for key in ("CJK_671F_CJK_9650_", "CJK_622A_CJK_6B62_", "15CJK_65E5_", "CJK_5341_CJK_4E94_CJK_65E5_", "2026-07"))
    return has_second and has_response and has_deadline


def s19_appeal_vs_trial(env) -> bool:
    text = _journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_role = "CJK_88AB_CJK_4E0A_CJK_8BC9_CJK_4EBA_" in text
    has_scope = any(key in text for key in ("CJK_56F4_CJK_7ED5_CJK_4E0A_CJK_8BC9_CJK_8BF7_CJK_6C42_", "CJK_4E0A_CJK_8BC9_CJK_8BF7_CJK_6C42_CJK_8303_CJK_56F4_", "CJK_4E8C_CJK_5BA1_CJK_5BA1_CJK_7406_CJK_8303_CJK_56F4_"))
    has_evidence = any(key in text for key in ("CJK_8BC1_CJK_636E_CJK_76EE_CJK_5F55_", "CJK_4E00_CJK_5BA1_CJK_8BC1_CJK_636E_", "CJK_8865_CJK_5145_CJK_8BC1_CJK_636E_", "CJK_4E3E_CJK_8BC1_CJK_671F_CJK_9650_"))
    has_cost = any(key in text for key in ("CJK_8BC9_CJK_8BBC_CJK_8D39_", "CJK_8D39_CJK_7528_", "CJK_9884_CJK_4EA4_"))
    return has_role and has_scope and has_evidence and has_cost


CHECKS = [
    ("s19_assistant_appeal_deadlines", s19_appeal_deadlines, 0.5),
    ("s19_persisted_second_instance_plan", s19_appeal_vs_trial, 0.5),
]
