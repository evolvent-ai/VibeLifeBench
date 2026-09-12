"""Stage 7: pre-departure checklist - durable itinerary names required items."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _workspace_file_nonempty, _workspace_file_text

def s7_must_list_items(env) -> bool:
    """Persist passport, JPY cash, charger/adapter, and business attire."""
    text = (_workspace_file_text(env, "/workspace/itinerary.md") + "\n" + _workspace_file_text(env, "/workspace/decision_log.md")).lower()
    has_passport = _any(text, ["passport"])
    has_cash = _any(text, ["cash", "jpy"])
    has_charger = _any(text, ["charger", "adapter", "power adapter"])
    has_suit = _any(text, ["suit", "business card", "business attire", "formal attire"])
    ok = has_passport and has_cash and has_charger and has_suit
    logger.info(f"s7_items: passport={has_passport} cash={has_cash} charger={has_charger} suit={has_suit} -> {ok}")
    return ok

def s7_file_exists(env) -> bool:
    ok = _workspace_file_nonempty(env, "/workspace/itinerary.md") or _workspace_file_nonempty(env, "/workspace/decision_log.md")
    logger.info(f"s7_file: {ok}")
    return ok

CHECKS = [
    ("s7_must_list_items", s7_must_list_items, 2.5),
    ("s7_file_exists", s7_file_exists, 1.0),
]
