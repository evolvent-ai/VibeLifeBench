"""HealthTrackerMockCapability — Terrarium binding for ``servers/health_tracker_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class HealthTrackerMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/health_tracker_mock:latest"
    SERVER_KEY = "health_tracker"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
