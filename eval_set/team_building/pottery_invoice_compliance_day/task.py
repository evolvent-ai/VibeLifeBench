"""Pottery invoice-compliance team-building benchmark runtime."""
from __future__ import annotations

from datetime import datetime, timezone
import importlib
import json
import re
import sys
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
STAGE_RESULTS_DIR = "/terrarium/stage_results"
MAX_STAGE_RESPONSE_CHARS = 20000
USER_ID = "user_luyao_tb011"

_AUTHORITATIVE_BACKEND_PROBES: tuple[tuple[str, str, dict[str, Any]], ...] = (
    ("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 1}),
    ("calendar", "list_events", {"max_results": 1}),
    ("notion", "API-post-search", {"query": "", "filter": {"value": "page"}, "page_size": 1}),
    ("review_platform", "search_merchants", {"category": "venue", "city": "天津", "limit": 1}),
    ("maps", "search_places", {"query": "天津", "limit": 1}),
    ("credit_card", "list_cards", {"user_id": USER_ID}),
    ("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 1}),
)

_CAPABILITIES_CONFIG = agent_caps_config(
    email_mock="pottery_invoice_compliance_day",
    calendar_mock="pottery_invoice_compliance_day",
    notion_mock="pottery_invoice_compliance_day",
    review_platform_mock="pottery_invoice_compliance_day",
    maps_mock="pottery_invoice_compliance_day",
    credit_card_mock="pottery_invoice_compliance_day",
    notification_hub_mock="pottery_invoice_compliance_day",
)


class TrialInvalidError(RuntimeError):
    """A required runtime invariant failed, so the trial must not be scored."""

    trial_invalid = True


def _rubric_pkg_name() -> str:
    name = f"_task_{THIS_DIR.name.replace('.', '_')}_rubrics"
    if name not in sys.modules:
        package = ModuleType(name)
        package.__path__ = [str(THIS_DIR / "rubrics")]
        package.__package__ = name
        sys.modules[name] = package
    return name


_RUBRIC_PKG = _rubric_pkg_name()


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
        if candidate is not None and isinstance(
            candidate, (dict, list, str, int, float, bool)
        ):
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
            f"backend protocol error for {server}.{tool}: unsupported response "
            f"{type(candidate).__name__}"
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
                text_signals = (
                    ("database is locked", "DB_LOCKED"),
                    ("db locked", "DB_LOCKED"),
                    ("service unavailable", "SERVICE_UNAVAILABLE"),
                    ("deadline exceeded", "TIMEOUT"),
                    ("timed out", "TIMEOUT"),
                    ("timeout", "TIMEOUT"),
                    ("internal server error", "INTERNAL_ERROR"),
                )
                for phrase, signal in text_signals:
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


def _load_events(path: Path) -> tuple[int, dict[int, list[dict[str, Any]]]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("stages"), dict):
        raise ValueError("event.yaml must contain a stages mapping")
    by_stage: dict[int, list[dict[str, Any]]] = {}
    for key, events in raw["stages"].items():
        stage = int(key)
        if not isinstance(events, list):
            raise ValueError(f"stage {stage} must be a list")
        by_stage[stage] = [dict(event) for event in events]
    expected = list(range(25))
    if sorted(by_stage) != expected:
        raise ValueError(f"event.yaml stages must be {expected}, got {sorted(by_stage)}")
    return 25, by_stage


def _load_rubric(name: str):
    module = importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    checks = getattr(module, "CHECKS", None)
    if not isinstance(checks, list) or not checks:
        raise RuntimeError(f"rubric module {name!r} must define non-empty CHECKS")
    return module


def _render_event(event: dict[str, Any]) -> str:
    when = event.get("time", "")
    kind = event.get("kind", "")
    body = event.get("body", "") or ""
    if kind == "user_message":
        tag = f"[来自 {event.get('from') or 'user'} 的消息 @ {when}]"
    elif kind == "notification":
        tag = f"[通知 @ {when}，来源 {event.get('source') or event.get('channel') or 'system'}]"
    elif kind == "world":
        tag = f"[世界事件 @ {when}，来源 {event.get('source') or 'system'}]"
    else:
        tag = f"[{kind} @ {when}]"
    return f"{tag}\n{body}"


def _field(value: Any, name: str, default: Any = None) -> Any:
    return value.get(name, default) if isinstance(value, dict) else getattr(value, name, default)


def _jsonable(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
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
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def _failure_text(value: str) -> bool:
    text = value.strip()
    if not text:
        return False
    try:
        return _has_failure_signal(json.loads(text))
    except Exception:
        return bool(re.search(
            r"(?i)(?:^|[\s\[{(:;,])(?:tool[_ -]?error|error|failure|exception|traceback)(?:\b|\s*[:：])",
            text,
        ))


def _has_failure_signal(value: Any) -> bool:
    value = _jsonable(value)
    if isinstance(value, str):
        return _failure_text(value)
    if isinstance(value, (list, tuple)):
        return any(_has_failure_signal(item) for item in value)
    if not isinstance(value, dict):
        return False
    normalized = {str(key).lower().replace("_", ""): item for key, item in value.items()}
    for key in ("iserror", "error", "failed", "failure"):
        if key in normalized and normalized[key] not in (None, False, "", 0, [], {}):
            return True
    for key in ("success", "ok"):
        if key in normalized and normalized[key] is False:
            return True
    if str(normalized.get("status") or "").lower() in {"error", "failed", "failure", "fail", "exception"}:
        return True
    return any(_has_failure_signal(item) for item in value.values())


def _result_success(value: Any) -> bool:
    return not _has_failure_signal(_decode_tool_value(value))


def _iter_mappings(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _iter_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_mappings(child)


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


def _structured_match(value: Any, expected: dict[str, Any]) -> bool:
    return not expected or any(_value_matches(candidate, expected) for candidate in _iter_mappings(value))


_SIDE_EFFECTING_POSTCONDITION_TOOLS = {
    "transfer", "pay_payee", "make_payment", "send_email", "reply_email", "forward_email",
    "save_draft", "update_draft", "create_event", "update_event", "delete_event",
    "API-post-page", "API-patch-page", "API-patch-block-children", "API-update-a-block",
}


def _validate_postcondition_tool(event_id: str, tool: str) -> None:
    if tool in _SIDE_EFFECTING_POSTCONDITION_TOOLS:
        raise ValueError(f"event {event_id}: postcondition tool {tool!r} is not observational")


def _invoke_observer(capability, tool: str, args: dict[str, Any]) -> Any:
    direct = getattr(capability, tool, None)
    if callable(direct):
        return _decode_tool_value(direct(**args))
    call_tool = getattr(capability, "call_tool", None)
    if not callable(call_tool):
        raise RuntimeError(f"capability does not expose observer {tool!r}")
    return _decode_tool_value(call_tool(tool, **args))


def _apply_postconditions(event: dict[str, Any], env) -> list[dict[str, Any]]:
    conditions = event.get("postconditions") or []
    if not conditions:
        raise ValueError(f"mutation {event.get('id')} has no observable postconditions")
    evidence: list[dict[str, Any]] = []
    for index, condition in enumerate(conditions):
        server = condition.get("server")
        tool = condition.get("tool")
        observed: Any = None
        has_observed = False
        try:
            if not server or not tool:
                raise ValueError(f"event {event.get('id')} has invalid postcondition: {condition}")
            _validate_postcondition_tool(str(event.get("id") or "mutation"), str(tool))
            capability = getattr(env, f"{server}_mock", None)
            if capability is None:
                raise RuntimeError(f"event {event.get('id')}: no capability for postcondition {server!r}")
            observed = _invoke_observer(capability, str(tool), dict(condition.get("args") or {}))
            has_observed = True
            if not _result_success(observed):
                raise RuntimeError(
                    f"event {event.get('id')} postcondition call failed for {server}.{tool}: {observed!r}"
                )
            assertion_ok = True
            if "expect" in condition:
                expected = condition["expect"]
                assertion_ok = (
                    _value_matches(observed, expected)
                    or any(_value_matches(candidate, expected) for candidate in _iter_mappings(observed))
                )
            if "equals" in condition:
                expected = condition["equals"]
                assertion_ok = assertion_ok and (
                    _value_matches(observed, expected)
                    or any(_value_matches(candidate, expected) for candidate in _iter_mappings(observed))
                )
            if not assertion_ok:
                raise RuntimeError(f"event {event.get('id')} postcondition fields missing for {server}.{tool}")
            blob = json.dumps(observed, ensure_ascii=False, default=str).lower()
            missing = [str(term) for term in condition.get("contains") or [] if str(term).lower() not in blob]
            forbidden = [str(term) for term in condition.get("not_contains") or [] if str(term).lower() in blob]
            if missing or forbidden:
                raise RuntimeError(
                    f"event {event.get('id')} postcondition failed for {server}.{tool}; "
                    f"missing={missing!r}, forbidden={forbidden!r}"
                )
            evidence.append({
                "server": server,
                "tool": tool,
                "passed": True,
                "observed": _jsonable(observed),
            })
        except Exception as exc:
            failure_evidence = list(evidence)
            failed_row = {
                "server": server,
                "tool": tool,
                "passed": False,
                "error": {"type": type(exc).__name__, "message": str(exc)},
            }
            if has_observed:
                failed_row["observed"] = _jsonable(observed)
            failure_evidence.append(failed_row)
            exc.postcondition_evidence = failure_evidence
            exc.failed_postcondition = {
                "kind": "postcondition",
                "index": index,
                "spec": _jsonable(condition),
            }
            raise
    return evidence


def _postconditions_satisfied(event: dict[str, Any], env) -> bool:
    try:
        _apply_postconditions(event, env)
    except Exception:
        return False
    return True


def _checkpoint_label(event_id: str, server: str) -> str:
    value = re.sub(r"[^0-9A-Za-z_-]+", "_", f"{event_id}_{server}")
    return value[:96] or "mutation"


def _create_runtime_checkpoint(capability, label: str) -> Any:
    method = getattr(capability, "create_runtime_checkpoint", None)
    if callable(method):
        return method(label)
    exec_python = getattr(capability, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoints")
    runtime_db = str(getattr(capability, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    backup_path = f"/tmp/{label}.runtime-backup.db"
    exec_python(f"""
import os, sqlite3
runtime_db = {runtime_db!r}
backup_path = {backup_path!r}
try:
    os.remove(backup_path)
except FileNotFoundError:
    pass
with sqlite3.connect(runtime_db, isolation_level=None, timeout=30) as src, sqlite3.connect(backup_path, isolation_level=None, timeout=30) as dst:
    src.execute('PRAGMA busy_timeout=30000')
    src.backup(dst)
""")
    return backup_path


def _restore_runtime_checkpoint(capability, token: Any) -> None:
    method = getattr(capability, "restore_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(capability, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoint restore")
    runtime_db = str(getattr(capability, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    backup_path = str(token)
    exec_python(f"""
import sqlite3
with sqlite3.connect({backup_path!r}, isolation_level=None, timeout=30) as src, sqlite3.connect({runtime_db!r}, isolation_level=None, timeout=30) as dst:
    dst.execute('PRAGMA busy_timeout=30000')
    src.backup(dst)
""")


def _delete_runtime_checkpoint(capability, token: Any) -> None:
    method = getattr(capability, "delete_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(capability, "_exec_python", None)
    if callable(exec_python):
        exec_python(f"import os\ntry:\n os.remove({str(token)!r})\nexcept FileNotFoundError:\n pass\n")


def _observer_surface_available(capability, tool: str) -> bool:
    return callable(getattr(capability, tool, None)) or callable(getattr(capability, "call_tool", None))


def _apply_mutation_event(event: dict[str, Any], env) -> dict[str, Any]:
    event_id = str(event.get("id") or "mutation")
    specs = event.get("apply") or []
    conditions = event.get("postconditions") or []
    requested_specs = [_jsonable(spec) for spec in specs]
    requested_postconditions = [_jsonable(condition) for condition in conditions]
    preflighted_specs: list[dict[str, Any]] = []
    preflighted_postconditions: list[dict[str, Any]] = []
    actually_applied_specs: list[dict[str, Any]] = []
    capabilities: dict[str, Any] = {}
    checkpoints: list[tuple[Any, Any]] = []
    writes_started = False
    failed_spec: dict[str, Any] | None = None
    postcondition_evidence: list[dict[str, Any]] = []

    def audit_state() -> dict[str, Any]:
        applied = _jsonable(actually_applied_specs)
        return {
            "event_id": event_id,
            "stage": event.get("_stage"),
            "requested_specs": _jsonable(requested_specs),
            "preflighted_specs": _jsonable(preflighted_specs),
            "actually_applied_specs": applied,
            # Backward-compatible field, now truthful rather than prefilled from requests.
            "applied_specs": applied,
            "requested_postconditions": _jsonable(requested_postconditions),
            "preflighted_postconditions": _jsonable(preflighted_postconditions),
            "idempotency_key": event.get("idempotency_key"),
        }

    try:
        if not specs:
            raise ValueError(f"mutation {event_id} has no state changes")
        if not conditions:
            raise ValueError(f"mutation {event_id} has no observable postconditions")

        # Full apply-surface preflight. No checkpoint or write may occur before this loop
        # and the postcondition observer loop both finish successfully.
        for index, spec in enumerate(specs):
            failed_spec = {"kind": "apply", "index": index, "spec": _jsonable(spec)}
            server = spec.get("server")
            if not server:
                raise ValueError(f"mutation {event_id}: missing server")
            capability = getattr(env, f"{server}_mock", None)
            if capability is None:
                raise RuntimeError(f"mutation {event_id}: no capability for {server!r}")
            if "sql_file" in spec:
                if not callable(getattr(capability, "apply_sql_file", None)):
                    raise RuntimeError(
                        f"mutation {event_id}: apply_sql_file is not callable for {server!r}"
                    )
                sql_path = THIS_DIR / str(spec["sql_file"])
                if not sql_path.is_file() or sql_path.stat().st_size == 0:
                    raise FileNotFoundError(f"mutation SQL file not found or empty: {spec['sql_file']}")
            elif "tool_call" in spec:
                tool_call = spec.get("tool_call")
                if not isinstance(tool_call, dict) or not tool_call.get("name"):
                    raise ValueError(f"mutation {event_id}: tool_call name is missing")
                tool_name = str(tool_call["name"])
                if not _observer_surface_available(capability, tool_name):
                    raise RuntimeError(
                        f"mutation {event_id}: tool_call {tool_name!r} is not callable for {server!r}"
                    )
            elif not callable(getattr(capability, "apply_mutation", None)):
                raise RuntimeError(
                    f"mutation {event_id}: apply_mutation is not callable for {server!r}"
                )
            capabilities[str(server)] = capability
            preflighted_specs.append(_jsonable(spec))

        for index, condition in enumerate(conditions):
            failed_spec = {"kind": "postcondition", "index": index, "spec": _jsonable(condition)}
            server = condition.get("server")
            tool = condition.get("tool")
            capability = getattr(env, f"{server}_mock", None) if server else None
            if capability is None:
                raise RuntimeError(f"mutation {event_id}: invalid postcondition capability {server!r}")
            if not tool:
                raise ValueError(f"mutation {event_id}: postcondition tool missing")
            _validate_postcondition_tool(event_id, str(tool))
            if not _observer_surface_available(capability, str(tool)):
                raise RuntimeError(
                    f"mutation {event_id}: postcondition observer {server}.{tool} is not callable"
                )
            preflighted_postconditions.append(_jsonable(condition))

        if _postconditions_satisfied(event, env):
            postcondition_evidence = _apply_postconditions(event, env)
            return {
                **audit_state(),
                "postconditions_passed": True,
                "postconditions": postcondition_evidence,
                "already_satisfied": True,
                "completed_at": _now(),
            }

        failed_spec = None
        for server, capability in capabilities.items():
            failed_spec = {"kind": "checkpoint", "server": server}
            checkpoints.append((capability, _create_runtime_checkpoint(
                capability, _checkpoint_label(event_id, server)
            )))

        for index, spec in enumerate(specs):
            failed_spec = {"kind": "apply", "index": index, "spec": _jsonable(spec)}
            writes_started = True
            capability = capabilities[str(spec["server"])]
            if "sql_file" in spec:
                capability.apply_sql_file(THIS_DIR / str(spec["sql_file"]))
            elif "tool_call" in spec:
                tool_call = spec["tool_call"]
                result = _invoke_observer(
                    capability, str(tool_call["name"]), dict(tool_call.get("args") or {})
                )
                if not _result_success(result):
                    raise RuntimeError(f"mutation tool call returned a failure: {result!r}")
            else:
                capability.apply_mutation(spec)
            actually_applied_specs.append(_jsonable(spec))

        failed_spec = {"kind": "postcondition", "index": 0, "spec": _jsonable(conditions[0])}
        postcondition_evidence = _apply_postconditions(event, env)
    except Exception as exc:
        postcondition_evidence = list(getattr(exc, "postcondition_evidence", postcondition_evidence))
        failed_spec = getattr(exc, "failed_postcondition", failed_spec)
        rollback_errors: list[str] = []
        rollback_attempted = bool(checkpoints and writes_started)
        if rollback_attempted:
            for capability, token in reversed(checkpoints):
                try:
                    _restore_runtime_checkpoint(capability, token)
                except Exception as rollback_exc:
                    rollback_errors.append(f"{type(rollback_exc).__name__}: {rollback_exc}")
        failed_audit = {
            **audit_state(),
            "postconditions_passed": False,
            "already_satisfied": False,
            "failed_spec": _jsonable(failed_spec),
            "exception": {"type": type(exc).__name__, "message": str(exc)},
            "rollback": {
                "attempted": rollback_attempted,
                "succeeded": rollback_attempted and not rollback_errors,
                "errors": rollback_errors,
            },
            "postcondition_evidence": _jsonable(postcondition_evidence),
            "trial_invalid": True,
            "completed_at": _now(),
        }
        stage = event.get("_stage")
        if stage is not None and getattr(env, "workspace", None) is not None:
            try:
                _persist_mutation_audit(env, int(stage), failed_audit)
            except Exception as audit_exc:
                raise TrialInvalidError(
                    f"mutation {event_id} failed ({type(exc).__name__}: {exc}); "
                    f"failure audit persistence also failed: {type(audit_exc).__name__}: {audit_exc}"
                ) from audit_exc
        rollback_suffix = f"; rollback failed: {rollback_errors}" if rollback_errors else ""
        raise TrialInvalidError(
            f"mutation {event_id} failed: {type(exc).__name__}: {exc}{rollback_suffix}"
        ) from exc
    finally:
        for capability, token in reversed(checkpoints):
            _delete_runtime_checkpoint(capability, token)

    return {
        **audit_state(),
        "postconditions_passed": True,
        "postconditions": postcondition_evidence,
        "already_satisfied": False,
        "completed_at": _now(),
    }


def _checked_shell_exec(env, command: str) -> Any:
    result = env.workspace.shell.exec(command, user="root")
    returncode = getattr(result, "returncode", getattr(result, "exit_code", 0))
    if returncode not in (None, 0):
        stderr = getattr(result, "stderr", "")
        raise RuntimeError(f"shell command failed ({returncode}): {command}; {stderr}")
    return result


def _atomic_write_json(env, directory: str, filename: str, payload: dict[str, Any]) -> str:
    _checked_shell_exec(env, f"mkdir -p {directory}")
    final_path = f"{directory}/{filename}"
    temporary_path = f"{final_path}.tmp"
    data = (json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8")
    env.workspace.fs.write_file(temporary_path, data)
    _checked_shell_exec(env, f"mv -f {temporary_path} {final_path}")
    try:
        persisted = env.workspace.fs.read_file(final_path)
    except Exception as exc:
        raise RuntimeError(f"persist read-back failed for {final_path}: {exc}") from exc
    if persisted != data:
        raise RuntimeError(f"persist read-back mismatch for {final_path}")
    return final_path


def _persist_mutation_audit(env, stage: int, audit: dict[str, Any]) -> str:
    safe_id = re.sub(r"[^0-9A-Za-z_-]+", "_", str(audit.get("event_id") or "mutation"))
    payload = dict(audit)
    payload["stage"] = int(stage)
    return _atomic_write_json(env, MUTATION_AUDIT_DIR, f"stage_{stage:02d}_{safe_id}.json", payload)


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
    rows = [
        {"check_id": str(check.name), "passed": bool(check.passed), "weight": weights[str(check.name)]}
        for check in checks
    ]
    payload = {
        "stage": int(stage),
        "frozen": True,
        "checks": rows,
        "passed_weight": float(passed_weight),
        "total_weight": float(total_weight),
        "score": (float(passed_weight) / float(total_weight)) if total_weight else 0.0,
        "response_path": response_path,
        "trace_path": trace_path,
        "completed_at": _now(),
    }
    _atomic_write_json(env, STAGE_RESULTS_DIR, f"stage_{stage:02d}.json", payload)
    return payload


def _read_frozen_file(env, path: str, stage: int, artifact: str) -> bytes:
    try:
        data = env.workspace.fs.read_file(path)
    except Exception as exc:
        raise TrialInvalidError(f"stage {stage} {artifact} is missing or unreadable: {path}") from exc
    if not isinstance(data, bytes):
        raise TrialInvalidError(f"stage {stage} {artifact} is unreadable: expected bytes at {path}")
    return data


def _validate_frozen_stage_results(
    env,
    frozen_results: list[dict[str, Any]],
    expected_stage_count: int,
) -> list[dict[str, Any]]:
    """Read back and validate the complete immutable Stage result set."""
    expected_stages = list(range(expected_stage_count))
    if len(frozen_results) != expected_stage_count:
        raise TrialInvalidError(
            f"frozen Stage result count must be {expected_stage_count}, got {len(frozen_results)}"
        )

    captured_by_stage: dict[int, dict[str, Any]] = {}
    for payload in frozen_results:
        if not isinstance(payload, dict) or payload.get("frozen") is not True:
            raise TrialInvalidError("every captured Stage result must be a frozen payload")
        try:
            stage = int(payload["stage"])
        except Exception as exc:
            raise TrialInvalidError("captured frozen Stage result has no parseable stage") from exc
        if stage in captured_by_stage:
            raise TrialInvalidError(f"captured frozen Stage results contain duplicate stage {stage}")
        captured_by_stage[stage] = payload
    if sorted(captured_by_stage) != expected_stages:
        raise TrialInvalidError(
            f"captured frozen Stage results must contain unique stages {expected_stages}, "
            f"got {sorted(captured_by_stage)}"
        )

    persisted_rows: list[dict[str, Any]] = []
    for expected_stage in expected_stages:
        stage_path = f"{STAGE_RESULTS_DIR}/stage_{expected_stage:02d}.json"
        try:
            raw = _read_frozen_file(env, stage_path, expected_stage, "result JSON")
        except TrialInvalidError as exc:
            raise TrialInvalidError(f"stage {expected_stage} result JSON is missing or unreadable") from exc
        try:
            decoded = raw.decode("utf-8")
            payload = json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TrialInvalidError(f"stage {expected_stage} result JSON parse failed") from exc
        if not isinstance(payload, dict):
            raise TrialInvalidError(f"stage {expected_stage} result JSON must be an object")
        persisted_rows.append(payload)

    persisted_stages: list[int] = []
    for payload in persisted_rows:
        try:
            persisted_stages.append(int(payload["stage"]))
        except Exception as exc:
            raise TrialInvalidError("persisted frozen Stage result has no parseable stage") from exc
    if len(set(persisted_stages)) != expected_stage_count:
        raise TrialInvalidError(f"persisted frozen Stage results contain duplicate stages: {persisted_stages}")
    if sorted(persisted_stages) != expected_stages:
        raise TrialInvalidError(
            f"persisted frozen Stage results must contain unique stages {expected_stages}, "
            f"got {sorted(persisted_stages)}"
        )

    validated: list[dict[str, Any]] = []
    for payload in sorted(persisted_rows, key=lambda row: int(row["stage"])):
        stage = int(payload["stage"])
        if payload.get("frozen") is not True:
            raise TrialInvalidError(f"stage {stage} result is not frozen")
        if payload != captured_by_stage[stage]:
            raise TrialInvalidError(f"stage {stage} persisted result differs from captured frozen payload")
        response_path = payload.get("response_path")
        trace_path = payload.get("trace_path")
        if not isinstance(response_path, str) or not response_path:
            raise TrialInvalidError(f"stage {stage} response path is missing")
        if not isinstance(trace_path, str) or not trace_path:
            raise TrialInvalidError(f"stage {stage} trace path is missing")
        response_data = _read_frozen_file(env, response_path, stage, "response")
        try:
            response_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise TrialInvalidError(f"stage {stage} response is unreadable UTF-8") from exc
        trace_data = _read_frozen_file(env, trace_path, stage, "trace")
        try:
            trace_payload = json.loads(trace_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TrialInvalidError(f"stage {stage} trace is unreadable or invalid JSON") from exc
        if not isinstance(trace_payload, list):
            raise TrialInvalidError(f"stage {stage} trace must be a JSON list")
        validated.append(payload)
    return validated


def _extract_assistant_text(messages) -> str:
    chunks: list[str] = []
    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        if isinstance(content, str) and content:
            chunks.append(content)
        elif isinstance(content, list):
            for block in content:
                if _field(block, "type") == "text" and _field(block, "text", ""):
                    chunks.append(str(_field(block, "text")))
    return "\n".join(chunks)


def _extract_full_trace(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    """Persist every attempt, but expose a scoreable name only for one valid pair."""
    trace: list[dict[str, Any]] = []
    calls_by_id: dict[str, list[int]] = {}
    results_by_id: dict[str, list[int]] = {}
    reported_result_names: dict[int, str] = {}

    for message in messages or []:
        role = str(_field(message, "role", ""))
        content = _field(message, "content", "")
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            block_type = str(_field(block, "type", ""))
            if block_type in {"toolCall", "tool_call", "tool_use"}:
                call_id = str(_field(block, "id", "") or "")
                attempted_name = str(_field(block, "name", "") or "")
                row_index = len(trace)
                trace.append({
                    "event_id": event_id,
                    "role": role,
                    "type": "tool_call",
                    "id": call_id,
                    "name": "",
                    "attempted_name": attempted_name,
                    "arguments": _jsonable(_field(block, "arguments", _field(block, "input", {}))),
                    "paired": False,
                    "pair_error": None,
                    "success": None,
                })
                calls_by_id.setdefault(call_id, []).append(row_index)
            elif block_type in {"toolResult", "tool_result", "tool_response"}:
                call_id = str(_field(
                    block,
                    "toolUseId",
                    _field(
                        block,
                        "tool_use_id",
                        _field(block, "toolCallId", _field(block, "tool_call_id", _field(block, "id", ""))),
                    ),
                ) or "")
                result = _jsonable(_field(
                    block, "content", _field(block, "result", _field(block, "output", ""))
                ))
                attempted_name = str(_field(block, "name", "") or "")
                attempted_success = _result_success(result)
                row_index = len(trace)
                trace.append({
                    "event_id": event_id,
                    "role": role,
                    "type": "tool_result",
                    "id": call_id,
                    "name": "",
                    "attempted_name": attempted_name,
                    "result": result,
                    "paired": False,
                    "pair_error": None,
                    "attempted_success": attempted_success,
                    # Only a structurally valid pair may expose success to the Rubric.
                    "success": False,
                })
                reported_result_names[row_index] = attempted_name
                results_by_id.setdefault(call_id, []).append(row_index)

    for call_id in set(calls_by_id) | set(results_by_id):
        call_indexes = calls_by_id.get(call_id, [])
        result_indexes = results_by_id.get(call_id, [])

        if len(call_indexes) == 1:
            call_attempted_name = str(trace[call_indexes[0]].get("attempted_name") or "")
            for result_index in result_indexes:
                if not trace[result_index].get("attempted_name"):
                    trace[result_index]["attempted_name"] = call_attempted_name

        if not call_id:
            pair_error = "empty_id"
        elif not call_indexes:
            pair_error = "orphan_result"
        elif len(call_indexes) > 1:
            pair_error = "duplicate_call_id"
        elif not result_indexes:
            pair_error = "missing_result"
        elif len(result_indexes) > 1:
            pair_error = "duplicate_result_id"
        else:
            call_row = trace[call_indexes[0]]
            result_row = trace[result_indexes[0]]
            reported_result_name = reported_result_names.get(result_indexes[0], "")
            if reported_result_name and reported_result_name != call_row["attempted_name"]:
                pair_error = "name_mismatch"
            elif result_row["attempted_success"] is not True:
                pair_error = "tool_failure"
            else:
                scoreable_name = str(call_row.get("attempted_name") or "")
                if not scoreable_name:
                    pair_error = "empty_name"
                else:
                    call_row["name"] = scoreable_name
                    call_row["paired"] = True
                    result_row["name"] = scoreable_name
                    result_row["paired"] = True
                    result_row["success"] = True
                    continue

        for row_index in call_indexes + result_indexes:
            trace[row_index]["pair_error"] = pair_error

    return trace


def _dispatch_event(event: dict[str, Any], env, agent) -> tuple[str, list[dict[str, Any]], dict[str, Any] | None]:
    kind = str(event.get("kind") or "")
    if kind == "mutation":
        return "", [], _apply_mutation_event(event, env)
    if event.get("silent"):
        return "", [], None
    if kind not in {"user_message", "notification", "world"}:
        raise ValueError(f"event {event.get('id')}: unknown kind {kind!r}")
    result = agent.act(_render_event(event))
    messages = getattr(result, "messages", []) or []
    return _extract_assistant_text(messages), _extract_full_trace(messages, str(event.get("id") or "")), None


def _run_checks(spec, env, tag: str) -> tuple[list[Check], float, float]:
    rows: list[Check] = []
    total = 0.0
    passed = 0.0
    for check_id, function, weight in spec:
        ok = bool(function(env))
        rows.append(Check(name=check_id, passed=ok, tags=[tag]))
        total += float(weight)
        if ok:
            passed += float(weight)
    return rows, total, passed


@entry(
    capabilities=[
        "email_mock", "calendar_mock", "notion_mock", "review_platform_mock",
        "maps_mock", "credit_card_mock", "notification_hub_mock", "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def pottery_invoice_compliance_day(env, agent):
    _register_all_mcp(env, agent)
    env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/terrarium/openclaw/workspace")
    _checked_shell_exec(env, "chmod -R a+rwX /terrarium/openclaw/workspace")
    _checked_shell_exec(
        env,
        f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {MUTATION_AUDIT_DIR} {STAGE_RESULTS_DIR}",
    )

    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    stage_modules = {stage: _load_rubric(f"stage_{stage}") for stage in range(stage_count)}
    cross_module = _load_rubric("cross_stage")
    tool_module = _load_rubric("tool_quality")
    final_module = _load_rubric("final")
    _preflight_authoritative_backends(env)

    all_checks: list[Check] = []
    frozen_results: list[dict[str, Any]] = []
    for stage in range(stage_count):
        response_chunks: list[str] = []
        trace_rows: list[dict[str, Any]] = []
        events = sorted(events_by_stage[stage], key=lambda item: (str(item.get("time", "")), str(item.get("id", ""))))
        for source_event in events:
            event = dict(source_event)
            event["_stage"] = stage
            text, trace, audit = _dispatch_event(event, env, agent)
            if audit is not None:
                _persist_mutation_audit(env, stage, audit)
            if text:
                response_chunks.append(text[:MAX_STAGE_RESPONSE_CHARS])
            trace_rows.extend(trace)

        response_path = f"{RESPONSES_DIR}/stage_{stage}.txt"
        trace_path = f"{TRACE_DIR}/stage_{stage}.json"
        env.workspace.fs.write_file(response_path, "\n---\n".join(response_chunks).encode("utf-8"))
        env.workspace.fs.write_file(
            trace_path,
            (json.dumps(trace_rows, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8"),
        )
        spec = stage_modules[stage].CHECKS
        checks, stage_total, stage_passed = _run_checks(spec, env, f"stage{stage}")
        frozen_results.append(_persist_stage_result(
            env, stage, spec, checks, stage_total, stage_passed, response_path, trace_path
        ))
        all_checks.extend(checks)

    validated_stage_results = _validate_frozen_stage_results(
        env, frozen_results, expected_stage_count=stage_count
    )
    total_weight = sum(float(payload["total_weight"]) for payload in validated_stage_results)
    passed_weight = sum(float(payload["passed_weight"]) for payload in validated_stage_results)

    for module, tag in ((cross_module, "cross_stage"), (tool_module, "tool_quality"), (final_module, "final")):
        checks, bucket_total, bucket_passed = _run_checks(module.CHECKS, env, tag)
        all_checks.extend(checks)
        total_weight += bucket_total
        passed_weight += bucket_passed

    if abs(total_weight - 100.0) > 1e-9:
        raise RuntimeError(f"rubric total must be 100, got {total_weight}")
    score = passed_weight / total_weight
    logger.info(f"pottery score={score:.4f} ({passed_weight:.2f}/{total_weight:.2f})")
    return CheckerResults(checks=all_checks, score=score)
