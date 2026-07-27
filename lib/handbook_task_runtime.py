"""Fail-closed, stage-frozen runtime helpers for HF benchmark tasks."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

import yaml
from loguru import logger

RESPONSES_DIR = "/terrarium/agent_responses"
TRACE_DIR = "/terrarium/agent_traces"
SCORES_DIR = "/terrarium/stage_scores"
SNAPSHOTS_DIR = "/terrarium/stage_snapshots"
RECEIPTS_DIR = "/terrarium/mutation_receipts"
MAX_STAGE_RESPONSE_CHARS = 20000
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def register_all_mcp(env, agent) -> None:
    from terrarium.models.mcp import MCPServerConfig
    for cap_name in env:
        for cap in getattr(env, cap_name):
            info = getattr(cap, "connection_info", None) or {}
            mcp = info.get("mcp_server") if isinstance(info, dict) else None
            if mcp:
                agent.add_mcp_server(MCPServerConfig(**mcp))


def bootstrap_workspace(env, task_dir: Path) -> None:
    env.workspace.fs.upload(str(task_dir / "workspace"), "/terrarium/openclaw/workspace")
    env.workspace.shell.exec("chmod -R a+rwX /terrarium/openclaw/workspace", user="root")
    env.workspace.shell.exec(
        f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {SCORES_DIR} {SNAPSHOTS_DIR} {RECEIPTS_DIR}",
        user="root",
    )


def load_events(path: Path) -> tuple[int, dict[int, list[dict[str, Any]]]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    by_stage: dict[int, list[dict[str, Any]]] = {}
    for key, values in (raw.get("stages") or {}).items():
        by_stage[int(key)] = [dict(value) for value in values or []]
    return (max(by_stage) + 1) if by_stage else 0, by_stage


def render_event(event: dict[str, Any]) -> str:
    time = event.get("time", "")
    kind = event.get("kind", "")
    body = event.get("body", "") or ""
    if kind == "user_message":
        tag = f"[来自 {event.get('from') or 'user'} 的消息 @ {time}]"
    elif kind == "notification":
        tag = f"[通知 @ {time}，来源 {event.get('channel') or event.get('source') or 'system'}]"
    elif kind == "world":
        tag = f"[世界事件 @ {time}，来源 {event.get('source') or 'system'}]"
    else:
        tag = f"[{kind} @ {time}]"
    return f"{tag}\n{body}"


def _field(obj: Any, name: str, default: Any = None) -> Any:
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)


def _jsonable(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        if isinstance(value, dict):
            return {str(key): _jsonable(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [_jsonable(item) for item in value]
        return str(value)


_SENSITIVE_KEY_PARTS = (
    "api_key",
    "apikey",
    "access_token",
    "request_token",
    "auth_token",
    "authorization",
    "password",
    "passwd",
    "credential",
    "secret",
)


def _redacted_jsonable(value: Any, key: str | None = None) -> Any:
    """Convert arbitrary message payloads to JSON-safe values without persisting credentials."""
    if key is not None:
        norm = key.lower().replace("-", "_")
        if any(part in norm for part in _SENSITIVE_KEY_PARTS):
            return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): _redacted_jsonable(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_redacted_jsonable(item) for item in value]
    return _jsonable(value)


def _tool_call_record(obj: Any, event_id: str | None) -> dict[str, Any] | None:
    typ = str(_field(obj, "type", "") or "")
    function = _field(obj, "function")
    name = _field(obj, "name")
    args = _field(obj, "arguments", _field(obj, "input", {}))
    if function is not None:
        name = _field(function, "name", name)
        args = _field(function, "arguments", args)
    is_tool = typ in ("toolCall", "tool_call", "tool_use", "function_call") or function is not None
    is_tool = is_tool or (name is not None and _field(obj, "arguments") is not None)
    if not is_tool or not name:
        return None
    return {
        "event_id": event_id,
        "id": _field(obj, "id"),
        "type": typ,
        "name": str(name),
        "arguments": _redacted_jsonable(args),
    }


def _walk_tool_calls(value: Any, event_id: str | None, out: list[dict[str, Any]]) -> None:
    record = _tool_call_record(value, event_id)
    if record:
        out.append(record)
        return
    if isinstance(value, dict):
        for key in ("tool_calls", "toolCalls", "tool_use", "content", "blocks"):
            if key in value:
                _walk_tool_calls(value[key], event_id, out)
        return
    if isinstance(value, list):
        for item in value:
            _walk_tool_calls(item, event_id, out)
        return
    for key in ("tool_calls", "toolCalls", "content"):
        nested = getattr(value, key, None)
        if nested is not None:
            _walk_tool_calls(nested, event_id, out)


def _tool_result_id(message: Any) -> str | None:
    for key in ("toolCallId", "tool_call_id", "call_id", "toolUseId", "tool_use_id"):
        value = _field(message, key)
        if value:
            return str(value)
    return None


def _result_error(result: dict[str, Any]) -> str | None:
    details = result.get("details")
    if isinstance(details, dict):
        status = str(details.get("status") or "").lower()
        error = details.get("error") or details.get("message") if status in {"error", "failed", "failure"} else details.get("error")
        if error:
            return str(error)
        if status in {"error", "failed", "failure"}:
            return status
    direct_error = result.get("error")
    if direct_error:
        return str(direct_error)
    content = result.get("content")
    texts: list[str] = []
    if isinstance(content, str):
        texts.append(content)
    elif isinstance(content, list):
        texts.extend(
            str(item["text"])
            for item in content
            if isinstance(item, dict) and isinstance(item.get("text"), str)
        )
    for text in texts:
        candidate = text.strip()
        if candidate.startswith("structuredContent:"):
            candidate = candidate.split(":", 1)[1].strip()
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            parsed = None
        if isinstance(parsed, dict):
            status = str(parsed.get("status") or "").lower()
            if parsed.get("success") is False or status in {"error", "failed", "failure"}:
                return str(parsed.get("error") or parsed.get("message") or status or "tool_result_error")
        if re.match(r"\s*Validation failed for tool\b", text, re.IGNORECASE):
            return text.strip()
        match = re.search(r"Command exited with code ([1-9][0-9]*)", text, re.IGNORECASE)
        if match:
            return f"command exited with code {match.group(1)}"
    if bool(result.get("isError") or result.get("is_error")):
        return "tool_result_error"
    return None


def _walk_tool_results(value: Any, out: dict[str, dict[str, Any]]) -> None:
    role = str(_field(value, "role", "") or "")
    typ = str(_field(value, "type", "") or "")
    call_id = _tool_result_id(value)
    is_result = role in {"toolResult", "tool_result", "tool", "function"} or typ in {
        "toolResult", "tool_result", "tool_result_message", "function_result"
    }
    if call_id and is_result:
        payload: dict[str, Any] = {
            "content": _redacted_jsonable(_field(value, "content", [])),
            "details": _redacted_jsonable(_field(value, "details", {})),
        }
        direct_error = _field(value, "error")
        if direct_error:
            payload["error"] = _redacted_jsonable(direct_error)
        if bool(_field(value, "isError", _field(value, "is_error", False))):
            payload["isError"] = True
        out[call_id] = payload
        return
    if isinstance(value, dict):
        for key in ("content", "blocks"):
            if key in value:
                _walk_tool_results(value[key], out)
        return
    if isinstance(value, list):
        for item in value:
            _walk_tool_results(item, out)
        return
    for key in ("content", "blocks"):
        nested = getattr(value, key, None)
        if nested is not None:
            _walk_tool_results(nested, out)


def _collect_tool_results(messages: Any) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    _walk_tool_results(messages or [], results)
    return results


def extract_tool_records(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    """Return tool calls correlated with their ToolResult messages.

    Missing results and explicit tool errors are recorded as failures. Rubrics can
    therefore distinguish an attempted call from a successful, observable action.
    """
    calls: list[dict[str, Any]] = []
    for message in messages or []:
        if _field(message, "role") == "assistant":
            _walk_tool_calls(message, event_id, calls)
    results = _collect_tool_results(messages)
    records: list[dict[str, Any]] = []
    for call in calls:
        call_id = str(call.get("id") or "")
        result = results.get(call_id)
        if result is None:
            error = "missing_tool_result"
            success = False
        else:
            error = _result_error(result)
            success = error is None
        records.append({
            **call,
            "result": result,
            "success": success,
            "error": error,
        })
    return records


def extract_tool_calls(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    """Backward-compatible name for the result-aware trace extractor."""
    return extract_tool_records(messages, event_id)


def extract_assistant_text(messages) -> str:
    chunks: list[str] = []
    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        if isinstance(content, str):
            if content:
                chunks.append(content)
            continue
        for block in content or []:
            if _field(block, "type") == "text":
                text = _field(block, "text", "") or ""
                if text:
                    chunks.append(text)
    text = "\n".join(chunks)
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return text[:MAX_STAGE_RESPONSE_CHARS] + (
        f"\n\n[TRUNCATED: agent response exceeded {MAX_STAGE_RESPONSE_CHARS} chars]"
    )


def _safe_identifier(value: str) -> str:
    if not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"unsafe SQLite identifier: {value!r}")
    return value


def _query_runtime_rows(cap, table: str, where: dict[str, Any]) -> list[dict[str, Any]]:
    custom = getattr(cap, "query_runtime_rows", None)
    if callable(custom):
        return list(custom(table, where))
    table = _safe_identifier(str(table))
    clauses: list[str] = []
    params: list[Any] = []
    for key, value in where.items():
        key = _safe_identifier(str(key))
        if value is None:
            clauses.append(f'"{key}" IS NULL')
        else:
            clauses.append(f'"{key}" = ?')
            params.append(value)
    if not clauses:
        raise ValueError("postcondition where must not be empty")
    sql = f'SELECT * FROM "{table}" WHERE ' + " AND ".join(clauses) + " LIMIT 100"
    runtime_db = str(getattr(cap, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    program = """
