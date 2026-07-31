"""CreditCardMockCapability — Terrarium binding for ``servers/credit_card_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class CreditCardMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/credit_card_mock:latest"
    SERVER_KEY = "credit_card"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
