"""Handbook-compliant shopping benchmark task: central_ac_install_30d."""
from __future__ import annotations

import difflib
import importlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable

import yaml
from loguru import logger
from terrarium.models.checker import Check, CheckerResults
from terrarium.models.mcp import MCPServerConfig
from terrarium.task.decorator import entry

from capabilities import agent_caps_config

THIS_DIR = Path(__file__).resolve().parent
RESPONSES_DIR = "/terrarium/agent_responses"
TRACE_DIR = "/terrarium/agent_traces"
SCORES_DIR = "/terrarium/stage_scores"
STAGE_AUDIT_DIR = "/terrarium/stage_audits"
MAX_STAGE_RESPONSE_CHARS = 20000
TRACKED_WORKSPACE_FILES = (
    "gear_plan.md", "budget.md", "decision_log.md", "risk_register.md",
    "order_tracker.md", "evidence_log.md", "final_summary.md", "HEARTBEAT.md",
)


@dataclass(frozen=True)
class ScoreBreakdown:
    passed_weight: float
    total_weight: float
    score: float
    failed_check_ids: tuple[str, ...]


def aggregate_score(outcomes: Iterable[tuple[str, float, bool]]) -> ScoreBreakdown:
    """Return the exact passed atomic weight divided by total atomic weight."""
    passed_weight = 0.0
    total_weight = 0.0
    failed: list[str] = []
    for check_id, raw_weight, passed in outcomes:
        weight = float(raw_weight)
        total_weight += weight
        if passed:
            passed_weight += weight
        else:
            failed.append(str(check_id))
    score = passed_weight / total_weight if total_weight else 0.0
    return ScoreBreakdown(
        passed_weight=passed_weight,
        total_weight=total_weight,
        score=score,
        failed_check_ids=tuple(failed),
    )


def _rubric_pkg_name() -> str:
    for p in sys.path:
        try:
            rel = THIS_DIR.relative_to(Path(p).resolve())
        except ValueError:
            continue
        return ".".join(rel.parts) + ".rubrics"
    raise RuntimeError(f"Cannot derive rubric package name for {THIS_DIR}")


_RUBRIC_PKG = _rubric_pkg_name()

_CAPABILITIES_CONFIG = agent_caps_config(
    ecommerce_mock="central_ac_install_30d",
    delivery_logistics_mock="central_ac_install_30d",
    credit_card_mock="central_ac_install_30d",
    email_mock="central_ac_install_30d",
    calendar_mock="central_ac_install_30d",
    notification_hub_mock="central_ac_install_30d",
    weather_mock="central_ac_install_30d",
)


def _register_all_mcp(env, agent) -> None:
    for cap_name in env:
        for cap in getattr(env, cap_name):
            info = getattr(cap, "connection_info", None) or {}
            mcp = info.get("mcp_server") if isinstance(info, dict) else None
            if mcp:
                agent.add_mcp_server(MCPServerConfig(**mcp))


def _load_events(yaml_path: Path) -> tuple[int, dict[int, list[dict]]]:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    by_stage: dict[int, list[dict]] = {}
    for k, evs in (raw.get("stages") or {}).items():
        idx = int(k)
        bucket = by_stage.setdefault(idx, [])
        for ev in evs or []:
            bucket.append(dict(ev))
    return (max(by_stage) + 1) if by_stage else 0, by_stage


def _render_event(ev: dict) -> str:
    time = ev.get("time", "")
    kind = ev.get("kind", "")
    body = ev.get("body", "") or ""
    if kind == "user_message":
        tag = f"[message from {ev.get('from') or 'user'} @ {time}]"
    elif kind == "notification":
        tag = f"[notification @ {time}; source={ev.get('channel') or ev.get('source') or 'system'}]"
    elif kind == "world":
        tag = f"[world event @ {time}; source={ev.get('source') or 'system'}]"
    else:
        tag = f"[{kind} @ {time}]"
    return f"{tag}\n{body}"


