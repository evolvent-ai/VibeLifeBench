"""Stage 2: CJK_9009_CJK_8058_CJK_5F8B_CJK_5E08_(CJK_573A_CJK_666F_CJK_7EA6_CJK_675F_CJK_77E9_CJK_9635_) — CJK_9010_CJK_6761_CJK_6392_CJK_9664_6CJK_4E2A_CJK_9677_CJK_9631_CJK_5F8B_CJK_5E08_, CJK_9501_CJK_5B9A_CJK_6700_CJK_4F18_, CJK_5B88_CJK_9884_CJK_4ED8_CJK_9884_CJK_7B97_CJK_786C_CJK_9876_.

CJK_573A_CJK_666F_CJK_7EA6_CJK_675F_CJK_578B_CJK_96BE_CJK_5EA6_CJK_6838_CJK_5FC3_: agent CJK_987B_CJK_771F_CJK_8BFB_CJK_5F8B_CJK_5E08_CJK_540D_CJK_5F55_(LD-001~008)、CJK_5BF9_CJK_7167_CJK_738B_CJK_82B3_CJK_7EA6_CJK_675F_CJK_9010_CJK_6761_CJK_6838_CJK_5BF9_、
CJK_6392_CJK_9664_CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_/CJK_540A_CJK_8BC1_/CJK_4E13_CJK_4E1A_CJK_4E0D_CJK_7B26_/CJK_5F02_CJK_5730_/CJK_8D85_CJK_9884_CJK_7B97_/CJK_8D85_CJK_4E0A_CJK_9650_, CJK_9501_CJK_5B9A_ LD-006, CJK_5B88_CJK_4F4F_ ¥8000 CJK_9884_CJK_4ED8_CJK_9884_CJK_7B97_。
CJK_540C_CJK_65F6_CJK_987A_CJK_5E26_CJK_8BFB_CJK_6700_CJK_8D34_CJK_8FD1_CJK_5224_CJK_4F8B_(s2_precedent_citation / d_statute_in_force)。
"""
from __future__ import annotations

from ._helpers import _journal_text, _notion_page_text
from .cross_stage import (
    d_reads_lawyer_roster, d_lawyer_conflict_excluded, d_lawyer_disbarred_excluded,
    d_lawyer_wrong_specialty_excluded, d_lawyer_wrong_jurisdiction_excluded,
    d_lawyer_over_budget_excluded, d_lawyer_contingency_cap, d_lawyer_best_pick,
    d_lawyer_budget_cap, d_statute_in_force,
)


def s2_precedent_citation(env) -> bool:
    """CJK_5224_CJK_4F8B_CJK_8981_CJK_65E8_、CJK_5F53_CJK_524D_CJK_6848_CJK_4EF6_CJK_9002_CJK_7528_CJK_548C_CJK_4E0B_CJK_4E00_CJK_6B65_CJK_5FC5_CJK_987B_CJK_6301_CJK_4E45_CJK_5316_。"""
    text = _journal_text(env)
    if not text:
        return False
    has_case = any(token in text for token in ("case_001", "2025CJK_6D59_0106CJK_6C11_CJK_521D_13201", "CJK_780D_CJK_5934_CJK_606F_"))
    has_holding = (
        any(token in text for token in ("CJK_5B9E_CJK_9645_CJK_5230_CJK_8D26_", "CJK_5B9E_CJK_9645_CJK_51FA_CJK_501F_", "CJK_5B9E_CJK_9645_CJK_672C_CJK_91D1_"))
        and any(token in text for token in ("36CJK_4E07_CJK_5143_", "36CJK_4E07_", "360000"))
    )
    has_application = (
        "CJK_738B_CJK_82B3_" in text
        and "CJK_9648_CJK_5F3A_" in text
        and any(token in text for token in ("CJK_6838_CJK_7B97_CJK_672C_CJK_91D1_", "CJK_5229_CJK_606F_CJK_4E0A_CJK_9650_", "CJK_8BC9_CJK_8BF7_", "CJK_4E0B_CJK_4E00_CJK_6B65_"))
    )
    return has_case and has_holding and has_application


