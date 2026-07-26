"""East China bereavement travel, document reissue, and low-disturbance coordination task."""
from __future__ import annotations

import importlib
import json
import sys
import time
from datetime import datetime, timezone
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
TASK_NAME = "east_china_bereavement_docs_reissue"
RESPONSES_DIR = "/terrarium/agent_responses"
TRACE_DIR = "/terrarium/agent_traces"
PARTIAL_SCORES_DIR = "/terrarium/partial_scores"
MAX_STAGE_RESPONSE_CHARS = 20000
MUTATION_MAX_ATTEMPTS = 2
AGENT_ACT_MAX_CALLS = 2
STAGE_SCORE_REQUIRED_FIELDS = {
    "stage",
    "timestamp",
    "event_status",
    "atomic_check_results",
    "total_weight",
    "passed_weight",
    "normalized_stage_score",
    "evidence_summaries",
    "errors",
}


class MutationApplyError(RuntimeError):
    """A required world mutation could not be validated or applied."""

    def __init__(
        self,
        *,
        task_name: str,
        stage_idx: int | None,
        event_id: str,
        server: str | None,
        path: str | None,
        detail: str,
    ) -> None:
        self.task_name = task_name
        self.stage_idx = stage_idx
        self.event_id = event_id
        self.server = server
        self.path = path
        self.detail = detail
        super().__init__(
            "mutation apply failed: "
            f"task={task_name} stage={stage_idx} event={event_id} "
            f"server={server} path={path} detail={detail}"
        )


def parse_event_time(value: str | datetime) -> datetime:
    """Parse an event time and require an explicit UTC offset."""

    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("event time is missing")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    else:
        raise TypeError(f"event time must be str or datetime, got {type(value).__name__}")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"event time must include a timezone offset: {value!r}")
    return parsed


def _rubric_pkg_name() -> str:
    pkg_name = f"_task_{THIS_DIR.name.replace('.', '_')}_rubrics"
    if pkg_name not in sys.modules:
        pkg = ModuleType(pkg_name)
        pkg.__path__ = [str(THIS_DIR / "rubrics")]  # type: ignore[attr-defined]
        pkg.__package__ = pkg_name
        sys.modules[pkg_name] = pkg
    return pkg_name


_RUBRIC_PKG = _rubric_pkg_name()

PROMPT = (
    "你长期协助林澈处理 2026 年 4 月北京到苏州、上海、宁波、再返京的紧急亲属丧事行程，"
    "同时协调母亲身份证遗失后的临时乘车证明、异地补办材料核验、老人电子票执行说明、"
    "紧急费用留痕和低打扰沟通。回复使用中文，克制简短，优先列状态、风险、下一步、"
    "授权需求和截止时间。把持久状态写入 Notion、Calendar 或 /workspace 固定文件，"
    "例如 /workspace/STATUS_BOARD.md、/workspace/EXPENSE_LEDGER.md、"
    "/workspace/DOCUMENT_PACKET.md、/workspace/ELDER_TICKET_CARD.md、"
    "/workspace/COMMUNICATION_LOG.md 和 /workspace/FINAL_SUMMARY.md；不要建立嵌套任务目录。"
    "可直接执行查询、比较、监控、低风险提醒、可取消且无费用的 hold、非敏感普通邮件草稿"
    "和状态记录。付款、高额或不可退订单、取消或改签已确认订单、发送证件/死亡证明/户籍页/"
    "银行卡流水等敏感材料、超预算方案、法律或公安窗口最终判断，都必须先取得林澈确认。"
    "不要调用内容平台或点评平台服务；不要讨论内部评估、后台结构、日志或长篇工具转储。"
)

