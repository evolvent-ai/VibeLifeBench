"""Task-local ordered world mutation controller for the Tokyo business trip task.

The controller is deliberately independent from the source task. It loads only
release JSON files shipped in this Harbor directory and applies their explicit
SQLite operations to the eight MCP service runtime databases.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DB_PATHS: dict[str, Path] = {
    "banking": Path("/banking-env/runtime.db"), "calendar": Path("/calendar-env/runtime.db"),
    "email": Path("/email-env/runtime.db"), "flight_booking": Path("/flight-booking-env/runtime.db"),
    "hotel_booking": Path("/hotel-booking-env/runtime.db"), "maps": Path("/maps-env/runtime.db"),
    "notion": Path("/notion-env/runtime.db"), "visa_and_advisory": Path("/visa-and-advisory-env/runtime.db"),
    "weather": Path("/weather-env/runtime.db"),
}
DB_ALIASES: dict[str, str] = {
    "banking": "svc_banking",
    "calendar": "svc_calendar",
    "email": "svc_email",
    "flight_booking": "svc_flight_booking",
    "hotel_booking": "svc_hotel_booking",
    "maps": "svc_maps",
    "notion": "svc_notion",
    "visa_and_advisory": "svc_visa_and_advisory",
    "weather": "svc_weather",
}
ALLOWED_SERVERS = frozenset(DB_PATHS)
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
STEP_NAME = re.compile(r"^event-(?:0[0-3][0-9])$")
EVIDENCE_ROOT = Path("/evidence")
WORKSPACE_ROOT = Path("/workspace-source")
STATE_PATH = Path("/controller-state/controller-state.json")
STATE_DB_PATH = Path("/controller-state/controller-state.db")
SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
CURRENT_STEP_PATH = Path("/controller-state/current-step")
SCENARIO_CLOCK_REQUIRED = True
CLOCK_TOKEN = os.environ.get("CLOCK_TOKEN", "")
STEP_MAP_PATH = Path(__file__).with_name("step-release-map.json")
RELEASE_DIR = Path(__file__).with_name("releases")
HEALTH_TOKEN = os.environ.get("HEALTH_TOKEN", "")
RELEASE_LOCK = threading.RLock()
SNAPSHOT_LOCK = threading.RLock()
BASELINE_WORKSPACE_NAMES = frozenset({"AGENTS.md", "PERSONA.md", "TOOLS.md", "USER.md", "IDENTITY.md", "SOUL.md"})
ALLOWED_WORKSPACE_SUFFIXES = frozenset({".md", ".txt", ".json", ".csv"})


def _load_step_map() -> dict[str, dict[str, Any]]:
    payload = json.loads(STEP_MAP_PATH.read_text(encoding="utf-8"))
    steps = payload.get("steps")
    expected_count = payload.get("step_count")
    if not isinstance(steps, dict) or not isinstance(expected_count, int) or len(steps) != expected_count:
        raise ValueError("invalid controller step map")
    for step, item in steps.items():
        if not STEP_NAME.fullmatch(step) or not isinstance(item, dict):
            raise ValueError(f"invalid step map entry: {step}")
        if not isinstance(item.get("virtual_stage"), int):
            raise ValueError(f"missing virtual stage: {step}")
        if not isinstance(item.get("stage_boundary"), bool):
            raise ValueError(f"missing stage boundary: {step}")
        if not item.get("source_event_id"):
            raise ValueError(f"missing source event id: {step}")
        scenario_time = item.get("scenario_time")
        if not isinstance(scenario_time, str):
            raise ValueError(f"missing scenario time: {step}")
        parsed = datetime.fromisoformat(scenario_time.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError(f"scenario time must include an offset: {step}")
    return steps


STEP_MAP = _load_step_map()
STEP_ORDER = tuple(STEP_MAP)



_CAPTURE_MODULES: tuple[Any, Any] | None = None


def _capture_modules() -> tuple[Any, Any]:
    global _CAPTURE_MODULES
    if _CAPTURE_MODULES is not None:
        return _CAPTURE_MODULES
    configured = os.environ.get("EVIDENCE_CAPTURE_DIR")
    candidates = [Path(configured)] if configured else []
    candidates.extend(
        [
            Path("/opt/world-controller/capture"),
            Path(__file__).resolve().parent.parent / "evidence-collector",
        ]
    )
    capture_dir = next(
        (candidate for candidate in candidates if (candidate / "harbor_env.py").is_file()),
        None,
    )
    if capture_dir is None:
        raise RuntimeError("world snapshot capture modules are unavailable")

    def load(name: str, filename: str) -> Any:
        spec = importlib.util.spec_from_file_location(name, capture_dir / filename)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load capture module: {filename}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    env_module = load("lin_ming_controller_capture_env", "harbor_env.py")
    snapshot_module = load("lin_ming_controller_snapshot_capture", "snapshot_capture.py")
    _CAPTURE_MODULES = env_module, snapshot_module
    return _CAPTURE_MODULES


def _default_snapshot_factory(stage: int) -> dict[str, Any]:
    env_module, snapshot_module = _capture_modules()
    env = env_module.HarborEnv(list(DB_PATHS), workspace_root=WORKSPACE_ROOT)
    return snapshot_module.capture_stage_snapshot(env, stage)


SNAPSHOT_FACTORY = _default_snapshot_factory

def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"}:
            raise ValueError("world clock must have exactly world_now")
        value = str(payload.get("world_now") or "")
        try:
            step = CURRENT_STEP_PATH.read_text(encoding="utf-8").strip()
        except OSError:
            step = ""
        if step not in STEP_MAP or STEP_MAP[step]["scenario_time"] != value:
            step = next((name for name, item in STEP_MAP.items() if item["scenario_time"] == value), "")
        if step not in STEP_MAP or not value:
            raise ValueError("invalid world clock payload")
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("scenario clock must include an offset")
        if value != STEP_MAP[step]["scenario_time"]:
            raise ValueError(f"scenario clock mismatch for {step}")
        return {"world_now": value, "step": step}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        raise RuntimeError(f"required world clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}") from exc


def scenario_now() -> datetime:
    return datetime.fromisoformat(scenario_clock()["world_now"].replace("Z", "+00:00"))


def utc_now() -> str:
    return scenario_now().astimezone(timezone.utc).isoformat()


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _clock_token(token: str | None) -> None:
    if not CLOCK_TOKEN or token != CLOCK_TOKEN:
        raise PermissionError("invalid clock token")


def set_clock(step_name: str, token: str | None = None) -> dict[str, Any]:
    """Advance the isolated historical-simulation clock to one Harbor step."""
    if step_name not in STEP_MAP:
        raise KeyError(step_name)
    _clock_token(token)
    target_index = STEP_ORDER.index(step_name)
    try:
        current = scenario_clock()
    except RuntimeError:
        current = None
    if current is not None:
        current_index = STEP_ORDER.index(current["step"])
        if target_index < current_index:
            raise ReleaseOrderError(
                f"scenario clock cannot move backward from {current['step']} to {step_name}"
            )
        if target_index > current_index + 1:
            raise ReleaseOrderError(
                f"scenario clock cannot skip from {current['step']} to {step_name}"
            )
        if target_index == current_index:
            return {**current, "status": "already_current", "advanced": False}
    payload = {"world_now": STEP_MAP[step_name]["scenario_time"]}
    write_json_atomic(SCENARIO_CLOCK_PATH, payload)
    CURRENT_STEP_PATH.write_text(step_name + "\n", encoding="utf-8")
    return {**payload, "status": "advanced", "advanced": True}


STATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS controller_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS release_journal (
    sequence_no INTEGER PRIMARY KEY AUTOINCREMENT,
    release_id TEXT UNIQUE NOT NULL,
    applied_at TEXT NOT NULL,
    changes_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS snapshot_journal (
    step TEXT PRIMARY KEY,
    captured_at TEXT NOT NULL
);
"""


