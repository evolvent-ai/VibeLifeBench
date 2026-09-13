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
import atexit
import json
import os
import threading
import time
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

    One stage freeze issues hundreds of small reads (per-statement detail,
    per-message email bodies and headers), and the world-controller collect
    hook that runs the freeze has a hard wall-clock budget. Opening a fresh
    streamable-HTTP transport plus ``ClientSession.initialize()`` for every
    call dominates that budget on a cold environment, so calls are served by
    a single worker task on a dedicated event loop that owns the session for
    the whole freeze and reuses it.

    The worker is also the only task that enters and exits the transport
    context managers: anyio forbids exiting an async context manager in a
    different task than it was entered in, so teardown from any other task
    (call site, reconnect, interpreter shutdown) must be funnelled through
    the worker itself. A call whose transport died is retried once on a
    freshly opened session before the failure is surfaced —
    ``snapshot_capture._call`` then records it as ``{"error": ...}`` exactly
    as before.
    """

    # A single tool read is fast; a call that outlives this budget is stuck
    # and should surface as an error instead of eating the hook's whole
    # wall-clock allowance.
    _CALL_TIMEOUT_SECONDS = 30.0

    def __init__(self, server: str) -> None:
        self.server = server
        host = os.environ.get(f"MCP_HOST_{server.upper()}", _service_host(server))
        port = os.environ.get("MCP_PORT", "8000")
        self.url = f"http://{host}:{port}/mcp"
        self._loop: asyncio.AbstractEventLoop | None = None
        self._queue: asyncio.Queue | None = None
        self._worker: asyncio.Task | None = None

    def _ensure_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is not None and not self._loop.is_closed():
            return self._loop
        loop = asyncio.new_event_loop()
        threading.Thread(
            target=loop.run_forever, name=f"mcp-{self.server}", daemon=True
        ).start()
        deadline = time.monotonic() + 5.0
        while not loop.is_running() and time.monotonic() < deadline:
            time.sleep(0.001)
        self._loop = loop
        atexit.register(self._shutdown)
        return loop

    def _shutdown(self) -> None:
        """Stop the worker at interpreter exit, inside its own task.

        The sentinel lets the worker tear the transport and session down from
        the task that entered them (anyio forbids exiting elsewhere), so the
        freeze process ends without dangling-context tracebacks on stderr.
        """
        loop = self._loop
        if loop is None or loop.is_closed():
            return
        try:
            asyncio.run_coroutine_threadsafe(self._stop_worker(), loop).result(10)
        except BaseException:  # noqa: BLE001 - exit path must never raise
            pass
        finally:
            try:
                loop.call_soon_threadsafe(loop.stop)
            except BaseException:  # noqa: BLE001
                pass

    async def _stop_worker(self) -> None:
        if self._queue is None or self._worker is None or self._worker.done():
            return
        await self._queue.put(None)
        try:
            await asyncio.wait_for(asyncio.shield(self._worker), 5.0)
        except BaseException:  # noqa: BLE001 - best-effort teardown
            pass

    async def _request(self, name: str, kwargs: dict[str, Any]) -> Any:
        loop = asyncio.get_running_loop()
        if self._queue is None or self._worker is None or self._worker.done():
            self._queue = asyncio.Queue()
            self._worker = loop.create_task(self._serve())
        fut: asyncio.Future = loop.create_future()
        await self._queue.put((name, kwargs, fut))
        return await fut

    async def _open_session(self) -> tuple[Any, Any]:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        transport = streamablehttp_client(self.url)
        read, write, _meta = await transport.__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        return transport, session

    async def _serve(self) -> None:
        session: Any = None
        transport: Any = None
        try:
            while True:
                item = await self._queue.get()
                if item is None:
                    break
                name, kwargs, fut = item
                if fut.done():
                    continue
                for attempt in (1, 2):
                    if session is None:
                        try:
                            transport, session = await self._open_session()
                        except BaseException as exc:  # noqa: BLE001 - surfaced on the future
                            session = transport = None
                            if attempt == 2:
                                fut.set_exception(exc)
                                break
                            continue
                    try:
                        result = await asyncio.wait_for(
                            session.call_tool(name, kwargs), self._CALL_TIMEOUT_SECONDS
                        )
                        fut.set_result(_unwrap_mcp(result))
                        break
                    except BaseException as exc:  # noqa: BLE001
                        # Tear the session down inside this task, then retry
                        # once on a fresh one before reporting the failure.
                        for exitable in (session, transport):
                            if exitable is None:
                                continue
                            try:
                                await exitable.__aexit__(None, None, None)
                            except BaseException:  # noqa: BLE001
                                pass
                        session = transport = None
                        if attempt == 2 and not fut.done():
                            fut.set_exception(exc)
        finally:
            for exitable in (transport, session):
                if exitable is None:
                    continue
                try:
                    await exitable.__aexit__(None, None, None)
                except BaseException:  # noqa: BLE001
                    pass

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        loop = self._ensure_loop()
        future = asyncio.run_coroutine_threadsafe(self._request(name, kwargs), loop)
        return future.result()


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
