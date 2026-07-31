"""FlightBookingMockCapability — Terrarium binding for ``servers/flight_booking_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class FlightBookingMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/flight_booking_mock:latest"
    SERVER_KEY = "flight_booking"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
