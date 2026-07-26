"""Factory visit safety day benchmark with fail-closed staged execution."""
from __future__ import annotations

import importlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml
from loguru import logger
from terrarium.models.checker import Check, CheckerResults
from terrarium.models.mcp import MCPServerConfig
from terrarium.task.decorator import entry

from capabilities import agent_caps_config

THIS_DIR = Path(__file__).resolve().parent
RESPONSES_DIR = "/terrarium/agent_responses"
TRACE_DIR = "/terrarium/agent_traces"
MUTATION_AUDIT_DIR = "/terrarium/mutation_audits"
STAGE_RESULT_DIR = "/terrarium/stage_results"
MAX_STAGE_RESPONSE_CHARS = 20000
USER_ID = "user_seed_tb_013"
SERVICES = (
    "email",
    "calendar",
    "notion",
    "maps",
    "review_platform",
    "banking",
    "notification_hub",
)
_AUTHORITATIVE_BACKEND_PROBES: tuple[tuple[str, str, dict[str, Any]], ...] = (
    ("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 1}),
    ("calendar", "list_events", {"max_results": 1}),
    ("notion", "API-post-search", {"query": "", "filter": {"value": "page"}, "page_size": 1}),
    ("review_platform", "search_merchants", {"category": "factory", "city": "嘉兴", "limit": 1}),
    ("maps", "search_places", {"query": "嘉兴", "limit": 1}),
    ("banking", "list_transactions", {"account_id": "acct_factory_main"}),
    ("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 1}),
)
SIDE_EFFECTING_POSTCONDITION_TOOLS = {
    "transfer", "add_payee", "pay_payee", "schedule_recurring", "cancel_recurring",
    "send_email", "reply_email", "forward_email", "delete_email", "delete_emails",
    "move_email", "move_emails", "mark_emails", "save_draft", "update_draft", "delete_draft",
    "create_event", "update_event", "delete_event", "reserve", "cancel_reservation",
    "save_merchant", "ask_question", "write_review", "create_subscription", "update_subscription",
    "pause_subscription", "resume_subscription", "delete_subscription", "mark_read", "mark_all_read",
    "API-post-page", "API-patch-page", "API-patch-block-children", "API-update-a-block",
    "API-delete-a-block",
}


class TrialInvalidError(RuntimeError):
    """A required runtime invariant failed, so the trial must not be scored."""

    trial_invalid = True


class PostconditionEvaluationError(RuntimeError):
    def __init__(
        self,
        message: str,
        evidence: list[dict[str, Any]],
        failed_condition: dict[str, Any],
    ) -> None:
        super().__init__(message)
        self.evidence = evidence
        self.failed_condition = failed_condition


class MutationPreflightError(TrialInvalidError):
    def __init__(
        self,
        message: str,
        failed_spec: dict[str, Any] | None,
        preflighted_specs: list[dict[str, Any]],
    ) -> None:
        super().__init__(message)
        self.failed_spec = failed_spec
        self.preflighted_specs = preflighted_specs


class MutationExecutionError(TrialInvalidError):
    def __init__(self, message: str, audit: dict[str, Any]) -> None:
        super().__init__(message)
        self.audit = audit


def _rubric_pkg_name() -> str:
    package_name = f"_task_{THIS_DIR.name.replace('.', '_')}_rubrics"
    if package_name not in sys.modules:
        package = ModuleType(package_name)
        package.__path__ = [str(THIS_DIR / "rubrics")]  # type: ignore[attr-defined]
        package.__package__ = package_name
        sys.modules[package_name] = package
    return package_name


_RUBRIC_PKG = _rubric_pkg_name()
_CAPABILITIES_CONFIG = agent_caps_config(
    email_mock="factory_visit_safety_day",
    calendar_mock="factory_visit_safety_day",
    notion_mock="factory_visit_safety_day",
    maps_mock="factory_visit_safety_day",
    review_platform_mock="factory_visit_safety_day",
    banking_mock="factory_visit_safety_day",
    notification_hub_mock="factory_visit_safety_day",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _register_all_mcp(env, agent) -> None:
    for capability_name in env:
        for capability in getattr(env, capability_name):
            info = getattr(capability, "connection_info", None) or {}
            server = info.get("mcp_server") if isinstance(info, dict) else None
            if server:
                agent.add_mcp_server(MCPServerConfig(**server))


def _decode_backend_probe_response(server: str, tool: str, value: Any) -> Any:
    """Require a decodable native or MCP-wrapped payload."""
    seen_wrappers: set[int] = set()

    def decode(candidate: Any) -> Any:
        if isinstance(candidate, bytes):
            try:
                candidate = candidate.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise TrialInvalidError(
                    f"backend protocol error for {server}.{tool}: response is not UTF-8"
                ) from exc
        if isinstance(candidate, str):
            try:
                candidate = json.loads(candidate)
            except json.JSONDecodeError as exc:
                raise TrialInvalidError(
                    f"backend protocol error for {server}.{tool}: response is not JSON"
                ) from exc
        if candidate is not None and isinstance(candidate, (dict, list, str, int, float, bool)):
            return candidate
        if candidate is None:
            raise TrialInvalidError(
                f"backend protocol error for {server}.{tool}: unsupported response NoneType"
            )

        wrapper_id = id(candidate)
        if wrapper_id in seen_wrappers:
            raise TrialInvalidError(
                f"backend protocol error for {server}.{tool}: cyclic MCP response wrapper"
            )
        seen_wrappers.add(wrapper_id)

        is_error = getattr(candidate, "isError", None)
        if is_error is None:
            is_error = getattr(candidate, "is_error", None)
        if is_error is True:
            raise TrialInvalidError(
                f"backend protocol error for {server}.{tool}: MCP tool error"
            )

        missing = object()
        structured = getattr(candidate, "structuredContent", missing)
        if structured is missing:
            structured = getattr(candidate, "structured_content", missing)
        if structured is not missing and structured is not None:
            if isinstance(structured, dict) and "result" in structured:
                return decode(structured["result"])
            return decode(structured)

        content = getattr(candidate, "content", None)
        if content is not None:
            saw_block = False
            for block in content:
                saw_block = True
                text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
                if text is not None:
                    return decode(text)
            if not saw_block and is_error is False:
                return []

        raise TrialInvalidError(
            f"backend protocol error for {server}.{tool}: unsupported response {type(candidate).__name__}"
        )

    return decode(value)


_INFRASTRUCTURE_ERROR_CODES = {
    "BACKEND_UNAVAILABLE",
    "CONNECTION_ERROR",
    "DATABASE_LOCKED",
    "DB_LOCKED",
    "DEADLINE_EXCEEDED",
    "INTERNAL_ERROR",
    "SERVICE_UNAVAILABLE",
    "TIMED_OUT",
    "TIMEOUT",
    "UNAVAILABLE",
}


def _infrastructure_error_signal(value: Any) -> str | None:
    """Return a structured infrastructure failure code, excluding business misses."""
    if isinstance(value, list):
        for item in value:
            signal = _infrastructure_error_signal(item)
            if signal:
                return signal
        return None
    if not isinstance(value, dict):
        return None
    for key, item in value.items():
        normalized_key = re.sub(r"[^a-z0-9]+", "", str(key).lower())
        if normalized_key in {"code", "errorcode", "status", "type"} and isinstance(item, str):
            code = re.sub(r"[^A-Z0-9]+", "_", item.upper()).strip("_")
            if code in _INFRASTRUCTURE_ERROR_CODES:
                return code
        if normalized_key in {"error", "errors", "detail", "details"}:
            if isinstance(item, str):
                code = re.sub(r"[^A-Z0-9]+", "_", item.upper()).strip("_")
                if code in _INFRASTRUCTURE_ERROR_CODES:
                    return code
                lowered = item.lower()
                for phrase, signal in (
                    ("database is locked", "DB_LOCKED"),
                    ("db locked", "DB_LOCKED"),
                    ("service unavailable", "SERVICE_UNAVAILABLE"),
                    ("deadline exceeded", "TIMEOUT"),
                    ("timed out", "TIMEOUT"),
                    ("timeout", "TIMEOUT"),
                    ("internal server error", "INTERNAL_ERROR"),
                ):
                    if phrase in lowered:
                        return signal
            signal = _infrastructure_error_signal(item)
            if signal:
                return signal
    return None


def _preflight_authoritative_backends(env) -> list[dict[str, Any]]:
    """Probe every authoritative service through one read-only MCP tool."""
    evidence: list[dict[str, Any]] = []
    for server, tool, args in _AUTHORITATIVE_BACKEND_PROBES:
        capability = getattr(env, f"{server}_mock", None)
        if capability is None:
            raise TrialInvalidError(f"required backend {server} capability is missing")
        call_tool = getattr(capability, "call_tool", None)
        if not callable(call_tool):
            raise TrialInvalidError(f"required backend {server} capability has no call_tool protocol")
        try:
            raw = call_tool(tool, **dict(args))
        except Exception as exc:
            raise TrialInvalidError(
                f"required backend {server}.{tool} is unreachable: {type(exc).__name__}: {exc}"
            ) from exc
        decoded = _decode_backend_probe_response(server, tool, raw)
        infrastructure_error = _infrastructure_error_signal(decoded)
        if infrastructure_error:
            raise TrialInvalidError(
                f"required backend {server}.{tool} returned infrastructure error "
                f"{infrastructure_error}: {decoded!r}"
            )
        evidence.append({
            "server": server,
            "tool": tool,
            "reachable": True,
            "response_type": type(decoded).__name__,
        })
    return evidence


def _bootstrap_workspace(env) -> None:
    workspace_root = "/terrarium/openclaw/workspace"
    try:
        env.workspace.fs.upload(str(THIS_DIR / "workspace"), workspace_root)
    except Exception as error:
        raise TrialInvalidError(f"bootstrap workspace upload failed: {error}") from error
    _checked_shell_exec(
        env,
        f"chmod -R a+rwX {workspace_root}",
        context="bootstrap",
    )
    _checked_shell_exec(
        env,
        f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {MUTATION_AUDIT_DIR} {STAGE_RESULT_DIR}",
        context="bootstrap",
    )
    writable_dirs = (
        workspace_root,
        RESPONSES_DIR,
        TRACE_DIR,
        MUTATION_AUDIT_DIR,
        STAGE_RESULT_DIR,
    )
    quoted_dirs = " ".join(writable_dirs)
    _checked_shell_exec(
        env,
        "for directory in " + quoted_dirs + "; do "
        'test -d "$directory" && test -w "$directory" && '
        'probe="$directory/.factory_runtime_write_probe" && '
        ': > "$probe" && rm -f "$probe" || exit 1; done',
        context="bootstrap writability",
    )


def _load_events(path: Path) -> tuple[int, dict[int, list[dict[str, Any]]]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("stages"), dict):
        raise ValueError("event.yaml must contain a stages mapping")
    by_stage: dict[int, list[dict[str, Any]]] = {}
    for key, values in raw["stages"].items():
        stage = int(key)
        if not isinstance(values, list):
            raise ValueError(f"stage {stage} events must be a list")
        by_stage[stage] = [dict(value) for value in values]
    if sorted(by_stage) != list(range(25)):
        raise ValueError(f"expected stages 0..24, got {sorted(by_stage)}")
    return 25, by_stage


def _load_rubric(name: str):
    module = importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    checks = getattr(module, "CHECKS", None)
    if not isinstance(checks, list) or not checks:
        raise RuntimeError(f"rubric module {name!r} must define non-empty CHECKS")
    return module


def _render_event(event: dict[str, Any]) -> str:
    timestamp = event.get("time", "")
    kind = event.get("kind", "")
    body = event.get("body", "") or ""
    if kind == "user_message":
        tag = f"[来自 {event.get('from') or 'user'} 的消息 @ {timestamp}]"
    elif kind == "notification":
        tag = f"[通知 @ {timestamp}，来源 {event.get('channel') or event.get('source') or 'system'}]"
    elif kind == "world":
        tag = f"[世界事件 @ {timestamp}，来源 {event.get('source') or 'system'}]"
    else:
        tag = f"[{kind} @ {timestamp}]"
    return f"{tag}\n{body}"


def _field(value: Any, name: str, default: Any = None) -> Any:
    return value.get(name, default) if isinstance(value, dict) else getattr(value, name, default)


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


def _decode_tool_value(value: Any) -> Any:
    value = _jsonable(value)
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _has_failure_signal(value: Any) -> bool:
    value = _decode_tool_value(value)
    if isinstance(value, str):
        return bool(re.search(r"(?i)(?:^|[\s\[{(:;,])(?:error|failure|failed|exception|traceback)(?:\b|\s*[:：])", value))
    if isinstance(value, list):
        return any(_has_failure_signal(item) for item in value)
    if not isinstance(value, dict):
        return False
    normalized = {str(key).lower().replace("_", ""): item for key, item in value.items()}
    if any(normalized.get(key) not in (None, False, "", 0, [], {}) for key in ("iserror", "error", "failed", "failure")):
        return True
    if normalized.get("success") is False or normalized.get("ok") is False:
        return True
    if str(normalized.get("status") or "").lower() in {"error", "failed", "failure", "exception"}:
        return True
    return any(_has_failure_signal(item) for item in value.values())


def _iter_mappings(value: Any):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from _iter_mappings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_mappings(item)


def _value_matches(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _value_matches(actual[key], item) for key, item in expected.items()
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


def _call_observation(capability: Any, tool: str, args: dict[str, Any]) -> Any:
    call_tool = getattr(capability, "call_tool", None)
    if callable(call_tool):
        return _decode_tool_value(call_tool(tool, **args))
    direct = getattr(capability, tool, None)
    if not callable(direct):
        raise RuntimeError(f"capability has no observational tool {tool!r}")
    return _decode_tool_value(direct(**args))


def _validate_postcondition(event_id: str, condition: dict[str, Any], env) -> None:
    server = condition.get("server")
    tool = condition.get("tool")
    if not server or not tool:
        raise ValueError(f"mutation {event_id} has invalid postcondition {condition!r}")
    if tool in SIDE_EFFECTING_POSTCONDITION_TOOLS:
        raise ValueError(f"mutation {event_id} postcondition tool {tool!r} is side-effecting")
    if getattr(env, f"{server}_mock", None) is None:
        raise RuntimeError(f"mutation {event_id}: missing capability for postcondition {server!r}")
    if not any(key in condition for key in ("contains", "not_contains", "equals", "expect")):
        raise ValueError(f"mutation {event_id} postcondition has no assertion")


def _apply_postconditions(event: dict[str, Any], env) -> list[dict[str, Any]]:
    conditions = event.get("postconditions") or []
    if not conditions:
        raise ValueError(f"mutation {event.get('id')} has no observable postconditions")
    results: list[dict[str, Any]] = []
    for condition_index, condition in enumerate(conditions):
        _validate_postcondition(str(event.get("id") or "mutation"), condition, env)
        failed_condition = {
            "kind": "postcondition",
            "index": condition_index,
            "spec": _jsonable(condition),
        }
        server = str(condition["server"])
        tool = str(condition["tool"])
        args = dict(condition.get("args") or {})
        try:
            value = _call_observation(getattr(env, f"{server}_mock"), tool, args)
        except Exception as error:
            evidence = {
                "server": server,
                "tool": tool,
                "args": _jsonable(args),
                "passed": False,
                "exception": {"type": type(error).__name__, "message": str(error)},
            }
            raise PostconditionEvaluationError(
                f"mutation {event.get('id')} postcondition call failed for {server}.{tool}: {error}",
                results + [evidence],
                failed_condition,
            ) from error
        if _has_failure_signal(value):
            evidence = {
                "server": server,
                "tool": tool,
                "args": _jsonable(args),
                "value": _jsonable(value),
                "passed": False,
                "failure_signal": True,
            }
            raise PostconditionEvaluationError(
                f"mutation {event.get('id')} postcondition call failed for {server}.{tool}: {value!r}",
                results + [evidence],
                failed_condition,
            )
        blob = json.dumps(value, ensure_ascii=False, default=str).lower()
        missing = [str(term) for term in condition.get("contains") or [] if str(term).lower() not in blob]
        forbidden = [str(term) for term in condition.get("not_contains") or [] if str(term).lower() in blob]
        structured_ok = True
        if "expect" in condition:
            expected = condition["expect"]
            structured_ok = (
                _value_matches(value, expected)
                or any(_value_matches(candidate, expected) for candidate in _iter_mappings(value))
            )
        if "equals" in condition:
            equals = condition["equals"]
            structured_ok = structured_ok and (
                _value_matches(value, equals)
                or any(_value_matches(candidate, equals) for candidate in _iter_mappings(value))
            )
        evidence = {
            "server": server,
            "tool": tool,
            "args": _jsonable(args),
            "value": _jsonable(value),
            "missing": missing,
            "forbidden": forbidden,
            "structured_ok": structured_ok,
            "passed": not missing and not forbidden and structured_ok,
        }
        if not evidence["passed"]:
            raise PostconditionEvaluationError(
                f"mutation {event.get('id')} postcondition failed for {server}.{tool}; "
                f"missing={missing!r}, forbidden={forbidden!r}, value={blob[:1200]!r}",
                results + [evidence],
                failed_condition,
            )
        results.append(evidence)
    return results


def _postconditions_satisfied(event: dict[str, Any], env) -> bool:
    try:
        _apply_postconditions(event, env)
    except Exception:
        return False
    return True


def _checkpoint_label(event_id: str, server: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in f"{event_id}_{server}")
    return safe[:96] or "mutation"


def _create_runtime_checkpoint(capability: Any, label: str) -> Any:
    method = getattr(capability, "create_runtime_checkpoint", None)
    if callable(method):
        return method(label)
    exec_python = getattr(capability, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoints")
    runtime_db = str(getattr(capability, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    backup_path = f"/tmp/{label}.runtime-backup.db"
    exec_python(
        "import os, sqlite3\n"
        f"src_path={runtime_db!r}\nbackup_path={backup_path!r}\n"
        "try:\n os.remove(backup_path)\nexcept FileNotFoundError:\n pass\n"
        "src=sqlite3.connect(src_path,isolation_level=None,timeout=30)\n"
        "dst=sqlite3.connect(backup_path,isolation_level=None,timeout=30)\n"
        "src.backup(dst)\ndst.close()\nsrc.close()\n"
    )
    return backup_path


def _restore_runtime_checkpoint(capability: Any, token: Any) -> None:
    method = getattr(capability, "restore_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(capability, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoint restore")
    runtime_db = str(getattr(capability, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    exec_python(
        "import sqlite3\n"
        f"src=sqlite3.connect({str(token)!r},isolation_level=None,timeout=30)\n"
        f"dst=sqlite3.connect({runtime_db!r},isolation_level=None,timeout=30)\n"
        "src.backup(dst)\ndst.close()\nsrc.close()\n"
    )


def _delete_runtime_checkpoint(capability: Any, token: Any) -> None:
    method = getattr(capability, "delete_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(capability, "_exec_python", None)
    if callable(exec_python):
        exec_python(f"import os\ntry:\n os.remove({str(token)!r})\nexcept FileNotFoundError:\n pass\n")


def _preflight_mutation_event(
    event: dict[str, Any],
    env,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    event_id = str(event.get("id") or "mutation")
    specs = list(event.get("apply") or [])
    if not specs:
        raise MutationPreflightError(
            f"mutation {event_id} has no state changes",
            None,
            [],
        )
    if not event.get("postconditions"):
        raise MutationPreflightError(
            f"mutation {event_id} has no observable postconditions",
            None,
            [],
        )

    capabilities: dict[str, Any] = {}
    preflighted_specs: list[dict[str, Any]] = []
    for index, spec in enumerate(specs):
        failed_spec = {"kind": "preflight", "index": index, "spec": _jsonable(spec)}
        server = spec.get("server")
        if not server:
            raise MutationPreflightError(
                f"mutation {event_id}: missing server in apply spec {index}",
                failed_spec,
                preflighted_specs,
            )
        capability = getattr(env, f"{server}_mock", None)
        if capability is None:
            raise MutationPreflightError(
                f"mutation {event_id}: missing capability {server!r}",
                failed_spec,
                preflighted_specs,
            )
        if not callable(getattr(capability, "create_runtime_checkpoint", None)) and not callable(
            getattr(capability, "_exec_python", None)
        ):
            raise MutationPreflightError(
                f"mutation {event_id}: capability {server!r} cannot checkpoint",
                failed_spec,
                preflighted_specs,
            )

        if "sql_file" in spec:
            sql_path = THIS_DIR / str(spec["sql_file"])
            if not sql_path.is_file() or sql_path.stat().st_size == 0:
                raise MutationPreflightError(
                    f"mutation {event_id}: SQL file missing or empty: {sql_path}",
                    failed_spec,
                    preflighted_specs,
                )
            if not callable(getattr(capability, "apply_sql_file", None)):
                raise MutationPreflightError(
                    f"mutation {event_id}: capability {server!r} apply_sql_file is not callable",
                    failed_spec,
                    preflighted_specs,
                )
        elif "tool_call" in spec:
            tool_call = spec.get("tool_call")
            tool_name = str(_field(tool_call, "name", "") or "")
            if not tool_name:
                raise MutationPreflightError(
                    f"mutation {event_id}: apply tool_call {index} has no tool name",
                    failed_spec,
                    preflighted_specs,
                )
            if not callable(getattr(capability, "call_tool", None)) and not callable(
                getattr(capability, tool_name, None)
            ):
                raise MutationPreflightError(
                    f"mutation {event_id}: capability {server!r} call_tool/{tool_name} is not callable",
                    failed_spec,
                    preflighted_specs,
                )
        elif not callable(getattr(capability, "apply_mutation", None)):
            raise MutationPreflightError(
                f"mutation {event_id}: capability {server!r} apply_mutation is not callable",
                failed_spec,
                preflighted_specs,
            )

        capabilities[str(server)] = capability
        preflighted_specs.append(_jsonable(spec))

    for index, condition in enumerate(event.get("postconditions") or []):
        failed_condition = {"kind": "postcondition", "index": index, "spec": _jsonable(condition)}
        try:
            _validate_postcondition(event_id, condition, env)
        except Exception as error:
            raise MutationPreflightError(
                f"mutation {event_id}: postcondition preflight failed at index {index}: {error}",
                failed_condition,
                preflighted_specs,
            ) from error
        server = str(condition["server"])
        tool = str(condition["tool"])
        capability = getattr(env, f"{server}_mock")
        if not callable(getattr(capability, "call_tool", None)) and not callable(
            getattr(capability, tool, None)
        ):
            raise MutationPreflightError(
                f"mutation {event_id}: observational tool {server}.{tool} is not callable",
                failed_condition,
                preflighted_specs,
            )
    return capabilities, preflighted_specs


def _mutation_failure_audit(
    event: dict[str, Any],
    error: Exception,
    requested_specs: list[dict[str, Any]],
    preflighted_specs: list[dict[str, Any]],
    actually_applied_specs: list[dict[str, Any]],
    failed_spec: Any,
    rollback_result: dict[str, Any],
    postcondition_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "event_id": str(event.get("id") or "mutation"),
        "stage": event.get("stage"),
        "requested_specs": _jsonable(requested_specs),
        "preflighted_specs": _jsonable(preflighted_specs),
        "actually_applied_specs": _jsonable(actually_applied_specs),
        "failed_spec": _jsonable(failed_spec),
        "exception": {"type": type(error).__name__, "message": str(error)},
        "rollback_result": _jsonable(rollback_result),
        "postcondition_evidence": _jsonable(postcondition_evidence),
        "postconditions_passed": False,
        "already_satisfied": False,
        "trial_invalid": True,
        "completed_at": _now(),
    }


def _apply_mutation_event(event: dict[str, Any], env) -> dict[str, Any]:
    event_id = str(event.get("id") or "mutation")
    specs = list(event.get("apply") or [])
    requested_specs = [_jsonable(spec) for spec in specs]
    preflighted_specs: list[dict[str, Any]] = []
    actually_applied_specs: list[dict[str, Any]] = []
    failed_spec: Any = (
        {"kind": "preflight", "index": 0, "spec": requested_specs[0]}
        if requested_specs else None
    )
    checkpoints: list[tuple[Any, Any]] = []
    writes_started = False
    rollback_result = {"attempted": False, "succeeded": False, "errors": []}
    postcondition_evidence: list[dict[str, Any]] = []
    try:
        capabilities, preflighted_specs = _preflight_mutation_event(event, env)
        if _postconditions_satisfied(event, env):
            postcondition_results = _apply_postconditions(event, env)
            return {
                "event_id": event_id,
                "stage": event.get("stage"),
                "requested_specs": requested_specs,
                "preflighted_specs": preflighted_specs,
                "actually_applied_specs": [],
                "postcondition_results": postcondition_results,
                "postconditions_passed": True,
                "already_satisfied": True,
                "completed_at": _now(),
            }

        for server, capability in capabilities.items():
            failed_spec = {"kind": "checkpoint", "server": server}
            checkpoints.append((
                capability,
                _create_runtime_checkpoint(capability, _checkpoint_label(event_id, server)),
            ))
        for index, spec in enumerate(specs):
            failed_spec = {"kind": "apply", "index": index, "spec": _jsonable(spec)}
            capability = capabilities[str(spec["server"])]
            writes_started = True
            if "sql_file" in spec:
                capability.apply_sql_file(THIS_DIR / str(spec["sql_file"]))
            elif "tool_call" in spec:
                tool_call = spec["tool_call"]
                result = _call_observation(
                    capability,
                    str(tool_call["name"]),
                    dict(tool_call.get("args") or {}),
                )
                if _has_failure_signal(result):
                    raise RuntimeError(f"mutation {event_id} tool call failed: {result!r}")
            else:
                capability.apply_mutation(spec)
            actually_applied_specs.append(_jsonable(spec))

        failed_spec = {
            "kind": "postcondition",
            "index": 0,
            "spec": _jsonable((event.get("postconditions") or [None])[0]),
        }
        postcondition_results = _apply_postconditions(event, env)
    except Exception as error:
        if isinstance(error, MutationPreflightError):
            preflighted_specs = list(error.preflighted_specs)
            failed_spec = error.failed_spec
        if isinstance(error, PostconditionEvaluationError):
            postcondition_evidence = list(error.evidence)
            failed_spec = error.failed_condition
        elif isinstance(failed_spec, dict) and failed_spec.get("kind") == "postcondition":
            postcondition_evidence = [{
                "conditions": _jsonable(event.get("postconditions") or []),
                "passed": False,
                "exception": {"type": type(error).__name__, "message": str(error)},
            }]
        if checkpoints and writes_started:
            rollback_result["attempted"] = True
            rollback_errors: list[str] = []
            for capability, token in reversed(checkpoints):
                try:
                    _restore_runtime_checkpoint(capability, token)
                except Exception as rollback_error:
                    rollback_errors.append(f"{type(rollback_error).__name__}: {rollback_error}")
            rollback_result["errors"] = rollback_errors
            rollback_result["succeeded"] = not rollback_errors
        audit = _mutation_failure_audit(
            event,
            error,
            requested_specs,
            preflighted_specs,
            actually_applied_specs,
            failed_spec,
            rollback_result,
            postcondition_evidence,
        )
        detail = f"mutation {event_id} failed: {error}"
        if rollback_result["errors"]:
            detail += f"; rollback errors={rollback_result['errors']}"
        raise MutationExecutionError(detail, audit) from error
    finally:
        for capability, token in reversed(checkpoints):
            try:
                _delete_runtime_checkpoint(capability, token)
            except Exception as cleanup_error:
                logger.warning(f"checkpoint cleanup for {event_id} raised {type(cleanup_error).__name__}: {cleanup_error}")

    return {
        "event_id": event_id,
        "stage": event.get("stage"),
        "requested_specs": requested_specs,
        "preflighted_specs": preflighted_specs,
        "actually_applied_specs": actually_applied_specs,
        "postcondition_results": postcondition_results,
        "postconditions_passed": True,
        "already_satisfied": False,
        "completed_at": _now(),
    }


def _safe_filename(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)[:120]


def _checked_shell_exec(env, command: str, *, context: str = "persist") -> Any:
    try:
        result = env.workspace.shell.exec(command, user="root")
    except Exception as error:
        raise TrialInvalidError(f"{context} command raised: {command}: {error}") from error
    if isinstance(result, dict):
        returncode = result.get("returncode")
        if returncode is None:
            returncode = result.get("exit_code")
        stderr = result.get("stderr", "")
    else:
        returncode = getattr(result, "returncode", None)
        if returncode is None:
            returncode = getattr(result, "exit_code", None)
        stderr = getattr(result, "stderr", "")
    if returncode is None:
        raise TrialInvalidError(f"{context} command returned no exit status: {command}")
    if returncode != 0:
        raise TrialInvalidError(
            f"{context} command failed ({returncode}): {command}; {stderr}"
        )
    return result


def _atomic_write(env, path: str, payload: dict[str, Any] | list[Any] | str) -> None:
    data = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    encoded = data.encode("utf-8")
    temp_path = f"{path}.tmp"
    env.workspace.fs.write_file(temp_path, encoded)
    _checked_shell_exec(env, f"mv -f {temp_path} {path}")
    try:
        persisted = env.workspace.fs.read_file(path)
    except Exception as exc:
        raise RuntimeError(f"persist read-back failed for {path}: {exc}") from exc
    if persisted != encoded:
        raise RuntimeError(f"persist read-back mismatch for {path}")


def _persist_mutation_audit(env, stage: int, audit: dict[str, Any]) -> dict[str, Any]:
    payload = dict(audit)
    payload["stage"] = stage
    path = f"{MUTATION_AUDIT_DIR}/stage_{stage:02d}_{_safe_filename(str(payload.get('event_id') or 'mutation'))}.json"
    _atomic_write(env, path, payload)
    return payload


def _persist_stage_result(
    env,
    stage: int,
    checks_spec,
    checks: list[Check],
    total_weight: float,
    passed_weight: float,
    response_path: str,
    trace_path: str,
) -> dict[str, Any]:
    weights = {str(check_id): float(weight) for check_id, _function, weight in checks_spec}
    payload = {
        "stage": stage,
        "checks": [
            {
                "check_id": str(getattr(check, "name", "")),
                "passed": bool(getattr(check, "passed", False)),
                "weight": weights.get(str(getattr(check, "name", "")), 0.0),
            }
            for check in checks
        ],
        "passed_weight": float(passed_weight),
        "total_weight": float(total_weight),
        "score": (float(passed_weight) / float(total_weight)) if total_weight else 0.0,
        "response_path": response_path,
        "trace_path": trace_path,
        "completed_at": _now(),
        "frozen": True,
    }
    _atomic_write(env, f"{STAGE_RESULT_DIR}/stage_{stage:02d}.json", payload)
    return payload


def _read_required_artifact(env, path: str, label: str) -> bytes:
    try:
        data = env.workspace.fs.read_file(path)
    except Exception as error:
        raise RuntimeError(f"{label} artifact is unreadable: {path}: {error}") from error
    if isinstance(data, str):
        return data.encode("utf-8")
    if not isinstance(data, bytes):
        raise RuntimeError(f"{label} artifact is unreadable: {path}: expected bytes, got {type(data).__name__}")
    return data


def _stage_weight(payload: dict[str, Any], field: str, stage: int) -> float:
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise RuntimeError(f"frozen Stage {stage} has invalid {field}: {value!r}")
    return float(value)


def _validate_frozen_stage_results(
    env,
    frozen_results: list[dict[str, Any]],
    stage_count: int,
) -> list[dict[str, Any]]:
    if len(frozen_results) != stage_count:
        raise RuntimeError(f"expected {stage_count} collected frozen Stage results, got {len(frozen_results)}")

    collected_by_stage: dict[int, dict[str, Any]] = {}
    for payload in frozen_results:
        if not isinstance(payload, dict) or payload.get("frozen") is not True:
            raise RuntimeError("all collected Stage results must be frozen payloads")
        stage = payload.get("stage")
        if isinstance(stage, bool) or not isinstance(stage, int):
            raise RuntimeError(f"collected frozen Stage result has invalid stage: {stage!r}")
        if stage in collected_by_stage:
            raise RuntimeError(f"collected frozen Stage identifiers must be unique; duplicate={stage}")
        collected_by_stage[stage] = payload

    persisted_results: list[dict[str, Any]] = []
    persisted_stages: list[int] = []
    for expected_stage in range(stage_count):
        stage_path = f"{STAGE_RESULT_DIR}/stage_{expected_stage:02d}.json"
        raw = _read_required_artifact(env, stage_path, f"Stage result stage_{expected_stage:02d}")
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError(f"Stage result stage_{expected_stage:02d} is not valid JSON: {error}") from error
        if not isinstance(payload, dict):
            raise RuntimeError(f"Stage result stage_{expected_stage:02d} must be a JSON object")
        stage = payload.get("stage")
        if isinstance(stage, bool) or not isinstance(stage, int):
            raise RuntimeError(f"Stage result stage_{expected_stage:02d} has invalid stage: {stage!r}")
        persisted_stages.append(stage)
        persisted_results.append(payload)

    if len(set(persisted_stages)) != stage_count:
        raise RuntimeError(f"persisted Stage identifiers must be unique; got {persisted_stages}")
    if set(persisted_stages) != set(range(stage_count)):
        raise RuntimeError(f"persisted Stage identifiers must cover 0..{stage_count - 1}; got {persisted_stages}")

    validated: list[dict[str, Any]] = []
    for payload in sorted(persisted_results, key=lambda item: int(item["stage"])):
        stage = int(payload["stage"])
        if payload.get("frozen") is not True:
            raise RuntimeError(f"persisted Stage {stage} is not frozen")
        if collected_by_stage.get(stage) != payload:
            raise RuntimeError(f"collected and persisted frozen Stage {stage} payloads differ")

        response_path = payload.get("response_path")
        trace_path = payload.get("trace_path")
        if not isinstance(response_path, str) or not response_path:
            raise RuntimeError(f"frozen Stage {stage} has invalid response path")
        if not isinstance(trace_path, str) or not trace_path:
            raise RuntimeError(f"frozen Stage {stage} has invalid trace path")
        _read_required_artifact(env, response_path, f"Stage {stage} response")
        trace_data = _read_required_artifact(env, trace_path, f"Stage {stage} trace")
        try:
            trace_payload = json.loads(trace_data)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError(f"Stage {stage} trace is not valid JSON: {trace_path}: {error}") from error
        if not isinstance(trace_payload, list):
            raise RuntimeError(f"Stage {stage} trace must be a JSON list: {trace_path}")

        checks = payload.get("checks")
        if not isinstance(checks, list):
            raise RuntimeError(f"frozen Stage {stage} checks must be a list")
        check_total = 0.0
        check_passed = 0.0
        for check in checks:
            if not isinstance(check, dict) or not str(check.get("check_id") or ""):
                raise RuntimeError(f"frozen Stage {stage} contains an invalid check entry")
            weight = _stage_weight(check, "weight", stage)
            if weight < 0:
                raise RuntimeError(f"frozen Stage {stage} contains a negative check weight")
            check_total += weight
            if check.get("passed") is True:
                check_passed += weight
        total_weight = _stage_weight(payload, "total_weight", stage)
        passed_weight = _stage_weight(payload, "passed_weight", stage)
        if total_weight < 0 or passed_weight < 0 or passed_weight > total_weight:
            raise RuntimeError(f"frozen Stage {stage} has invalid passed/total weights")
        if abs(check_total - total_weight) > 1e-9 or abs(check_passed - passed_weight) > 1e-9:
            raise RuntimeError(f"frozen Stage {stage} check weights do not match passed/total weights")
        validated.append(payload)
    return validated


def _extract_full_trace(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    """Persist ordered calls/results while exposing only successful one-to-one pairs to scoring."""
    trace: list[dict[str, Any]] = []
    call_rows_by_id: dict[str, list[dict[str, Any]]] = {}
    result_rows_by_id: dict[str, list[dict[str, Any]]] = {}
    for message in messages or []:
        role = str(_field(message, "role", "") or "")
        content = _field(message, "content", "")
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            block_type = str(_field(block, "type", "") or "")
            if block_type in {"toolCall", "tool_call", "tool_use", "function_call"}:
                function = _field(block, "function")
                call_id = str(
                    _field(
                        block,
                        "tool_use_id",
                        _field(block, "toolUseId", _field(block, "id", "")),
                    )
                    or ""
                )
                attempted_name = str(
                    _field(function, "name", _field(block, "name", ""))
                    if function is not None else _field(block, "name", "")
                )
                arguments = (
                    _field(function, "arguments", _field(block, "arguments", _field(block, "input", {})))
                    if function is not None else _field(block, "arguments", _field(block, "input", {}))
                )
                row = {
                    "event_id": event_id,
                    "role": role,
                    "type": "tool_call",
                    "id": call_id,
                    "name": "",
                    "attempted_name": attempted_name,
                    "arguments": _jsonable(arguments),
                    "paired": False,
                    "success": False,
                }
                trace.append(row)
                call_rows_by_id.setdefault(call_id, []).append(row)
            elif block_type in {"toolResult", "tool_result", "tool_response", "function_result"}:
                call_id = str(
                    _field(
                        block,
                        "tool_use_id",
                        _field(
                            block,
                            "toolUseId",
                            _field(
                                block,
                                "toolCallId",
                                _field(block, "tool_call_id", _field(block, "id", "")),
                            ),
                        ),
                    )
                    or ""
                )
                result = _jsonable(
                    _field(block, "content", _field(block, "result", _field(block, "output", "")))
                )
                failure_probe = {
                    "is_error": bool(_field(block, "is_error", _field(block, "isError", False))),
                    "result": result,
                }
                row = {
                    "event_id": event_id,
                    "role": role,
                    "type": "tool_result",
                    "id": call_id,
                    "name": "",
                    "attempted_name": str(_field(block, "name", "") or ""),
                    "result": result,
                    "paired": False,
                    "success": not _has_failure_signal(failure_probe),
                }
                trace.append(row)
                result_rows_by_id.setdefault(call_id, []).append(row)

    for call_id, call_rows in call_rows_by_id.items():
        result_rows = result_rows_by_id.get(call_id, [])
        paired = bool(call_id) and len(call_rows) == 1 and len(result_rows) == 1
        result_success = paired and result_rows[0].get("success") is True
        attempted_name = str(call_rows[0].get("attempted_name") or "")
        call_rows[0]["paired"] = paired
        call_rows[0]["success"] = result_success
        call_rows[0]["name"] = attempted_name if result_success else ""
        if paired:
            result_rows[0]["paired"] = True
            result_rows[0]["attempted_name"] = attempted_name
            result_rows[0]["name"] = attempted_name if result_success else ""
    return trace


def _extract_tool_calls(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    """Backward-compatible alias retained for existing tests and checker helpers."""
    return _extract_full_trace(messages, event_id)


def _extract_assistant_text(messages) -> str:
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
            if _field(block, "type") == "text" and _field(block, "text", ""):
                chunks.append(str(_field(block, "text")))
    return "\n".join(chunks)


def _dispatch_event(event: dict[str, Any], env, agent, stage: int) -> tuple[str, list[dict[str, Any]], dict[str, Any] | None]:
    kind = event.get("kind", "")
    if kind == "mutation":
        staged_event = dict(event)
        staged_event["stage"] = stage
        try:
            audit = _apply_mutation_event(staged_event, env)
        except MutationExecutionError as error:
            _persist_mutation_audit(env, stage, error.audit)
            raise
        except Exception as error:
            rollback_result = {"attempted": False, "succeeded": False, "errors": []}
            requested_specs = [_jsonable(spec) for spec in staged_event.get("apply") or []]
            failed_spec = (
                {"kind": "preflight", "index": 0, "spec": requested_specs[0]}
                if requested_specs else None
            )
            audit = _mutation_failure_audit(
                staged_event,
                error,
                requested_specs,
                [],
                [],
                failed_spec,
                rollback_result,
                [],
            )
            _persist_mutation_audit(env, stage, audit)
            raise TrialInvalidError(
                f"mutation {staged_event.get('id') or 'mutation'} failed: "
                f"{type(error).__name__}: {error}"
            ) from error
        _persist_mutation_audit(env, stage, audit)
        return "", [], audit
    if event.get("silent"):
        return "", [], None
    if kind not in {"user_message", "notification", "world"}:
        raise ValueError(f"event {event.get('id')}: unknown kind {kind!r}")
    result = agent.act(_render_event(event))
    messages = getattr(result, "messages", []) or []
    return _extract_assistant_text(messages), _extract_tool_calls(messages, event.get("id")), None


def _limit_text(text: str) -> str:
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return text[:MAX_STAGE_RESPONSE_CHARS] + f"\n\n[TRUNCATED: response exceeded {MAX_STAGE_RESPONSE_CHARS} chars]"


def _run_rubric_checks(checks_spec, env, tag: str) -> tuple[list[Check], float, float]:
    checks: list[Check] = []
    total_weight = 0.0
    passed_weight = 0.0
    for check_id, function, weight in checks_spec:
        try:
            passed = bool(function(env))
        except Exception as error:
            raise TrialInvalidError(
                f"checker {check_id!r} in {tag} raised {type(error).__name__}: {error}"
            ) from error
        checks.append(Check(name=check_id, passed=passed, tags=[tag]))
        total_weight += float(weight)
        if passed:
            passed_weight += float(weight)
    return checks, total_weight, passed_weight


@entry(
    capabilities=[
        "email_mock", "calendar_mock", "notion_mock", "maps_mock",
        "review_platform_mock", "banking_mock", "notification_hub_mock", "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def factory_visit_safety_day(env, agent):
    _register_all_mcp(env, agent)
    _bootstrap_workspace(env)
    _preflight_authoritative_backends(env)
    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    stage_modules = {stage: _load_rubric(f"stage_{stage}") for stage in range(stage_count)}
    final_module = _load_rubric("final")
    cross_module = _load_rubric("cross_stage")
    tool_module = _load_rubric("tool_quality")

    frozen_results: list[dict[str, Any]] = []

    for stage in range(stage_count):
        stage_texts: list[str] = []
        stage_calls: list[dict[str, Any]] = []
        for event in sorted(events_by_stage[stage], key=lambda item: (str(item.get("time", "")), str(item.get("id", "")))):
            text, calls, _audit = _dispatch_event(event, env, agent, stage)
            if text:
                stage_texts.append(_limit_text(text))
            stage_calls.extend(calls)

        response_path = f"{RESPONSES_DIR}/stage_{stage}.txt"
        trace_path = f"{TRACE_DIR}/stage_{stage}.json"
        _atomic_write(env, response_path, "\n---\n".join(stage_texts))
        _atomic_write(env, trace_path, stage_calls)
        checks_spec = stage_modules[stage].CHECKS
        checks, stage_total, stage_passed = _run_rubric_checks(checks_spec, env, f"stage{stage}")
        frozen_results.append(_persist_stage_result(
            env, stage, checks_spec, checks, stage_total, stage_passed, response_path, trace_path
        ))

    validated_frozen_results = _validate_frozen_stage_results(env, frozen_results, stage_count)
    all_checks = [
        Check(name=str(check["check_id"]), passed=bool(check["passed"]), tags=[f"stage{payload['stage']}"])
        for payload in validated_frozen_results
        for check in payload["checks"]
    ]
    total_weight = sum(float(payload["total_weight"]) for payload in validated_frozen_results)
    passed_weight = sum(float(payload["passed_weight"]) for payload in validated_frozen_results)

    for name, module in (("cross_stage", cross_module), ("tool_quality", tool_module), ("final", final_module)):
        checks, bucket_total, bucket_passed = _run_rubric_checks(module.CHECKS, env, name)
        all_checks.extend(checks)
        total_weight += bucket_total
        passed_weight += bucket_passed

    if abs(total_weight - 100.0) > 1e-9:
        raise RuntimeError(f"rubric total weight must be 100, got {total_weight}")
    score = passed_weight / total_weight
    logger.info(f"factory score: passed_weight={passed_weight:.2f} total_weight={total_weight:.2f} score={score:.3f}")
    return CheckerResults(checks=all_checks, score=score)
