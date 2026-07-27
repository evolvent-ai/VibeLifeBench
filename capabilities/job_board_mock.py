"""JobBoardMockCapability — Terrarium binding for ``servers/job_board_mock``."""
from __future__ import annotations

from capabilities.base import AgentMockServerCapability


class JobBoardMockCapability(AgentMockServerCapability):
    IMAGE = "vibe-agent-benchmark/job_board_mock:latest"
    SERVER_KEY = "job_board"
    MCP_PORT = 8000
    DEFAULT_ENV = "empty"
