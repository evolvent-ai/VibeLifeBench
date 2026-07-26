"""Stage 5: 立案材料清单(cron_fire) — 起诉状/被告/材料/诉讼费/申请检验核对."""
from __future__ import annotations

from ._helpers import _stage_corpus
from .cross_stage import d_fees, d_defendant_election


def s5_filing_checklist(env) -> bool:
    """对照官方须知核对立案材料(起诉状/被告/材料/诉讼费)。"""
    text = _stage_corpus(env, 5)
    has_complaint = any(k in text for k in ["起诉状", "诉讼请求", "事实与理由"])
    has_defendants = any(k in text for k in ["被告", "环球优选", "优鲜购", "生产者", "平台"])
    has_forum = any(k in text for k in ["浦东", "法院", "收货地", "管辖"])
    has_fees = any(k in text for k in ["诉讼费", "受理费", "预交", "败诉方承担"])
    has_inspection = any(k in text for k in ["检验", "送检", "SQI", "鉴定"])
    return sum([has_complaint, has_defendants, has_forum, has_fees, has_inspection]) >= 4


def s5_defendant_consideration(env) -> bool:
    """被告该列谁(卖家/生产者/平台)的考量。"""
    text = _stage_corpus(env, 5)
    has_subjects = sum(
        1 for ks in [
            ["环球优选", "卖家", "销售者"],
            ["优鲜购", "平台"],
            ["生产者", "厂家"],
        ]
        if any(k in text for k in ks)
    ) >= 2
    has_choice = any(k in text for k in ["择一", "选择", "是否追加", "考虑", "方案", "你来定", "你决定"])
    return has_subjects and has_choice


CHECKS = [
    ("d_fees", d_fees, 0.5),
    ("d_defendant_election", d_defendant_election, 1),
]
