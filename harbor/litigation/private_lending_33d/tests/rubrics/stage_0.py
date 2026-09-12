"""Stage 0: kickoff - create a Notion recovery page, follow official feeds, and read saved cases."""
from __future__ import annotations

from ._helpers import _journal_text, _stage_corpus, _notion_page_text, _saved_case_ids


def s0_notion_page(env) -> bool:
    """A recovery page exists in the frozen Notion evidence (side effect)."""
    # Search the expected title first; the empty-query fallback also handles
    # legacy seeded pages whose title was encoded before the English migration.
    text = (
        _notion_page_text(env, "private lending recovery")
        or _notion_page_text(env, "recovery")
        or _notion_page_text(env, "loan")
        or _notion_page_text(env, "")
    )
    if text is None:
        return False  # required evidence unavailable → fail closed
    return any(
        k.lower() in text.lower()
        for k in ("private lending", "private-lending", "recovery", "Chen Qiang", "IOU")
    )


def s0_reads_saved_cases(env) -> bool:
    """Saved cases are read and applied to Wang Fang's case journal."""
    ids = _saved_case_ids(env)
    if not ids or "case_001" not in ids:
        return False
    response = _stage_corpus(env, 0)
    journal = _journal_text(env)
    if not response or not journal:
        return False
    has_read_trace = (
        "case_001" in response
        and any(token.lower() in response.lower() for token in ("case_009", "saved", "case"))
    )
    has_application = (
        any(token in journal for token in ("case_001", "2025-0106-13201", "principal", "actual principal"))
        and "Wang Fang" in journal
        and "Chen Qiang" in journal
        and any(token in journal for token in ("360,000", "360000", "actual transfer", "actual transferred principal"))
        and any(token.lower() in journal.lower() for token in ("next step", "calculate principal", "claim", "interest cap"))
    )
    return has_read_trace and has_application


CHECKS = [
    ("s0_notion_page", s0_notion_page, 0.5),
    ("s0_reads_saved_cases", s0_reads_saved_cases, 0.5),
]
