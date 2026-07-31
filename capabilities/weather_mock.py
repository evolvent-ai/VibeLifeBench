"""WeatherMockCapability — Terrarium binding for ``servers/weather_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class WeatherMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/weather_mock:latest"
    SERVER_KEY = "weather"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
