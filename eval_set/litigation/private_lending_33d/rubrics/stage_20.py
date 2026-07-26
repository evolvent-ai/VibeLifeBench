"""Stage 20: 归档 heartbeat — 案件材料/证据/节点在 Notion 归档(side effect)."""
from __future__ import annotations

from ._helpers import _notion_page_text


def s20_archive_in_notion(env) -> bool:
    """案件归档整理进 Notion (含证据/节点/判决结果)。"""
    text = _notion_page_text(env, "民间借贷追偿") or _notion_page_text(env, "归档")
    if text is None:
        return False  # required evidence unavailable → fail closed
    n = sum(1 for k in ["证据", "判决", "本金", "时间线", "开庭", "上诉", "360000"] if k in text)
    return n >= 2


CHECKS = [
    ("s20_archive_in_notion", s20_archive_in_notion, 0.5),
]
