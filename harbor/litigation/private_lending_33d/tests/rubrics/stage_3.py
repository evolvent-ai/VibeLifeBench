"""Stage 3: CJK_672C_CJK_606F_CJK_8BA1_CJK_7B97_ + CJK_8BC9_CJK_6C42_CJK_7B5B_CJK_9009_CJK_77E9_CJK_9635_.

CJK_8BA1_CJK_7B97_: CJK_780D_CJK_5934_CJK_606F_→CJK_7B2C_CJK_4E00_CJK_7B14_CJK_672C_CJK_91D1_CJK_6309_CJK_5B9E_CJK_9645_36CJK_4E07_; CJK_5229_CJK_7387_CJK_8D85_LPRCJK_56DB_CJK_500D_CJK_5C01_CJK_9876_; CJK_8FD8_CJK_6B3E_CJK_5148_CJK_62B5_CJK_606F_CJK_540E_CJK_62B5_CJK_672C_.
CJK_8BC9_CJK_6C42_CJK_7B5B_CJK_9009_(CJK_96BE_CJK_5EA6_CJK_6838_CJK_5FC3_): CJK_9010_CJK_6761_CJK_7504_CJK_522B_CJK_738B_CJK_82B3_CJK_60F3_CJK_8FFD_CJK_7684_6CJK_7B14_CJK_8D26_, CJK_6BCF_CJK_9879_CJK_53CD_CJK_76F4_CJK_89C9_CJK_6B63_CJK_786E_CJK_7ED3_CJK_8BBA_。
"""
from __future__ import annotations

from ._helpers import _journal_text, _stage_corpus
from .cross_stage import (
    d_kantou_interest_principal, d_lpr_four_times, d_repayment_offset,
    d_claim_mental_damages, d_claim_lost_wages, d_claim_interest_capped,
    d_not_professional_lending,
)


def s3_reads_facts(env) -> bool:
    """CJK_53CC_CJK_65B9_、CJK_4E24_CJK_7B14_CJK_501F_CJK_6B3E_、CJK_5B9E_CJK_9645_CJK_4EA4_CJK_4ED8_CJK_548C_CJK_8BC1_CJK_636E_CJK_6E20_CJK_9053_CJK_5FC5_CJK_987B_CJK_5199_CJK_5165_CJK_53F0_CJK_8D26_。"""
    text = _journal_text(env)
    if not text:
        return False
    has_parties = "CJK_738B_CJK_82B3_" in text and "CJK_9648_CJK_5F3A_" in text
    has_first = (
        any(token in text for token in ("40CJK_4E07_CJK_5143_", "40CJK_4E07_", "400000"))
        and any(token in text for token in ("36CJK_4E07_CJK_5143_", "36CJK_4E07_", "360000"))
        and any(token in text for token in ("CJK_5B9E_CJK_9645_CJK_5230_CJK_8D26_", "CJK_94F6_CJK_884C_CJK_8F6C_CJK_8D26_", "CJK_8F6C_CJK_8D26_"))
    )
    has_second = (
        any(token in text for token in ("20CJK_4E07_CJK_5143_", "20CJK_4E07_", "200000"))
        and any(token in text for token in ("CJK_7B2C_CJK_4E8C_CJK_7B14_", "2025CJK_5E74_6CJK_6708_", "6CJK_6708_"))
    )
    has_evidence = sum(token in text for token in ("CJK_501F_CJK_6761_", "CJK_94F6_CJK_884C_CJK_6D41_CJK_6C34_", "CJK_8F6C_CJK_8D26_", "CJK_5FAE_CJK_4FE1_CJK_50AC_CJK_6B3E_", "CJK_8FD8_CJK_6B3E_CJK_8BB0_CJK_5F55_")) >= 3
    return has_parties and has_first and has_second and has_evidence


def s3_reads_claims_draft(env) -> bool:
    """CJK_771F_CJK_8BFB_CJK_4E86_CJK_738B_CJK_82B3_CJK_7684_CJK_8BC9_CJK_6C42_CJK_8349_CJK_7A3F_(CJK_90AE_CJK_4EF6_#8), CJK_9010_CJK_6761_CJK_56DE_CJK_5E94_CJK_800C_CJK_975E_CJK_6CDB_CJK_6CDB_。"""
    text = _stage_corpus(env, 3)
    # CJK_987B_CJK_9010_CJK_6761_CJK_7504_CJK_522B_(CJK_51FA_CJK_73B0_≥3CJK_7C7B_CJK_8BC9_CJK_6C42_CJK_5173_CJK_952E_CJK_8BCD_ + CJK_660E_CJK_786E_CJK_7684_"CJK_80FD_/CJK_4E0D_CJK_80FD_CJK_4E3B_CJK_5F20_"CJK_5224_CJK_65AD_)
    n = sum(1 for k in ["CJK_7CBE_CJK_795E_", "CJK_8BEF_CJK_5DE5_", "CJK_914D_CJK_5076_", "CJK_5218_CJK_654F_", "CJK_62C5_CJK_4FDD_", "CJK_8001_CJK_5468_", "CJK_5229_CJK_606F_"] if k in text)
    has_verdict = any(k in text for k in ["CJK_4E0D_CJK_652F_CJK_6301_", "CJK_4E0D_CJK_80FD_CJK_4E3B_CJK_5F20_", "CJK_53EF_CJK_4EE5_CJK_4E3B_CJK_5F20_", "CJK_4E0D_CJK_4E88_", "CJK_5254_CJK_9664_", "CJK_80FD_CJK_8981_", "CJK_4E0D_CJK_80FD_CJK_8981_", "CJK_53EF_CJK_4E3B_CJK_5F20_"])
    return n >= 3 and has_verdict


CHECKS = [
    ("s3_reads_facts", s3_reads_facts, 0.5),
    ("s3_reads_claims_draft", s3_reads_claims_draft, 0.5),
    ("d_kantou_interest_principal", d_kantou_interest_principal, 1),
    ("d_lpr_four_times", d_lpr_four_times, 0.5),
    ("d_repayment_offset", d_repayment_offset, 0.5),
    ("d_claim_interest_capped", d_claim_interest_capped, 0.5),
    ("d_claim_mental_damages", d_claim_mental_damages, 0.5),
    ("d_claim_lost_wages", d_claim_lost_wages, 0.5),
    ("d_not_professional_lending", d_not_professional_lending, 0.5),
]
