"""career_equity_buyback_recovery — 离职 RSU 限制性股票回购争议核对与维权 + 再就业 benchmark task.

Self-contained Terrarium-native task. The @entry body:

  1. Registers each capability's MCP server with the agent + sets the system prompt.
  2. Uploads ``workspace/`` into the agent's working dir, fixes perms, and
     pre-creates two sidecar dirs (responses + tool-call traces) that the agent
     cannot see but rubric checkers read.
  3. Loads ``event.yaml`` and the per-stage rubric modules under ``rubrics/``.
  4. Drives the stage loop:
       — ``mutation`` events write out-of-band (sqlite / sql_file / tool_call);
       — ``user_message`` / ``notification`` / ``world`` drive one ``agent.act``.
       — after each stage the matching rubric's ``CHECKS`` list runs.
  5. Returns one ``CheckerResults``. Scoring is a flat pool:
       ``score = Σ(passed weight) / Σ(all weight)`` over stage + cross + final.
"""
from __future__ import annotations

import importlib
import json
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

# Sidecar dirs (rubric-only, outside the agent's workspace view).
RESPONSES_DIR = "/terrarium/agent_responses"   # stage_<N>.txt  → 💬 reply dimension
TRACE_DIR = "/terrarium/agent_traces"           # stage_<N>.json → 🔧 tool-call dimension
PARTIAL_SCORES_DIR = "/terrarium/partial_scores"  # stage_<N>.json → frozen per-stage score
MAX_STAGE_RESPONSE_CHARS = 20000


def _rubric_pkg_name() -> str:
    for p in sys.path:
        try:
            rel = THIS_DIR.relative_to(Path(p).resolve())
        except ValueError:
            continue
        return ".".join(rel.parts) + ".rubrics"
    raise RuntimeError(f"Cannot derive rubric package name for {THIS_DIR}")


_RUBRIC_PKG = _rubric_pkg_name()


PROMPT = (
    "你正在协助纪辰处理离职时的RSU 限制性股票回购争议与重新就业。"
    "股权主线必须先查询历史持股计划/授予文件，核对已归属股数和约定的结算基准日，再用 brokerage 查询该基准日可得的最新市场价，"
    "分别记录参考公允价值、公司方案、实际到账与差额。市场价是本任务合同约定下的估值证据，不要宣称法律对所有股权争议一律强制按收盘价结算。"
    "legal_search 应核对《民法典》第509、496、497、151条及案号隐去的脱敏裁判摘要，说明合同履行、格式条款和显失公平规则的适用边界。"
    "banking 工资流水仅用于核算收入水平与过渡期现金流旁证，不能作为股权价差的计算基数，工作年限也不能代替股权估值。"
    "求职主线在 job_board 按上海后端/平台方向搜索和投递公司自有正编岗位，规避外包、派遣和无补偿竞业。"
    "在 Notion、calendar 与 workspace 中维护可追溯记录；金额、股数、价格、日期、job_id、application_id、message_id、tx_id、case_id 和 article_id 必须来自工具结果。"
    "下单卖出或赎回、签署结算/解除协议、接受或拒绝 offer、谈薪与承诺到岗都必须先取得用户明确授权；对招聘方最小披露离职争议和其他 offer 信息。"
    "不要引用 benchmark、rubric 或隐藏评分信息。每次可见回复控制在 800 汉字以内，不要原样复制数据库、SQL、JSON 或长工具输出。"
)

_CAPABILITIES_CONFIG = agent_caps_config(
    job_board_mock="career_equity_buyback_recovery",
    legal_search_mock="rsu_buyback_2026",
    brokerage_mock="career_equity_buyback_recovery",
    banking_mock="career_equity_buyback_recovery",
    notion_mock="career_equity_buyback_recovery",
    email_mock="career_equity_buyback_recovery",
    calendar_mock="career_equity_buyback_recovery",
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


def _render_event(ev: dict) -> str:
    time = ev.get("time", "")
    kind = ev.get("kind", "")
    body = ev.get("body", "") or ""
    if kind == "user_message":
        tag = f"[来自 {ev.get('from') or 'user'} 的消息 @ {time}]"
    elif kind == "notification":
        tag = f"[通知 @ {time}，来源 {ev.get('channel') or ev.get('source') or 'system'}]"
    elif kind == "world":
        tag = f"[世界事件 @ {time}，来源 {ev.get('source') or 'system'}]"
    else:
        tag = f"[{kind} @ {time}]"
    return f"{tag}\n{body}"


# ── Tool-call extraction (🔧 dimension data source) ──────────────────────

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
                "arguments": _jsonable(
                    _field(blk, "arguments", _field(blk, "input", {}))
                ),
            })
    return calls


