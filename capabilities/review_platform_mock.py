"""ReviewPlatformMockCapability — Terrarium binding for ``servers/review_platform_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class ReviewPlatformMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/review_platform_mock:latest"
    SERVER_KEY = "review_platform"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
