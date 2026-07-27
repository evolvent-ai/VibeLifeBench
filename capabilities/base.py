"""Base class for all xhs mock-server Terrarium capabilities.

Each concrete subclass only declares 4 class-level constants:

    IMAGE        — docker image tag (e.g. "vibe-agent-benchmark/banking_mock:latest")
    SERVER_KEY   — short name matching envs/<SERVER_KEY>/ (e.g. "banking")
    MCP_PORT     — port the server listens on inside the container (8000)
    DEFAULT_ENV  — fallback env_name when capabilities_config does not specify

The base class provides three access channels:

    ① connection_info["mcp_url"]  — for ``agent.add_mcp_server(...)`` registration
    ② cap.call_tool(name, **kw)   — for read-side checker queries via MCP
    ③ cap.apply_mutation(entry)   — out-of-band sqlite writes, bypassing MCP

Mutation path (Scheme B): runtime.db never reaches the host. Writes are dispatched
through ``python -c '... sqlite3 ...'`` inside the container via ``Sandbox.exec``.
"""
from __future__ import annotations

import asyncio
import json
import os
import textwrap
import time
from pathlib import Path
from typing import Any

from terrarium.environment.capability import BaseCapability
from terrarium.environment.exceptions import CapabilityError
from terrarium.environment.sandbox import ImageSpec, SandboxSpec, VolumeMount

from capabilities import PROJECT_ROOT