_CAPABILITIES_CONFIG = agent_caps_config(
flight_booking_mock="east_china_bereavement_docs_reissue",
rail_booking_mock="east_china_bereavement_docs_reissue",
hotel_booking_mock="east_china_bereavement_docs_reissue",
legal_search_mock="east_china_bereavement_docs_reissue",
email_mock="east_china_bereavement_docs_reissue",
calendar_mock="east_china_bereavement_docs_reissue",
maps_mock="east_china_bereavement_docs_reissue",
banking_mock="east_china_bereavement_docs_reissue",
notion_mock="east_china_bereavement_docs_reissue",
notification_hub_mock="east_china_bereavement_docs_reissue",
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
        stage_idx = int(k)
        bucket = by_stage.setdefault(stage_idx, [])
        for ev in evs or []:
            bucket.append(dict(ev))
    stage_count = (max(by_stage) + 1) if by_stage else 0
    return stage_count, by_stage



_SOURCE_LABELS = {
    "email_mock": "邮箱",
    "notification_hub_mock": "行程监控",
    "maps_mock": "地图与路况",
    "calendar_mock": "日历",
    "legal_search_mock": "规则资料",
    "rail_booking_mock": "铁路订单",
    "hotel_booking_mock": "酒店订单",
    "flight_booking_mock": "航班订单",
    "weather_mock": "天气服务",
    "workspace": "旅行资料",
    "funeral_home_contact": "殡仪馆联络",
}


def _display_source(value: Any) -> str:
    raw = str(value or "system")
    return _SOURCE_LABELS.get(raw, raw.removesuffix("_mock").replace("_", " "))

def _render_event(ev: dict) -> str:
    time = ev.get("time", "")
    kind = ev.get("kind", "")
    body = ev.get("body", "") or ""
    if kind == "user_message":
        tag = f"[来自 {ev.get('from') or 'user'} 的消息 @ {time}]"
    elif kind == "notification":
        tag = f"[通知 @ {time}，来源 {_display_source(ev.get('channel') or ev.get('source'))}]"
    elif kind == "world":
        tag = f"[世界事件 @ {time}，来源 {_display_source(ev.get('source'))}]"
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


def _read_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, dict):
        for key in ("content", "data", "text"):
            if key in value:
                return _read_bytes(value[key])
    raise TypeError(f"workspace read returned unsupported value: {type(value).__name__}")


def _persist_verified_file(env, path: str, content: bytes) -> None:
    env.workspace.fs.write_file(path, content)
    actual = _read_bytes(env.workspace.fs.read_file(path))
    if actual != content:
        raise IOError(f"workspace persistence verification failed: {path}")


def persist_stage_score(env, stage_idx: int, payload: dict[str, Any]) -> None:
    """Atomically persist and verify one frozen per-stage score payload."""

    missing = STAGE_SCORE_REQUIRED_FIELDS.difference(payload)
    if missing:
        raise ValueError(f"stage score payload missing fields: {sorted(missing)}")
    if payload.get("stage") != stage_idx:
        raise ValueError(
            f"stage score payload stage mismatch: expected {stage_idx}, got {payload.get('stage')!r}"
        )
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    env.workspace.shell.exec(f"mkdir -p {PARTIAL_SCORES_DIR}", user="root")
    final_path = f"{PARTIAL_SCORES_DIR}/stage_{stage_idx}.json"
    temp_path = f"{final_path}.{time.time_ns()}.tmp"
    rename = getattr(env.workspace.fs, "rename", None)
    if callable(rename):
        env.workspace.fs.write_file(temp_path, encoded)
        rename(temp_path, final_path)
    else:
        env.workspace.fs.write_file(final_path, encoded)
    stored = _read_bytes(env.workspace.fs.read_file(final_path))
    decoded = json.loads(stored.decode("utf-8"))
    if decoded != payload:
        raise IOError(f"stage score read-back mismatch: {final_path}")
    logger.info(
        "TRAVEL_STAGE_SCORE_JSON "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    )


def _extract_tool_calls(messages, event_id: str | None = None) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for m in messages or []:
        if _field(m, "role") != "assistant":
            continue
        content = _field(m, "content", "")
        blocks = content if isinstance(content, list) else []
        for blk in blocks:
            typ = _field(blk, "type", "")
            if typ not in ("toolCall", "tool_call", "tool_use"):
                continue
            calls.append({
                "event_id": event_id,
                "id": _field(blk, "id"),
                "name": _field(blk, "name"),
                "arguments": _jsonable(_field(blk, "arguments", _field(blk, "input", {}))),
            })
    return calls


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


