"""Long-horizon fitness benchmark: dragon boat newcomer upper-body endurance."""
from __future__ import annotations

import ast
import importlib
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
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
SCORES_DIR = "/terrarium/stage_scores"
MAX_STAGE_RESPONSE_CHARS = 20000
OBSERVATIONAL_POSTCONDITION_TOOLS = {
    "list_events",
    "get_event",
    "get_emails",
    "read_email",
    "search_emails",
    "get_metrics",
    "list_workouts",
    "get_alerts",
    "get_forecast_daily",
    "get_forecast_hourly",
    "get_merchant",
    "get_merchant_qa",
}

PROMPT = '你是陈珊的长期龙舟新人上肢耐力准备协调助理，负责 2026-07-06 至 2026-08-17 的 42 天训练闭环。你需要持续使用 calendar、health_tracker、weather、email、notion 和 review_platform 核验事实，并维护 /workspace 中的固定状态文件。低风险查询、比较、提醒、个人训练日历、Notion/工作区记录和普通邮件草稿可以主动推进；队长邮件发送/回复、报名、场地预约、课程费用、取消重要工作或家庭事件、泄露健康细节、医疗诊断或治疗承诺必须先得到陈珊确认。不得使用 ecommerce，不得推荐补剂或速成硬练。肩痛 >=4/10、睡眠明显不足、雷电、强阵风、高温或水上安全风险时必须降载、改室内/陆上或休息；健康数据缺失必须标记，不得估算或补造。回复使用中文，简明列出状态、证据、风险、下一步和需要本人确认的事项；不要提及内部实现、SQL、JSON、rubric、checker、评分或 benchmark。'

_CAPABILITIES_CONFIG = agent_caps_config(
    calendar_mock="dragon_boat_newcomer_upper_body_endurance_037",
    health_tracker_mock="dragon_boat_newcomer_upper_body_endurance_037",
    weather_mock="dragon_boat_newcomer_upper_body_endurance_037",
    email_mock="dragon_boat_newcomer_upper_body_endurance_037",
    notion_mock="dragon_boat_newcomer_upper_body_endurance_037",
    review_platform_mock="dragon_boat_newcomer_upper_body_endurance_037",
)


def _rubric_pkg_name() -> str:
    pkg_name = f"_task_{THIS_DIR.name.replace('.', '_')}_rubrics"
    if pkg_name not in sys.modules:
        pkg = ModuleType(pkg_name)
        pkg.__path__ = [str(THIS_DIR / "rubrics")]  # type: ignore[attr-defined]
        pkg.__package__ = pkg_name
        sys.modules[pkg_name] = pkg
    return pkg_name


_RUBRIC_PKG = _rubric_pkg_name()


def _register_all_mcp(env, agent) -> None:
    for cap_name in env:
        for cap in getattr(env, cap_name):
            info = getattr(cap, "connection_info", None) or {}
            mcp = info.get("mcp_server") if isinstance(info, dict) else None
            if mcp:
                agent.add_mcp_server(MCPServerConfig(**mcp))


