"""Stage 0: kickoff — 建 Notion 追偿页、关注公众号、读已收藏判例."""
from __future__ import annotations

from ._helpers import _journal_text, _stage_corpus, _notion_page_text, _saved_case_ids


def s0_notion_page(env) -> bool:
    """追偿 Notion 页面存在 (side effect)。"""
    text = _notion_page_text(env, "民间借贷追偿") or _notion_page_text(env, "追偿") or _notion_page_text(env, "借贷")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["民间借贷", "追偿", "借款", "陈强", "借条"])


def s0_reads_saved_cases(env) -> bool:
    """收藏判例必须被读取并应用到王芳案件台账。"""
    ids = _saved_case_ids(env)
    if not ids or "case_001" not in ids:
        return False
    response = _stage_corpus(env, 0)
    journal = _journal_text(env)
    if not response or not journal:
        return False
    has_read_trace = (
        "case_001" in response
        and any(token in response for token in ("case_009", "收藏", "判例"))
    )
    has_application = (
        any(token in journal for token in ("case_001", "2025浙0106民初13201", "砍头息"))
        and "王芳" in journal
        and "陈强" in journal
        and any(token in journal for token in ("36万元", "36万", "实际到账", "实际本金"))
        and any(token in journal for token in ("下一步", "核算本金", "诉请", "利息上限"))
    )
    return has_read_trace and has_application


CHECKS = [
    ("s0_notion_page", s0_notion_page, 0.5),
    ("s0_reads_saved_cases", s0_reads_saved_cases, 0.5),
]
