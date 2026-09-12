"""Stage 21: CJK_590D_CJK_76D8_CJK_603B_CJK_7ED3_ — Notion CJK_603B_CJK_7ED3_ + CJK_7ECF_CJK_9A8C_CJK_6559_CJK_8BAD_ + CJK_4E8C_CJK_5BA1_CJK_9636_CJK_6BB5_CJK_65B9_CJK_5411_(side effect+text)."""
from __future__ import annotations

from ._helpers import _notion_page_text, _stage_corpus


def s21_retro_in_notion(env) -> bool:
    """CJK_590D_CJK_76D8_CJK_603B_CJK_7ED3_CJK_5199_CJK_8FDB_ Notion (CJK_8FC7_CJK_7A0B_/CJK_8282_CJK_70B9_/CJK_8BC1_CJK_636E_CJK_6CD5_CJK_6761_/CJK_6210_CJK_672C_)。"""
    text = _notion_page_text(env, "CJK_590D_CJK_76D8_") or _notion_page_text(env, "CJK_603B_CJK_7ED3_") or _notion_page_text(env, "CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_CJK_8FFD_CJK_507F_")
    if text is None:
        return False  # required evidence unavailable → fail closed
    n = sum(1 for k in ["CJK_590D_CJK_76D8_", "CJK_603B_CJK_7ED3_", "CJK_7ECF_CJK_9A8C_", "CJK_6559_CJK_8BAD_", "CJK_8BC1_CJK_636E_", "CJK_6CD5_CJK_6761_", "CJK_672C_CJK_91D1_", "CJK_8282_CJK_70B9_"] if k in text)
    return n >= 2


def s21_lessons_learned(env) -> bool:
    """CJK_8BB0_CJK_5F55_CJK_501F_CJK_8D37_CJK_7ECF_CJK_9A8C_CJK_6559_CJK_8BAD_ (CJK_780D_CJK_5934_CJK_606F_/CJK_73B0_CJK_91D1_CJK_7559_CJK_51ED_CJK_8BC1_/CJK_62C5_CJK_4FDD_CJK_5199_CJK_6E05_/CJK_53CA_CJK_65F6_CJK_50AC_CJK_6536_)。"""
    text = _stage_corpus(env, 21)
    return any(k in text for k in ["CJK_780D_CJK_5934_CJK_606F_", "CJK_73B0_CJK_91D1_", "CJK_7559_CJK_51ED_CJK_8BC1_", "CJK_7559_CJK_8BC1_", "CJK_62C5_CJK_4FDD_", "CJK_50AC_CJK_6536_", "CJK_53CA_CJK_65F6_", "CJK_6559_CJK_8BAD_", "CJK_7ECF_CJK_9A8C_"])


def s21_next_steps(env) -> bool:
    """CJK_7ED9_CJK_51FA_CJK_4E8C_CJK_5BA1_CJK_9636_CJK_6BB5_CJK_7684_CJK_51C6_CJK_5907_CJK_65B9_CJK_5411_。"""
    text = _stage_corpus(env, 21)
    has_appeal = any(k in text for k in ["CJK_4E8C_CJK_5BA1_", "CJK_4E0A_CJK_8BC9_", "CJK_5E94_CJK_8BC9_", "CJK_5EAD_CJK_5BA1_", "CJK_7B54_CJK_8FA9_"])
    has_direction = any(k in text for k in ["CJK_51C6_CJK_5907_", "CJK_65B9_CJK_5411_", "CJK_8BC1_CJK_636E_", "CJK_4E0B_CJK_4E00_CJK_6B65_", "CJK_5EFA_CJK_8BAE_"])
    return has_appeal and has_direction


CHECKS = [
    ("s21_retro_in_notion", s21_retro_in_notion, 0.5),
    ("s21_lessons_learned", s21_lessons_learned, 0.5),
    ("s21_next_steps", s21_next_steps, 0.5),
]
