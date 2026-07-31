"""BrokerageMockCapability — Terrarium binding for ``servers/brokerage_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class BrokerageMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/brokerage_mock:latest"
    SERVER_KEY = "brokerage"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
