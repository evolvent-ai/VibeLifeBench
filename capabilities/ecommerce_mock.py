"""EcommerceMockCapability — Terrarium binding for ``servers/ecommerce_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class EcommerceMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/ecommerce_mock:latest"
    SERVER_KEY = "ecommerce"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
