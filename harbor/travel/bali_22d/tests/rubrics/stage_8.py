"""Stage 8: bind the 14-day storm outlook to exact dates, arrival risk, and verified backups."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _agent_responses, _tool_call_matches, workspace_file_content


def _state(env) -> str:
    return (workspace_file_content(env, "/workspace/itinerary.md") + "\n" + workspace_file_content(env, "/workspace/risk_register.md") + "\n" + workspace_file_content(env, "/workspace/HEARTBEAT.md")).casefold()


def s8_mother_arrival_conflict(env) -> bool:
    forecast = _tool_call_matches(
        env,
        "weather",
        "get_forecast_daily",
        lambda a: "bali_ubud" in str(a.get("geo") or "").casefold() and int(a.get("days") or 0) >= 14,
        stage=8,
    )
    resp = _agent_responses(env, 8).casefold()
    text = _state(env)
    specific = all(x in (resp + "\n" + text) for x in ("2026-06-20", "2026-06-22")) and any(
        x in (resp + "\n" + text) for x in ("60-90", "storm", "heavy rain", "storm")
    )
    mother = any(x in (resp + "\n" + text) for x in ("liu fang", "mother", "mother")) and any(
        x in (resp + "\n" + text) for x in ("arrival", "arrive", "pickup")
    )
    owned = any(x in text for x in ("owner", "owner")) and any(
        x in text for x in ("next review", "next check", "next check")
    )
    result = bool(forecast and specific and mother and owned)
    logger.info("s8_mother_arrival_conflict: {}", "PASS" if result else "FAIL")
    return result


def s8_indoor_backup_plan(env) -> bool:
    maps_checked = _tool_call_matches(
        env,
        "maps",
        "search_places",
        lambda a: any(x in str(a.get("query") or "").casefold() for x in ("ubud", "indoor", "wellness", "palace", "cafe")),
        stage=8,
    )
    text = _state(env)
    venues = ("ubud royal palace", "the yoga barn", "como shambhala", "cafe pomegranate", "locavore")
    named = sum(1 for venue in venues if venue in text) >= 2
    dated = "2026-06-20" in text and "2026-06-22" in text
    statuses = any(x in text for x in ("backup", "backup", "option")) and any(
        x in text for x in ("weather trigger", "if rain", "storm", "trigger")
    )
    result = bool(maps_checked and named and dated and statuses)
    logger.info("s8_indoor_backup_plan: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [
    ("s8_mother_arrival_conflict", s8_mother_arrival_conflict, 2.0),
    ("s8_indoor_backup_plan", s8_indoor_backup_plan, 1.5),
]