import json, os, sqlite3
sql = os.environ['__HF_QUERY']
params = json.loads(os.environ['__HF_PARAMS'])
with sqlite3.connect(os.environ['__HF_DB'], timeout=30) as conn:
    conn.row_factory = sqlite3.Row
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
print(json.dumps(rows, ensure_ascii=False, default=str))
"""
    sandbox = getattr(cap, "_sandbox", None)
    if sandbox is None:
        raise RuntimeError("capability does not expose sandbox for postcondition query")
    result = sandbox.exec(
        ["python", "-c", program],
        env={
            "__HF_QUERY": sql,
            "__HF_PARAMS": json.dumps(params, ensure_ascii=False),
            "__HF_DB": runtime_db,
        },
    )
    if result.exit_code != 0:
        raise RuntimeError(result.stderr or result.stdout or "runtime row query failed")
    return list(json.loads(result.stdout or "[]"))


def _value_matches(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _value_matches(actual[key], value) for key, value in expected.items()
        )
    if isinstance(expected, list):
        return isinstance(actual, list) and all(
            any(_value_matches(candidate, item) for candidate in actual) for item in expected
        )
    if isinstance(actual, bool) or isinstance(expected, bool):
        return bool(actual) == bool(expected)
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return actual == expected
    return str(actual) == str(expected)


def _workspace_postcondition(condition: dict[str, Any], env) -> None:
    path = str(condition["workspace_path"])
    fs = env.workspace.fs
    if not fs.exists(path):
        raise RuntimeError(f"workspace postcondition missing {path}")
    blob = fs.read_file(path).decode("utf-8", errors="replace")
    missing = [str(term) for term in condition.get("contains") or [] if str(term) not in blob]
    if missing:
        raise RuntimeError(f"workspace postcondition {path} missing {missing!r}")
    expected_sha = condition.get("sha256")
    if expected_sha and hashlib.sha256(blob.encode("utf-8")).hexdigest() != expected_sha:
        raise RuntimeError(f"workspace postcondition {path} sha256 mismatch")


def apply_postconditions(event: dict[str, Any], env) -> None:
    conditions = event.get("postconditions") or []
    if not conditions:
        raise ValueError(f"mutation {event.get('id')} has no postconditions")
    for condition in conditions:
        if condition.get("workspace_path"):
            _workspace_postcondition(condition, env)
            continue
        server = condition.get("server")
        table = condition.get("table")
        where = condition.get("where")
        if not server or not table or not isinstance(where, dict) or not where:
            raise ValueError(f"mutation {event.get('id')} has invalid row postcondition: {condition!r}")
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            raise RuntimeError(f"mutation {event.get('id')}: no capability for {server!r}")
        rows = _query_runtime_rows(cap, str(table), where)
        if not rows:
            raise RuntimeError(
                f"mutation {event.get('id')} postcondition found no {server}.{table} row for {where!r}"
            )
        expected = condition.get("expect") or {}
        if expected and not any(_value_matches(row, expected) for row in rows):
            raise RuntimeError(
                f"mutation {event.get('id')} postcondition expected {expected!r}; rows={rows!r}"
            )
        blob = json.dumps(rows, ensure_ascii=False, default=str).lower()
        missing = [str(term) for term in condition.get("contains") or [] if str(term).lower() not in blob]
        forbidden = [str(term) for term in condition.get("not_contains") or [] if str(term).lower() in blob]
        if missing or forbidden:
            raise RuntimeError(
                f"mutation {event.get('id')} postcondition failed; missing={missing!r}, "
                f"forbidden={forbidden!r}"
            )


def postconditions_satisfied(event: dict[str, Any], env) -> bool:
    try:
        apply_postconditions(event, env)
    except Exception:
        return False
    return True


def _checkpoint_label(event_id: str, server: str) -> str:
    raw = f"{event_id}_{server}"
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in raw)[:96]


def _create_runtime_checkpoint(cap, label: str) -> Any:
    method = getattr(cap, "create_runtime_checkpoint", None)
    if callable(method):
        return method(label)
    exec_python = getattr(cap, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoints")
    runtime_db = str(getattr(cap, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    backup_path = f"/tmp/{label}.runtime-backup.db"
    exec_python(
        "import sqlite3\n"
        f"src=sqlite3.connect({runtime_db!r}, isolation_level=None, timeout=30)\n"
        f"dst=sqlite3.connect({backup_path!r}, isolation_level=None, timeout=30)\n"
        "src.backup(dst)\ndst.close()\nsrc.close()\n"
    )
    return backup_path


def _restore_runtime_checkpoint(cap, token: Any) -> None:
    method = getattr(cap, "restore_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(cap, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoint restore")
    runtime_db = str(getattr(cap, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    exec_python(
        "import sqlite3\n"
        f"src=sqlite3.connect({str(token)!r}, isolation_level=None, timeout=30)\n"
        f"dst=sqlite3.connect({runtime_db!r}, isolation_level=None, timeout=30)\n"
        "src.backup(dst)\ndst.close()\nsrc.close()\n"
    )


def _delete_runtime_checkpoint(cap, token: Any) -> None:
    method = getattr(cap, "delete_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(cap, "_exec_python", None)
    if callable(exec_python):
        exec_python(
            f"import os\n"
            f"p={str(token)!r}\n"
            "os.path.exists(p) and os.remove(p)\n"
        )


def _capture_workspace_files(event: dict[str, Any], env) -> list[tuple[str, bool, bytes]]:
    captured: list[tuple[str, bool, bytes]] = []
    for spec in event.get("apply") or []:
        path = spec.get("workspace_path")
        if not path:
            continue
        path = str(path)
        exists = bool(env.workspace.fs.exists(path))
        content = env.workspace.fs.read_file(path) if exists else b""
        captured.append((path, exists, content))
    return captured


def _restore_workspace_files(captured: Iterable[tuple[str, bool, bytes]], env) -> None:
    for path, existed, content in captured:
        if existed:
            env.workspace.fs.write_file(path, content)
        elif env.workspace.fs.exists(path):
            env.workspace.shell.exec(f"python -c \"import os; os.remove({path!r})\"", user="root")


def _apply_workspace_spec(spec: dict[str, Any], env, task_dir: Path) -> None:
    path = str(spec["workspace_path"])
    source_file = spec.get("source_file")
    if source_file:
        source = task_dir / str(source_file)
        if not source.is_file():
            raise FileNotFoundError(source)
        content = source.read_bytes()
    else:
        content = str(spec.get("content") or "").encode("utf-8")
    parent = str(Path(path).parent)
    env.workspace.shell.exec(f"mkdir -p {parent}", user="root")
    env.workspace.fs.write_file(path, content)


def _receipt_path(event: dict[str, Any]) -> str:
    key = str(event.get("idempotency_key") or "")
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return f"{RECEIPTS_DIR}/{digest}.json"


def _write_receipt(event: dict[str, Any], env) -> None:
    payload = {
        "event_id": event.get("id"),
        "idempotency_key": event.get("idempotency_key"),
    }
    env.workspace.fs.write_file(
        _receipt_path(event),
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8"),
    )


def apply_mutation_event(event: dict[str, Any], env, task_dir: Path) -> None:
    specs = event.get("apply") or []
    if not specs:
        raise ValueError(f"mutation {event.get('id')} has no state changes")
    if event.get("abort_stage") is not True:
        raise ValueError(f"mutation {event.get('id')} must set abort_stage=true")
    if not event.get("idempotency_key"):
        raise ValueError(f"mutation {event.get('id')} has no idempotency_key")
    if not event.get("postconditions"):
        raise ValueError(f"mutation {event.get('id')} has no postconditions")
    receipt = _receipt_path(event)
    if env.workspace.fs.exists(receipt):
        return
    if postconditions_satisfied(event, env):
        _write_receipt(event, env)
        return

    capabilities: dict[str, Any] = {}
    for spec in specs:
        if spec.get("workspace_path"):
            continue
        server = spec.get("server")
        if not server:
            raise ValueError(f"mutation {event.get('id')}: missing server")
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            raise RuntimeError(f"mutation {event.get('id')}: no capability for {server!r}")
        if "sql_file" in spec and not (task_dir / str(spec["sql_file"])).is_file():
            raise FileNotFoundError(task_dir / str(spec["sql_file"]))
        capabilities[str(server)] = cap

    checkpoints: list[tuple[Any, Any]] = []
    workspace_before = _capture_workspace_files(event, env)
    try:
        for server, cap in capabilities.items():
            token = _create_runtime_checkpoint(
                cap, _checkpoint_label(str(event.get("id") or "mutation"), server)
            )
            checkpoints.append((cap, token))
        try:
            for spec in specs:
                if spec.get("workspace_path"):
                    _apply_workspace_spec(spec, env, task_dir)
                    continue
                cap = capabilities[str(spec["server"])]
                if "sql_file" in spec:
                    cap.apply_sql_file(task_dir / str(spec["sql_file"]))
                elif "tool_call" in spec:
                    tool_call = spec["tool_call"]
                    result = cap.call_tool(tool_call["name"], **(tool_call.get("args") or {}))
                    if isinstance(result, dict) and result.get("success") is False:
                        raise RuntimeError(f"mutation tool call failed: {result!r}")
                else:
                    cap.apply_mutation(spec)
            apply_postconditions(event, env)
            _write_receipt(event, env)
        except Exception:
            rollback_errors: list[str] = []
            for cap, token in reversed(checkpoints):
                try:
                    _restore_runtime_checkpoint(cap, token)
                except Exception as exc:
                    rollback_errors.append(f"{type(exc).__name__}: {exc}")
            try:
                _restore_workspace_files(workspace_before, env)
            except Exception as exc:
                rollback_errors.append(f"workspace: {type(exc).__name__}: {exc}")
            if rollback_errors:
                raise RuntimeError(
                    f"mutation {event.get('id')} failed and rollback failed: {rollback_errors}"
                )
            raise
    finally:
        for cap, token in reversed(checkpoints):
            try:
                _delete_runtime_checkpoint(cap, token)
            except Exception as exc:
                logger.warning(
                    f"mutation checkpoint cleanup failed for {event.get('id')}: "
                    f"{type(exc).__name__}: {exc}"
                )


def dispatch_event(event: dict[str, Any], env, agent, task_dir: Path) -> tuple[str, list[dict[str, Any]]]:
    kind = event.get("kind", "")
    if kind == "mutation":
        apply_mutation_event(event, env, task_dir)
        return "", []
    if event.get("silent"):
        return "", []
    if kind not in ("user_message", "notification", "world"):
        raise ValueError(f"event {event.get('id')}: unknown kind {kind!r}")
    result = agent.act(render_event(event))
    messages = getattr(result, "messages", []) or []
    return extract_assistant_text(messages), extract_tool_calls(messages, event.get("id"))


def run_rubric_checks(checks_spec, env, tag: str) -> tuple[list[Any], float, float]:
    from terrarium.models.checker import Check
    checks: list[Any] = []
    total_weight = 0.0
    passed_weight = 0.0
    for check_id, function, weight in checks_spec:
        try:
            passed = bool(function(env))
        except Exception as exc:
            logger.warning(f"checker {check_id!r} raised: {type(exc).__name__}: {exc}")
            passed = False
        checks.append(Check(name=check_id, passed=passed, tags=[tag]))
        total_weight += float(weight)
        if passed:
            passed_weight += float(weight)
    return checks, total_weight, passed_weight


def persist_stage_score(
    env,
    stage_idx: int,
    checks: list[Any],
    total_weight: float,
    passed_weight: float,
) -> None:
    payload = {
        "stage": stage_idx,
        "total_weight": total_weight,
        "passed_weight": passed_weight,
        "score": (passed_weight / total_weight) if total_weight else None,
        "checks": [
            {"name": str(getattr(check, "name", "")), "passed": bool(getattr(check, "passed", False))}
            for check in checks
        ],
    }
    env.workspace.fs.write_file(
        f"{SCORES_DIR}/stage_{stage_idx}.json",
        json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
    )


def _runtime_db_fingerprint(cap) -> dict[str, Any]:
    custom = getattr(cap, "runtime_fingerprint", None)
    if callable(custom):
        return dict(custom())
    sandbox = getattr(cap, "_sandbox", None)
    if sandbox is None:
        return {"error": "capability has no sandbox"}
    runtime_db = str(getattr(cap, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    program = """
