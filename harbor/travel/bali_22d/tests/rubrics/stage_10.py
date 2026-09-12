"""Stage 10: Level-2 wording must be backed by the live alert and a monitoring trigger."""
from __future__ import annotations

import re

from loguru import logger

from .shared._helpers import _agent_responses, _call, _tool_call_matches, workspace_file_content


def _claims_current_level_3(text: str) -> bool:
    text = text.casefold()
    patterns = (
        r"\b(?:now|currently|current alert(?: level)?(?: is)?|alert(?: level)? is)\s+(?:at\s+)?(?:level\s*3|siaga)\b",
        r"\bmount agung is\s+(?:now\s+|currently\s+)?(?:at\s+)?(?:level\s*3|siaga)\b",
        r"\b(?:level\s*3|siaga)\b\s+(?:is\s+)?(?:now|current|active|in effect)\b",
        r"\b(?:raised|upgraded|moved|changed)\s+to\s+(?:level\s*3|siaga)\b",
    )
    return any(re.search(pattern, text) for pattern in patterns)


def s10_volcano_level_correct(env) -> bool:
    checked = _tool_call_matches(
        env,
        "weather",
        "get_alerts",
        lambda a: "bali_kintamani" in str(a.get("geo") or "").casefold(),
        stage=10,
    )
    alerts = _call(env, "weather", "get_alerts", geo="bali_kintamani")
    backend = str(alerts).casefold()
    resp = _agent_responses(env, 10).casefold()
    risk = (workspace_file_content(env, "/workspace/risk_register.md") + "\n" + workspace_file_content(env, "/workspace/HEARTBEAT.md")).casefold()
    exact = "alert_volcano_l2" in backend and "level 2" in backend and "4km" in backend.replace(" ", "")
    communicated = any(x in resp for x in ("level 2", "waspada")) and not _claims_current_level_3(resp)
    monitor = "agung" in risk and any(x in risk for x in ("level 2", "waspada", "level 2")) and any(
        x in risk for x in ("next review", "next check", "next check")
    ) and any(x in risk for x in ("level 3", "siaga", "airport closure", "closed"))
    result = bool(checked and exact and communicated and monitor)
    logger.info("s10_volcano_level_correct: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s10_volcano_level_correct", s10_volcano_level_correct, 2.0)]