def s2_lawyer_choice_in_notion(env) -> bool:
    """CJK_573A_CJK_666F_CJK_7EA6_CJK_675F_·CJK_6267_CJK_884C_: CJK_9009_CJK_5B9A_CJK_7684_CJK_5F8B_CJK_5E08_(CJK_53CA_CJK_7406_CJK_7531_/CJK_6536_CJK_8D39_)CJK_987B_CJK_8BB0_CJK_5165_ Notion, CJK_4E0D_CJK_80FD_CJK_53EA_CJK_53E3_CJK_5934_。"""
    text = _notion_page_text(env, "CJK_5F8B_CJK_5E08_") or _notion_page_text(env, "CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_CJK_8FFD_CJK_507F_")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["CJK_5F8B_CJK_5E08_", "LD-006", "CJK_5468_CJK_654F_", "CJK_59D4_CJK_6258_", "CJK_98CE_CJK_9669_CJK_4EE3_CJK_7406_", "CJK_4EE3_CJK_7406_"])


# CJK_6743_CJK_91CD_CJK_54F2_CJK_5B66_: CJK_5F8B_CJK_5E08_CJK_9009_CJK_8058_CJK_77E9_CJK_9635_(CJK_8BC4_CJK_4F30_ d_ + CJK_8BFB_CJK_540D_CJK_5F55_)CJK_662F_CJK_573A_CJK_666F_CJK_7EA6_CJK_675F_CJK_578B_ reliable-fail——CJK_8DE8_ run CJK_7A33_CJK_5B9A_CJK_5931_CJK_8D25_
# (CJK_5F3A_CJK_6A21_CJK_578B_CJK_5E38_CJK_731C_ user_id `wangfang` CJK_800C_CJK_975E_ `usr_wang_fang`, CJK_627E_CJK_4E0D_CJK_5230_ oa_lawyer_hub CJK_540D_CJK_5F55_; CJK_5373_CJK_4FBF_CJK_627E_CJK_5230_,
# 8 CJK_6761_CJK_53CD_CJK_76F4_CJK_89C9_CJK_5F8B_CJK_5E08_ profile CJK_4E5F_CJK_9700_CJK_9010_CJK_6761_CJK_6838_CJK_5BF9_), CJK_6545_CJK_5360_CJK_4E3B_CJK_5BFC_CJK_6743_CJK_91CD_ 12/8; agent CJK_5B9E_CJK_6D4B_CJK_4F1A_ PASS CJK_7684_CJK_4E00_CJK_5F8B_ 0.5。
CHECKS = [
    ("s2_precedent_citation", s2_precedent_citation, 0.049),
    ("s2_lawyer_choice_in_notion", s2_lawyer_choice_in_notion, 0.049),
    ("d_statute_in_force", d_statute_in_force, 0.049),
    ("d_reads_lawyer_roster", d_reads_lawyer_roster, 0.78),
    ("d_lawyer_conflict_excluded", d_lawyer_conflict_excluded, 1.17),
    ("d_lawyer_disbarred_excluded", d_lawyer_disbarred_excluded, 1.17),
    ("d_lawyer_wrong_specialty_excluded", d_lawyer_wrong_specialty_excluded, 1.17),
    ("d_lawyer_wrong_jurisdiction_excluded", d_lawyer_wrong_jurisdiction_excluded, 1.17),
    ("d_lawyer_over_budget_excluded", d_lawyer_over_budget_excluded, 1.17),
    ("d_lawyer_contingency_cap", d_lawyer_contingency_cap, 1.17),
    ("d_lawyer_best_pick", d_lawyer_best_pick, 1.17),
    ("d_lawyer_budget_cap", d_lawyer_budget_cap, 0.049),
]
