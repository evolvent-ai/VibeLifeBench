"""BankingMockCapability — Terrarium binding for ``servers/banking_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class BankingMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/banking_mock:latest"
    SERVER_KEY = "banking"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
