"""Stage 1: 程序判断 — 收货地管辖/退一赔十/知假买假不影响(读官方须知).

知识回忆型 d_(程序点)权重压低(0.5), 真正难点在后续场景约束矩阵。
退一赔十 与 知假买假 是反直觉核心, 给 2.0。
"""
from __future__ import annotations

from ._helpers import _food_journal_text
from .cross_stage import (
    d_tenfold_not_treble, d_knowing_purchase_ok, d_delivery_jurisdiction,
)


def s1_reads_official_notice(env) -> bool:
    """官方须知及三项适用结论必须持久化到案件台账。"""
    text = _food_journal_text(env)
    if not text:
        return False
    has_source = any(k in text for k in ("浦东法院", "oa_pudong_court", "官方须知", "立案与诉讼须知"))
    has_jurisdiction = (
        any(k in text for k in ("收货地", "合同履行地"))
        and any(k in text for k in ("上海浦东", "浦东法院", "浦东"))
    )
    has_tenfold = (
        any(k in text for k in ("退一赔十", "十倍赔偿", "价款十倍"))
        and any(k in text for k in ("第一百四十八条", "148条", "食品安全法"))
    )
    has_knowing = (
        "知假买假" in text
        and any(k in text for k in ("不影响", "仍可索赔", "抗辩不成立", "仍可赔"))
    )
    return has_source and has_jurisdiction and has_tenfold and has_knowing


CHECKS = [
    ("s1_reads_official_notice", s1_reads_official_notice, 0.5),
    ("d_tenfold_not_treble_safety", d_tenfold_not_treble, 2),  # safety-critical: 退一赔十非三倍
    ("d_knowing_purchase_ok", d_knowing_purchase_ok, 1),
    ("d_delivery_jurisdiction", d_delivery_jurisdiction, 1),
]