# ── Event dispatch ───────────────────────────────────────────────────────

def _dispatch_event(ev: dict, env, agent) -> tuple[str, list[dict[str, Any]]]:
    kind = ev.get("kind", "")
    if kind == "mutation":
        for entry_spec in ev.get("apply") or []:
            server = entry_spec.get("server")
            if not server:
                logger.warning(f"mutation {ev.get('id')}: missing server")
                continue
            cap = getattr(env, f"{server}_mock", None)
            if cap is None:
                logger.warning(f"mutation {ev.get('id')}: no capability for {server!r}")
                continue
            if "sql_file" in entry_spec:
                cap.apply_sql_file(THIS_DIR / entry_spec["sql_file"])
            elif "tool_call" in entry_spec:
                tc = entry_spec["tool_call"]
                cap.call_tool(tc["name"], **(tc.get("args") or {}))
            else:
                cap.apply_mutation(entry_spec)
        return "", []

    if ev.get("silent"):
        return "", []

    if kind not in ("user_message", "notification", "world"):
        logger.warning(f"event {ev.get('id')}: unknown kind {kind!r}; skipping")
        return "", []

    result = agent.act(_render_event(ev))
    messages = getattr(result, "messages", []) or []
    text = _limit_text(_extract_assistant_text(messages))
    tool_calls = _extract_tool_calls(messages, ev.get("id"))
    return text, tool_calls


def _limit_text(text: str) -> str:
    if len(text) <= MAX_STAGE_RESPONSE_CHARS:
        return text
    return (
        text[:MAX_STAGE_RESPONSE_CHARS]
        + f"\n\n[TRUNCATED: agent response exceeded {MAX_STAGE_RESPONSE_CHARS} chars]"
    )


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


# ── Rubric loading + execution ─────────────────────────────────────────────

def _load_rubric(name: str):
    try:
        return importlib.import_module(f"{_RUBRIC_PKG}.{name}")
    except ModuleNotFoundError as e:
        missing = e.name or ""
        if missing == _RUBRIC_PKG or missing.startswith(f"{_RUBRIC_PKG}."):
            logger.warning(f"rubric module {name!r} missing; using empty CHECKS")
            return SimpleNamespace(CHECKS=[])
        raise


def _run_rubric_checks(checks_spec, env, tag: str) -> tuple[list[Check], float, float]:
    """Run each atomic check independently; no unrelated global paperwork gate."""
    out: list[Check] = []
    total_w = 0.0
    passed_w = 0.0
    for cid, fn, weight in checks_spec:
        try:
            ok = bool(fn(env))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"checker {cid!r} raised: {e}")
            ok = False
        out.append(Check(name=cid, passed=ok, tags=[tag]))
        total_w += float(weight)
        if ok:
            passed_w += float(weight)
    return out, total_w, passed_w


