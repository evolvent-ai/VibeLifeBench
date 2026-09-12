"""Stage 0: establish the minimum durable travel-state skeleton."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import workspace_file_content


def s0_heartbeat_file_created(env) -> bool:
    heartbeat = workspace_file_content(env, "/workspace/HEARTBEAT.md").casefold()
    itinerary = workspace_file_content(env, "/workspace/itinerary.md").casefold()
    risk = workspace_file_content(env, "/workspace/risk_register.md").casefold()
    expense = workspace_file_content(env, "/workspace/expense_summary.md").casefold()
    heartbeat_ok = len(heartbeat.strip()) >= 40 and any(x in heartbeat for x in ("last review", "last review")) and any(x in heartbeat for x in ("next", "next action", "next"))
    itinerary_ok = all(x in itinerary for x in ("2026-06-10", "2026-07-01")) and any(x in itinerary for x in ("option", "tentative", "tentative", "draft"))
    risk_ok = any(x in risk for x in ("zika", "passport", "passport", "pregnan", " pregnancy")) and any(x in risk for x in ("owner", "owner"))
    expense_ok = "45000" in expense.replace(",", "") and any(x in expense for x in ("cny", "CNY")) and any(x in expense for x in ("committed", "committed", "running", "running total"))
    result = bool(heartbeat_ok and itinerary_ok and risk_ok and expense_ok)
    logger.info("s0_durable_skeleton: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s0_heartbeat_file_created", s0_heartbeat_file_created, 1.5)]
