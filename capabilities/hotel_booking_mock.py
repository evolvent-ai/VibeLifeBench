"""HotelBookingMockCapability — Terrarium binding for ``servers/hotel_booking_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class HotelBookingMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/hotel_booking_mock:latest"
    SERVER_KEY = "hotel_booking"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
