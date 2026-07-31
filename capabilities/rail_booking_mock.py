"""RailBookingMockCapability - Terrarium binding for ``servers/rail_booking_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class RailBookingMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/rail_booking_mock:latest"
    SERVER_KEY = "rail_booking"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
