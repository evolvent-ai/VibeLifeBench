"""VisaAndAdvisoryMockCapability — Terrarium binding for ``servers/visa_and_advisory_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class VisaAndAdvisoryMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/visa_and_advisory_mock:latest"
    SERVER_KEY = "visa_and_advisory"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
