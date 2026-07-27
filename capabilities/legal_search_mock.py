"""LegalSearchMockCapability — Terrarium binding for ``servers/legal_search_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class LegalSearchMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/legal_search_mock:latest"
    SERVER_KEY = "legal_search"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
