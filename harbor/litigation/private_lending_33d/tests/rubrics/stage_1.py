"""Stage 1: CJK_641E_CJK_6E05_CJK_7A0B_CJK_5E8F_ — CJK_65E0_CJK_4EF2_CJK_88C1_CJK_524D_CJK_7F6E_ + CJK_65F6_CJK_6548_3CJK_5E74_CJK_4E2D_CJK_65AD_ + CJK_7BA1_CJK_8F96_CJK_63A5_CJK_6536_CJK_8D27_CJK_5E01_CJK_4E00_CJK_65B9_ (CJK_6838_CJK_5FC3_CJK_7A0B_CJK_5E8F_CJK_4E09_CJK_8FDE_)."""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import (
    d_no_arbitration_precondition, d_limitation_3y_interruption, d_jurisdiction_lender,
)


def s1_reads_official_notice(env) -> bool:
    """CJK_8BFB_CJK_4E86_CJK_6CD5_CJK_9662_CJK_5B98_CJK_65B9_CJK_7ACB_CJK_6848_CJK_987B_CJK_77E5_ (CJK_5F15_CJK_7528_CJK_987B_CJK_77E5_CJK_7279_CJK_6709_CJK_5185_CJK_5BB9_, CJK_800C_CJK_975E_CJK_6CDB_CJK_6CDB_CJK_5E38_CJK_8BC6_)。"""
    text = _stage_corpus(env, 1)
    return any(k in text for k in ["CJK_7ACB_CJK_6848_CJK_987B_CJK_77E5_", "CJK_676D_CJK_5DDE_CJK_6CD5_CJK_9662_", "CJK_8BC9_CJK_8BBC_CJK_670D_CJK_52A1_", "CJK_897F_CJK_6E56_CJK_533A_CJK_4EBA_CJK_6C11_CJK_6CD5_CJK_9662_", "oa_hz_court", "CJK_5B98_CJK_65B9_CJK_987B_CJK_77E5_", "CJK_987B_CJK_77E5_"])


CHECKS = [
    ("s1_reads_official_notice", s1_reads_official_notice, 0.5),
    ("d_no_arbitration_precondition", d_no_arbitration_precondition, 0.5),
    ("d_limitation_3y_interruption", d_limitation_3y_interruption, 0.5),
    ("d_jurisdiction_lender", d_jurisdiction_lender, 0.5),
]
