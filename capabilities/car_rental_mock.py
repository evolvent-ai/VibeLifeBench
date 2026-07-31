"""CarRentalMockCapability - Terrarium binding for ``servers/car_rental_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class CarRentalMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/car_rental_mock:latest"
    SERVER_KEY = "car_rental"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