def _capability_for_server(env, server: str):
    candidates = [server]
    if server.endswith("_mock"):
        candidates.append(server.removesuffix("_mock"))
    else:
        candidates.append(f"{server}_mock")
    for name in candidates:
        try:
            cap = getattr(env, name, None)
        except Exception:  # Terrarium raises CapabilityNotFoundError for aliases.
            continue
        if cap is not None:
            return cap
    return None


def _mutation_error(
    ev: dict[str, Any],
    entry_spec: dict[str, Any],
    stage_idx: int | None,
    detail: str,
) -> MutationApplyError:
    server_value = entry_spec.get("server") or ev.get("target")
    server = str(server_value) if server_value else None
    path = None
    if entry_spec.get("sql_file"):
        path = str(THIS_DIR / str(entry_spec["sql_file"]))
    return MutationApplyError(
        task_name=TASK_NAME,
        stage_idx=stage_idx,
        event_id=str(ev.get("id") or "<missing-event-id>"),
        server=server,
        path=path,
        detail=detail,
    )


def _preflight_mutation_entry(
    ev: dict[str, Any], entry_spec: dict[str, Any], env, stage_idx: int | None
) -> tuple[Any, Path | None]:
    server_value = entry_spec.get("server") or ev.get("target")
    if not server_value:
        raise _mutation_error(ev, entry_spec, stage_idx, "missing server")
    server = str(server_value)
    cap = _capability_for_server(env, server)
    if cap is None:
        raise _mutation_error(
            ev, entry_spec, stage_idx, f"missing capability for server {server!r}"
        )
    sql_path = None
    if "sql_file" in entry_spec:
        sql_path = THIS_DIR / str(entry_spec["sql_file"])
        if not sql_path.is_file():
            raise _mutation_error(ev, entry_spec, stage_idx, "SQL file is missing")
    elif "tool_call" in entry_spec:
        tool_call = entry_spec["tool_call"]
        if not isinstance(tool_call, dict) or not tool_call.get("name"):
            raise _mutation_error(
                ev, entry_spec, stage_idx, "tool_call requires a non-empty name"
            )
    return cap, sql_path


def _apply_mutation_entry(
    ev: dict[str, Any], entry_spec: dict[str, Any], env, stage_idx: int | None = None
) -> None:
    cap, sql_path = _preflight_mutation_entry(ev, entry_spec, env, stage_idx)
    try:
        if sql_path is not None:
            for attempt in range(MUTATION_MAX_ATTEMPTS):
                try:
                    cap.apply_sql_file(sql_path)
                    return
                except Exception as exc:  # noqa: BLE001
                    locked = "database is locked" in str(exc).casefold()
                    if locked and attempt < MUTATION_MAX_ATTEMPTS - 1:
                        time.sleep(min(1.5, 0.3 * (attempt + 1)))
                        continue
                    raise _mutation_error(
                        ev,
                        entry_spec,
                        stage_idx,
                        f"execution failed: {type(exc).__name__}: {exc}",
                    ) from exc
        if "tool_call" in entry_spec:
            tc = entry_spec["tool_call"]
            cap.call_tool(tc["name"], **(tc.get("args") or {}))
        else:
            cap.apply_mutation(entry_spec)
    except MutationApplyError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise _mutation_error(
            ev,
            entry_spec,
            stage_idx,
            f"execution failed: {type(exc).__name__}: {exc}",
        ) from exc


def _act_with_empty_retry(agent, instruction: str, event_id: str) -> list[Any]:
    """Retry one transient empty OpenClaw turn, never exceeding two calls."""

    messages: list[Any] = []
    for call_index in range(AGENT_ACT_MAX_CALLS):
        result = agent.act(instruction)
        messages = list(getattr(result, "messages", []) or [])
        if messages:
            return messages
        if call_index < AGENT_ACT_MAX_CALLS - 1:
            logger.warning(
                f"event {event_id}: agent turn returned no session messages; retrying once"
            )
            time.sleep(0.5)
    return messages


