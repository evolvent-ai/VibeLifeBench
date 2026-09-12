"""Stage 18 checker: user asks to schedule meetings."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _stage_tools,
    _tool_called_in_stage,
    _calendar_events,
    _flatten_text,
    _any,
)


def s18_created_event(env) -> bool:
    """Stage 18 called create_event AND backend calendar has an agent-added meaningful event
    (client visit, flight, hotel, EVUS, or summit-related)."""
    # 1. Tool trace check
    created = _tool_called_in_stage(env, 18, ["create_event"])

    # 2. Backend state check
    events = _calendar_events(env, "2026-03-15T00:00:00", "2026-04-10T23:59:59")
    agent_added = False
    seen_slots: set[tuple[str, str]] = set()
    duplicate = False
    for ev in events:
        ev_id = str(ev.get("id", ev.get("event_id", ""))).upper()
        if ev_id in ("EV001", "EV_STANDUP"):
            continue
        title = str(ev.get("title", ev.get("summary", ""))).lower()
        if _any(title, [
            "client visit", "client visit",
            "flight", "flight", "departure", "departure", "arrival",
            "hotel", "hotel", "check-in", "checkin",
            "evus", "visa", "passport", "visa",
            "summit", "summit",
        ]):
            start = str(ev.get("start") or ev.get("start_dt") or "")
            slot = (" ".join(title.split()), start)
            if slot in seen_slots:
                duplicate = True
            seen_slots.add(slot)
            agent_added = True

    logger.info(f"s18_created_event: created={created}, agent_added={agent_added}, duplicate={duplicate}")
    return bool(created and agent_added and not duplicate)


CHECKS = [
    ("s18_created_event", s18_created_event, 2.0),
]