def _legacy_state() -> dict[str, Any]:
    try:
        payload = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _migrate_legacy_state(conn: sqlite3.Connection) -> None:
    """Import the old JSON state once; SQLite is authoritative afterwards."""
    marker = conn.execute(
        "SELECT value FROM controller_meta WHERE key='legacy_json_migrated'"
    ).fetchone()
    if marker is not None:
        return
    legacy = _legacy_state()
    history = legacy.get("release_history")
    history = history if isinstance(history, list) else []
    by_release = {
        str(row.get("release_id")): row
        for row in history
        if isinstance(row, dict) and row.get("release_id")
    }
    released = legacy.get("released")
    if not isinstance(released, list):
        released = list(by_release)
    snapshots = legacy.get("snapshots")
    snapshots = snapshots if isinstance(snapshots, list) else []

    conn.execute("BEGIN IMMEDIATE")
    try:
        # Recheck after acquiring the write lock so concurrent initialization
        # cannot import the compatibility mirror twice.
        marker = conn.execute(
            "SELECT value FROM controller_meta WHERE key='legacy_json_migrated'"
        ).fetchone()
        if marker is None:
            for release_id_value in released:
                release_id = str(release_id_value)
                row = by_release.get(release_id, {})
                applied_at = str(
                    row.get("applied_at")
                    or legacy.get("updated_at")
                    or "1970-01-01T00:00:00+00:00"
                )
                changes = row.get("changes")
                if not isinstance(changes, list):
                    changes = []
                conn.execute(
                    """
                    INSERT OR IGNORE INTO release_journal(
                        release_id, applied_at, changes_json
                    ) VALUES (?, ?, ?)
                    """,
                    (
                        release_id,
                        applied_at,
                        json.dumps(changes, ensure_ascii=False, sort_keys=True),
                    ),
                )
            for row in snapshots:
                if not isinstance(row, dict) or not row.get("step"):
                    continue
                conn.execute(
                    """
                    INSERT OR IGNORE INTO snapshot_journal(step, captured_at)
                    VALUES (?, ?)
                    """,
                    (
                        str(row["step"]),
                        str(
                            row.get("captured_at")
                            or legacy.get("updated_at")
                            or "1970-01-01T00:00:00+00:00"
                        ),
                    ),
                )
            conn.execute(
                """
                INSERT INTO controller_meta(key, value)
                VALUES ('legacy_json_migrated', '1')
                """
            )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _connect_state() -> sqlite3.Connection:
    STATE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(STATE_DB_PATH), timeout=10.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 10000")
    journal_mode = str(conn.execute("PRAGMA main.journal_mode = DELETE").fetchone()[0])
    if journal_mode.lower() == "wal":
        conn.close()
        raise RuntimeError("controller state database cannot use WAL journal mode")
    conn.executescript(STATE_SCHEMA)
    _migrate_legacy_state(conn)
    return conn


