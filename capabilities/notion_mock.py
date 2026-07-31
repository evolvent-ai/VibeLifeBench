"""NotionMockCapability — Terrarium binding for ``servers/notion_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class NotionMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/notion_mock:latest"
    SERVER_KEY = "notion"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
