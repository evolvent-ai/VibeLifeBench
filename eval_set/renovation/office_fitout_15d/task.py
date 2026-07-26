"""Commercial office fit-out task runtime."""
from __future__ import annotations

import asyncio
import hashlib
import importlib
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import yaml
from loguru import logger
from terrarium.models.checker import Check, CheckerResults
from terrarium.models.mcp import MCPServerConfig
from terrarium.task.decorator import entry

from capabilities import agent_caps_config

THIS_DIR = Path(__file__).resolve().parent
RESPONSES_DIR = "/terrarium/agent_responses"
STAGE_SCORES_DIR = "/terrarium/stage_scores"
CONTAINER_WORKSPACE = "/terrarium/openclaw/workspace"

SNAPSHOT_FILES = ('fit_out_plan.md', 'requirements_brief.md', 'vendor_comparison.md', 'budget_tracker.md', 'schedule.md', 'strong_weak_power_plan.md', 'fire_compliance_checklist.md', 'decoration_decisions.md', 'risk_register.md', 'communications_log.md', 'handover_punch_list.md')
STAGE_MODULES = tuple(f"stage_{index}" for index in range(21))
FINAL_MODULES = ("cross_stage", "final")
CAPABILITIES = ['email_mock', 'calendar_mock', 'notion_mock', 'maps_mock', 'visa_and_advisory_mock', 'hotel_booking_mock', 'weather_mock', 'workspace']
CAPABILITIES_CONFIG = agent_caps_config(**{'email_mock': 'office_fitout_15d', 'calendar_mock': 'office_fitout_15d', 'notion_mock': 'office_fitout_15d', 'maps_mock': 'office_fitout_15d', 'visa_and_advisory_mock': 'office_fitout_15d', 'hotel_booking_mock': 'office_fitout_15d', 'weather_mock': 'office_fitout_15d'})


def _rubric_pkg_name() -> str:
    for p in sys.path:
        try:
            rel = THIS_DIR.relative_to(Path(p).resolve())
        except ValueError:
            continue
        if not rel.parts:
            return "rubrics"
        return ".".join(rel.parts) + ".rubrics"
    raise RuntimeError(f"Cannot derive rubric package name: {THIS_DIR} is not under any sys.path entry.")


_RUBRIC_PKG = _rubric_pkg_name()


class _AsyncFS:
    def __init__(self, fs):
        self._fs = fs

    async def exists(self, path: str) -> bool:
        try:
            return bool(self._fs.exists(path))
        except Exception:
            return False

    async def read_file(self, path: str) -> str:
        data = self._fs.read_file(path)
        if isinstance(data, bytes):
            return data.decode("utf-8", errors="replace")
        return str(data or "")


class _ToolManager:
    def __init__(self, cap):
        self._cap = cap

    async def call_tool(self, tool: str, **args: Any) -> Any:
        if tool == "query_database":
            tool = "API-post-database-query"
            if "database" in args and "database_id" not in args:
                args["database_id"] = args.pop("database")
        elif tool == "get_page":
            tool = "API-retrieve-a-page"
        elif tool == "search":
            tool = "API-post-search"
        async_call = getattr(self._cap, "call_tool_async", None)
        if async_call is not None:
            return await async_call(tool, **args)
        return await asyncio.to_thread(self._cap.call_tool, tool, **args)


def _first_cap(env, cap_name: str):
    cap = getattr(env, cap_name, None)
    if cap is None:
        return None
    if isinstance(cap, (list, tuple)):
        return cap[0] if cap else None
    try:
        return next(iter(cap))
    except TypeError:
        return cap
    except StopIteration:
        return None


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
        stage_idx = int(k)
        bucket = by_stage.setdefault(stage_idx, [])
        for ev in evs or []:
            event = dict(ev)
            event["_stage"] = stage_idx
            bucket.append(event)
    stage_count = (max(by_stage) + 1) if by_stage else 0
    return stage_count, by_stage


def _event_body(ev: dict) -> str:
    return str(ev.get("body") or ev.get("payload") or ev.get("text") or "")


def _event_datetime(ev: dict) -> str:
    raw = str(ev.get("time") or "")
    if "T" in raw:
        return raw
    stage = int(ev.get("_stage", 0))
    day = date(2026, 7, 1) + timedelta(days=stage)
    return f"{day.isoformat()}T{raw or '09:00'}:00+08:00"


