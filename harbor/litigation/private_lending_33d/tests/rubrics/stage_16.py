"""Stage 16: CJK_5224_CJK_51B3_CJK_9001_CJK_8FBE_(world) — CJK_54CD_CJK_5E94_CJK_5224_CJK_51B3_CJK_7ED3_CJK_679C_、CJK_9884_CJK_8B66_15CJK_65E5_CJK_4E0A_CJK_8BC9_CJK_671F_(s_)."""
from __future__ import annotations

from ._helpers import _stage_corpus


def s16_acknowledges_judgment(env) -> bool:
    """CJK_5BF9_CJK_5224_CJK_51B3_CJK_7ED3_CJK_679C_(CJK_652F_CJK_6301_CJK_672C_CJK_91D1_360000, CJK_9A73_CJK_56DE_CJK_7B2C_CJK_4E8C_CJK_7B14_/CJK_914D_CJK_5076_/CJK_62C5_CJK_4FDD_)CJK_4F5C_CJK_51FA_CJK_54CD_CJK_5E94_。"""
    text = _stage_corpus(env, 16)
    has_amount = any(k in text for k in ["360000", "360,000", "36CJK_4E07_", "CJK_4E09_CJK_5341_CJK_516D_CJK_4E07_"])
    has_result = any(k in text for k in ["CJK_5224_CJK_51B3_", "CJK_652F_CJK_6301_", "CJK_8FD4_CJK_8FD8_", "CJK_9A73_CJK_56DE_", "CJK_80DC_"])
    return has_amount and has_result


CHECKS = [
    ("s16_acknowledges_judgment", s16_acknowledges_judgment, 0.5),
]
