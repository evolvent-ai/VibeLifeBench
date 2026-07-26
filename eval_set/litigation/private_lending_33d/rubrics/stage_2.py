"""Stage 2: 选聘律师(场景约束矩阵) — 逐条排除6个陷阱律师, 锁定最优, 守预付预算硬顶.

场景约束型难度核心: agent 须真读律师名录(LD-001~008)、对照王芳约束逐条核对、
排除利益冲突/吊证/专业不符/异地/超预算/超上限, 锁定 LD-006, 守住 ¥8000 预付预算。
同时顺带读最贴近判例(s2_precedent_citation / d_statute_in_force)。
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
    """判例要旨、当前案件适用和下一步必须持久化。"""
    text = _journal_text(env)
    if not text:
        return False
    has_case = any(token in text for token in ("case_001", "2025浙0106民初13201", "砍头息"))
    has_holding = (
        any(token in text for token in ("实际到账", "实际出借", "实际本金"))
        and any(token in text for token in ("36万元", "36万", "360000"))
    )
    has_application = (
        "王芳" in text
        and "陈强" in text
        and any(token in text for token in ("核算本金", "利息上限", "诉请", "下一步"))
    )
    return has_case and has_holding and has_application


def s2_lawyer_choice_in_notion(env) -> bool:
    """场景约束·执行: 选定的律师(及理由/收费)须记入 Notion, 不能只口头。"""
    text = _notion_page_text(env, "律师") or _notion_page_text(env, "民间借贷追偿")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["律师", "LD-006", "周敏", "委托", "风险代理", "代理"])


# 权重哲学: 律师选聘矩阵(评估 d_ + 读名录)是场景约束型 reliable-fail——跨 run 稳定失败
# (强模型常猜 user_id `wangfang` 而非 `usr_wang_fang`, 找不到 oa_lawyer_hub 名录; 即便找到,
# 8 条反直觉律师 profile 也需逐条核对), 故占主导权重 12/8; agent 实测会 PASS 的一律 0.5。
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