def _parse_inbound_email(ev: dict) -> dict[str, str] | None:
    if ev.get("kind") != "world" or ev.get("source") not in {"email", "emails"}:
        return None
    body = _event_body(ev)
    if "From:" not in body or "Subject:" not in body:
        return None
    from_match = re.search(r"(?m)^\s*From:\s*(.+?)\s*$", body)
    subject_match = re.search(r"(?m)^\s*Subject:\s*(.+?)\s*$", body)
    if not from_match or not subject_match:
        raise ValueError(f"email event {ev.get('id')} lacks a parseable From/Subject header")
    content_start = subject_match.end()
    content = body[content_start:].lstrip("\r\n ")
    if not content:
        raise ValueError(f"email event {ev.get('id')} has no message body")
    return {
        "from_addr": from_match.group(1).strip(),
        "subject": subject_match.group(1).strip(),
        "body_text": content,
    }


def _email_event_row_id(event_id: str) -> int:
    """Return a deterministic negative SQLite row id for a scenario event."""
    digest = hashlib.sha256(event_id.encode("utf-8")).digest()
    positive = int.from_bytes(digest[:8], "big") & 0x7FFF_FFFF_FFFF_FFFF
    return -(positive or 1)


def _materialize_email_event(ev: dict, env) -> None:
    parsed = _parse_inbound_email(ev)
    if parsed is None:
        return
    cap = _first_cap(env, "email_mock")
    if cap is None:
        raise RuntimeError(f"email event {ev.get('id')}: email capability unavailable")
    event_id = str(ev.get("id") or "unknown")
    timestamp = _event_datetime(ev)
    cap.apply_mutation({
        "server": "email",
        "table": "messages",
        "op": "upsert",
        "conflict_keys": ["id"],
        "values": {
            "id": _email_event_row_id(event_id),
            "folder_id": 1,
            "message_id": f"<event-{event_id}@office-fitout.local>",
            "subject": parsed["subject"],
            "from_addr": parsed["from_addr"],
            "to_addr_json": '["zhou_mu@startup-coo.example.com"]',
            "cc_addr_json": "[]",
            "bcc_addr_json": "[]",
            "date": timestamp,
            "body_text": parsed["body_text"],
            "body_html": None,
            "is_read": 0,
            "is_important": 1,
            "is_flagged": 0,
            "in_reply_to": None,
            "references_header": None,
            "headers_json": json.dumps({"X-Scenario-Event": event_id}, ensure_ascii=False),
            "uid": None,
            "size": len(parsed["body_text"]),
            "created_at": timestamp,
        },
    })


def _render_event(ev: dict) -> str:
    time = _event_datetime(ev)
    kind = ev.get("kind", "")
    body = _event_body(ev)
    if kind == "user_message":
        tag = f"[Message from {ev.get('from') or 'user'} @ {time}]"
    elif kind == "notification":
        tag = f"[Notification @ {time} from {ev.get('channel') or ev.get('source') or 'system'}]"
    elif kind == "world" and (email := _parse_inbound_email(ev)) is not None:
        return (
            f"[New email @ {time}]\n"
            f"收件箱收到来自 {email['from_addr']} 的邮件《{email['subject']}》。"
            "请读取收件箱原文后再判断和行动。"
        )
    elif kind == "world":
        tag = f"[World event @ {time} from {ev.get('source') or 'system'}]"
    elif kind == "cron_fire":
        tag = f"[Reminder @ {time}]"
    else:
        tag = f"[{kind} @ {time}]"
    return f"{tag}\n{body}"


def _extract_assistant_text(messages) -> str:
    chunks: list[str] = []
    for message in messages or []:
        if _blk_field(message, "role", None) != "assistant":
            continue
        content = _blk_field(message, "content", "")
        if isinstance(content, str):
            if content:
                chunks.append(content)
            continue
        for block in content or []:
            if _blk_field(block, "type", "") == "text":
                text = _blk_field(block, "text", "") or ""
                if text:
                    chunks.append(text)
    return "\n".join(chunks)


def _blk_field(obj, name, default=None):
    """Read a field from a pydantic block or a plain dict."""
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _decode_tool_value(value):
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="ignore")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:  # noqa: BLE001
            return value
    return value


