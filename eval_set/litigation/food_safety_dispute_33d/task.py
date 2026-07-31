"""Food-Safety-Dispute Litigation — 33-day litigation benchmark task.

赵萌(网购不符合食品安全标准的进口食品的消费者)准备退一赔十诉讼: 立案准备期 → 诉讼推进期 → 判后期.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import yaml
from loguru import logger
from terrarium.models.checker import Check, CheckerResults
from terrarium.models.mcp import MCPServerConfig
from terrarium.task.decorator import entry

from capabilities import agent_caps_config

THIS_DIR = Path(__file__).resolve().parent


def _rubric_pkg_name() -> str:
    for p in sys.path:
        try:
            rel = THIS_DIR.relative_to(Path(p).resolve())
        except ValueError:
            continue
        return ".".join(rel.parts) + ".rubrics"
    raise RuntimeError(
        f"Cannot derive rubric package name: {THIS_DIR} is not under any "
        "sys.path entry. Add the project root to sys.path before running."
    )


_RUBRIC_PKG = _rubric_pkg_name()
_WEIGHT_PROFILE = importlib.import_module(f"{_RUBRIC_PKG}.weight_profile")

RESPONSES_DIR = "/terrarium/agent_responses"

PROMPT = (
    "You are assisting Zhao Meng (赵萌) with a food-safety online-shopping dispute: "
    "she bought, on the 优鲜购 e-commerce platform from the 环球优选 store (seller "
    "domiciled in 杭州), an imported infant formula with NO Chinese label and a "
    "'health' tea that unlawfully claims disease-treatment effects and is suspected "
    "of illegal additives — both failing food-safety standards. She wants to sue for "
    "退一赔十 (refund plus 10× punitive damages). Your workspace has her persona, the "
    "case facts, and authorization boundaries. Work with her through case-building, "
    "the litigation procedure, and the post-judgment phase. ALWAYS use the MCP tools "
    "to look up real data rather than reasoning from memory alone: search and read "
    "precedent judgments and follow their citations to the governing statute articles "
    "(legal_search), verify articles are currently in force (status=现行有效), read the "
    "official 立案/诉讼 procedural notices and subscribe to case-status alerts "
    "(notification_hub), put statutory deadlines (three-year limitation, "
    "evidence-submission window, inspection/检验 application, appeal window) on the "
    "calendar (calendar), maintain the case timeline / evidence chain / legal basis in "
    "Notion (notion), and read her mailbox for the dispute facts and draft "
    "communications (email). Treat official procedural notices and in-force statutes as "
    "authoritative over community posts. NEVER file the lawsuit, fix the claim amount or "
    "the chosen defendants, apply for the 食品检验, or accept mediation/settlement on her "
    "behalf — prepare and recommend, she decides. Base every claim on real evidence she "
    "actually has; never fabricate. Persist follow-up items in Notion or workspace files "
    "so later stages can recover them."
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
        tag = f"[Message from {ev.get('from') or 'user'} @ {time}]"
    elif kind == "notification":
        tag = f"[Notification @ {time} from {ev.get('channel') or ev.get('source') or 'system'}]"
    elif kind == "cron_fire":
        tag = f"[Scheduled reminder @ {time} from {ev.get('source') or 'scheduler'}]"
    elif kind == "world":
        tag = f"[World event @ {time} from {ev.get('source') or 'system'}]"
    else:
        tag = f"[{kind} @ {time}]"
    return f"{tag}\n{body}"


def _dispatch_event(ev: dict, env, agent) -> str:
    kind = ev.get("kind", "")
    if kind == "mutation":
        for entry_spec in ev.get("apply") or []:
            server = entry_spec.get("server")
            if not server:
                raise RuntimeError(f"mutation {ev.get('id')}: missing 'server' in apply entry")
            cap = getattr(env, f"{server}_mock", None)
            if cap is None:
                raise RuntimeError(
                    f"mutation {ev.get('id')}: no capability for server {server!r}"
                )
            if "sql_file" in entry_spec:
                sql_path = THIS_DIR / entry_spec["sql_file"]
                cap.apply_sql_file(sql_path)
            elif "tool_call" in entry_spec:
                tc = entry_spec["tool_call"]
                cap.call_tool(tc["name"], **(tc.get("args") or {}))
            else:
                raise RuntimeError(
                    f"mutation {ev.get('id')}: apply entry has neither sql_file nor tool_call"
                )
        return ""

    if ev.get("silent"):
        return ""

    # cron_fire is a scheduler-driven heartbeat: like a notification, it triggers an agent turn.
    if kind not in ("user_message", "notification", "world", "cron_fire"):
        logger.warning(f"event {ev.get('id')}: unknown kind {kind!r} — skipping")
        return ""

    result = agent.act(_render_event(ev))
    return _extract_assistant_text(getattr(result, "messages", []) or [])


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
    return importlib.import_module(f"{_RUBRIC_PKG}.{name}")


def _clear_rubric_caches(env) -> None:
    """Keep journal memoization stage-scoped as the environment evolves."""
    for attr in ("_food_journal_cache", "_pl_journal_cache"):
        try:
            delattr(env, attr)
        except AttributeError:
            pass


def _run_rubric_checks(checks_spec, env, tag: str) -> tuple[list[Check], float, float]:
    out: list[Check] = []
    total_w = 0.0
    passed_w = 0.0
    for cid, fn, declared_weight in checks_spec:
        weight = _WEIGHT_PROFILE.weight_for(cid, declared_weight)
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


@entry(
    capabilities=[
        "legal_search_mock",
        "notification_hub_mock",
        "calendar_mock",
        "notion_mock",
        "email_mock",
        "workspace",
    ],
    capabilities_config=agent_caps_config(
        legal_search_mock="food_safety_2026",
        notification_hub_mock="zhao_meng_litigation",
        calendar_mock="zhao_meng_litigation",
        notion_mock="zhao_meng_litigation",
        email_mock="zhao_meng_litigation",
    ),
)
def food_safety_dispute_33d(env, agent):
    _register_all_mcp(env, agent)
    # system prompt override removed: let openclaw use its own default system prompt.
    # (task.py no longer injects PROMPT; openclaw assembles the final system prompt itself.)

    env.workspace.fs.upload(str(THIS_DIR / "workspace"), "/workspace")
    env.workspace.shell.exec(
        "cp /workspace/IDENTITY.md /workspace/USER.md /workspace/SOUL.md "
        "/workspace/PERSONA.md /workspace/AGENTS.md /workspace/TOOLS.md "
        "/terrarium/openclaw/"
    )
    env.workspace.shell.exec(f"mkdir -p {RESPONSES_DIR}")
    # The upload above runs as root, but the agent process is NOT root: without this
    # the agent gets EACCES on every workspace write (known terrarium/openclaw pitfall,
    # observed as "0.0 score + per-turn EACCES"). Widen perms on both the mounted
    # workspace and the openclaw copy so the agent can persist follow-up files.
    try:
        env.workspace.shell.exec(
            f"chmod -R a+rwX /terrarium/openclaw /workspace {RESPONSES_DIR}", user="root"
        )
    except Exception as e:  # noqa: BLE001 — never let a perms tweak abort the run
        logger.warning(f"workspace chmod failed: {e}")

    stage_count, events_by_stage = _load_events(THIS_DIR / "event.yaml")
    stage_modules = {i: _load_rubric(f"stage_{i}") for i in range(stage_count)}
    final_mod = _load_rubric("final")
    runtime_check_ids = [
        cid
        for stage_idx in range(stage_count)
        for cid, _fn, _weight in stage_modules[stage_idx].CHECKS
    ]
    runtime_check_ids.extend(cid for cid, _fn, _weight in final_mod.CHECKS)
    _WEIGHT_PROFILE.validate_profile(runtime_check_ids)

    all_checks: list[Check] = []
    total_w = 0.0
    passed_w = 0.0

    for stage_idx in range(stage_count):
        events = list(events_by_stage.get(stage_idx, []))
        events.sort(key=lambda e: (str(e.get("time", "")), str(e.get("id", ""))))
        stage_texts: list[str] = []
        for ev in events:
            txt = _dispatch_event(ev, env, agent)
            if txt:
                stage_texts.append(txt)

        env.workspace.fs.write_file(
            f"{RESPONSES_DIR}/stage_{stage_idx}.txt",
            "\n---\n".join(stage_texts).encode("utf-8"),
        )

        checks_spec = stage_modules[stage_idx].CHECKS
        _clear_rubric_caches(env)
        checks, t, p = _run_rubric_checks(checks_spec, env, f"stage{stage_idx}")
        all_checks.extend(checks)
        total_w += t
        passed_w += p

    _clear_rubric_caches(env)
    checks, t, p = _run_rubric_checks(final_mod.CHECKS, env, "final")
    all_checks.extend(checks)
    total_w += t
    passed_w += p

    score = (passed_w / total_w) if total_w > 0 else 0.0
    return CheckerResults(checks=all_checks, score=score)
