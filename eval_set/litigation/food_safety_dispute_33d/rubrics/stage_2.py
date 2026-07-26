"""Stage 2: 选聘食品检验机构(场景约束矩阵) — 逐条排除6家陷阱机构, 锁定最优, 守检验费预算硬顶.

场景约束型难度核心: agent 须真读检验机构名录(JY-001~008)、对照赵萌约束逐条核对、
排除利益关联/范围不含或外地/无CMA资质/浮动收费保检出/超预算套餐/被暂停资质, 锁定 JY-006, 守住 ¥3000 预算。
同时顺带读最贴近判例(s2_precedent_citation / d_statute_in_force)。

权重哲学(见 house_sale_dispute_33d): 检验机构选聘矩阵(8 个 d_ + 读名录)是场景约束型 reliable-fail——
跨 run 稳定失败(强模型常猜 user_id `zhao_meng` 而非 `usr_zhao_meng`, 找不到 oa_jianyan_hub 名录;
即便找到, 8 条反直觉 profile 也需逐条核对), 故占主导权重 8-12; agent 实测会 PASS 的一律 0.5。
"""
from __future__ import annotations

from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import (
    d_reads_inspect_roster, d_inspect_conflict_excluded, d_inspect_wrong_scope_excluded,
    d_inspect_no_cma_excluded, d_inspect_contingent_fee_excluded,
    d_inspect_over_budget_excluded, d_inspect_suspended_excluded, d_inspect_best_pick,
    d_inspect_budget_cap, d_statute_in_force,
)


def s2_precedent_citation(env) -> bool:
    """引用最贴近判例 case_f02 (进口无中文标签退一赔十) 的裁判要旨/结果。"""
    text = _stage_corpus(env, 2)
    has_case = any(k in text for k in ["case_f02", "无中文标签", "进口食品无中文", "(2025)沪0112民初18900"])
    has_holding = any(k in text for k in ["退一赔十", "价款十倍", "十倍赔偿", "不符合食品安全标准", "裁判要旨"])
    return has_case and has_holding


def s2_inspect_choice_in_notion(env) -> bool:
    """场景约束·执行: 选定的检验机构(及理由/收费)须记入 Notion, 不能只口头。"""
    text = _notion_page_text(env, "检验") or _notion_page_text(env, "食品安全维权")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["检验", "JY-006", "沪正", "检验机构", "检验报告", "检验费", "CMA"])


CHECKS = [
    ("d_reads_inspect_roster", d_reads_inspect_roster, 0.733),
    ("d_inspect_conflict_excluded", d_inspect_conflict_excluded, 1.099),
    ("d_inspect_wrong_scope_excluded", d_inspect_wrong_scope_excluded, 1.099),
    ("d_inspect_no_cma_excluded", d_inspect_no_cma_excluded, 1.099),
    ("d_inspect_contingent_fee_excluded", d_inspect_contingent_fee_excluded, 1.099),
    ("d_inspect_over_budget_excluded", d_inspect_over_budget_excluded, 1.099),
    ("d_inspect_suspended_excluded", d_inspect_suspended_excluded, 1.099),
    ("d_inspect_best_pick", d_inspect_best_pick, 1.099),
    ("d_inspect_budget_cap", d_inspect_budget_cap, 0.046),
]