def _result_success(value) -> bool:
    value = _decode_tool_value(value)
    if isinstance(value, str):
        probe = value.replace('\\"', '"').lower()
        if re.search(r'"(?:success|ok)"\s*:\s*false', probe):
            return False
        if re.search(r'"status"\s*:\s*"(?:error|failed|failure|exception)"', probe):
            return False
        if re.search(r'"error"\s*:\s*"(?!\s*")', probe):
            return False
        return True
    if isinstance(value, dict):
        if value.get("success") is False or value.get("ok") is False:
            return False
        status = str(value.get("status") or "").lower()
        if status in {"error", "failed", "failure", "exception"}:
            return False
        if value.get("error") not in (None, "", False):
            return False
        return all(_result_success(child) for child in value.values())
    if isinstance(value, list):
        return all(_result_success(child) for child in value)
    return True


def _extract_tool_calls(messages) -> list[dict]:
    """Collect one-to-one tool calls with result and success evidence."""
    results: dict[str, list[tuple[object, bool]]] = {}
    for message in messages or []:
        content = _blk_field(message, "content", "")
        for block in content if isinstance(content, list) else []:
            if _blk_field(block, "type", "") not in (
                "toolResult", "tool_result", "tool_response", "function_result",
            ):
                continue
            call_id = str(_blk_field(
                block, "tool_use_id",
                _blk_field(block, "toolUseId", _blk_field(
                    block, "toolCallId",
                    _blk_field(block, "tool_call_id", _blk_field(block, "id", "")),
                )),
            ) or "")
            if not call_id:
                continue
            result = _decode_tool_value(_blk_field(
                block, "content", _blk_field(block, "result", _blk_field(block, "output"))
            ))
            explicit_error = bool(_blk_field(block, "is_error", _blk_field(block, "isError", False)))
            results.setdefault(call_id, []).append(
                (result, not explicit_error and _result_success(result))
            )

    raw_calls: list[tuple[str, str, object]] = []
    seen_ids: set[str] = set()
    for message in messages or []:
        if _blk_field(message, "role") != "assistant":
            continue
        content = _blk_field(message, "content", "")
        for block in content if isinstance(content, list) else []:
            if _blk_field(block, "type", "") not in (
                "tool_use", "toolCall", "tool_call", "function_call",
            ):
                continue
            function = _blk_field(block, "function", None)
            call_id = str(_blk_field(
                block, "tool_use_id", _blk_field(block, "toolUseId", _blk_field(block, "id", ""))
            ) or "")
            name = (
                _blk_field(function, "name", _blk_field(block, "name", ""))
                if function is not None else _blk_field(block, "name", "")
            )
            args = _blk_field(block, "input", None)
            if args is None:
                args = (
                    _blk_field(function, "arguments", _blk_field(block, "arguments", {}))
                    if function is not None else _blk_field(block, "arguments", {})
                )
            raw_calls.append((call_id, str(name or ""), args))
            if call_id:
                seen_ids.add(call_id)
        for call in _blk_field(message, "tool_calls", None) or []:
            function = _blk_field(call, "function", None)
            call_id = str(_blk_field(call, "id", "") or "")
            if call_id and call_id in seen_ids:
                continue
            name = _blk_field(call, "name", None) or (
                _blk_field(function, "name", None) if function is not None else None
            )
            args = _blk_field(call, "arguments", None)
            if args is None and function is not None:
                args = _blk_field(function, "arguments", None)
            raw_calls.append((call_id, str(name or ""), args))

    id_counts: dict[str, int] = {}
    for call_id, _, _ in raw_calls:
        id_counts[call_id] = id_counts.get(call_id, 0) + 1

    calls: list[dict] = []
    for call_id, name, args in raw_calls:
        result_rows = results.get(call_id, [])
        paired = bool(call_id) and id_counts.get(call_id) == 1 and len(result_rows) == 1
        result = result_rows[0][0] if paired else None
        calls.append({
            "id": call_id or None,
            "name": name,
            "input": _coerce_args(args),
            "result": result,
            "succeeded": paired and result_rows[0][1] is True,
        })
    return calls


def _coerce_args(args):
    """Normalize tool arguments to a dict (backends may send a JSON string)."""
    if isinstance(args, str):
        try:
            return json.loads(args)
        except Exception:  # noqa: BLE001
            return {"_raw": args}
    if isinstance(args, dict):
        return args
    if args is None:
        return {}
    if hasattr(args, "model_dump"):
        try:
            return args.model_dump()
        except Exception:  # noqa: BLE001
            pass
    return {"_raw": str(args)}