class AgentMockServerCapability(BaseCapability):
    """Base for xhs mock-server capabilities. See module docstring."""

    IMAGE: str = ""
    SERVER_KEY: str = ""
    MCP_PORT: int = 8000
    DEFAULT_ENV: str = "empty"

    # Container-side path the entrypoint copies init.sql into and where
    # runtime.db gets created. Hard-coded in our Dockerfile to /env.
    _CONTAINER_ENV_DIR = "/env"
    _CONTAINER_RUNTIME_DB = "/env/runtime.db"

    def __init__(self, config=None, sandbox=None):
        super().__init__(config, sandbox)
        cfg = config or {}
        self.env_name: str = cfg.get("env_name", type(self).DEFAULT_ENV)
        self._env_dir: Path = self._resolve_env_dir(self.SERVER_KEY, self.env_name)
        self._mcp_host: str | None = None
        self._mcp_port: int | None = None

    @classmethod
    def _resolve_env_dir(cls, server_key: str, env_name: str) -> Path:
        candidate = PROJECT_ROOT / "envs" / server_key / env_name
        if not candidate.is_dir():
            raise FileNotFoundError(
                f"env dir not found: {candidate} "
                f"(server_key={server_key!r}, env_name={env_name!r})"
            )
        return candidate

    @classmethod
    def sandbox_spec(cls, config: dict | None = None) -> SandboxSpec:
        cfg = config or {}
        env_name = cfg.get("env_name", cls.DEFAULT_ENV)
        env_dir = cls._resolve_env_dir(cls.SERVER_KEY, env_name)
        return SandboxSpec(
            image=ImageSpec(name=cls.IMAGE),
            ports=[cls.MCP_PORT],
            volumes=[
                VolumeMount(
                    source=str(env_dir),
                    target="/env-seed",
                    read_only=True,
                ),
            ],
        )

    def wait_ready(self, timeout: float | None = None) -> None:
        """Block until the MCP server completes a real ``initialize`` handshake.

        TCP-port-open is not enough: uvicorn binds the port before fastmcp
        finishes wiring its app, and a POST /mcp during that window can stall
        or 500. We probe by opening a streamable-HTTP client, running
        ``initialize``, and only return when it succeeds.
        """
        if timeout is None:
            timeout = float(os.environ.get("XHS_MCP_READY_TIMEOUT", "120"))
        host, port = self._sandbox.get_host(self.MCP_PORT)
        self._mcp_host, self._mcp_port = host, port
        deadline = time.monotonic() + timeout
        last_err: BaseException | None = None
        while time.monotonic() < deadline:
            try:
                asyncio.run(self._mcp_handshake_probe(per_attempt_timeout=3.0))
                return
            except BaseException as e:  # noqa: BLE001 — any failure means "not ready yet"
                last_err = e
                time.sleep(0.25)
        raise CapabilityError(
            f"{self.SERVER_KEY!r} MCP not ready at {host}:{port} after {timeout}s; "
            f"last error: {last_err!r}"
        )

    async def _mcp_handshake_probe(self, per_attempt_timeout: float) -> None:
        """One MCP initialize attempt. Times out if server is slow."""
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        url = f"http://{self._mcp_host}:{self._mcp_port}/mcp"
        async with asyncio.timeout(per_attempt_timeout):
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize()

    # ── Channel ① — connection info for agent.add_mcp_server ──────────────

    @property
    def connection_info(self) -> dict:
        """Connection details for this capability.

        The ``mcp_server.url`` uses the sandbox's internal docker-network
        hostname + the container-side port, since the agent runs in a peer
        container on the same network and cannot reach the host's port
        forward. (Host-side callers — ``wait_ready``, ``call_tool`` — use
        ``self._mcp_host:self._mcp_port`` from ``sandbox.get_host(...)``.)

        ``mcp_server`` is a sub-dict directly unpackable into
        ``MCPServerConfig``::

            agent.add_mcp_server(MCPServerConfig(**cap.connection_info["mcp_server"]))
        """
        host = self._sandbox.hostname()
        return {
            "mcp_server": {
                "name": self.SERVER_KEY,
                "transport": "streamable-http",
                "url": f"http://{host}:{self.MCP_PORT}/mcp",
            },
        }

    # ── Channel ② — read-side call_tool (async + sync wrapper) ────────────

    async def call_tool_async(self, name: str, **kwargs: Any) -> Any:
        """Open a fresh MCP session, call one tool, unwrap+decode, return.

        Uses the host-mapped address (``_mcp_host:_mcp_port`` set by
        ``wait_ready``), not ``connection_info`` — checkers run host-side
        and cannot reach the docker-network hostname.
        """
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        url = f"http://{self._mcp_host}:{self._mcp_port}/mcp"
        async with streamablehttp_client(url) as (read, write, _meta):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(name, kwargs)
        return _unwrap_mcp(result)

    def call_tool(self, name: str, **kwargs: Any) -> Any:
        """Synchronous wrapper. Simple per-call session; fine for checkers."""
        return asyncio.run(self.call_tool_async(name, **kwargs))

    # ── Channel ③ — out-of-band mutation via in-container sqlite3 ─────────

    def apply_mutation(self, entry: dict) -> None:
        """Apply one inline mutation entry (table/op/set/where/values/conflict_keys)."""
        sql, params = _build_inline_sql(entry)
        self._run_sqlite_in_container(sql, params)

    def apply_sql_file(self, host_sql_path: str | Path) -> None:
        """Upload a multi-statement SQL script and executescript() it in-container."""
        host_path = Path(host_sql_path)
        if not host_path.exists():
            raise FileNotFoundError(f"sql_file not found: {host_path}")
        self.fs.write_file("/tmp/mutation.sql", host_path.read_bytes())
        program = textwrap.dedent(
            f"""\
            import sqlite3
            sql = open('/tmp/mutation.sql').read()
            with sqlite3.connect({self._CONTAINER_RUNTIME_DB!r}, isolation_level=None, timeout=30) as conn:
                conn.execute('PRAGMA busy_timeout=30000')
                conn.executescript(sql)
            """
        )
        self._exec_python(program)

    def _run_sqlite_in_container(self, sql: str, params: list) -> None:
        program = textwrap.dedent(
            f"""\
            import json, os, sqlite3
            sql = os.environ['__XHS_SQL']
            params = json.loads(os.environ['__XHS_PARAMS'])
            with sqlite3.connect({self._CONTAINER_RUNTIME_DB!r}, isolation_level=None, timeout=30) as conn:
                conn.execute('PRAGMA busy_timeout=30000')
                conn.execute(sql, params)
            """
        )
        self._exec_python(
            program,
            env={"__XHS_SQL": sql, "__XHS_PARAMS": json.dumps(params)},
        )

    def _exec_python(self, program: str, env: dict[str, str] | None = None) -> None:
        last_result = None
        for attempt in range(4):
            result = self._sandbox.exec(
                ["python", "-c", program],
                env=env,
            )
            if result.exit_code == 0:
                return
            last_result = result
            output = result.stderr or result.stdout or ""
            if "database is locked" not in output.lower() or attempt == 3:
                break
            time.sleep(1.5 * (attempt + 1))

        raise CapabilityError(
            f"{self.SERVER_KEY} mutation failed (exit={last_result.exit_code}): "
            f"{last_result.stderr or last_result.stdout}"
        )