import hashlib, json, os, sqlite3
path=os.environ['__HF_DB']
with open(path,'rb') as fh:
    digest=hashlib.sha256(fh.read()).hexdigest()
with sqlite3.connect(path, timeout=30) as conn:
    names=[r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    counts={name: conn.execute('SELECT COUNT(*) FROM "'+name.replace('"','""')+'"').fetchone()[0] for name in names}
print(json.dumps({'sha256':digest,'table_counts':counts}, sort_keys=True))
"""
    result = sandbox.exec(["python", "-c", program], env={"__HF_DB": runtime_db})
    if result.exit_code != 0:
        return {"error": result.stderr or result.stdout or "fingerprint failed"}
    return dict(json.loads(result.stdout or "{}"))


def persist_environment_fingerprint(env, stage_idx: int, services: Iterable[str]) -> None:
    payload: dict[str, Any] = {"stage": stage_idx, "services": {}}
    for server in services:
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            payload["services"][server] = {"error": "capability unavailable"}
            continue
        try:
            payload["services"][server] = _runtime_db_fingerprint(cap)
        except Exception as exc:
            payload["services"][server] = {"error": f"{type(exc).__name__}: {exc}"}
    env.workspace.fs.write_file(
        f"{SNAPSHOTS_DIR}/stage_{stage_idx}.json",
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8"),
    )
