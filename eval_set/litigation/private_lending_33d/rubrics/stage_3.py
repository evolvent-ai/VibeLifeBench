"""Stage 3: 本息计算 + 诉求筛选矩阵.

计算: 砍头息→第一笔本金按实际36万; 利率超LPR四倍封顶; 还款先抵息后抵本.
诉求筛选(难度核心): 逐条甄别王芳想追的6笔账, 每项反直觉正确结论。
"""
from __future__ import annotations

from ._helpers import _journal_text, _stage_corpus
from .cross_stage import (
    d_kantou_interest_principal, d_lpr_four_times, d_repayment_offset,
    d_claim_mental_damages, d_claim_lost_wages, d_claim_interest_capped,
    d_not_professional_lending,
)


def s3_reads_facts(env) -> bool:
    """双方、两笔借款、实际交付和证据渠道必须写入台账。"""
    text = _journal_text(env)
    if not text:
        return False
    has_parties = "王芳" in text and "陈强" in text
    has_first = (
        any(token in text for token in ("40万元", "40万", "400000"))
        and any(token in text for token in ("36万元", "36万", "360000"))
        and any(token in text for token in ("实际到账", "银行转账", "转账"))
    )
    has_second = (
        any(token in text for token in ("20万元", "20万", "200000"))
        and any(token in text for token in ("第二笔", "2025年6月", "6月"))
    )
    has_evidence = sum(token in text for token in ("借条", "银行流水", "转账", "微信催款", "还款记录")) >= 3
    return has_parties and has_first and has_second and has_evidence


def s3_reads_claims_draft(env) -> bool:
    """真读了王芳的诉求草稿(邮件#8), 逐条回应而非泛泛。"""
    text = _stage_corpus(env, 3)
    # 须逐条甄别(出现≥3类诉求关键词 + 明确的"能/不能主张"判断)
    n = sum(1 for k in ["精神", "误工", "配偶", "刘敏", "担保", "老周", "利息"] if k in text)
    has_verdict = any(k in text for k in ["不支持", "不能主张", "可以主张", "不予", "剔除", "能要", "不能要", "可主张"])
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
