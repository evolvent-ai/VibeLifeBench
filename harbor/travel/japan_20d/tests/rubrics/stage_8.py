"""Stage 8 rubric — weather monitoring + durable follow-up state (D8)."""
from __future__ import annotations


from .shared._helpers import _all_corpus, _any_kw, _workspace_file_text

from loguru import logger


def _heartbeat_text(env) -> str:
    return _workspace_file_text(env, "/workspace/HEARTBEAT.md")


def s8_persistent_followup_recorded(env) -> bool:
    """Agent recorded future checks in Notion/workspace instead of cron."""
    text = (_all_corpus(env) + "\n" + _heartbeat_text(env)).lower()
    if not text.strip():
        logger.info("s8 follow-up: no corpus — FAIL")
        return False
    topic_groups = [
        ["weather", "typhoon", "rain", "aqi"],
        ["visa", "passport", "rfi", "decision"],
        ["doctor", "insulin", "medical", "packing"],
        ["check-in", "flight status", "gate", "departure"],
    ]
    topic_hits = sum(1 for group in topic_groups if _any_kw(text, group))
    has_time_anchor = _any_kw(
        text,
        ["2026-04", "2026-05", "d-", "stage", "daily", "before", "by ", "due"],
    )
    if topic_hits >= 2 and has_time_anchor:
        logger.info(f"s8 follow-up: PASS — topic_hits={topic_hits}")
        return True
    logger.info(
        f"s8 follow-up: FAIL — topic_hits={topic_hits}, time_anchor={has_time_anchor}"
    )
    return False


def s8_heartbeat_established(env) -> bool:
    """Agent has a non-trivial HEARTBEAT.md in /workspace by stage 8."""
    text = _heartbeat_text(env)
    if not text:
        logger.info("s8 heartbeat: FAIL — file missing")
        return False
    meaningful = [ln for ln in text.splitlines()
                  if ln.strip() and not ln.strip().startswith("#")]
    if len(meaningful) >= 2:
        logger.info(f"s8 heartbeat: PASS — {len(meaningful)} meaningful lines")
        return True
    logger.info("s8 heartbeat: FAIL — no non-empty HEARTBEAT.md by s8")
    return False


CHECKS = [
    ("s8_persistent_followup_recorded", s8_persistent_followup_recorded, 1),
    ("s8_heartbeat_established",        s8_heartbeat_established,        1.5),
]