def _service_cap_name(server: str) -> str:
    return {
        "emails": "email_mock",
        "email": "email_mock",
        "calendar": "calendar_mock",
        "google_calendar": "calendar_mock",
        "hotel_booking": "hotel_booking_mock",
        "maps": "maps_mock",
        "notion": "notion_mock",
        "visa_and_advisory": "visa_and_advisory_mock",
        "weather": "weather_mock",
    }.get(server, f"{server}_mock")


def _apply_mutation_event(ev: dict, env) -> None:
    for entry_spec in ev.get("apply") or []:
        server = entry_spec.get("server")
        if not server:
            raise ValueError(f"mutation {ev.get('id')}: missing 'server' in apply entry")
        cap = _first_cap(env, _service_cap_name(server))
        if cap is None:
            raise RuntimeError(f"mutation {ev.get('id')}: no capability for server {server!r}")
        if "sql_file" in entry_spec:
            cap.apply_sql_file(THIS_DIR / entry_spec["sql_file"])
        elif "tool_call" in entry_spec:
            tc = entry_spec["tool_call"]
            if not tc.get("name"):
                raise ValueError(f"mutation {ev.get('id')}: tool_call missing name")
            cap.call_tool(tc["name"], **(tc.get("args") or {}))
        else:
            cap.apply_mutation(entry_spec)


def _dispatch_event(ev: dict, env, agent) -> tuple[str, list[dict]]:
    kind = ev.get("kind", "")
    if kind == "mutation":
        _apply_mutation_event(ev, env)
        return "", []
    if ev.get("silent"):
        return "", []
    if kind not in ("user_message", "notification", "world", "cron_fire"):
        logger.warning(f"event {ev.get('id')}: unknown kind {kind!r}; rendering as text")
    result = agent.act(_render_event(ev))
    messages = getattr(result, "messages", []) or []
    return _extract_assistant_text(messages), _extract_tool_calls(messages)


def _dispatch_stage_events(events: list[dict], env, agent) -> list[dict]:
    """Dispatch one stage while batching consecutive visible events.

    Mutations are applied in order, but adjacent visible messages are merged so
    long renovation stages do not burn one full model turn per notification.
    """
    turn_entries: list[dict] = []
    pending_events: list[dict] = []

    def flush() -> None:
        if not pending_events:
            return
        prompt = "\n\n---\n\n".join(_render_event(ev) for ev in pending_events)
        result = agent.act(prompt)
        messages = getattr(result, "messages", []) or []
        response = _extract_assistant_text(messages)
        tool_calls = _extract_tool_calls(messages)
        for idx, ev in enumerate(pending_events):
            turn_entries.append({
                "event_id": ev.get("id"),
                "response": response if idx == 0 else "",
                "tool_calls": tool_calls if idx == 0 else [],
                "write_response": idx == 0,
            })
        pending_events.clear()

    for ev in events:
        kind = ev.get("kind", "")
        if kind == "mutation":
            flush()
            _apply_mutation_event(ev, env)
            turn_entries.append({"event_id": ev.get("id"), "response": "", "tool_calls": []})
            continue
        if ev.get("silent"):
            continue
        if kind not in ("user_message", "notification", "world", "cron_fire"):
            logger.warning(f"event {ev.get('id')}: unknown kind {kind!r}; rendering as text")
        _materialize_email_event(ev, env)
        pending_events.append(ev)

    flush()
    return turn_entries


def _load_rubric(name: str):
    return importlib.import_module(f"{_RUBRIC_PKG}.{name}")


async def _run_one_check(fn, ctx) -> bool:
    result = fn(ctx)
    if hasattr(result, "__await__"):
        result = await result
    return bool(result)


def _run_check_list(checks_spec, ctx, tag: str) -> tuple[list[Check], float, float]:
    out: list[Check] = []
    total_w = 0.0
    passed_w = 0.0
    for cid, fn, weight in checks_spec:
        try:
            ok = asyncio.run(_run_one_check(fn, ctx))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"checker {cid!r} raised: {e}")
            ok = False
        out.append(Check(name=cid, passed=ok, tags=[tag]))
        total_w += float(weight)
        if ok:
            passed_w += float(weight)
    return out, total_w, passed_w