def _dispatch_event(
    ev: dict, env, agent, stage_idx: int | None = None
) -> tuple[str, list[dict[str, Any]]]:
    kind = ev.get("kind", "")
    if kind == "mutation":
        entries = ev.get("apply") or []
        if not entries:
            raise _mutation_error(ev, {}, stage_idx, "mutation has no apply entries")
        for entry_spec in entries:
            _preflight_mutation_entry(ev, entry_spec, env, stage_idx)
        for entry_spec in entries:
            _apply_mutation_entry(ev, entry_spec, env, stage_idx)
        return "", []

    if ev.get("silent"):
        return "", []
    if kind not in ("user_message", "notification", "world"):
        logger.warning(f"event {ev.get('id')}: unknown kind {kind!r}; skipping")
        return "", []

    messages = _act_with_empty_retry(agent, _render_event(ev), str(ev.get("id") or "<unknown>"))
    return _extract_assistant_text(messages), _extract_tool_calls(messages, ev.get("id"))


def _limit_text(text: str) -> str:
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return text[:MAX_STAGE_RESPONSE_CHARS] + f"\n\n[TRUNCATED: agent response exceeded {MAX_STAGE_RESPONSE_CHARS} chars]"


def _safe_runtime_io(label: str, fn) -> None:
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        logger.warning(f"{label} failed: {type(e).__name__}: {e}")


def _load_rubric(name: str):
    try:
        return importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    except ModuleNotFoundError as e:
        missing = e.name or ""
        if missing == _RUBRIC_PKG or missing.startswith(f"{_RUBRIC_PKG}."):
            logger.warning(f"rubric module {name!r} missing; using empty CHECKS")
            return SimpleNamespace(CHECKS=[])
        raise


def _run_rubric_checks(
    checks_spec, env, tag: str
) -> tuple[list[Check], float, float, list[dict[str, Any]]]:
    out: list[Check] = []
    total_w = 0.0
    passed_w = 0.0
    details: list[dict[str, Any]] = []
    for cid, fn, weight in checks_spec:
        error = None
        try:
            ok = bool(fn(env))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"checker {cid!r} raised: {e}")
            ok = False
            error = f"{type(e).__name__}: {e}"
        out.append(Check(name=cid, passed=ok, tags=[tag]))
        total_w += float(weight)
        if ok:
            passed_w += float(weight)
        details.append(
            {
                "id": str(cid),
                "passed": ok,
                "weight": float(weight),
                "evidence_summary": "passed" if ok else "failed",
                "error": error,
            }
        )
    return out, total_w, passed_w, details


def _stage_score_payload(
    stage_idx: int,
    events: list[dict[str, Any]],
    details: list[dict[str, Any]],
    total_weight: float,
    passed_weight: float,
) -> dict[str, Any]:
    return {
        "stage": stage_idx,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_status": {
            "total": len(events),
            "completed": len(events),
            "failed": 0,
            "events": [
                {
                    "id": str(event.get("id") or "<missing-event-id>"),
                    "status": "completed",
                    "time": parse_event_time(event.get("time")).isoformat(),
                }
                for event in events
            ],
        },
        "atomic_check_results": [
            {
                "id": row["id"],
                "passed": row["passed"],
                "weight": row["weight"],
            }
            for row in details
        ],
        "total_weight": float(total_weight),
        "passed_weight": float(passed_weight),
        "normalized_stage_score": (
            float(passed_weight) / float(total_weight) if total_weight else 0.0
        ),
        "evidence_summaries": [
            {"check_id": row["id"], "summary": row["evidence_summary"]}
            for row in details
        ],
        "errors": [
            {"check_id": row["id"], "error": row["error"]}
            for row in details
            if row["error"]
        ],
    }


