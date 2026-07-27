"""ContentPlatformMockCapability — Terrarium binding for ``servers/content_platform_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class ContentPlatformMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/content_platform_mock:latest"
    SERVER_KEY = "content_platform"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
