"""Stage 15: 庭后小结进 Notion — 争点/主张/依据(side effect)."""
from __future__ import annotations

from ._helpers import _journal_text, _notion_page_text


def s15_summary_in_notion(env) -> bool:
    """庭后小结写进 Notion (side effect)。"""
    text = _notion_page_text(env, "庭后") or _notion_page_text(env, "民间借贷追偿")
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(k in text for k in ["争点", "庭后", "质证", "主张", "依据", "本金", "砍头息"])


def s15_captures_arguments(env) -> bool:
    """庭后台账须同时覆盖双方主张、证据争议和下一程序。"""
    text = _journal_text(env)
    if not text:
        return False
    has_plaintiff = any(token in text for token in ("我方主张", "王芳主张", "原告主张"))
    has_defendant = any(token in text for token in ("陈强抗辩", "对方抗辩", "被告抗辩"))
    has_issue = sum(token in text for token in ("砍头息", "现金交付", "夫妻共同债务", "担保", "实际本金")) >= 2
    has_evidence = sum(token in text for token in ("银行流水", "借条", "催款记录", "微信", "质证")) >= 2
    has_next = any(token in text for token in ("等待法院判决", "等待判决", "判决待送达", "质证结论"))
    return has_plaintiff and has_defendant and has_issue and has_evidence and has_next


CHECKS = [
    ("s15_summary_in_notion", s15_summary_in_notion, 0.5),
    ("s15_captures_arguments", s15_captures_arguments, 0.5),
]
