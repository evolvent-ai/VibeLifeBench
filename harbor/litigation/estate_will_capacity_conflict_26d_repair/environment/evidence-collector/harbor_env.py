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
from concurrent.futures import TimeoutError as _FutureTimeout
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

    One stage snapshot issues hundreds of sequential tool calls against the
    same servers. Opening a fresh streamable-http transport and session per
    call costs three HTTP round trips each, which used to push the snapshot
    collect hook past its timeout budget, so a single session per server is
    opened on a private event-loop thread and shared by every call. A per-call
    timeout plus one reconnect-and-retry keeps a wedged transport from hanging
    the collect hook: a dead call surfaces as an error entry inside the
    snapshot instead of an infrastructure timeout, and every captured tool is
    a read, so the single retry cannot double-apply a mutation.
    """

    _CONNECT_TIMEOUT = float(os.environ.get("SNAPSHOT_MCP_CONNECT_TIMEOUT", "60"))
    _CALL_TIMEOUT = float(os.environ.get("SNAPSHOT_MCP_CALL_TIMEOUT", "120"))

    def __init__(self, server: str) -> None:
        self.server = server
        host = os.environ.get(f"MCP_HOST_{server.upper()}", _service_host(server))
        port = os.environ.get("MCP_PORT", "8000")
        self.url = f"http://{host}:{port}/mcp"
        self._lock = threading.Lock()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._session: Any = None
        self._contexts: tuple[Any, ...] = ()

    # -- session lifecycle ------------------------------------------------
    def _ensure_loop(self) -> asyncio.AbstractEventLoop:
        # httpx/anyio transports are bound to the loop that opened them, so
        # every call must run on one long-lived loop instead of the throwaway
        # loop asyncio.run() would create per call.
        if self._loop is None:
            loop = asyncio.new_event_loop()
            threading.Thread(
                target=loop.run_forever,
                name=f"mcp-capture-{self.server}",
                daemon=True,
            ).start()
            self._loop = loop
        return self._loop

    async def _open_session(self) -> Any:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        try:
            transport_cm = streamablehttp_client(
                self.url, httpx_client_factory=self._http_client_factory
            )
        except TypeError:
            # Older mcp without the factory hook; container-level NO_PROXY
            # then remains the only proxy guard.
            transport_cm = streamablehttp_client(self.url)
        read, write, _meta = await asyncio.wait_for(
            transport_cm.__aenter__(), self._CONNECT_TIMEOUT
        )
        session_cm = ClientSession(read, write)
        session = await session_cm.__aenter__()
        try:
            await asyncio.wait_for(session.initialize(), self._CONNECT_TIMEOUT)
        except BaseException:
            await self._close_contexts((transport_cm, session_cm))
            raise
        self._contexts = (transport_cm, session_cm)
        return session

    @staticmethod
    def _http_client_factory(**factory_kwargs: Any) -> Any:
        # The mocks live on the compose network; never route them through an
        # ambient HTTP proxy even when the container exports one.
        import httpx

        factory_kwargs.setdefault("trust_env", False)
        # Mirror mcp's default factory so only proxy handling differs.
        factory_kwargs.setdefault("follow_redirects", True)
        return httpx.AsyncClient(**factory_kwargs)

    async def _close_contexts(self, contexts: tuple[Any, ...]) -> None:
        for context in reversed(contexts):
            try:
                await asyncio.wait_for(context.__aexit__(None, None, None), 10)
            except BaseException:  # noqa: BLE001 - best-effort teardown
                pass

    def _ensure_session(self) -> Any:
        with self._lock:
            if self._session is not None:
                return self._session
            loop = self._ensure_loop()
            session = asyncio.run_coroutine_threadsafe(
                self._open_session(), loop
            ).result(self._CONNECT_TIMEOUT + 30.0)
            self._session = session
            return session

    def _drop_session(self) -> None:
        with self._lock:
            contexts = self._contexts
            self._session = None
            self._contexts = ()
            loop = self._loop
        if loop is not None and contexts:
            asyncio.run_coroutine_threadsafe(self._close_contexts(contexts), loop)

    # -- calls -------------------------------------------------------------
    def _call_once(self, name: str, kwargs: dict[str, Any]) -> Any:
        session = self._ensure_session()
        loop = self._loop
        assert loop is not None
        future = asyncio.run_coroutine_threadsafe(
            asyncio.wait_for(session.call_tool(name, kwargs), self._CALL_TIMEOUT), loop
        )
        try:
            result = future.result(self._CALL_TIMEOUT + 30.0)
        except _FutureTimeout:
            future.cancel()
            raise TimeoutError(f"{self.server} MCP call {name!r} timed out") from None
        return _unwrap_mcp(result)

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        try:
            return self._call_once(name, kwargs)
        except BaseException:  # noqa: BLE001 - one clean retry on a fresh session
            # A broken transport poisons every later call on the shared
            # session; rebuild it once before giving up.
            self._drop_session()
            return self._call_once(name, kwargs)


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
