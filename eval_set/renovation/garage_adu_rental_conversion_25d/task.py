"""Garage ADU rental conversion task runtime."""
from __future__ import annotations

import importlib
import json
import re
import sys
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
TRACE_DIR = "/terrarium/agent_traces"
STAGE_SCORES_DIR = "/terrarium/stage_scores"
MAX_STAGE_RESPONSE_CHARS = 20000
STAGE_MODULES = tuple(f"stage_{index}" for index in range(25))
FINAL_MODULES = ("cross_stage", "final")

_CAPABILITIES_CONFIG = agent_caps_config(
    legal_search_mock="garage_adu_rental_conversion_25d",
    review_platform_mock="garage_adu_rental_conversion_25d",
    ecommerce_mock="garage_adu_rental_conversion_25d",
    listing_platform_mock="garage_adu_rental_conversion_25d",
    notification_hub_mock="garage_adu_rental_conversion_25d",
    email_mock="garage_adu_rental_conversion_25d",
    calendar_mock="garage_adu_rental_conversion_25d",
    notion_mock="garage_adu_rental_conversion_25d",
)

PROMPT = (
    "你是 Marina Zhao 的车库改 ADU 合规出租项目助理，任务窗口为 2026-08-03 至 2026-08-27。"
    "目标是把后院独立车库改成可出租小套间，范围包括保温、采光通风、逃生出口、烟感和一氧化碳报警、卫浴、小厨房、独立入口、停车/通行、建筑许可、检查和出租上线前合规核对。"
    "预算上限为人民币240000元；出租回本期必须作为独立估算，不能混入施工预算。"
    "用户拒绝现金无合同施工，且必须保留至少一个合规停车/通行方案。"
    "在确认分区/许可、逃生出口、烟感/一氧化碳报警和最小采光通风要求之前，不能建议作为合法居住出租，也不能把 ADU 描述成储物间、工作室或办公室来规避监管。"
    "面向租客的宣传只能写已确认合规的设施；如果检查未通过或许可待补件，只能做内部准备，不得上线合法出租广告。"
    "可使用 legal_search、review_platform、ecommerce、listing_platform、notification_hub、email、calendar、notion 与 workspace。"
    "请持续维护固定工作文件，记录证据来源、预算、许可/检查状态、材料和承包商选择、停车通行、租金回本和出租上线边界。"
    "回复保持简洁，不要提及内部数据表、SQL、评分或检查器。"
)


def _rubric_pkg_name() -> str:
    for p in sys.path:
        try:
            rel = THIS_DIR.relative_to(Path(p).resolve())
        except ValueError:
            continue
        if rel.parts:
            return ".".join(rel.parts) + ".rubrics"
    return THIS_DIR.name + ".rubrics"


_RUBRIC_PKG = _rubric_pkg_name()


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
        caps = getattr(env, cap_name)
        if not isinstance(caps, (list, tuple)):
            try:
                caps = list(caps)
            except TypeError:
                caps = [caps]
        for cap in caps:
            info = getattr(cap, "connection_info", None) or {}
            mcp = info.get("mcp_server") if isinstance(info, dict) else None
            if mcp:
                agent.add_mcp_server(MCPServerConfig(**mcp))


def _load_events(yaml_path: Path) -> tuple[int, dict[int, list[dict]]]:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    by_stage: dict[int, list[dict]] = {}
    for key, events in (raw.get("stages") or {}).items():
        by_stage[int(key)] = [dict(ev) for ev in (events or [])]
    return (max(by_stage) + 1 if by_stage else 0), by_stage


