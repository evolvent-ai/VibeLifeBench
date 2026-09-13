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
    """Read-side MCP capability used during trusted collection.

    One stage snapshot issues a few hundred sequential tool calls (per-message
    email detail alone is two calls per message across a 75-message INBOX).
    Opening a fresh streamable-HTTP connection plus MCP handshake for every
    call pushes a single snapshot well past Harbor's 60s collect-hook ceiling,
    so the ``ClientSession`` is opened once per server on a private event loop
    and reused for the whole capture. A call that fails at the transport level
    (stale/idle-closed session) reconnects once and retries before surfacing
    the error to the caller.
    """

    CONNECT_TIMEOUT_SEC = 15.0
    CALL_TIMEOUT_SEC = 20.0

    def __init__(self, server: str) -> None:
        self.server = server
        host = os.environ.get(f"MCP_HOST_{server.upper()}", _service_host(server))
        port = os.environ.get("MCP_PORT", "8000")
        self.url = f"http://{host}:{port}/mcp"
        self._lock = threading.Lock()
        self._state: dict[str, Any] | None = None

    async def _session_keeper(self, state: dict[str, Any]) -> None:
        """Hold one initialized ClientSession open until ``close`` is set."""
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        close_event = asyncio.Event()
        state["close"] = close_event
        try:
            async with streamablehttp_client(self.url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await asyncio.wait_for(session.initialize(), self.CONNECT_TIMEOUT_SEC)
                    state["session"] = session
                    state["ready"].set()
                    await close_event.wait()
        except BaseException:
            state["session"] = None
            state["ready"].set()
            raise

    def _run_loop(self, state: dict[str, Any]) -> None:
        loop = asyncio.new_event_loop()
        state["loop"] = loop
        try:
            loop.run_until_complete(self._session_keeper(state))
        except BaseException:
            state["session"] = None
            state["ready"].set()
        finally:
            loop.close()

    def _ensure_session(self) -> Any:
        state = self._state
        if state is not None and state.get("session") is not None:
            return state["session"]
        if self._state is not None:
            self._discard_session()
        state: dict[str, Any] = {
            "ready": threading.Event(),
            "session": None,
            "loop": None,
            "close": None,
        }
        self._state = state
        threading.Thread(
            target=self._run_loop,
            args=(state,),
            daemon=True,
            name=f"mcp-capture-{self.server}",
        ).start()
        if not state["ready"].wait(self.CONNECT_TIMEOUT_SEC):
            raise TimeoutError(
                f"MCP session for {self.server} did not initialize "
                f"within {self.CONNECT_TIMEOUT_SEC}s"
            )
        session = state.get("session")
        if session is None:
            raise RuntimeError(f"MCP session for {self.server} failed to initialize")
        return session

    def _discard_session(self) -> None:
        state, self._state = self._state, None
        if state is None:
            return
        loop, close = state.get("loop"), state.get("close")
        if loop is not None and close is not None and not loop.is_closed():
            try:
                loop.call_soon_threadsafe(close.set)
            except RuntimeError:
                pass  # loop already torn down; the daemon thread exits alone

    def _call_once(self, session: Any, name: str, kwargs: dict[str, Any]) -> Any:
        loop = self._state["loop"]
        future = asyncio.run_coroutine_threadsafe(session.call_tool(name, kwargs), loop)
        return _unwrap_mcp(future.result(self.CALL_TIMEOUT_SEC))

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        with self._lock:
            try:
                return self._call_once(self._ensure_session(), name, kwargs)
            except BaseException:
                # Transport-level failure (idle-closed session, reset link).
                # Reconnect once so one stale connection cannot zero out the
                # rest of the snapshot.
                self._discard_session()
                return self._call_once(self._ensure_session(), name, kwargs)


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