def _make_context(env, turn_log: list[dict], snapshots: dict[str, dict[str, str]]):
    fs = _AsyncFS(env.workspace.fs)
    ctx = SimpleNamespace(
        env=env,
        fs=fs,
        filesystem=fs,
        workspace=env.workspace,
        container_workspace=CONTAINER_WORKSPACE,
        turn_log=turn_log,
        snapshots=snapshots,
    )
    for service, cap_name in {
        "emails": "email_mock",
        "email": "email_mock",
        "calendar": "calendar_mock",
        "google_calendar": "calendar_mock",
        "hotel_booking": "hotel_booking_mock",
        "maps": "maps_mock",
        "notion": "notion_mock",
        "visa_and_advisory": "visa_and_advisory_mock",
        "weather": "weather_mock",
    }.items():
        cap = _first_cap(env, cap_name)
        if cap is not None:
            setattr(ctx, service, _ToolManager(cap))
    return ctx


def _snapshot(env) -> dict[str, str]:
    out: dict[str, str] = {}
    for name in SNAPSHOT_FILES:
        path = f"{CONTAINER_WORKSPACE}/{name}"
        try:
            if env.workspace.fs.exists(path):
                data = env.workspace.fs.read_file(path)
                out[name] = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else str(data or "")
        except Exception:
            continue
    return out


def _run_stage_rubrics(ctx, stage_idx: int) -> tuple[list[Check], float, float]:
    module_name = f"stage_{stage_idx}"
    module = _load_rubric(module_name)
    return _run_check_list(getattr(module, "CHECKS", []), ctx, module_name)


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
        "score": (passed_weight / total_weight) if total_weight else 0.0,
        "checks": [
            {
                "name": getattr(check, "name", ""),
                "passed": bool(getattr(check, "passed", False)),
                "tags": list(getattr(check, "tags", []) or []),
            }
            for check in checks
        ],
    }
    env.workspace.fs.write_file(
        f"{STAGE_SCORES_DIR}/stage_{stage_idx}.json",
        json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
    )


@entry(
    capabilities=[
        'email_mock',
        'calendar_mock',
        'notion_mock',
        'maps_mock',
        'visa_and_advisory_mock',
        'hotel_booking_mock',
        'weather_mock',
        'workspace',
    ],
    capabilities_config=CAPABILITIES_CONFIG,
)
def office_fitout_15d(env, agent):
    _register_all_mcp(env, agent)
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)

    env.workspace.fs.upload(str(THIS_DIR / "workspace"), CONTAINER_WORKSPACE)
    env.workspace.shell.exec(f"chmod -R a+rwX {CONTAINER_WORKSPACE}", user="root")
    env.workspace.shell.exec(f"mkdir -p {RESPONSES_DIR} {STAGE_SCORES_DIR}")

    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    turn_log: list[dict] = []
    snapshots: dict[str, dict[str, str]] = {}
    all_checks: list[Check] = []
    total_weight = 0.0
    passed_weight = 0.0

    for stage_idx in range(stage_count):
        events = list(events_by_stage.get(stage_idx, []))
        events.sort(key=lambda e: (str(e.get("time", "")), str(e.get("id", ""))))
        stage_entries = _dispatch_stage_events(events, env, agent)
        stage_texts: list[str] = []
        for entry in stage_entries:
            entry["stage"] = stage_idx
            turn_log.append(entry)
            if entry.get("response") and entry.get("write_response", True):
                stage_texts.append(entry["response"])
        env.workspace.fs.write_file(
            f"{RESPONSES_DIR}/stage_{stage_idx}.txt",
            "\n---\n".join(stage_texts).encode("utf-8"),
        )
        snapshots[f"T{stage_idx}"] = _snapshot(env)
        stage_ctx = _make_context(env, turn_log, snapshots)
        checks, stage_total, stage_passed = _run_stage_rubrics(stage_ctx, stage_idx)
        _persist_stage_score(env, stage_idx, checks, stage_total, stage_passed)
        all_checks.extend(checks)
        total_weight += stage_total
        passed_weight += stage_passed

    ctx = _make_context(env, turn_log, snapshots)
    for module_name in FINAL_MODULES:
        module = _load_rubric(module_name)
        checks, module_total, module_passed = _run_check_list(
            getattr(module, "CHECKS", []), ctx, module_name
        )
        all_checks.extend(checks)
        total_weight += module_total
        passed_weight += module_passed
    return CheckerResults(
        checks=all_checks,
        score=(passed_weight / total_weight) if total_weight else 0.0,
    )
