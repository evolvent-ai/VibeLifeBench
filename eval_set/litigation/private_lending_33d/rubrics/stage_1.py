"""Stage 1: 搞清程序 — 无仲裁前置 + 时效3年中断 + 管辖接收货币一方 (核心程序三连)."""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import (
    d_no_arbitration_precondition, d_limitation_3y_interruption, d_jurisdiction_lender,
)


def s1_reads_official_notice(env) -> bool:
    """读了法院官方立案须知 (引用须知特有内容, 而非泛泛常识)。"""
    text = _stage_corpus(env, 1)
    return any(k in text for k in ["立案须知", "杭州法院", "诉讼服务", "西湖区人民法院", "oa_hz_court", "官方须知", "须知"])


CHECKS = [
    ("s1_reads_official_notice", s1_reads_official_notice, 0.5),
    ("d_no_arbitration_precondition", d_no_arbitration_precondition, 0.5),
    ("d_limitation_3y_interruption", d_limitation_3y_interruption, 0.5),
    ("d_jurisdiction_lender", d_jurisdiction_lender, 0.5),
]
