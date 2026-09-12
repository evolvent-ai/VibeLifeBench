"""Stage 11: CJK_8D28_CJK_8BC1_CJK_5E94_CJK_5BF9_ — CJK_63A5_CJK_53D7_CJK_780D_CJK_5934_CJK_606F_(CJK_672C_CJK_91D1_CJK_6309_CJK_5B9E_CJK_9645_36CJK_4E07_) + CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_CJK_4E3E_CJK_8BC1_CJK_5E94_CJK_5BF9_; CJK_843D_ Notion."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import d_defense_kantou_accepted


def s11_finds_supporting_case(env) -> bool:
    """CJK_68C0_CJK_7D22_CJK_5230_CJK_652F_CJK_6301_CJK_8D28_CJK_8BC1_CJK_7684_CJK_540C_CJK_7C7B_CJK_5224_CJK_4F8B_ (case_001 CJK_780D_CJK_5934_CJK_606F_CJK_672C_CJK_91D1_CJK_6309_CJK_5B9E_CJK_9645_ / case_012 CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_CJK_6B63_CJK_9762_CJK_8BA4_CJK_5B9A_)。"""
    text = _stage_corpus(env, 11)
    return any(k in text for k in ["case_001", "case_012", "case_003", "CJK_672C_CJK_91D1_CJK_6309_CJK_5B9E_CJK_9645_", "CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_", "CJK_53D6_CJK_73B0_CJK_51ED_CJK_8BC1_", "CJK_7EFC_CJK_5408_CJK_8BA4_CJK_5B9A_"])


def s11_rebuttal_in_notion(env) -> bool:
    """CJK_8D28_CJK_8BC1_CJK_610F_CJK_89C1_CJK_843D_CJK_5230_ Notion (side effect)。"""
    text = _notion_page_text(env, "CJK_8D28_CJK_8BC1_") or _notion_page_text(env, "CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_CJK_8FFD_CJK_507F_")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["CJK_8D28_CJK_8BC1_", "CJK_53CD_CJK_9A73_", "CJK_672C_CJK_91D1_", "CJK_780D_CJK_5934_CJK_606F_", "CJK_73B0_CJK_91D1_", "CJK_4EA4_CJK_4ED8_"])


CHECKS = [
    ("s11_finds_supporting_case", s11_finds_supporting_case, 0.5),
    ("s11_rebuttal_in_notion", s11_rebuttal_in_notion, 0.5),
    ("d_defense_kantou_accepted", d_defense_kantou_accepted, 0.5),
]
