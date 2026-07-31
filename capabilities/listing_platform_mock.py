"""ListingPlatformMockCapability — Terrarium binding for ``servers/listing_platform_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class ListingPlatformMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/listing_platform_mock:latest"
    SERVER_KEY = "listing_platform"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