# ── helpers ───────────────────────────────────────────────────────────────


def _build_inline_sql(entry: dict) -> tuple[str, list]:
    """Translate a v3 inline-mutation entry into (sql, params)."""
    op = str(entry.get("op", "")).lower()
    table = entry.get("table")
    if not table:
        raise ValueError("inline mutation missing 'table'")

    if op == "insert":
        values = dict(entry.get("values") or {})
        if not values:
            raise ValueError("insert needs non-empty 'values'")
        cols = ", ".join(values)
        placeholders = ", ".join("?" * len(values))
        return (
            f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
            list(values.values()),
        )

    if op == "update":
        set_ = dict(entry.get("set") or {})
        where = dict(entry.get("where") or {})
        if not set_:
            raise ValueError("update needs non-empty 'set'")
        set_sql = ", ".join(f"{k} = ?" for k in set_)
        where_sql = " AND ".join(f"{k} = ?" for k in where) if where else "1=1"
        return (
            f"UPDATE {table} SET {set_sql} WHERE {where_sql}",
            list(set_.values()) + list(where.values()),
        )

    if op == "delete":
        where = dict(entry.get("where") or {})
        where_sql = " AND ".join(f"{k} = ?" for k in where) if where else "1=1"
        return f"DELETE FROM {table} WHERE {where_sql}", list(where.values())

    if op == "upsert":
        values = dict(entry.get("values") or {})
        keys = list(entry.get("conflict_keys") or [])
        if not values:
            raise ValueError("upsert needs non-empty 'values'")
        if not keys:
            raise ValueError("upsert needs non-empty 'conflict_keys'")
        cols = ", ".join(values)
        placeholders = ", ".join("?" * len(values))
        update_cols = [c for c in values if c not in keys]
        conflict_sql = ", ".join(keys)
        if update_cols:
            update_sql = ", ".join(f"{c} = excluded.{c}" for c in update_cols)
            tail = f"ON CONFLICT({conflict_sql}) DO UPDATE SET {update_sql}"
        else:
            tail = f"ON CONFLICT({conflict_sql}) DO NOTHING"
        return (
            f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) {tail}",
            list(values.values()),
        )

    raise ValueError(f"unknown op {op!r}")


def _unwrap_mcp(result: Any) -> Any:
    """Decode a FastMCP CallToolResult into native Python.

    Our servers always return ``json.dumps(...)`` (SPEC §8). FastMCP carries
    that string in both ``structuredContent={"result": "<json>"}`` and
    ``content=[TextContent(text="<json>")]``. We prefer structuredContent
    and fall back to content; non-JSON server returns raise loudly.
    """
    if result is None:
        return None
    sc = getattr(result, "structuredContent", None) or getattr(
        result, "structured_content", None
    )
    if isinstance(sc, dict) and "result" in sc:
        v = sc["result"]
        return json.loads(v) if isinstance(v, str) else v
    for block in getattr(result, "content", None) or []:
        text = getattr(block, "text", None)
        if text:
            return json.loads(text)
    return result