def _state_from_connection(conn: sqlite3.Connection) -> dict[str, Any]:
    release_history: list[dict[str, Any]] = []
    for row in conn.execute(
        """
        SELECT release_id, applied_at, changes_json
        FROM release_journal
        ORDER BY sequence_no
        """
    ):
        try:
            changes = json.loads(str(row["changes_json"]))
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"invalid durable changes for release {row['release_id']}"
            ) from exc
        if not isinstance(changes, list):
            raise RuntimeError(
                f"invalid durable changes for release {row['release_id']}"
            )
        release_history.append(
            {
                "release_id": str(row["release_id"]),
                "applied_at": str(row["applied_at"]),
                "changes": changes,
            }
        )
    snapshots = [
        {"step": str(row["step"]), "captured_at": str(row["captured_at"])}
        for row in conn.execute(
            "SELECT step, captured_at FROM snapshot_journal ORDER BY rowid"
        )
    ]
    timestamps = [row["applied_at"] for row in release_history]
    timestamps.extend(row["captured_at"] for row in snapshots)
    return {
        "released": [row["release_id"] for row in release_history],
        "release_history": release_history,
        "snapshots": snapshots,
        "updated_at": max(timestamps) if timestamps else None,
    }


def read_state() -> dict[str, Any]:
    conn = _connect_state()
    try:
        return _state_from_connection(conn)
    finally:
        conn.close()


