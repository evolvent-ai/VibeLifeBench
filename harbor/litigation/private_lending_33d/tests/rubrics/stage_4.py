"""Stage 4: CJK_8BC1_CJK_636E_CJK_94FE_CJK_6574_CJK_7406_ — CJK_5927_CJK_989D_CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_CJK_4E3E_CJK_8BC1_CJK_98CE_CJK_9669_ + CJK_8BC1_CJK_636E_CJK_6E05_CJK_5355_CJK_8FDB_ Notion."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import d_cash_delivery_risk


def s4_evidence_list_in_notion(env) -> bool:
    """CJK_8BC1_CJK_636E_CJK_6E05_CJK_5355_CJK_5199_CJK_8FDB_ Notion (side effect)。"""
    text = _notion_page_text(env, "CJK_8BC1_CJK_636E_") or _notion_page_text(env, "CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_CJK_8FFD_CJK_507F_")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["CJK_8BC1_CJK_636E_", "CJK_501F_CJK_6761_", "CJK_8F6C_CJK_8D26_", "CJK_5FAE_CJK_4FE1_", "CJK_50AC_CJK_6536_"])


def s4_evidence_inventory(env) -> bool:
    """CJK_5217_CJK_51FA_CJK_4E86_CJK_591A_CJK_7C7B_CJK_5173_CJK_952E_CJK_8BC1_CJK_636E_ (CJK_501F_CJK_6761_/CJK_8F6C_CJK_8D26_CJK_56DE_CJK_5355_/CJK_5FAE_CJK_4FE1_CJK_50AC_CJK_6536_/CJK_8FD8_CJK_6B3E_CJK_8BB0_CJK_5F55_/CJK_8BC1_CJK_4EBA_)。"""
    text = _stage_corpus(env, 4)
    n = sum(1 for k in ["CJK_501F_CJK_6761_", "CJK_8F6C_CJK_8D26_", "CJK_56DE_CJK_5355_", "CJK_5FAE_CJK_4FE1_", "CJK_50AC_CJK_6536_", "CJK_8FD8_CJK_6B3E_", "CJK_8BC1_CJK_4EBA_", "CJK_6797_CJK_6D9B_"] if k in text)
    return n >= 3


CHECKS = [
    ("s4_evidence_list_in_notion", s4_evidence_list_in_notion, 0.5),
    ("s4_evidence_inventory", s4_evidence_inventory, 0.5),
    ("d_cash_delivery_risk", d_cash_delivery_risk, 1),
]