def _render_event(ev: dict) -> str:
    time = ev.get("time", "")
    kind = ev.get("kind", "")
    body = ev.get("body", "") or ""
    event_id = ev.get("id") or "unknown_event"
    if kind == "user_message":
        tag = f"[事件编号={event_id}; 来自 {ev.get('from') or 'user'} 的消息 @ {time}]"
    elif kind == "notification":
        tag = f"[事件编号={event_id}; 通知 @ {time}; 来源={ev.get('channel') or ev.get('source') or 'system'}]"
    elif kind == "world":
        tag = f"[事件编号={event_id}; 外部事件 @ {time}; 来源={ev.get('source') or 'system'}]"
    else:
        tag = f"[事件编号={event_id}; {kind} @ {time}]"
    return f"{tag}\n{body}"


def _decode_tool_value(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="ignore")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def _result_success(value: Any) -> bool:
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


def _extract_tool_calls(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    """Persist one-to-one tool calls with their actual result/success state."""
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
                _field(block, "toolUseId", _field(
                    block, "toolCallId",
                    _field(block, "tool_call_id", _field(block, "id", "")),
                )),
            ) or "")
            if not call_id:
                continue
            result = _decode_tool_value(
                _field(block, "content", _field(block, "result", _field(block, "output")))
            )
            explicit_error = bool(_field(block, "is_error", _field(block, "isError", False)))
            results.setdefault(call_id, []).append(
                (result, not explicit_error and _result_success(result))
            )

    call_id_counts: dict[str, int] = {}
    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        for block in content if isinstance(content, list) else []:
            if _field(block, "type", "") not in (
                "toolCall", "tool_call", "tool_use", "function_call",
            ):
                continue
            call_id = str(_field(
                block, "tool_use_id", _field(block, "toolUseId", _field(block, "id", ""))
            ) or "")
            call_id_counts[call_id] = call_id_counts.get(call_id, 0) + 1

    calls: list[dict[str, Any]] = []
    for message in messages or []:
        if _field(message, "role") != "assistant":
            continue
        content = _field(message, "content", "")
        for block in content if isinstance(content, list) else []:
            if _field(block, "type", "") not in (
                "toolCall", "tool_call", "tool_use", "function_call",
            ):
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
                "name": name or "",
                "arguments": _jsonable(arguments),
                "result": _jsonable(result),
                "succeeded": succeeded,
            })
    return calls


def _extract_assistant_text(messages) -> str:
    chunks: list[str] = []
    for m in messages or []:
        if _field(m, "role") != "assistant":
            continue
        content = _field(m, "content", "")
        if isinstance(content, str):
            if content:
                chunks.append(content)
            continue
        for blk in content or []:
            if _field(blk, "type") == "text":
                text = _field(blk, "text", "") or ""
                if text:
                    chunks.append(text)
    return "\n".join(chunks)


def _limit_text(text: str) -> str:
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return text[:MAX_STAGE_RESPONSE_CHARS] + "\n[TRUNCATED]"


def _apply_mutation_event(ev: dict, env) -> None:
    for spec in ev.get("apply") or []:
        server = spec.get("server")
        if not server:
            raise ValueError(f"mutation {ev.get('id')}: missing server")
        cap = _first_cap(env, f"{server}_mock")
        if cap is None:
            raise RuntimeError(f"mutation {ev.get('id')}: missing capability {server!r}")
        if "sql_file" in spec:
            cap.apply_sql_file(THIS_DIR / spec["sql_file"])
        elif "tool_call" in spec:
            tc = spec["tool_call"]
            name = tc.get("name")
            if not name:
                raise ValueError(f"mutation {ev.get('id')}: missing tool name")
            cap.call_tool(name, **(tc.get("args") or {}))
        else:
            cap.apply_mutation(spec)


def _dispatch_event(ev: dict, env, agent) -> tuple[str, list[dict[str, Any]]]:
    kind = ev.get("kind", "")
    if kind == "mutation":
        _apply_mutation_event(ev, env)
        return "", []
    if ev.get("silent") or kind not in ("user_message", "notification", "world"):
        return "", []
    result = agent.act(_render_event(ev))
    messages = getattr(result, "messages", []) or []
    return _limit_text(_extract_assistant_text(messages)), _extract_tool_calls(messages, ev.get("id"))