def _write_compatibility_state(state: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = state if state is not None else read_state()
    write_json_atomic(STATE_PATH, payload)
    return payload


def _release_record(state: dict[str, Any], release_id: str) -> dict[str, Any]:
    for row in state["release_history"]:
        if row["release_id"] == release_id:
            return row
    raise RuntimeError(f"durable release journal is missing {release_id}")


def _repair_release_artifacts(release_id: str) -> dict[str, Any]:
    state = read_state()
    record = _release_record(state, release_id)
    _write_compatibility_state(state)
    write_json_atomic(
        EVIDENCE_ROOT / "releases" / f"{release_id}.json",
        {
            "release_id": release_id,
            "applied_at": record["applied_at"],
            "changes": record["changes"],
        },
    )
    return record


def _load_release_config() -> tuple[
    dict[str, list[dict[str, Any]]], dict[str, str], dict[str, str | None]
]:
    specs: dict[str, list[dict[str, Any]]] = {}
    tokens: dict[str, str] = {}
    previous: dict[str, str | None] = {}
    expected_previous: str | None = None
    paths = sorted(RELEASE_DIR.glob("release-*.json"))
    if not paths:
        raise RuntimeError(f"no release fixtures found in {RELEASE_DIR}")
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        release_id = str(payload.get("release_id") or "")
        if release_id != path.stem:
            raise ValueError(f"release id/path mismatch: {path.name}")
        if release_id in specs:
            raise ValueError(f"duplicate release id: {release_id}")
        declared_previous = payload.get("previous")
        if declared_previous != expected_previous:
            raise ValueError(
                f"{release_id} declares previous={declared_previous!r}, "
                f"expected {expected_previous!r}"
            )
        token = str(payload.get("token") or "")
        if len(token) < 24:
            raise ValueError(f"release token is too short: {release_id}")
        operations = payload.get("operations")
        if not isinstance(operations, list) or not operations:
            raise ValueError(f"release has no operations: {release_id}")
        normalized: list[dict[str, Any]] = []
        for operation in operations:
            if not isinstance(operation, dict):
                raise ValueError(f"invalid operation in {release_id}")
            server = str(operation.get("server") or "")
            table = str(operation.get("table") or "")
            op = str(operation.get("op") or "")
            if server not in ALLOWED_SERVERS:
                raise ValueError(f"unsupported release server: {server}")
            if not IDENTIFIER.fullmatch(table):
                raise ValueError(f"unsafe release table: {table!r}")
            if op == "insert" and not isinstance(operation.get("values"), dict):
                raise ValueError(f"insert has no values in {release_id}")
            if op == "update" and not isinstance(operation.get("set"), dict):
                raise ValueError(f"update has no set in {release_id}")
            if op in {"update", "delete"} and not isinstance(operation.get("where"), dict):
                raise ValueError(f"{op} has no where in {release_id}")
            if op not in {"insert", "update", "delete"}:
                raise ValueError(f"unsupported release operation: {op}")
            if "allow_zero" in operation and not isinstance(operation["allow_zero"], bool):
                raise ValueError(f"allow_zero must be boolean in {release_id}")
            if "allow_many" in operation and not isinstance(operation["allow_many"], bool):
                raise ValueError(f"allow_many must be boolean in {release_id}")
            if "idempotent" in operation and not isinstance(operation["idempotent"], bool):
                raise ValueError(f"idempotent must be boolean in {release_id}")
            if "key_columns" in operation and not isinstance(operation["key_columns"], list):
                raise ValueError(f"key_columns must be a list in {release_id}")
            for key in (operation.get("values", {}) or {}):
                if not IDENTIFIER.fullmatch(str(key)):
                    raise ValueError(f"unsafe value column: {key!r}")
            for key in (operation.get("set", {}) or {}):
                if not IDENTIFIER.fullmatch(str(key)):
                    raise ValueError(f"unsafe set column: {key!r}")
            for key in (operation.get("where", {}) or {}):
                if not IDENTIFIER.fullmatch(str(key)):
                    raise ValueError(f"unsafe where column: {key!r}")
            normalized.append(dict(operation))
        specs[release_id] = normalized
        tokens[release_id] = token
        previous[release_id] = declared_previous
        expected_previous = release_id
    return specs, tokens, previous


RELEASE_SPECS, RELEASE_TOKENS, PREVIOUS_RELEASE = _load_release_config()


class ReleaseOrderError(RuntimeError):
    """A release was requested before its declared predecessor."""


class DatabaseNotReady(RuntimeError):
    """At least one sidecar runtime database is not ready."""


def databases_ready() -> bool:
    return all(path.is_file() and os.access(path, os.R_OK | os.W_OK) for path in DB_PATHS.values())


def _connect(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise DatabaseNotReady(f"database is not ready: {path}")
    conn = sqlite3.connect(str(path), timeout=10.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def _quote(identifier: str) -> str:
    if not IDENTIFIER.fullmatch(identifier):
        raise ValueError(f"unsafe SQL identifier: {identifier!r}")
    return f'"{identifier}"'


def _predicate(where: dict[str, Any]) -> tuple[str, list[Any]]:
    if not where:
        raise ValueError("an operation predicate cannot be empty")
    clauses = []
    values = []
    for key, value in where.items():
        clauses.append(f"{_quote(str(key))} = ?")
        values.append(value)
    return " AND ".join(clauses), values


def _qualified_table(table: str, schema: str | None = None) -> str:
    quoted_table = _quote(table)
    if schema is None:
        return quoted_table
    return f"{_quote(schema)}.{quoted_table}"


def apply_operation(
    conn: sqlite3.Connection,
    operation: dict[str, Any],
    *,
    schema: str | None = None,
) -> dict[str, Any]:
    table = _qualified_table(str(operation["table"]), schema)
    op = str(operation["op"])
    if op == "insert":
        values = dict(operation["values"])
        columns = list(values)
        if not columns:
            raise ValueError("insert values cannot be empty")
        sql = (
            f"INSERT INTO {table} ({', '.join(_quote(str(c)) for c in columns)}) "
            f"VALUES ({', '.join('?' for _ in columns)})"
        )
        try:
            cursor = conn.execute(sql, [values[column] for column in columns])
        except sqlite3.IntegrityError:
            if not bool(operation.get("idempotent", False)):
                raise
            key_columns = [str(c) for c in operation.get("key_columns", [])]
            if not key_columns or any(c not in values for c in key_columns):
                raise
            set_values = {c: v for c, v in values.items() if c not in key_columns}
            if not set_values:
                return {"op": op, "table": operation["table"], "rowcount": 0}
            predicate, where_values = _predicate({c: values[c] for c in key_columns})
            assignments = ", ".join(f"{_quote(str(k))} = ?" for k in set_values)
            cursor = conn.execute(
                f"UPDATE {table} SET {assignments} WHERE {predicate}",
                [set_values[column] for column in set_values] + where_values,
            )
        return {"op": op, "table": operation["table"], "rowcount": cursor.rowcount}
    if op == "update":
        values = dict(operation["set"])
        if not values:
            raise ValueError("update set cannot be empty")
        predicate, where_values = _predicate(dict(operation["where"]))
        assignments = ", ".join(f"{_quote(str(k))} = ?" for k in values)
        cursor = conn.execute(
            f"UPDATE {table} SET {assignments} WHERE {predicate}",
            [values[column] for column in values] + where_values,
        )
        if cursor.rowcount != 1 and not bool(operation.get("allow_many", False)) and not bool(operation.get("allow_zero", False)):
            raise RuntimeError(
                f"update expected one row in {operation['table']}, got {cursor.rowcount}"
            )
        return {"op": op, "table": operation["table"], "rowcount": cursor.rowcount}
    if op == "delete":
        predicate, where_values = _predicate(dict(operation["where"]))
        cursor = conn.execute(f"DELETE FROM {table} WHERE {predicate}", where_values)
        if cursor.rowcount != 1:
            raise RuntimeError(
                f"delete expected one row in {operation['table']}, got {cursor.rowcount}"
            )
        return {"op": op, "table": operation["table"], "rowcount": cursor.rowcount}
    raise ValueError(f"unsupported operation: {op}")


def _release_token(release_id: str, token: str | None) -> None:
    expected = RELEASE_TOKENS.get(release_id)
    if expected is None:
        raise KeyError(release_id)
    if token != expected:
        raise PermissionError("invalid release token")


def _attach_service_databases(conn: sqlite3.Connection) -> None:
    for server, path in DB_PATHS.items():
        if not path.is_file():
            raise DatabaseNotReady(f"database is not ready: {path}")
        alias = DB_ALIASES[server]
        # The state DB is the main database. All six service databases are
        # attached to this one connection so SQLite can use one transaction
        # and one COMMIT for both the world mutation and durable journal row.
        conn.execute(f"ATTACH DATABASE ? AS {_quote(alias)}", (str(path),))
        # The vendored MCP services keep a process-lifetime connection and use
        # their canonical journal mode (currently WAL). Do not attempt to
        # switch it here: changing a live service database needs an exclusive
        # lock and can fail with ``database is locked``.


def apply_release(release_id: str, token: str | None = None) -> dict[str, Any]:
    with RELEASE_LOCK:
        _release_token(release_id, token)
        conn = _connect_state()
        changes: list[dict[str, Any]] = []
        try:
            _attach_service_databases(conn)
            # A deferred transaction lets SQLite acquire each WAL database's
            # write lock only when its release operation touches it. Acquiring
            # an immediate lock across all attached services is incompatible
            # with the canonical MCP servers' long-lived WAL readers.
            conn.execute("BEGIN")
            existing = conn.execute(
                """
                SELECT release_id, applied_at, changes_json
                FROM release_journal
                WHERE release_id = ?
                """,
                (release_id,),
            ).fetchone()
            if existing is not None:
                conn.execute("ROLLBACK")
                record = _repair_release_artifacts(release_id)
                return {
                    "release_id": release_id,
                    "status": "already_released",
                    "applied": False,
                    "changes": record["changes"],
                }

            last = conn.execute(
                """
                SELECT release_id
                FROM release_journal
                ORDER BY sequence_no DESC
                LIMIT 1
                """
            ).fetchone()
            last_release = str(last["release_id"]) if last is not None else None
            previous = PREVIOUS_RELEASE.get(release_id)
            if previous is None:
                if last_release is not None:
                    raise ReleaseOrderError(f"{release_id} must be the first release")
            elif last_release != previous:
                raise ReleaseOrderError(f"{release_id} requires {previous} first")

            applied_at = utc_now()
            for operation in RELEASE_SPECS[release_id]:
                server = str(operation["server"])
                change = apply_operation(
                    conn,
                    operation,
                    schema=DB_ALIASES[server],
                )
                change["server"] = server
                change["source_event_id"] = operation.get("source_event_id")
                changes.append(change)
            conn.execute(
                """
                INSERT INTO release_journal(release_id, applied_at, changes_json)
                VALUES (?, ?, ?)
                """,
                (
                    release_id,
                    applied_at,
                    json.dumps(changes, ensure_ascii=False, sort_keys=True),
                ),
            )
            conn.execute("COMMIT")
        except Exception:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

        _repair_release_artifacts(release_id)
        return {"release_id": release_id, "status": "released", "applied": True, "changes": changes}


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _database_summary(path: Path) -> dict[str, Any]:
    conn = _connect(path)
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        counts = {
            str(row["name"]): int(
                conn.execute(f"SELECT count(*) AS n FROM {_quote(str(row['name']))}").fetchone()["n"]
            )
            for row in tables
        }
        return {"tables": counts, "database_sha256": _file_sha256(path)}
    finally:
        conn.close()


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON evidence: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _read_json_array(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON evidence: {path}") from exc
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        raise ValueError(f"expected JSON object array: {path}")
    return payload


def _existing_manifest(target: Path) -> dict[str, Any] | None:
    if not target.is_dir():
        return None
    return _read_json_object(target / "manifest.json")


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): _file_sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
    }


def _write_manifest(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    manifest = dict(payload)
    manifest["hashes"] = _hash_tree(root)
    write_json_atomic(root / "manifest.json", manifest)
    return manifest


def _publish_directory(target: Path, build: Any) -> dict[str, Any]:
    existing = _existing_manifest(target)
    if existing is not None:
        return existing
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=f".{target.name}.tmp-", dir=target.parent))
    try:
        manifest = build(tmp)
        try:
            os.replace(tmp, target)
        except OSError:
            existing = _existing_manifest(target)
            if existing is None:
                raise
            return existing
        return manifest
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


def _business_workspace_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    if not WORKSPACE_ROOT.is_dir():
        return files
    for source in sorted(WORKSPACE_ROOT.rglob("*")):
        if not source.is_file() or source.is_symlink():
            continue
        relative = source.relative_to(WORKSPACE_ROOT)
        if any(part.startswith(".") for part in relative.parts):
            continue
        if len(relative.parts) == 1 and relative.name in BASELINE_WORKSPACE_NAMES:
            continue
        if source.suffix.lower() not in ALLOWED_WORKSPACE_SUFFIXES:
            continue
        files.append((source, relative))
    return files


def _copy_business_workspace(destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for source, relative in _business_workspace_files():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(str(relative))
    return copied


def _validate_staging(step_name: str) -> tuple[Path, dict[str, Any]]:
    current = WORKSPACE_ROOT / ".harbor-stage" / "current"
    metadata = _read_json_object(current / "metadata.json")
    expected = STEP_MAP[step_name]
    exact = {
        "schema_version": 1,
        "step": step_name,
        "virtual_stage": expected["virtual_stage"],
        "source_event_id": expected["source_event_id"],
        "stage_boundary": expected["stage_boundary"],
    }
    for key, value in exact.items():
        if metadata.get(key) != value:
            raise ValueError(
                f"staging metadata mismatch for {step_name}: {key}={metadata.get(key)!r}, expected {value!r}"
            )
    for name in ("trajectory.json", "response.txt", "trace.json"):
        path = current / name
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing trusted staging file: {name}")
    _read_json_array(current / "trace.json")
    return current, metadata


def _validate_world_snapshot(snapshot: dict[str, Any], stage: int) -> None:
    """Check the snapshot addresses the stage it claims to.

    There is deliberately no error-density check here. This function used to
    tolerate a snapshot until half its fields were capture errors, which only
    made sense while ``snapshot_capture`` recorded failures as values. It could
    not work: it counted ``{"error": ...}`` dicts, while a server-side failure
    decoded to a bare *string*, so a snapshot whose every field was an error
    was measured passing this check with an error count of zero. Capture now
    raises instead of returning failures, so a snapshot that exists was read
    from a live world and there is no density left to judge.
    """
    if snapshot.get("stage") != stage:
        raise ValueError("controller world snapshot stage mismatch")


def _build_step_evidence(
    root: Path, step_name: str, current: Path, metadata: dict[str, Any]
) -> dict[str, Any]:
    workspace_files = _copy_business_workspace(root / "workspace")
    for name in (
        "metadata.json", "trajectory.json", "response.txt", "trace.json",
        "session.jsonl",
    ):
        source = current / name
        if source.is_file() and not source.is_symlink():
            shutil.copy2(source, root / name)
    if metadata["stage_boundary"]:
        stage = int(metadata["virtual_stage"])
        snapshot = SNAPSHOT_FACTORY(stage)
        if not isinstance(snapshot, dict):
            raise ValueError("controller world snapshot is not an object")
        _validate_world_snapshot(snapshot, stage)
        write_json_atomic(root / "snapshot.json", snapshot)
    return _write_manifest(
        root,
        {
            "schema_version": 1,
            "kind": "event",
            "step": step_name,
            "virtual_stage": metadata["virtual_stage"],
            "source_event_id": metadata["source_event_id"],
            "stage_boundary": metadata["stage_boundary"],
            "captured_at": metadata.get("captured_at") or utc_now(),
            "workspace_files": workspace_files,
        },
    )


def _stage_steps(stage: int, boundary_step: str) -> list[str]:
    names = []
    for name in STEP_ORDER:
        item = STEP_MAP[name]
        if item["virtual_stage"] == stage:
            names.append(name)
        if name == boundary_step:
            break
    if not names or names[-1] != boundary_step:
        raise ValueError(f"invalid boundary step for stage {stage}: {boundary_step}")
    return names


def _build_stage_evidence(root: Path, stage: int, boundary_step: str) -> dict[str, Any]:
    event_steps = _stage_steps(stage, boundary_step)
    event_dirs = [EVIDENCE_ROOT / "steps" / name for name in event_steps]
    for name, event_dir in zip(event_steps, event_dirs, strict=True):
        if _existing_manifest(event_dir) is None:
            raise ValueError(f"missing private event evidence: {name}")

    boundary_dir = event_dirs[-1]
    snapshot = _read_json_object(boundary_dir / "snapshot.json")
    if snapshot.get("stage") != stage:
        raise ValueError("stage snapshot number mismatch")
    shutil.copy2(boundary_dir / "snapshot.json", root / "snapshot.json")
    shutil.copytree(boundary_dir / "workspace", root / "workspace")

    responses: list[str] = []
    trace: list[dict[str, Any]] = []
    trajectories = root / "trajectories"
    trajectories.mkdir()
    trajectory_rows: list[dict[str, Any]] = []
    for name, event_dir in zip(event_steps, event_dirs, strict=True):
        response = (event_dir / "response.txt").read_text(encoding="utf-8")
        if response:
            responses.append(response)
        trace.extend(_read_json_array(event_dir / "trace.json"))
        trajectory_target = trajectories / f"{name}.json"
        shutil.copy2(event_dir / "trajectory.json", trajectory_target)
        try:
            trajectory_payload: Any = json.loads(trajectory_target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            trajectory_payload = {"raw": trajectory_target.read_text(encoding="utf-8", errors="replace")}
        trajectory_rows.append({"step": name, "trajectory": trajectory_payload})

    (root / "response.txt").write_text("\n---\n".join(responses), encoding="utf-8")
    write_json_atomic(root / "trace.json", trace)
    write_json_atomic(
        root / "trajectory.json",
        {"schema_version": 1, "virtual_stage": stage, "steps": trajectory_rows},
    )
    return _write_manifest(
        root,
        {
            "schema_version": 1,
            "kind": "stage",
            "step": boundary_step,
            "virtual_stage": stage,
            "event_steps": event_steps,
            "captured_at": _read_json_object(boundary_dir / "metadata.json").get("captured_at")
            or utc_now(),
        },
    )


def _record_snapshot(step_name: str, captured_at: str) -> None:
    conn = _connect_state()
    try:
        conn.execute("BEGIN IMMEDIATE")
        existing = conn.execute(
            "SELECT captured_at FROM snapshot_journal WHERE step = ?",
            (step_name,),
        ).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO snapshot_journal(step, captured_at) VALUES (?, ?)",
                (step_name, captured_at),
            )
        elif str(existing["captured_at"]) != captured_at:
            raise RuntimeError(
                f"snapshot journal mismatch for {step_name}: "
                f"{existing['captured_at']} != {captured_at}"
            )
        conn.execute("COMMIT")
    except Exception:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()
    _write_compatibility_state()


def snapshot(step_name: str) -> dict[str, Any]:
    if step_name not in STEP_MAP:
        raise ValueError(f"unknown Harbor step: {step_name}")
    with SNAPSHOT_LOCK:
        step_target = EVIDENCE_ROOT / "steps" / step_name
        existing = _existing_manifest(step_target)
        if existing is not None:
            item = STEP_MAP[step_name]
            if item["stage_boundary"]:
                stage = int(item["virtual_stage"])
                _publish_directory(
                    EVIDENCE_ROOT / "stages" / f"stage-{stage:02d}",
                    lambda root: _build_stage_evidence(root, stage, step_name),
                )
            _record_snapshot(step_name, str(existing["captured_at"]))
            return existing
        current, metadata = _validate_staging(step_name)
        manifest = _publish_directory(
            step_target,
            lambda root: _build_step_evidence(root, step_name, current, metadata),
        )
        if metadata["stage_boundary"]:
            stage = int(metadata["virtual_stage"])
            _publish_directory(
                EVIDENCE_ROOT / "stages" / f"stage-{stage:02d}",
                lambda root: _build_stage_evidence(root, stage, step_name),
            )
        _record_snapshot(step_name, str(manifest["captured_at"]))
        return manifest


def _token_from_request(headers: Any) -> str | None:
    direct = headers.get("X-Release-Token")
    if direct:
        return direct
    authorization = headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        return authorization[len("Bearer "):]
    return None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            ready = databases_ready()
            self.respond(200 if ready else 503, {"status": "ok" if ready else "starting", "database_ready": ready})
            return
        if self.path == "/admin/state":
            if self.headers.get("X-Health-Token") != HEALTH_TOKEN:
                self.respond(403, {"error": "forbidden"})
                return
            self.respond(200, read_state())
            return
        self.respond(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/admin/reset":
            if self.headers.get("X-Health-Token") != HEALTH_TOKEN:
                self.respond(403, {"error": "forbidden"})
                return
            state = read_state()
            if state["released"]:
                self.respond(409, {"error": "database reset requires recreating service volumes"})
                return
            for path in (
                STATE_PATH,
                STATE_DB_PATH,
                Path(f"{STATE_DB_PATH}-wal"),
                Path(f"{STATE_DB_PATH}-shm"),
            ):
                if path.exists():
                    path.unlink()
            self.respond(200, {"status": "reset"})
            return
        if self.path.startswith("/clock/"):
            step_name = self.path[len("/clock/"):]
            try:
                result = set_clock(step_name, self.headers.get("X-Clock-Token"))
            except KeyError:
                self.respond(404, {"error": "unknown step"})
                return
            except PermissionError:
                self.respond(403, {"error": "forbidden"})
                return
            except (ReleaseOrderError, RuntimeError, ValueError) as exc:
                self.respond(409, {"error": f"{type(exc).__name__}: {exc}"})
                return
            self.respond(200, result)
            return
        prefix = "/releases/" if self.path.startswith("/releases/") else "/events/" if self.path.startswith("/events/") else None
        if prefix is None:
            self.respond(404, {"error": "not found"})
            return
        release_id = self.path[len(prefix):]
        try:
            result = apply_release(release_id, _token_from_request(self.headers))
        except KeyError:
            self.respond(404, {"error": "unknown release"})
            return
        except PermissionError:
            self.respond(403, {"error": "forbidden"})
            return
        except (ReleaseOrderError, DatabaseNotReady, sqlite3.Error, RuntimeError, ValueError) as exc:
            self.respond(409, {"error": f"{type(exc).__name__}: {exc}"})
            return
        self.respond(200, result)

    def respond(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def serve() -> None:
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCENARIO_CLOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SCENARIO_CLOCK_PATH.is_file():
        write_json_atomic(
            SCENARIO_CLOCK_PATH,
            {"world_now": STEP_MAP["event-000"]["scenario_time"]},
        )
    conn = _connect_state()
    conn.close()
    _write_compatibility_state()
    server = ThreadingHTTPServer(("0.0.0.0", 8090), Handler)
    server.serve_forever()


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if command == "serve":
        serve()
        return
    if command == "snapshot" and len(sys.argv) == 3:
        print(json.dumps(snapshot(sys.argv[2]), ensure_ascii=False))
        return
    if command == "release" and len(sys.argv) == 4:
        print(json.dumps(apply_release(sys.argv[2], sys.argv[3]), ensure_ascii=False))
        return
    if command == "clock" and len(sys.argv) == 4:
        print(json.dumps(set_clock(sys.argv[2], sys.argv[3]), ensure_ascii=False))
        return
    raise SystemExit(
        "usage: controller.py serve | snapshot <event-step> | "
        "release <release-id> <token> | clock <event-step> <token>"
    )


if __name__ == "__main__":
    main()
