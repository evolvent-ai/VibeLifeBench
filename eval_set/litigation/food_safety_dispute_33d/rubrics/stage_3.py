"""Stage 3: 诉求筛选矩阵 — 逐条甄别赵萌邮件《我想跟卖家要的几笔账》6 项诉求.

每项有反直觉正确结论, 迫使 agent 逐条甄别而非一律"都能要":
- 退货款 + 退一赔十(可, d_refund_plus_penalty / d_ten_vs_three_higher)
- 就医费(实际损失可另主张, d_medical_loss_separate)
- 精神损失费(纯财产消费一般不支持, d_no_mental_damages)
- 平台能否赔(失联可先行赔付, d_platform_liability)
- 看过差评(食品领域知假买假不影响 — 已在 s1 计数)
"""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import (
    d_refund_plus_penalty, d_ten_vs_three_higher, d_medical_loss_separate,
    d_no_mental_damages, d_platform_liability,
)


def s3_reads_claims_draft(env) -> bool:
    """读赵萌《我想跟卖家要的几笔账》草稿并逐条甄别。"""
    text = _stage_corpus(env, 3)
    return any(k in text for k in ["退一赔十", "退货款", "就医", "精神损失", "平台", "差评"])


CHECKS = [
    ("d_refund_plus_penalty", d_refund_plus_penalty, 1),
    ("d_ten_vs_three_higher", d_ten_vs_three_higher, 1),
    ("d_medical_loss_separate", d_medical_loss_separate, 1),
    ("d_no_mental_damages", d_no_mental_damages, 2),
    ("d_platform_liability", d_platform_liability, 2),
]