@entry(
    capabilities=[
    "flight_booking_mock",
    "rail_booking_mock",
    "hotel_booking_mock",
    "legal_search_mock",
    "email_mock",
    "calendar_mock",
    "maps_mock",
    "banking_mock",
    "notion_mock",
    "notification_hub_mock",
        "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def east_china_bereavement_docs_reissue(env, agent):
    _register_all_mcp(env, agent)
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)

    _safe_runtime_io(
        "workspace upload",
        lambda: env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/terrarium/openclaw/workspace"),
    )
    _safe_runtime_io(
        "workspace chmod",
        lambda: env.workspace.shell.exec("chmod -R a+rwX /terrarium/openclaw/workspace", user="root"),
    )
    _safe_runtime_io(
        "runtime dirs mkdir",
        lambda: env.workspace.shell.exec(
            f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {PARTIAL_SCORES_DIR}"
        ),
    )

    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    stage_modules = {i: _load_rubric(f"stage_{i}") for i in range(stage_count)}
    final_mod = _load_rubric("final")
    cross_mod = _load_rubric("cross_stage")
    tool_mod = _load_rubric("tool_quality")

    all_checks: list[Check] = []
    total_weight = 0.0
    passed_weight = 0.0
    stage_passed_weight = 0.0

    for stage_idx in range(stage_count):
        events = list(events_by_stage.get(stage_idx, []))
        events.sort(key=lambda e: (parse_event_time(e.get("time")), str(e.get("id", ""))))
        stage_texts: list[str] = []
        stage_tool_calls: list[dict[str, Any]] = []
        for ev in events:
            txt, tool_calls = _dispatch_event(ev, env, agent, stage_idx=stage_idx)
            if txt:
                stage_texts.append(_limit_text(txt))
            stage_tool_calls.extend(tool_calls)

        _persist_verified_file(
            env,
            f"{RESPONSES_DIR}/stage_{stage_idx}.txt",
            "\n---\n".join(stage_texts).encode("utf-8"),
        )
        _persist_verified_file(
            env,
            f"{TRACE_DIR}/stage_{stage_idx}.json",
            json.dumps(stage_tool_calls, ensure_ascii=False, indent=2).encode("utf-8"),
        )

        checks, tw, pw, details = _run_rubric_checks(
            stage_modules[stage_idx].CHECKS, env, f"stage{stage_idx}"
        )
        all_checks.extend(checks)
        total_weight += tw
        passed_weight += pw
        stage_passed_weight += pw
        persist_stage_score(
            env,
            stage_idx,
            _stage_score_payload(stage_idx, events, details, tw, pw),
        )

    cross_checks, cross_tw, cross_pw, _ = _run_rubric_checks(
        cross_mod.CHECKS, env, "cross_stage"
    )
    all_checks.extend(cross_checks)
    total_weight += cross_tw
    passed_weight += cross_pw

    tool_checks, tool_tw, tool_pw, _ = _run_rubric_checks(
        tool_mod.CHECKS, env, "tool_quality"
    )
    all_checks.extend(tool_checks)
    total_weight += tool_tw
    passed_weight += tool_pw

    final_checks, final_tw, final_pw, _ = _run_rubric_checks(final_mod.CHECKS, env, "final")
    all_checks.extend(final_checks)
    total_weight += final_tw
    passed_weight += final_pw

    stage_total = total_weight - cross_tw - tool_tw - final_tw
    expected = {
        "stage": (stage_total, 52.0),
        "cross": (cross_tw, 28.0),
        "tool": (tool_tw, 8.0),
        "final": (final_tw, 12.0),
    }
    for bucket, (actual, target) in expected.items():
        if abs(actual - target) > 1e-9:
            raise ValueError(
                f"unexpected {bucket} rubric weight: expected {target}, got {actual}"
            )

    score = (passed_weight / total_weight) if total_weight > 0 else 0.0
    logger.info(
        "score buckets: "
        f"stage={stage_passed_weight:.2f}/52 cross={cross_pw:.2f}/28 "
        f"tool={tool_pw:.2f}/8 final={final_pw:.2f}/12 "
        f"passed={passed_weight:.2f}/{total_weight:.2f} -> score={score:.3f}"
    )
    return CheckerResults(checks=all_checks, score=score)
