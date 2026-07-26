"""Stage 11: 质证反驳三抗辩 — 食品十倍优先/知假买假不影响/无中文标签属实质不符合.

三抗辩各锚定 env 判例分别反驳。食品十倍(d_tenfold 在 s1)、知假买假(d_knowing 在 s1)、
实质不符合(d_substantive_vs_flaw 在 s5? no — 放本 stage)。本 stage 承载 substantive_vs_flaw + 质证入 Notion。
"""
from __future__ import annotations

from ._helpers import _food_journal_text, _notion_page_text
from .cross_stage import d_substantive_vs_flaw, d_health_claim_violation


def s11_rebut_three_defenses(env) -> bool:
    """三项抗辩须逐项、带来源地写入案件台账。"""
    text = _food_journal_text(env)
    if not text:
        return False
    rebut_ten = (
        any(k in text for k in ("退一赔十", "十倍赔偿", "价款十倍"))
        and any(k in text for k in ("不是三倍", "排除退一赔三", "非退一赔三"))
        and any(k in text for k in ("148条", "第一百四十八条", "case_f01", "case_f12"))
    )
    rebut_knowing = (
        "知假买假" in text
        and any(k in text for k in ("不影响", "仍可赔", "抗辩不成立"))
        and any(k in text for k in ("case_f04", "第三条", "食品药品规则", "食品领域"))
    )
    rebut_flaw = (
        any(k in text for k in ("无中文标签", "非法添加"))
        and any(k in text for k in ("实质不符合", "不是普通标签瑕疵", "不属于标签瑕疵", "不适用但书"))
    )
    return rebut_ten and rebut_knowing and rebut_flaw


def s11_rebuttal_in_notion(env) -> bool:
    """质证意见进 Notion。"""
    text = _notion_page_text(env, "质证") or _notion_page_text(env, "食品安全维权")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["质证", "反驳", "抗辩", "退一赔十", "知假买假", "标签"])


CHECKS = [
    ("s11_rebut_three_defenses", s11_rebut_three_defenses, 2),
    ("s11_rebuttal_in_notion", s11_rebuttal_in_notion, 0.5),
    ("d_substantive_vs_flaw", d_substantive_vs_flaw, 2),
    ("d_health_claim_violation", d_health_claim_violation, 0.5),
]
