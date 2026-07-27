"""MapsMockCapability — Terrarium binding for ``servers/maps_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class MapsMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/maps_mock:latest"
    SERVER_KEY = "maps"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
