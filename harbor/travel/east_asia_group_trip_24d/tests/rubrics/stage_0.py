"""Stage 0 gate: create the Notion journal and record traveler constraints."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _agent_used_tool,
    _notion_page_count,
    _notion_text,
    _workspace_file_text,
    _any,
    _stage_corpus,
)


def s0_gate(env) -> bool:
    """Call API-post-page and persist the journal plus all traveler constraints."""
    used_notion_page = _agent_used_tool(env, "notion", "API-post-page", stage=0)

    # The backend must contain the requested journal page.
    notion = _notion_text(env).lower()
    has_journal = _any(notion, ["journal", "east asia group trip"])

    # 🗄 page count ≥ 1
    page_exists = _notion_page_count(env) >= 1
    from ._helpers import _notion_block_count
    block_ok = _notion_block_count(env) >= 5

    # profiles.md must contain all key traveler information.
    profiles = _workspace_file_text(env, "/workspace/profiles.md").lower()
    has_people = (
        "li ting" in profiles
        and "wang hao" in profiles
        and "zhao" in profiles
    )
    # Zhao Min joins only the Tokyo segment.
    has_zhao_trip = _any(profiles, ["tokyo", "only tokyo", "skip seoul", "does not travel to seoul"])
    has_bp = _any(profiles, ["hypertension", "blood pressure"])
    has_passport = _any(profiles, ["passport", "validity", "expires"])

    ok = (
        used_notion_page and (has_journal and page_exists and block_ok)
        and has_people
        and has_zhao_trip
        and has_bp
        and has_passport
    )
    logger.info(
        f"s0_gate: notion_page={used_notion_page} journal={has_journal} "
        f"people={has_people} zhao_trip={has_zhao_trip} bp={has_bp} passport={has_passport} "
        f"→ {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [("s0_gate", s0_gate, 1.5)]
