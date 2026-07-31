"""Stage 15: 庭后小结 — 争点、主张、依据和抗辩回应须持久化。"""
from __future__ import annotations

from ._helpers import _food_journal_text


def s15_post_hearing_notion(env) -> bool:
    text = _food_journal_text(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_context = any(key in text for key in ("庭后", "庭审小结", "开庭小结"))
    has_issues = any(key in text for key in ("争点", "焦点"))
    has_claim = any(key in text for key in ("我方主张", "原告主张", "诉讼请求"))
    has_basis = any(key in text for key in ("依据", "食品安全法", "判例"))
    has_response = any(key in text for key in ("抗辩回应", "质证", "反驳"))
    return has_context and has_issues and has_claim and has_basis and has_response


CHECKS = [
    ("s15_persisted_post_hearing_summary", s15_post_hearing_notion, 0.75),
]
