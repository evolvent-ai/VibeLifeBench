"""CalendarMockCapability — Terrarium binding for ``servers/calendar_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class CalendarMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/calendar_mock:latest"
    SERVER_KEY = "calendar"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