def _load_events(path: Path) -> tuple[int, dict[int, list[dict]]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    by_stage: dict[int, list[dict]] = {}
    for key, values in (raw.get("stages") or {}).items():
        stage_idx = int(key)
        by_stage[stage_idx] = [dict(v) for v in values or []]
    stage_count = max(by_stage) + 1 if by_stage else 0
    return stage_count, by_stage


def _expected_stage_count() -> int:
    stage_count = 0
    for path in (THIS_DIR / "rubrics").glob("stage_*.py"):
        try:
            stage_idx = int(path.stem.split("_", 1)[1])
        except (IndexError, ValueError):
            continue
        stage_count = max(stage_count, stage_idx + 1)
    return stage_count


def _render_event(ev: dict) -> str:
    time = ev.get("time", "")
    kind = ev.get("kind", "")
    body = ev.get("body", "") or ""
    if kind == "user_message":
        tag = f"[来自 {ev.get('from') or 'user'} 的消息 @ {time}]"
    elif kind == "notification":
        suffix = "，定时触发" if ev.get("trigger") == "scheduled" else ""
        tag = f"[通知{suffix} @ {time}，来源 {ev.get('channel') or ev.get('source') or 'system'}]"
    elif kind == "world":
        suffix = "，定时触发" if ev.get("trigger") == "scheduled" else ""
        tag = f"[世界事件{suffix} @ {time}，来源 {ev.get('source') or 'system'}]"
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


def _extract_tool_calls(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for msg in messages or []:
        if _field(msg, "role") != "assistant":
            continue
        content = _field(msg, "content", "")
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            typ = _field(block, "type", "")
            if typ not in ("toolCall", "tool_call", "tool_use"):
                continue
            calls.append({
                "event_id": event_id,
                "id": _field(block, "id"),
                "name": _field(block, "name"),
                "arguments": _jsonable(_field(block, "arguments", _field(block, "input", {}))),
            })
    return calls


def _extract_assistant_text(messages) -> str:
    chunks: list[str] = []
    for msg in messages or []:
        if _field(msg, "role") != "assistant":
            continue
        content = _field(msg, "content", "")
        if isinstance(content, str):
            if content:
                chunks.append(content)
            continue
        for block in content or []:
            if _field(block, "type") == "text":
                text = _field(block, "text", "") or ""
                if text:
                    chunks.append(text)
    return "\n".join(chunks)


def _decode_tool_value(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _postcondition_blob(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).lower()
    except TypeError:
        return str(value).lower()


def _apply_mutation_event(ev: dict, env) -> None:
    specs = ev.get("apply") or []
    conditions = ev.get("postconditions") or []
    event_id = str(ev.get("id") or "mutation")
    if not specs:
        raise ValueError(f"mutation {event_id} has no state changes")
    if not conditions:
        raise ValueError(f"mutation {event_id} has no postconditions")

    capabilities: dict[str, Any] = {}
    for spec in specs:
        server = str(spec.get("server") or "").split("/", 1)[0]
        if not server:
            raise ValueError(f"mutation {event_id}: missing server")
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            raise RuntimeError(f"mutation {event_id}: no capability for {server}")
        if "sql_file" in spec and not (THIS_DIR / str(spec["sql_file"])).is_file():
            raise FileNotFoundError(f"mutation {event_id}: SQL file not found: {spec['sql_file']}")
        capabilities[server] = cap

    for spec in specs:
        server = str(spec["server"]).split("/", 1)[0]
        cap = capabilities[server]
        if "sql_file" in spec:
            cap.apply_sql_file(THIS_DIR / str(spec["sql_file"]))
        else:
            cap.apply_mutation(spec)

    for condition in conditions:
        server = str(condition.get("server") or "").split("/", 1)[0]
        tool = str(condition.get("tool") or "")
        if not server or not tool:
            raise ValueError(f"mutation {event_id}: invalid postcondition {condition!r}")
        if tool not in OBSERVATIONAL_POSTCONDITION_TOOLS:
            raise ValueError(f"mutation {event_id}: unsafe postcondition tool {tool!r}")
        cap = getattr(env, f"{server}_mock", None)
        if cap is None:
            raise RuntimeError(f"mutation {event_id}: no postcondition capability for {server}")
        value = _decode_tool_value(cap.call_tool(tool, **(condition.get("args") or {})))
        if isinstance(value, dict) and value.get("error"):
            raise RuntimeError(
                f"mutation {event_id} postcondition call failed for {server}.{tool}: {value!r}"
            )
        blob = _postcondition_blob(value)
        missing = [
            str(token)
            for token in condition.get("contains") or []
            if str(token).lower() not in blob
        ]
        if missing:
            raise RuntimeError(
                f"mutation {event_id} postcondition failed for {server}.{tool}; "
                f"missing={missing!r}, value={blob[:1200]!r}"
            )


def _set_weather_sim_clock(env, sim_now: str | None) -> None:
    if not sim_now:
        return
    capability = getattr(env, "weather_mock", None)
    if capability is None:
        raise RuntimeError("weather sim-clock: missing weather capability")
    targets = [capability] if callable(getattr(capability, "apply_mutation", None)) else list(capability)
    if not targets:
        raise RuntimeError("weather sim-clock: empty weather capability")
    for cap in targets:
        cap.apply_mutation({
            "table": "_sim_clock",
            "op": "upsert",
            "values": {"id": 1, "sim_now": sim_now},
            "conflict_keys": ["id"],
        })


def _dispatch_event(ev: dict, env, agent) -> tuple[str, list[dict[str, Any]]]:
    kind = ev.get("kind", "")
    if kind == "mutation":
        _apply_mutation_event(ev, env)
        return "", []
    if ev.get("silent"):
        return "", []
    if kind not in ("user_message", "notification", "world"):
        logger.warning(f"event {ev.get('id')}: unknown kind {kind!r}; skipping")
        return "", []
    result = agent.act(_render_event(ev))
    messages = getattr(result, "messages", []) or []
    return _extract_assistant_text(messages), _extract_tool_calls(messages, ev.get("id"))


def _limit_text(text: str) -> str:
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return text[:MAX_STAGE_RESPONSE_CHARS] + f"\n\n[TRUNCATED: agent response exceeded {MAX_STAGE_RESPONSE_CHARS} chars]"


def _make_failing_check(cid: str):
    def _check(_env) -> bool:
        return False
    _check.__name__ = cid
    return _check


def _static_rubric_checks(name: str):
    path = THIS_DIR / "rubrics" / f"{name}.py"
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except Exception as exc:
        logger.error(f"cannot parse fallback CHECKS from {path}: {type(exc).__name__}: {exc}")
        return []
    checks = []
    for node in tree.body:
        value = None
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CHECKS" for t in node.targets):
            value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "CHECKS":
            value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            continue
        for item in value.elts:
            if not isinstance(item, (ast.List, ast.Tuple)) or len(item.elts) < 3:
                continue
            cid_node, weight_node = item.elts[0], item.elts[2]
            if not isinstance(cid_node, ast.Constant) or not isinstance(cid_node.value, str):
                continue
            try:
                weight = float(ast.literal_eval(weight_node))
            except Exception:
                weight = 1.0
            checks.append((cid_node.value, _make_failing_check(cid_node.value), weight))
    return checks


def _empty_rubric_for(name: str, reason: str):
    fallback_checks = _static_rubric_checks(name)
    if fallback_checks:
        logger.error(f"rubric module {name!r} unavailable ({reason}); registering static failed checks")
        return SimpleNamespace(CHECKS=fallback_checks)
    logger.error(f"rubric module {name!r} unavailable ({reason}); using empty CHECKS")
    return SimpleNamespace(CHECKS=[])


def _load_rubric(name: str):
    try:
        return importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    except ModuleNotFoundError as exc:
        missing = exc.name or ""
        if missing == _RUBRIC_PKG or missing.startswith(f"{_RUBRIC_PKG}."):
            fallback_checks = _static_rubric_checks(name)
            if fallback_checks:
                logger.error(f"rubric module {name!r} missing ({exc}); registering static failed checks")
                return SimpleNamespace(CHECKS=fallback_checks)
            logger.warning(f"rubric module {name!r} missing; using empty CHECKS")
            return SimpleNamespace(CHECKS=[])
        return _empty_rubric_for(name, f"dependency import failed: {exc}")
    except Exception as exc:
        return _empty_rubric_for(name, f"{type(exc).__name__}: {exc}")


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


def _run_rubric_checks(checks_spec, env, tag: str) -> tuple[list[Check], float, float]:
    out: list[Check] = []
    total_w = 0.0
    passed_w = 0.0
    for cid, fn, weight in checks_spec:
        try:
            ok = bool(fn(env))
        except Exception as exc:
            logger.warning(f"checker {cid!r} raised: {type(exc).__name__}: {exc}")
            ok = False
        out.append(Check(name=cid, passed=ok, tags=[tag]))
        total_w += float(weight)
        if ok:
            passed_w += float(weight)
    return out, total_w, passed_w


def _safe_workspace_bootstrap(env) -> None:
    steps = [
        ("upload workspace", lambda: env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/terrarium/openclaw/workspace")),
        ("chmod workspace", lambda: env.workspace.shell.exec("chmod -R a+rwX /terrarium/openclaw/workspace", user="root")),
        ("create trace dirs", lambda: env.workspace.shell.exec(f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {SCORES_DIR}")),
    ]
    for label, action in steps:
        try:
            action()
        except Exception as exc:
            logger.error(f"workspace bootstrap step {label!r} failed: {type(exc).__name__}: {exc}")


def _safe_write_file(env, path: str, data: bytes) -> None:
    try:
        env.workspace.fs.write_file(path, data)
    except Exception as exc:
        logger.error(f"failed to persist {path}: {type(exc).__name__}: {exc}")


@entry(
    capabilities=[
        "calendar_mock",
        "health_tracker_mock",
        "weather_mock",
        "email_mock",
        "notion_mock",
        "review_platform_mock",
        "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def dragon_boat_newcomer_upper_body_endurance_037(env, agent):
    try:
        _register_all_mcp(env, agent)
    except Exception as exc:
        logger.error(f"MCP registration failed: {type(exc).__name__}: {exc}")
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)

    _safe_workspace_bootstrap(env)

    stage_count = _expected_stage_count()
    events_by_stage: dict[int, list[dict]] = {}
    try:
        loaded_stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
        stage_count = max(stage_count, loaded_stage_count)
    except Exception as exc:
        logger.error(f"event loading failed: {type(exc).__name__}: {exc}; continuing with rubric stage count")

    stage_mods = {stage_idx: _load_rubric(f"stage_{stage_idx}") for stage_idx in range(stage_count)}
    all_checks: list[Check] = []
    total_weight = 0.0
    passed_weight = 0.0

    for stage_idx in range(stage_count):
        events = list(events_by_stage.get(stage_idx, []))
        events.sort(key=lambda e: (str(e.get("time", "")), str(e.get("id", ""))))
        if events:
            first_time = str(events[0].get("time") or "")
            _set_weather_sim_clock(env, first_time if "+" in first_time else first_time + "+08:00")
        stage_texts: list[str] = []
        stage_tool_calls: list[dict[str, Any]] = []
        for ev in events:
            if ev.get("kind") == "mutation":
                text, tool_calls = _dispatch_event(ev, env, agent)
            else:
                try:
                    text, tool_calls = _dispatch_event(ev, env, agent)
                except Exception as exc:
                    logger.error(
                        f"dispatch failed for event {ev.get('id')} in stage {stage_idx}: "
                        f"{type(exc).__name__}: {exc}"
                    )
                    stage_texts.append(
                        f"[DISPATCH_ERROR {ev.get('id')}: {type(exc).__name__}: {exc}]"
                    )
                    continue
            if text:
                stage_texts.append(_limit_text(text))
            stage_tool_calls.extend(tool_calls)
        _safe_write_file(
            env,
            f"{RESPONSES_DIR}/stage_{stage_idx}.txt",
            "\n---\n".join(stage_texts).encode("utf-8"),
        )
        _safe_write_file(
            env,
            f"{TRACE_DIR}/stage_{stage_idx}.json",
            json.dumps(stage_tool_calls, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        checks, tw, pw = _run_rubric_checks(
            stage_mods[stage_idx].CHECKS, env, f"stage{stage_idx}"
        )
        _persist_stage_score(env, stage_idx, checks, tw, pw)
        all_checks.extend(checks)
        total_weight += tw
        passed_weight += pw

    for name, tag in [("cross_stage", "cross_stage"), ("final", "final")]:
        mod = _load_rubric(name)
        checks, tw, pw = _run_rubric_checks(mod.CHECKS, env, tag)
        all_checks.extend(checks)
        total_weight += tw
        passed_weight += pw
    score = (passed_weight / total_weight) if total_weight > 0 else 0.0
    logger.info(f"flat-pool score: passed={passed_weight:.2f} total={total_weight:.2f} score={score:.3f}")
    return CheckerResults(checks=all_checks, score=score)