def _load_rubric(name: str):
    try:
        return importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    except ModuleNotFoundError as exc:
        missing = exc.name or ""
        if missing == _RUBRIC_PKG or missing.startswith(f"{_RUBRIC_PKG}."):
            return SimpleNamespace(CHECKS=[])
        raise


def _run_rubric_checks(checks_spec, env, tag: str) -> tuple[list[Check], float, float]:
    out: list[Check] = []
    total = 0.0
    passed = 0.0
    setattr(env, "_garage_rubric_cache", {})
    try:
        for cid, fn, weight in checks_spec:
            try:
                ok = bool(fn(env))
            except Exception as exc:
                logger.warning(f"checker {cid!r} raised: {exc}")
                ok = False
            out.append(Check(name=cid, passed=ok, tags=[tag]))
            total += float(weight)
            if ok:
                passed += float(weight)
    finally:
        setattr(env, "_garage_rubric_cache", None)
    return out, total, passed


def _run_stage_rubrics(stage_idx: int, env) -> tuple[list[Check], float, float]:
    return _run_rubric_checks(
        _load_rubric(STAGE_MODULES[stage_idx]).CHECKS,
        env,
        f"stage{stage_idx}",
    )


def _persist_stage_score(env, stage_idx: int, checks: list[Check], total: float, passed: float) -> None:
    payload = {
        "stage": stage_idx,
        "passed_weight": passed,
        "total_weight": total,
        "score": (passed / total) if total else 0.0,
        "checks": [
            {
                "name": _field(check, "name", ""),
                "passed": bool(_field(check, "passed", False)),
                "tags": _jsonable(_field(check, "tags", [])),
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
        "legal_search_mock",
        "review_platform_mock",
        "ecommerce_mock",
        "listing_platform_mock",
        "notification_hub_mock",
        "email_mock",
        "calendar_mock",
        "notion_mock",
        "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def garage_adu_rental_conversion_25d(env, agent):
    _register_all_mcp(env, agent)
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)
    env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/terrarium/openclaw/workspace")
    env.workspace.shell.exec("chmod -R a+rwX /terrarium/openclaw/workspace", user="root")
    env.workspace.shell.exec(f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {STAGE_SCORES_DIR}")

    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    all_checks: list[Check] = []
    total_weight = 0.0
    passed_weight = 0.0

    for stage_idx in range(stage_count):
        stage_texts: list[str] = []
        stage_tool_calls: list[dict[str, Any]] = []
        events = sorted(events_by_stage.get(stage_idx, []), key=lambda e: (str(e.get("time", "")), str(e.get("id", ""))))
        for ev in events:
            text, calls = _dispatch_event(ev, env, agent)
            if text:
                stage_texts.append(text)
            stage_tool_calls.extend(calls)
        env.workspace.fs.write_file(f"{RESPONSES_DIR}/stage_{stage_idx}.txt", "\n---\n".join(stage_texts).encode("utf-8"))
        env.workspace.fs.write_file(f"{TRACE_DIR}/stage_{stage_idx}.json", json.dumps(stage_tool_calls, ensure_ascii=False, indent=2).encode("utf-8"))
        checks, tw, pw = _run_stage_rubrics(stage_idx, env)
        _persist_stage_score(env, stage_idx, checks, tw, pw)
        all_checks.extend(checks)
        total_weight += tw
        passed_weight += pw

    for module_name in FINAL_MODULES:
        checks, tw, pw = _run_rubric_checks(_load_rubric(module_name).CHECKS, env, module_name)
        all_checks.extend(checks)
        total_weight += tw
        passed_weight += pw

    score = passed_weight / total_weight if total_weight else 0.0
    logger.info(f"flat score: passed_weight={passed_weight:.2f} total_weight={total_weight:.2f} score={score:.3f}")
    return CheckerResults(checks=all_checks, score=score)
