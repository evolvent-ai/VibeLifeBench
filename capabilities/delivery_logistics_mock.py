"""DeliveryLogisticsMockCapability — Terrarium binding for ``servers/delivery_logistics_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class DeliveryLogisticsMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/delivery_logistics_mock:latest"
    SERVER_KEY = "delivery_logistics"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
