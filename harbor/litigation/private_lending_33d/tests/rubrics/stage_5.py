"""Stage 5: CJK_8D77_CJK_8BC9_CJK_6750_CJK_6599_CJK_6E05_CJK_5355_ — CJK_8BC9_CJK_8BBC_CJK_8D39_CJK_9636_CJK_68AF_CJK_6536_CJK_53D6_(CJK_53CD_CJK_76F4_CJK_89C9_) + CJK_8FD8_CJK_6B3E_CJK_62B5_CJK_5145_CJK_5DF2_CJK_5728_ stage_3."""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import d_litigation_fee_tiered


def s5_filing_checklist(env) -> bool:
    """CJK_7ED9_CJK_51FA_CJK_4E86_CJK_7ACB_CJK_6848_CJK_6750_CJK_6599_CJK_6E05_CJK_5355_ (CJK_8D77_CJK_8BC9_CJK_72B6_ + CJK_8EAB_CJK_4EFD_/CJK_501F_CJK_6761_/CJK_8F6C_CJK_8D26_CJK_51ED_CJK_8BC1_ + CJK_63D0_CJK_4EA4_CJK_6CD5_CJK_9662_)。"""
    text = _stage_corpus(env, 5)
    has_complaint = any(k in text for k in ["CJK_8D77_CJK_8BC9_CJK_72B6_", "CJK_8D77_CJK_8BC9_CJK_4E66_", "CJK_8BC9_CJK_72B6_", "CJK_7ACB_CJK_6848_CJK_6750_CJK_6599_"])
    has_materials = any(k in text for k in ["CJK_8EAB_CJK_4EFD_CJK_8BC1_", "CJK_501F_CJK_6761_", "CJK_8F6C_CJK_8D26_", "CJK_8BC1_CJK_636E_", "CJK_526F_CJK_672C_", "CJK_6750_CJK_6599_CJK_6E05_CJK_5355_"])
    return has_complaint and has_materials


CHECKS = [
    ("s5_filing_checklist", s5_filing_checklist, 0.5),
    ("d_litigation_fee_tiered", d_litigation_fee_tiered, 1),
]
