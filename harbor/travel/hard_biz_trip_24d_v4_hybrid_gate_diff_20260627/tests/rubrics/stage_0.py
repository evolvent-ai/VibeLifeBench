"""Stage 0: startup - create durable Notion and workspace control records."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _agent_used_tool, _notion_text, _workspace_file_text, _workspace_file_nonempty, OUTPUT_PATHS

def s0_notion_created(env) -> bool:
    notion = _notion_text(env).lower()
    has_title = _any(notion, ["tokyo business trip 2026", "journal", "tokyo"])
    has_operational_sections = all(_any(notion, [kw]) for kw in ["flight", "hotel", "budget"]) or all(
        _any(notion, [kw]) for kw in ["flight", "hotel", "budget"]
    )
    wrote_notion = _agent_used_tool(env, "notion", "API-post-page", stage=0) or _agent_used_tool(env, "notion", "API-patch-block-children", stage=0)
    ok = wrote_notion and len(notion.strip()) > 80 and has_title and has_operational_sections
    logger.info(f"s0_notion: title={has_title} sections={has_operational_sections} -> {ok}")
    return ok

def s0_must_mention_four(env) -> bool:
    """Durable startup records cover journal, flight, hotel, and budget."""
    ws_text = (
        _workspace_file_text(env, "/workspace/decision_log.md") + "\n" +
        _workspace_file_text(env, "/workspace/risk_register.md") + "\n" +
        _workspace_file_text(env, "/workspace/budget.md")
    ).lower()
    has_journal = _any(ws_text, ["journal", "notion", "tokyo"])
    has_flight = _any(ws_text, ["flight", "flight ticket", "pvg", "nrt"])
    has_hotel = _any(ws_text, ["hotel", "accommodation", "roppongi"])
    has_budget = _any(ws_text, ["budget", "expense", "cny", "jpy"])
    has_persistence_plan = all(_any(ws_text, [name]) for name in ["itinerary", "decision", "risk", "budget"])
    scaffold_count = sum(1 for path in OUTPUT_PATHS if _workspace_file_nonempty(env, path))
    ok = has_journal and has_flight and has_hotel and has_budget and has_persistence_plan and scaffold_count >= 4
    logger.info(f"s0_four: journal={has_journal} flight={has_flight} hotel={has_hotel} budget={has_budget} persist={has_persistence_plan} scaffolds={scaffold_count} -> {ok}")
    return ok

CHECKS = [
    ("s0_notion_created", s0_notion_created, 1.5),
    ("s0_must_mention_four", s0_must_mention_four, 2.0),
]
