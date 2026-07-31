"""EmailMockCapability — Terrarium binding for ``servers/email_mock``.

Note: the Python package inside ``servers/email_mock/src/`` is still named
``emails_mcp`` (untouched to avoid editing internal source). Only the external
surface (directory, console script, capability, image) is renamed to
``email_mock`` to align with the other capabilities.
"""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class EmailMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/email_mock:latest"
    SERVER_KEY = "email"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
