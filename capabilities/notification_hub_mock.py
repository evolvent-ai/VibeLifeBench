"""NotificationHubMockCapability — Terrarium binding for ``servers/notification_hub_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class NotificationHubMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/notification_hub_mock:latest"
    SERVER_KEY = "notification_hub"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
