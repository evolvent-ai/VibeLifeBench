"""Stage 0: kickoff — 建 Notion 维权页、读已收藏判例、从邮件拼出案情。"""
from __future__ import annotations

from ._helpers import _food_journal_text, _notion_page_text, _saved_case_ids


def s0_notion_page(env) -> bool:
    """建/可见「食品安全维权」Notion 页(s0 mutation 注入 + agent 补充)。"""
    text = _notion_page_text(env, "食品安全维权") or _notion_page_text(env, "食品")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["食品安全", "维权", "退一赔十", "中文标签", "进口"])


def s0_reads_saved(env) -> bool:
    """读已收藏判例(赵萌收藏了 case_f02/case_f07)。"""
    ids = _saved_case_ids(env)
    if ids is None:
        return False  # required evidence unavailable → fail closed
    return len(ids) >= 1


def s0_grasps_facts(env) -> bool:
    """完整案情必须进入案件台账，回复中复述不计分。"""
    text = _food_journal_text(env)
    if not text:
        return False
    groups = (
        ("环球优选", "卖家"),
        ("优鲜购", "平台"),
        ("奶粉",),
        ("无中文标签", "没有中文标签"),
        ("养生茶", "代用茶"),
        ("宣称", "降糖", "降血压", "非法添加"),
        ("1880", "1,880"),
        ("680",),
        ("1200", "1,200"),
        ("就医", "急诊", "320"),
    )
    return all(any(token in text for token in group) for group in groups)


CHECKS = [
    ("s0_grasps_facts", s0_grasps_facts, 0.5),
]
