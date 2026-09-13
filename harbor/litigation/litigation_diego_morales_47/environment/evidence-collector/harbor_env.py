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
import json
import os
import threading
from contextlib import AsyncExitStack
from datetime import timedelta
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


_CALL_CONNECT_TIMEOUT = 10.0
_CALL_READ_TIMEOUT = timedelta(seconds=20)
_CALL_FUTURE_TIMEOUT = 40.0


class _McpSessionHost:
    """One long-lived MCP session on a private event-loop thread.

    A stage-boundary capture issues hundreds of single-round-trip reads inside
    Harbor's 60s collect-hook budget. Opening a streamable-HTTP session (TCP
    connect + initialize handshake) per call costs ~60ms each, which alone
    blows the budget once the Notion block fan-out reaches ~200 calls. Hosting
    one session and issuing every call over it keeps per-call cost at a single
    round trip; the session is shared across captures and rebuilt on failure,
    because it may go stale while the collector sits idle between boundaries.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self._loop = asyncio.new_event_loop()
        self._ready = threading.Event()
        self._thread = threading.Thread(
            target=self._run_loop, name=f"mcp-capture:{url}", daemon=True
        )
        self._stack: AsyncExitStack | None = None
        self._session: Any = None
        self._reset_lock = asyncio.Lock()
        self._thread.start()
        self._ready.wait()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._ready.set()
        self._loop.run_forever()

    async def _connect(self) -> None:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        # Every call is bounded: a hung connection must fail fast (into an
        # error envelope) instead of eating the whole hook timeout.
        self._stack = AsyncExitStack()
        try:
            read, write, _meta = await self._stack.enter_async_context(
                streamablehttp_client(self.url, timeout=_CALL_CONNECT_TIMEOUT)
            )
            self._session = await self._stack.enter_async_context(
                ClientSession(read, write, read_timeout_seconds=_CALL_READ_TIMEOUT)
            )
            await self._session.initialize()
        except BaseException:
            await self._disconnect()
            raise

    async def _disconnect(self) -> None:
        stack, self._stack, self._session = self._stack, None, None
        if stack is not None:
            await stack.aclose()

    async def _call_with_retry(self, name: str, kwargs: dict[str, Any]) -> Any:
        await self._ensure_connected()
        try:
            result = await self._session.call_tool(name, kwargs)
        except BaseException:
            # Stale or broken session (idle between stage boundaries, service
            # restart): rebuild once on this loop and retry before giving up.
            async with self._reset_lock:
                await self._disconnect()
                await self._connect()
            result = await self._session.call_tool(name, kwargs)
        return _unwrap_mcp(result)

    async def _ensure_connected(self) -> None:
        if self._session is None:
            await self._connect()

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        coroutine = self._call_with_retry(name, kwargs)
        future = asyncio.run_coroutine_threadsafe(coroutine, self._loop)
        return future.result(timeout=_CALL_FUTURE_TIMEOUT)


_SESSION_HOSTS: dict[tuple[str, str], "_McpSessionHost"] = {}
_SESSION_HOSTS_LOCK = threading.Lock()


def _session_host(server: str, url: str) -> _McpSessionHost:
    key = (server, url)
    with _SESSION_HOSTS_LOCK:
        host = _SESSION_HOSTS.get(key)
        if host is None:
            host = _SESSION_HOSTS[key] = _McpSessionHost(url)
        return host


class _McpCapability:
    """Read-side MCP capability used during trusted collection."""

    def __init__(self, server: str) -> None:
        self.server = server
        host = os.environ.get(f"MCP_HOST_{server.upper()}", _service_host(server))
        port = os.environ.get("MCP_PORT", "8000")
        self.url = f"http://{host}:{port}/mcp"

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        return _session_host(self.server, self.url).call_tool(name, **kwargs)


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