def _field(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _jsonable(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        if isinstance(value, dict):
            return {str(k): _jsonable(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [_jsonable(v) for v in value]
        return str(value)



def _decode_tool_value(value: Any) -> Any:
    value = _jsonable(value)
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def _failure_text(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    try:
        return _has_failure_signal(json.loads(stripped))
    except Exception:
        return bool(re.search(
            r"(?i)(?:^|[\s\[{(:;,])(?:tool[_ -]?error|error|failure|exception|traceback)(?:\b|\s*[:：])",
            stripped,
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
    status = str(normalized.get("status") or "").strip().lower()
    if status in {"error", "failed", "failure", "fail", "exception"}:
        return True
    code = normalized.get("code")
    if isinstance(code, str) and re.search(
        r"(?i)(?:^|[_-])(?:err(?:or)?|fail(?:ed|ure)?|exception)(?:$|[_-])", code
    ):
        return True
    if isinstance(code, (int, float)) and code < 0:
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
            key in actual and _value_matches(actual[key], value)
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        return isinstance(actual, list) and all(
            any(_value_matches(candidate, item) for candidate in actual)
            for item in expected
        )
    if isinstance(actual, bool) or isinstance(expected, bool):
        return bool(actual) == bool(expected)
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return actual == expected
    return str(actual) == str(expected)


def _structured_match(value: Any, expected: dict[str, Any]) -> bool:
    if not expected:
        return True
    return any(_value_matches(candidate, expected) for candidate in _iter_mappings(value))


_SIDE_EFFECTING_POSTCONDITION_TOOLS = {
    "transfer", "add_payee", "pay_payee", "schedule_recurring", "cancel_recurring",
    "make_payment", "freeze_card", "unfreeze_card", "dispute_transaction", "redeem_rewards",
    "place_order", "cancel_order", "request_refund", "add_to_cart", "update_cart_item",
    "remove_from_cart", "apply_coupon", "remove_coupon",
    "cancel_shipment", "change_address", "report_issue", "request_pickup", "reschedule_delivery",
    "subscribe_status", "unsubscribe", "contact_agent",
    "create_price_alert", "create_subscription", "delete_subscription", "mark_all_read", "mark_read",
    "pause_subscription", "resume_subscription", "subscribe_official_account", "update_subscription",
    "subscribe_alerts", "read_email", "send_email", "reply_email", "forward_email", "delete_email", "delete_emails",
    "move_email", "move_emails", "mark_emails", "save_draft", "update_draft", "delete_draft",
    "import_emails", "export_emails", "download_attachment", "create_folder", "delete_folder",
    "create_event", "update_event", "delete_event",
    "API-post-page", "API-patch-page", "API-patch-block-children", "API-update-a-block", "API-delete-a-block",
}


def _validate_postcondition_tool(event_id: str, tool: str) -> None:
    if tool in _SIDE_EFFECTING_POSTCONDITION_TOOLS:
        raise ValueError(f"event {event_id}: postcondition tool {tool!r} is not observational")


def _apply_postconditions(event: dict, env) -> None:
    conditions = event.get("postconditions") or []
    if not conditions:
        raise ValueError(f"mutation {event.get('id')} has no observable postconditions")
    for condition in conditions:
        server = condition.get("server")
        tool = condition.get("tool")
        if not server or not tool:
            raise ValueError(f"event {event.get('id')} has invalid postcondition: {condition}")
        _validate_postcondition_tool(str(event.get("id") or "mutation"), str(tool))
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            raise RuntimeError(f"event {event.get('id')}: no capability for postcondition {server!r}")
        value = _decode_tool_value(cap.call_tool(tool, **(condition.get("args") or {})))
        if not _result_success(value):
            raise RuntimeError(
                f"event {event.get('id')} postcondition call failed for {server}.{tool}: {value!r}"
            )
        expected = condition.get("expect") or {}
        if not _structured_match(value, expected):
            raise RuntimeError(
                f"event {event.get('id')} postcondition fields missing for {server}.{tool}; "
                f"expected={expected!r}, value={value!r}"
            )
        blob = json.dumps(value, ensure_ascii=False, default=str).lower()
        missing = [
            str(term) for term in condition.get("contains") or []
            if str(term).lower() not in blob
        ]
        forbidden = [
            str(term) for term in condition.get("not_contains") or []
            if str(term).lower() in blob
        ]
        if missing or forbidden:
            raise RuntimeError(
                f"event {event.get('id')} postcondition failed for {server}.{tool}; "
                f"missing={missing!r}, forbidden={forbidden!r}, value={blob[:1200]!r}"
            )


def _postconditions_satisfied(event: dict, env) -> bool:
    try:
        _apply_postconditions(event, env)
    except Exception:
        return False
    return True


def _checkpoint_label(event_id: str, server: str) -> str:
    raw = f"{event_id}_{server}"
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in raw)
    return safe[:96] or "mutation"


def _create_runtime_checkpoint(cap, label: str) -> Any:
    method = getattr(cap, "create_runtime_checkpoint", None)
    if callable(method):
        return method(label)
    exec_python = getattr(cap, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoints")
    runtime_db = str(getattr(cap, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
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


def _restore_runtime_checkpoint(cap, token: Any) -> None:
    method = getattr(cap, "restore_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(cap, "_exec_python", None)
    if not callable(exec_python):
        raise RuntimeError("capability does not support runtime checkpoint restore")
    runtime_db = str(getattr(cap, "_CONTAINER_RUNTIME_DB", "/env/runtime.db"))
    backup_path = str(token)
    exec_python(f"""
import sqlite3
runtime_db = {runtime_db!r}
backup_path = {backup_path!r}
with sqlite3.connect(backup_path, isolation_level=None, timeout=30) as src, sqlite3.connect(runtime_db, isolation_level=None, timeout=30) as dst:
    dst.execute('PRAGMA busy_timeout=30000')
    src.backup(dst)
""")


def _delete_runtime_checkpoint(cap, token: Any) -> None:
    method = getattr(cap, "delete_runtime_checkpoint", None)
    if callable(method):
        method(token)
        return
    exec_python = getattr(cap, "_exec_python", None)
    if callable(exec_python):
        exec_python(f"import os\ntry:\n os.remove({str(token)!r})\nexcept FileNotFoundError:\n pass\n")


def _apply_mutation_event(event: dict, env) -> None:
    specs = event.get("apply") or []
    if not specs:
        raise ValueError(f"mutation {event.get('id')} has no state changes")
    if event.get("abort_stage") is not True:
        raise ValueError(f"mutation {event.get('id')} must set abort_stage=true")
    if not event.get("idempotency_key"):
        raise ValueError(f"mutation {event.get('id')} has no idempotency_key")
    if not event.get("postconditions"):
        raise ValueError(f"mutation {event.get('id')} has no observable postconditions")

    capabilities: dict[str, Any] = {}
    for spec in specs:
        server = spec.get("server")
        if not server:
            raise ValueError(f"mutation {event.get('id')}: missing server")
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            raise RuntimeError(f"mutation {event.get('id')}: no capability for {server!r}")
        if "sql_file" in spec and not (THIS_DIR / spec["sql_file"]).is_file():
            raise FileNotFoundError(f"mutation SQL file not found: {spec['sql_file']}")
        capabilities[str(server)] = cap
    for condition in event.get("postconditions") or []:
        server = condition.get("server")
        tool = condition.get("tool")
        if not server or getattr(env, f"{server}_mock", None) is None:
            raise RuntimeError(f"mutation {event.get('id')}: invalid postcondition server {server!r}")
        if not tool:
            raise ValueError(f"mutation {event.get('id')}: invalid postcondition tool {tool!r}")
        _validate_postcondition_tool(str(event.get("id") or "mutation"), str(tool))

    if _postconditions_satisfied(event, env):
        return

    checkpoints: list[tuple[Any, Any]] = []
    try:
        for server, cap in capabilities.items():
            checkpoints.append((cap, _create_runtime_checkpoint(
                cap, _checkpoint_label(str(event.get("id") or "mutation"), server)
            )))
        try:
            for spec in specs:
                cap = capabilities[str(spec["server"])]
                if "sql_file" in spec:
                    cap.apply_sql_file(THIS_DIR / spec["sql_file"])
                elif "tool_call" in spec:
                    tc = spec["tool_call"]
                    result = _decode_tool_value(cap.call_tool(tc["name"], **(tc.get("args") or {})))
                    if not _result_success(result):
                        raise RuntimeError(f"mutation tool call failed: {result}")
                else:
                    cap.apply_mutation(spec)
            _apply_postconditions(event, env)
        except Exception:
            rollback_errors: list[str] = []
            for cap, token in reversed(checkpoints):
                try:
                    _restore_runtime_checkpoint(cap, token)
                except Exception as rollback_exc:
                    rollback_errors.append(f"{type(rollback_exc).__name__}: {rollback_exc}")
            if rollback_errors:
                raise RuntimeError(
                    f"mutation {event.get('id')} failed and rollback failed: {rollback_errors}"
                )
            raise
    finally:
        for cap, token in reversed(checkpoints):
            try:
                _delete_runtime_checkpoint(cap, token)
            except Exception as cleanup_exc:
                logger.warning(
                    f"mutation checkpoint cleanup failed for {event.get('id')}: "
                    f"{type(cleanup_exc).__name__}: {cleanup_exc}"
                )


def _extract_tool_calls(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    results: dict[str, list[tuple[Any, bool]]] = {}
    for message in messages or []:
        content = _field(message, "content", "")
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            if _field(block, "type", "") not in (
                "toolResult", "tool_result", "tool_response", "function_result",
            ):
                continue
            call_id = str(_field(
                block,
                "tool_use_id",
                _field(
                    block,
                    "toolUseId",
                    _field(block, "toolCallId", _field(block, "tool_call_id", _field(block, "id", ""))),
                ),
            ) or "")
            if call_id:
                result = _decode_tool_value(
                    _field(block, "content", _field(block, "result", _field(block, "output")))
                )
                explicit_error = bool(_field(block, "is_error", _field(block, "isError", False)))
                results.setdefault(call_id, []).append(
                    (result, not explicit_error and _result_success(result))
                )

    calls: list[dict[str, Any]] = []
    call_id_counts: dict[str, int] = {}
    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            typ = _field(block, "type", "")
            if typ not in ("toolCall", "tool_call", "tool_use", "function_call"):
                continue
            call_id = str(_field(
                block, "tool_use_id", _field(block, "toolUseId", _field(block, "id", ""))
            ) or "")
            call_id_counts[call_id] = call_id_counts.get(call_id, 0) + 1

    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            typ = _field(block, "type", "")
            if typ not in ("toolCall", "tool_call", "tool_use", "function_call"):
                continue
            function = _field(block, "function")
            call_id = str(_field(
                block, "tool_use_id", _field(block, "toolUseId", _field(block, "id", ""))
            ) or "")
            result_rows = results.get(call_id, [])
            paired = bool(call_id) and call_id_counts.get(call_id) == 1 and len(result_rows) == 1
            result = result_rows[0][0] if paired else None
            succeeded = paired and result_rows[0][1] is True
            name = (
                _field(function, "name", _field(block, "name"))
                if function is not None else _field(block, "name")
            )
            arguments = (
                _field(function, "arguments", _field(block, "arguments", _field(block, "input", {})))
                if function is not None else _field(block, "arguments", _field(block, "input", {}))
            )
            calls.append({
                "event_id": event_id,
                "id": call_id or None,
                "name": name,
                "arguments": _jsonable(arguments),
                "result": result,
                "succeeded": succeeded,
            })
    return calls


def _dispatch_event(ev: dict, env, agent) -> tuple[str, list[dict[str, Any]]]:
    kind = ev.get("kind", "")
    if kind == "mutation":
        _apply_mutation_event(ev, env)
        return "", []
    if ev.get("silent"):
        return "", []
    if kind not in ("user_message", "notification"):
        raise ValueError(f"event {ev.get('id')}: unknown kind {kind!r}")
    result = agent.act(_render_event(ev))
    messages = getattr(result, "messages", []) or []
    return _extract_assistant_text(messages), _extract_tool_calls(messages, ev.get("id"))


def _limit_text(text: str) -> str:
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return text[:MAX_STAGE_RESPONSE_CHARS] + f"\n\n[TRUNCATED: agent response exceeded {MAX_STAGE_RESPONSE_CHARS} chars]"


def _extract_assistant_text(messages) -> str:
    chunks: list[str] = []
    for m in messages:
        if getattr(m, "role", None) != "assistant":
            continue
        c = getattr(m, "content", "")
        if isinstance(c, str):
            if c:
                chunks.append(c)
            continue
        for blk in c or []:
            if getattr(blk, "type", "") == "text":
                t = getattr(blk, "text", "") or ""
                if t:
                    chunks.append(t)
    return "\n".join(chunks)


def _load_rubric(name: str):
    try:
        return importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    except ModuleNotFoundError as e:
        missing = e.name or ""
        if missing == _RUBRIC_PKG or missing.startswith(f"{_RUBRIC_PKG}."):
            logger.warning(f"rubric module {name!r} missing; using empty CHECKS")
            return SimpleNamespace(CHECKS=[])
        raise



def _workspace_snapshot(env) -> dict[str, bytes | None]:
    fs = env.workspace.fs
    snapshot: dict[str, bytes | None] = {}
    for basename in TRACKED_WORKSPACE_FILES:
        logical_path = f"/workspace/{basename}"
        runtime_path = f"/terrarium/openclaw/workspace/{basename}"
        try:
            value = fs.read_file(runtime_path)
            snapshot[logical_path] = value if isinstance(value, bytes) else str(value).encode("utf-8")
        except Exception:
            snapshot[logical_path] = None
    return snapshot


def _persist_stage_audit(
    env, stage_idx: int, event_ids: list[str],
    before: dict[str, bytes | None], after: dict[str, bytes | None],
) -> None:
    changed_paths = sorted(
        path for path in set(before) | set(after)
        if before.get(path) != after.get(path) and after.get(path) is not None
    )
    added_text_by_path: dict[str, str] = {}
    changed_context_by_path: dict[str, str] = {}
    changed_hunks_by_path: dict[str, list[dict[str, str]]] = {}
    for path in changed_paths:
        old_text = (before.get(path) or b"").decode("utf-8", errors="replace").splitlines()
        new_text = (after.get(path) or b"").decode("utf-8", errors="replace").splitlines()
        matcher = difflib.SequenceMatcher(a=old_text, b=new_text, autojunk=False)
        added_lines: list[str] = []
        context_lines: list[str] = []
        hunks: list[dict[str, str]] = []
        for tag, _i1, _i2, j1, j2 in matcher.get_opcodes():
            if tag not in ("insert", "replace"):
                continue
            added_lines.extend(new_text[j1:j2])
            heading = ""
            for line in reversed(new_text[:j1]):
                if line.lstrip().startswith("#"):
                    heading = line
                    break
            if heading:
                context_lines.append(heading)
            context_lines.extend(new_text[j1:j2])
            hunks.append({
                "heading": heading,
                "added_text": "\n".join(new_text[j1:j2]),
            })
        added_text_by_path[path] = "\n".join(added_lines)
        changed_context_by_path[path] = "\n".join(context_lines)
        changed_hunks_by_path[path] = hunks
    payload = {
        "stage": stage_idx,
        "event_ids": [str(event_id) for event_id in event_ids if event_id],
        "changed_paths": changed_paths,
        "added_text_by_path": added_text_by_path,
        "changed_context_by_path": changed_context_by_path,
        "changed_hunks_by_path": changed_hunks_by_path,
    }
    env.workspace.fs.write_file(
        f"{STAGE_AUDIT_DIR}/stage_{stage_idx}.json",
        json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
    )


def _persist_stage_score(
    env,
    stage_idx: int,
    checks: list[Check],
    total_weight: float,
    passed_weight: float,
) -> None:
    payload = {
        "stage": stage_idx,
        "total_weight": total_weight,
        "passed_weight": passed_weight,
        "score": (passed_weight / total_weight) if total_weight else None,
        "checks": [
            {
                "name": str(getattr(check, "name", "")),
                "passed": bool(getattr(check, "passed", False)),
            }
            for check in checks
        ],
    }
    env.workspace.fs.write_file(
        f"{SCORES_DIR}/stage_{stage_idx}.json",
        json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
    )

def _run_rubric_checks(
    checks_spec, env, tag: str
) -> tuple[list[Check], float, float, list[tuple[str, float, bool]]]:
    out: list[Check] = []
    outcomes: list[tuple[str, float, bool]] = []
    total_w = 0.0
    passed_w = 0.0
    for cid, fn, weight in checks_spec:
        try:
            ok = bool(fn(env))
        except Exception as e:
            logger.warning(f"checker {cid!r} raised: {e}")
            ok = False
        out.append(Check(name=cid, passed=ok, tags=[tag]))
        numeric_weight = float(weight)
        outcomes.append((str(cid), numeric_weight, ok))
        total_w += numeric_weight
        if ok:
            passed_w += numeric_weight
    return out, total_w, passed_w, outcomes


@entry(
    capabilities=[
        "ecommerce_mock", "delivery_logistics_mock", "credit_card_mock",
        "email_mock", "calendar_mock", "notification_hub_mock",
        "weather_mock", "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def central_ac_install_30d(env, agent):
    _register_all_mcp(env, agent)
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)
    env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/terrarium/openclaw/workspace")
    env.workspace.shell.exec("chmod -R a+rwX /terrarium/openclaw/workspace", user="root")
    env.workspace.shell.exec(f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {SCORES_DIR} {STAGE_AUDIT_DIR}")
    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    stage_modules = {i: _load_rubric(f"stage_{i}") for i in range(stage_count)}
    final_mod = _load_rubric("final")
    all_checks: list[Check] = []
    all_outcomes: list[tuple[str, float, bool]] = []
    stage_ratio_sum = 0.0
    for stage_idx in range(stage_count):
        before_workspace = _workspace_snapshot(env)
        events = list(events_by_stage.get(stage_idx, []))
        events.sort(key=lambda e: (str(e.get("time", "")), str(e.get("id", ""))))
        stage_texts: list[str] = []
        stage_tool_calls: list[dict[str, Any]] = []
        for ev in events:
            txt, tool_calls = _dispatch_event(ev, env, agent)
            if txt:
                stage_texts.append(_limit_text(txt))
            stage_tool_calls.extend(tool_calls)
        env.workspace.fs.write_file(f"{RESPONSES_DIR}/stage_{stage_idx}.txt", "\n---\n".join(stage_texts).encode("utf-8"))
        env.workspace.fs.write_file(f"{TRACE_DIR}/stage_{stage_idx}.json", json.dumps(stage_tool_calls, ensure_ascii=False, indent=2).encode("utf-8"))
        after_workspace = _workspace_snapshot(env)
        _persist_stage_audit(
            env, stage_idx, [str(event.get("id") or "") for event in events],
            before_workspace, after_workspace,
        )
        checks, tw, pw, outcomes = _run_rubric_checks(
            stage_modules[stage_idx].CHECKS, env, f"stage{stage_idx}"
        )
        _persist_stage_score(env, stage_idx, checks, tw, pw)
        all_checks.extend(checks)
        all_outcomes.extend(outcomes)
        stage_ratio_sum += (pw / tw) if tw > 0 else 0.0
    stage_ratio = (stage_ratio_sum / stage_count) if stage_count else 0.0
    final_checks, final_tw, final_pw, final_outcomes = _run_rubric_checks(final_mod.CHECKS, env, "final")
    all_checks.extend(final_checks)
    all_outcomes.extend(final_outcomes)
    final_ratio = (final_pw / final_tw) if final_tw > 0 else 0.0
    cross_mod = _load_rubric("cross_stage")
    cross_checks, cross_tw, cross_pw, cross_outcomes = _run_rubric_checks(
        cross_mod.CHECKS, env, "cross_stage"
    )
    all_checks.extend(cross_checks)
    all_outcomes.extend(cross_outcomes)
    cross_ratio = (cross_pw / cross_tw) if cross_tw > 0 else 0.0
    breakdown = aggregate_score(all_outcomes)
    logger.info(
        "score diagnostics: stage={:.3f} final={:.3f} cross={:.3f} "
        "passed_weight={:.3f} total_weight={:.3f} score={:.3f}".format(
            stage_ratio, final_ratio, cross_ratio,
            breakdown.passed_weight, breakdown.total_weight, breakdown.score,
        )
    )
    return CheckerResults(checks=all_checks, score=breakdown.score)
