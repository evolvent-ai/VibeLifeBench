"""Live world access for the trusted evidence collector — capture side only.

This module belongs to the **collector**, which runs during Harbor's verifier
collect phase and freezes the world at each stage boundary. It is the one place
that is *supposed* to touch live state:

* ``getattr(env, f"{server}_mock").call_tool(tool, **kwargs)`` — real MCP reads
  against the running services, used by ``snapshot_capture.py`` to build each
  stage's ``snapshot.json``.
* ``env.workspace.fs`` — a read-only view of the live agent workspace at
  ``/workspace``, captured into the same snapshot.

**Do not confuse this with the scoring side.** ``tests/`` has no adapter at all:
rubrics there read frozen evidence through ``tests/harbor_evidence.py``, which
has no MCP client by construction. Scoring a historical stage against live state
would silently re-score every earlier stage against the *final* world, rewarding
last-turn back-fill and punishing an agent that correctly superseded stale
values. Capture reads the live world; scoring never does.

Anything outside the slice is intentionally absent: a rubric reaching for it
should fail loudly rather than silently score zero.
"""
from __future__ import annotations

import asyncio
import contextlib
import json
import os
from pathlib import Path
from typing import Any

# Ordered: the first existing root wins. /workspace is the live agent workspace
# (present when the verifier shares the main service); the evidence copy is the
# collected snapshot used for offline replay.
DEFAULT_WORKSPACE_ROOT = Path(os.environ.get("HARBOR_WORKSPACE_ROOT", "/workspace"))


def _service_host(server: str) -> str:
    """docker-compose hostnames are the underscore-free capability name."""
    return server.replace("_", "-")


def _unwrap_mcp(result: Any) -> Any:
    """Decode a FastMCP CallToolResult into native Python.

    Mirrors ``capabilities/base.py::_unwrap_mcp`` so the captured snapshot has
    byte-identical shapes to the source capture — the rubrics match on nested
    fields, so a different wrapper shape would fail every check.
    """
    if result is None:
        return None
    sc = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
    if isinstance(sc, dict) and "result" in sc:
        value = sc["result"]
        return json.loads(value) if isinstance(value, str) else value
    for block in getattr(result, "content", None) or []:
        text = getattr(block, "text", None)
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    return result


class _McpCapability:
    """Read-side MCP capability used during trusted collection."""

    def __init__(self, server: str) -> None:
        self.server = server
        host = os.environ.get(f"MCP_HOST_{server.upper()}", _service_host(server))
        port = os.environ.get("MCP_PORT", "8000")
        self.url = f"http://{host}:{port}/mcp"
        self._loop: asyncio.AbstractEventLoop | None = None
        self._stack: contextlib.AsyncExitStack | None = None
        self._session: Any = None

    async def _open_session(self) -> Any:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        stack = contextlib.AsyncExitStack()
        read, write, _meta = await stack.enter_async_context(
            streamablehttp_client(self.url)
        )
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        self._stack = stack
        return session

    async def _close_session(self) -> None:
        stack, self._stack = self._stack, None
        self._session = None
        if stack is not None:
            with contextlib.suppress(Exception):
                await stack.aclose()

    async def _call_async(self, name: str, **kwargs: Any) -> Any:
        if self._session is None:
            self._session = await self._open_session()
        try:
            result = await self._session.call_tool(name, kwargs)
        except BaseException:
            # A poisoned transport would fail every later read; drop the
            # session so the next call starts from a fresh handshake.
            await self._close_session()
            raise
        return _unwrap_mcp(result)

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        """Reuse one initialized session per server across the capture.

        The snapshot freezes dozens of reads per stage; paying a full
        streamablehttp handshake on every call dominated the snapshot budget
        and pushed the collect past its hook timeout. The session therefore
        lives on a per-capability loop that survives between calls.
        """
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
        return self._loop.run_until_complete(self._call_async(name, **kwargs))


class _Fs:
    """Live read-only workspace adapter used only during trusted collection."""

    def __init__(self, workspace_root: Path | str = DEFAULT_WORKSPACE_ROOT) -> None:
        self.workspace_root = Path(workspace_root)

    def _candidate(self, path: str) -> Path:
        raw = str(path).rstrip("/") or "/"
        # Bare "/workspace" must resolve to the root itself. Falling through to
        # the generic branch below would append "workspace/" and silently yield
        # an empty listing — and because the rubrics only ask whether *any*
        # workspace value is non-empty, that produces zero captured evidence
        # instead of an error.
        if raw == "/workspace":
            return self.workspace_root
        if raw.startswith("/workspace/"):
            return self.workspace_root / raw[len("/workspace/") :]
        return self.workspace_root / raw.lstrip("/")

    def read_file(self, path: str) -> bytes:
        candidate = self._candidate(path)
        if not candidate.is_file() or candidate.is_symlink():
            raise FileNotFoundError(path)
        return candidate.read_bytes()

    def exists(self, path: str) -> bool:
        candidate = self._candidate(path)
        return candidate.exists() and not candidate.is_symlink()

    def list_dir(self, path: str) -> list[str]:
        candidate = self._candidate(path)
        if not candidate.is_dir() or candidate.is_symlink():
            return []
        return sorted(child.name for child in candidate.iterdir() if not child.is_symlink())

    def write_file(self, path: str, data: bytes) -> None:
        raise PermissionError("trusted collector workspace view is read-only")


class _Workspace:
    def __init__(self, workspace_root: Path | str = DEFAULT_WORKSPACE_ROOT) -> None:
        self.fs = _Fs(workspace_root)


class HarborEnv:
    """Duck-typed ``env`` exposing ``<server>_mock`` and ``workspace``."""

    def __init__(
        self, servers: list[str], workspace_root: Path | str = DEFAULT_WORKSPACE_ROOT
    ) -> None:
        self.workspace = _Workspace(workspace_root)
        self._caps: dict[str, _McpCapability] = {}
        for server in servers:
            cap = _McpCapability(server)
            self._caps[server] = cap
            setattr(self, f"{server}_mock", cap)

    def capability(self, server: str) -> _McpCapability | None:
        return self._caps.get(server)
