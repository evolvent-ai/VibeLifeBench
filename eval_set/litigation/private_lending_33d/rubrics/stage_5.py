"""Stage 5: 起诉材料清单 — 诉讼费阶梯收取(反直觉) + 还款抵充已在 stage_3."""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import d_litigation_fee_tiered


def s5_filing_checklist(env) -> bool:
    """给出了立案材料清单 (起诉状 + 身份/借条/转账凭证 + 提交法院)。"""
    text = _stage_corpus(env, 5)
    has_complaint = any(k in text for k in ["起诉状", "起诉书", "诉状", "立案材料"])
    has_materials = any(k in text for k in ["身份证", "借条", "转账", "证据", "副本", "材料清单"])
    return has_complaint and has_materials


CHECKS = [
    ("s5_filing_checklist", s5_filing_checklist, 0.5),
    ("d_litigation_fee_tiered", d_litigation_fee_tiered, 1),
]
