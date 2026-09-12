"""Stage 14: CJK_5EAD_CJK_5BA1_CJK_7ED3_CJK_675F_ — CJK_5B9E_CJK_9645_CJK_5EAD_CJK_5BA1_CJK_4E89_CJK_70B9_CJK_987B_CJK_6301_CJK_4E45_CJK_5316_。"""
from __future__ import annotations

from ._helpers import _journal_text


def s14_hearing_result_captured(env) -> bool:
    journal = _journal_text(env)
    if journal is None:
        return False  # required evidence unavailable -> fail closed
    has_hearing = any(key in journal for key in ("CJK_5EAD_CJK_5BA1_CJK_7ED3_CJK_675F_", "CJK_5F00_CJK_5EAD_CJK_7ED3_CJK_675F_", "CJK_5EAD_CJK_5BA1_CJK_8BB0_CJK_5F55_", "CJK_5EAD_CJK_5BA1_CJK_5C0F_CJK_7ED3_"))
    issue_count = sum(
        key in journal
        for key in ("CJK_780D_CJK_5934_CJK_606F_", "CJK_5B9E_CJK_9645_CJK_5230_CJK_8D26_", "CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_", "CJK_5229_CJK_606F_", "CJK_62C5_CJK_4FDD_", "CJK_592B_CJK_59BB_CJK_5171_CJK_540C_CJK_503A_CJK_52A1_")
    )
    has_next = any(key in journal for key in ("CJK_62E9_CJK_671F_CJK_5BA3_CJK_5224_", "CJK_7B49_CJK_5F85_CJK_5224_CJK_51B3_", "CJK_5EAD_CJK_540E_CJK_610F_CJK_89C1_"))
    return has_hearing and issue_count >= 3 and has_next


CHECKS = [
    ("s14_persisted_hearing_result", s14_hearing_result_captured, 0.5),
]
