"""Stage 15: CJK_5EAD_CJK_540E_CJK_5C0F_CJK_7ED3_CJK_8FDB_ Notion — CJK_4E89_CJK_70B9_/CJK_4E3B_CJK_5F20_/CJK_4F9D_CJK_636E_(side effect)."""
from __future__ import annotations

from ._helpers import _journal_text, _notion_page_text


def s15_summary_in_notion(env) -> bool:
    """CJK_5EAD_CJK_540E_CJK_5C0F_CJK_7ED3_CJK_5199_CJK_8FDB_ Notion (side effect)。"""
    text = _notion_page_text(env, "CJK_5EAD_CJK_540E_") or _notion_page_text(env, "CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_CJK_8FFD_CJK_507F_")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["CJK_4E89_CJK_70B9_", "CJK_5EAD_CJK_540E_", "CJK_8D28_CJK_8BC1_", "CJK_4E3B_CJK_5F20_", "CJK_4F9D_CJK_636E_", "CJK_672C_CJK_91D1_", "CJK_780D_CJK_5934_CJK_606F_"])


def s15_captures_arguments(env) -> bool:
    """CJK_5EAD_CJK_540E_CJK_53F0_CJK_8D26_CJK_987B_CJK_540C_CJK_65F6_CJK_8986_CJK_76D6_CJK_53CC_CJK_65B9_CJK_4E3B_CJK_5F20_、CJK_8BC1_CJK_636E_CJK_4E89_CJK_8BAE_CJK_548C_CJK_4E0B_CJK_4E00_CJK_7A0B_CJK_5E8F_。"""
    text = _journal_text(env)
    if not text:
        return False
    has_plaintiff = any(token in text for token in ("CJK_6211_CJK_65B9_CJK_4E3B_CJK_5F20_", "CJK_738B_CJK_82B3_CJK_4E3B_CJK_5F20_", "CJK_539F_CJK_544A_CJK_4E3B_CJK_5F20_"))
    has_defendant = any(token in text for token in ("CJK_9648_CJK_5F3A_CJK_6297_CJK_8FA9_", "CJK_5BF9_CJK_65B9_CJK_6297_CJK_8FA9_", "CJK_88AB_CJK_544A_CJK_6297_CJK_8FA9_"))
    has_issue = sum(token in text for token in ("CJK_780D_CJK_5934_CJK_606F_", "CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_", "CJK_592B_CJK_59BB_CJK_5171_CJK_540C_CJK_503A_CJK_52A1_", "CJK_62C5_CJK_4FDD_", "CJK_5B9E_CJK_9645_CJK_672C_CJK_91D1_")) >= 2
    has_evidence = sum(token in text for token in ("CJK_94F6_CJK_884C_CJK_6D41_CJK_6C34_", "CJK_501F_CJK_6761_", "CJK_50AC_CJK_6B3E_CJK_8BB0_CJK_5F55_", "CJK_5FAE_CJK_4FE1_", "CJK_8D28_CJK_8BC1_")) >= 2
    has_next = any(token in text for token in ("CJK_7B49_CJK_5F85_CJK_6CD5_CJK_9662_CJK_5224_CJK_51B3_", "CJK_7B49_CJK_5F85_CJK_5224_CJK_51B3_", "CJK_5224_CJK_51B3_CJK_5F85_CJK_9001_CJK_8FBE_", "CJK_8D28_CJK_8BC1_CJK_7ED3_CJK_8BBA_"))
    return has_plaintiff and has_defendant and has_issue and has_evidence and has_next


CHECKS = [
    ("s15_summary_in_notion", s15_summary_in_notion, 0.5),
    ("s15_captures_arguments", s15_captures_arguments, 0.5),
]