def _persist_stage_score(env, stage: int, checks_spec, checks: list[Check],
                         total_weight: float, passed_weight: float) -> dict[str, Any]:
    """Atomically freeze one stage's score before any later-stage mutation runs."""
    check_rows = []
    for (cid, _fn, weight), check in zip(checks_spec, checks, strict=True):
        check_rows.append({
            "id": cid,
            "passed": bool(_field(check, "passed", False)),
            "weight": float(weight),
        })
    payload = {
        "stage": int(stage),
        "total_weight": float(total_weight),
        "passed_weight": float(passed_weight),
        "score": (float(passed_weight) / float(total_weight)) if total_weight else 0.0,
        "checks": check_rows,
    }
    env.workspace.shell.exec(f"mkdir -p {PARTIAL_SCORES_DIR}", user="root")
    final_path = f"{PARTIAL_SCORES_DIR}/stage_{stage}.json"
    temp_path = f"{final_path}.tmp"
    env.workspace.fs.write_file(
        temp_path,
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    env.workspace.shell.exec(f"mv -f {temp_path} {final_path}", user="root")
    logger.info(
        "CAREER_STAGE_SCORE_JSON "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    )
    return payload


# ── Entry point ────────────────────────────────────────────────────────────

@entry(
    capabilities=[
        "job_board_mock",
        "legal_search_mock",
        "brokerage_mock",
        "banking_mock",
        "notion_mock",
        "email_mock",
        "calendar_mock",
        "workspace",
    ],
    capabilities_config=_CAPABILITIES_CONFIG,
)
def career_equity_buyback_recovery(env, agent):
    logger.info("Starting career_equity_buyback_recovery task")

    # 1. Configure agent.
    _register_all_mcp(env, agent)
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)

    # 2. Workspace bootstrap (three fixed steps, order matters).
    env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/terrarium/openclaw/workspace")
    env.workspace.shell.exec("chmod -R a+rwX /terrarium/openclaw/workspace", user="root")
    env.workspace.shell.exec(f"mkdir -p {RESPONSES_DIR} {TRACE_DIR} {PARTIAL_SCORES_DIR}", user="root")

    # 3. Load events + rubrics.
    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    logger.info(f"Loaded {stage_count} stages from event.yaml")
    stage_modules = {i: _load_rubric(f"stage_{i}") for i in range(stage_count)}
    final_mod = _load_rubric("final")
    cross_mod = _load_rubric("cross_stage")

    all_checks: list[Check] = []
    total_w = 0.0
    passed_w = 0.0

    # 4. Stage loop.
    for stage_idx in range(stage_count):
        events = list(events_by_stage.get(stage_idx, []))
        events.sort(key=lambda e: (str(e.get("time", "")), str(e.get("id", ""))))
        stage_texts: list[str] = []
        stage_tool_calls: list[dict[str, Any]] = []
        for ev in events:
            try:
                txt, tool_calls = _dispatch_event(ev, env, agent)
                if txt:
                    stage_texts.append(txt)
                stage_tool_calls.extend(tool_calls)
            except Exception as e:  # noqa: BLE001
                logger.error(
                    f"dispatch failed for event {ev.get('id')} in stage {stage_idx}: {e}"
                )

        # 4b. Persist agent reply text + tool-call trace for rubric checkers.
        env.workspace.fs.write_file(
            f"{RESPONSES_DIR}/stage_{stage_idx}.txt",
            "\n---\n".join(stage_texts).encode("utf-8"),
        )
        env.workspace.fs.write_file(
            f"{TRACE_DIR}/stage_{stage_idx}.json",
            json.dumps(stage_tool_calls, ensure_ascii=False, indent=2).encode("utf-8"),
        )

        # 4c. Run this stage's rubric.
        stage_checks_spec = stage_modules[stage_idx].CHECKS
        checks, tw, pw = _run_rubric_checks(stage_checks_spec, env, f"stage{stage_idx}")
        _persist_stage_score(env, stage_idx, stage_checks_spec, checks, tw, pw)
        all_checks.extend(checks)
        total_w += tw
        passed_w += pw

    # 5. Cross-stage continuity checks.
    cross_checks, cross_tw, cross_pw = _run_rubric_checks(cross_mod.CHECKS, env, "cross")
    all_checks.extend(cross_checks)
    total_w += cross_tw
    passed_w += cross_pw

    # 6. Final-bucket checks.
    final_checks, final_tw, final_pw = _run_rubric_checks(final_mod.CHECKS, env, "final")
    all_checks.extend(final_checks)
    total_w += final_tw
    passed_w += final_pw

    # 7. Flat-pool score (no bucket normalization).
    score = (passed_w / total_w) if total_w > 0 else 0.0
    logger.info(f"career_equity_buyback_recovery score={score:.3f} (passed={passed_w}/{total_w})")
    return CheckerResults(checks=all_checks, score=score)
