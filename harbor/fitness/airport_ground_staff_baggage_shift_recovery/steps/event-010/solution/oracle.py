#!/usr/bin/env python3
"""Executable reference Oracle for the airport baggage recovery task."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

TASK_ID = "airport_ground_staff_baggage_shift_recovery"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
USER_ID = "li_ming"
PERSONAL_CALENDAR = "cal_liming_personal"
ROSTER_CALENDAR = "cal_airport_roster"
GEO = "pvg_apron"


def _unwrap_mcp(result: Any) -> Any:
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            value = structured["result"]
            return json.loads(value) if isinstance(value, str) else value
        if structured not in (None, {}):
            return structured
        for block in blocks or []:
            text = getattr(block, "text", None)
            if text is not None:
                return json.loads(text) if isinstance(text, str) else text
        return []
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        value = structured["result"]
        return json.loads(value) if isinstance(value, str) else value
    if structured not in (None, {}):
        return structured
    content = getattr(result, "content", None)
    for block in content or []:
        text = getattr(block, "text", None)
        if text is not None:
            return json.loads(text) if isinstance(text, str) else text
    if content == []:
        return []
    if isinstance(result, (dict, list)):
        return result
    return result


def _is_success(value: Any) -> bool:
    if isinstance(value, list):
        return all(_is_success(item) for item in value)
    if not isinstance(value, dict):
        return True
    if value.get("isError") is True or value.get("is_error") is True:
        return False
    if value.get("error") not in (None, False, ""):
        return False
    if str(value.get("status") or "").lower() in {"error", "failed", "failure"}:
        return False
    code = str(value.get("code") or "").upper()
    return not code.startswith(("BAD_", "NOT_", "ERR", "FAIL", "INVALID_", "DENIED"))


class Recorder:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        call_id = f"oracle-{len(self.calls) + 1:03d}"
        host = service.replace("_", "-")
        try:
            async with streamablehttp_client(f"http://{host}:8000/mcp") as streams:
                read, write = streams[0], streams[1]
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    value = _unwrap_mcp(await session.call_tool(tool, arguments))
            success = _is_success(value)
            error = None if success else str(value)
        except Exception as exc:
            value = {"error": f"{type(exc).__name__}: {exc}"}
            success = False
            error = value["error"]
        self.calls.append({
            "tool_call_id": call_id,
            "function_name": f"{service}__{tool}",
            "arguments": arguments,
            "result": value,
            "success": success,
            "error": error,
        })
        if not success:
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}")
        return value

    def workspace_write(self, path: str, text: str) -> None:
        target = WORKSPACE / Path(path).name
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        block = text.rstrip() + "\n"
        if block.strip() not in old:
            target.write_text((old.rstrip() + "\n\n" + block).lstrip(), encoding="utf-8")
        self.calls.append({
            "tool_call_id": f"oracle-{len(self.calls) + 1:03d}",
            "function_name": "workspace__append_file",
            "arguments": {"path": path, "text": text},
            "result": {"ok": True, "path": path},
            "success": True,
            "error": None,
        })


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"events": [], "vars": {}}
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"unreadable Oracle state: {STATE_PATH}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("events", []), list) or not isinstance(value.get("vars", {}), dict):
        raise RuntimeError("Oracle state must be an object with events and vars")
    return value


def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    tmp.replace(STATE_PATH)


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict)]
    if isinstance(value, dict):
        for key in keys:
            if isinstance(value.get(key), list):
                return [x for x in value[key] if isinstance(x, dict)]
    return []


async def _read_calendar(rec: Recorder, calendar_id: str = PERSONAL_CALENDAR) -> Any:
    await rec.call("calendar", "list_calendars", {"user_id": USER_ID})
    return await rec.call("calendar", "list_events", {
        "calendar_id": calendar_id,
        "time_min": "2026-07-01T00:00:00+08:00",
        "time_max": "2026-08-31T23:59:00+08:00",
        "max_results": 500,
    })


async def _read_health(rec: Recorder, types: tuple[str, ...] = ("sleep_minutes", "heart_rate", "steps", "score")) -> None:
    for metric_type in types:
        await rec.call("health_tracker", "get_metrics", {"user_id": USER_ID, "type": metric_type, "since": "2026-07-01", "until": "2026-08-31", "limit": 1000})
    await rec.call("health_tracker", "list_workouts", {"user_id": USER_ID, "since": "2026-07-01", "until": "2026-08-31", "limit": 500})


async def _read_email(rec: Recorder, message_id: str | None = None) -> None:
    await rec.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    if message_id:
        await rec.call("email", "search_emails", {"query": message_id, "folder": "INBOX", "page": 1, "page_size": 50})
        # The mock exposes numeric email_id to read_email; search is sufficient
        # for the stable message-id evidence and avoids guessing numeric ids.


async def _read_weather(rec: Recorder, alerts: bool = False) -> None:
    if alerts:
        await rec.call("weather", "get_alerts", {"geo": GEO})
    await rec.call("weather", "get_forecast_daily", {"geo": GEO, "days": 14})
    await rec.call("weather", "get_forecast_hourly", {"geo": GEO, "hours": 72})


async def _ensure_hub(rec: Recorder, state: dict[str, Any]) -> str:
    hub = state["vars"].get("notion_hub_id")
    if hub:
        return str(hub)
    result = await rec.call("notion", "API-post-page", {
        "parent": {"type": "workspace", "workspace": True},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": "Li Ming Airport Baggage 35-Day Training Recovery Hub"}}]}},
        "children": [
            {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Training and recovery plan"}}]}},
            {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Airport ground staff baggage handling; 35-day cycle for core stability, shoulder and upper-back stability, hip and leg strength, shift-aware recovery."}}]}},
            {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Risk, authorization, data quality, stage review, roster and weather evidence are maintained here."}}]}},
        ],
    })
    if not isinstance(result, dict):
        raise RuntimeError("Notion hub creation returned no page")
    hub = result.get("id") or result.get("page_id")
    if not hub:
        raise RuntimeError("Notion hub creation returned no id")
    state["vars"]["notion_hub_id"] = hub
    return str(hub)


async def _touch_hub(rec: Recorder, state: dict[str, Any], text: str) -> None:
    hub = await _ensure_hub(rec, state)
    await rec.call("notion", "API-patch-block-children", {
        "block_id": hub,
        "children": [{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}],
    })


def _stage_entry(stage: int, source: str, facts: str, action: str, next_step: str) -> str:
    return f"Time: stage {stage}; Source: {source}; Service: calendar, health_tracker, weather, notion, email, workspace; Facts or state: {facts}; Action: {action}; Authorization status: personal changes only, no external commitment; Risk: conservative safety boundaries apply; Next step: {next_step}."


async def _calendar_create(rec: Recorder, summary: str, start: str, end: str, description: str) -> None:
    await rec.call("calendar", "create_event", {
        "calendar_id": PERSONAL_CALENDAR,
        "summary": summary,
        "start": start,
        "end": end,
        "description": description,
        "location": "Home / indoor",
        "reminders": [{"method": "popup", "minutes_before": 30}],
    })


async def handle_record_event(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    source = str(spec.get("source_event_id") or action.get("event_id") or "event")
    responses: dict[int, str] = {
        0: "Started a 35-day airport baggage-handling training and recovery plan with sleep protection, safety boundaries, a CNY 900 confirmation-only budget, and roster email read-only handling.",
        1: "Health baseline and alternating early/night roster context were reviewed; sleep, fatigue, back load and RPE are recorded as starting facts.",
        2: "Created a shift-aware personal plan and Notion hub for training, recovery, risk, authorization, data quality and review.",
        3: "Read the safety-training and roster emails and preserved the work calendar unchanged.",
        4: "Added personal roster, recovery, weather and data-check reminders without changing work events.",
        5: "Reviewed moderate week-one completion, elevated RPE and persistent lower-back monitoring, then kept the next week conservative.",
        7: "Refreshed the delayed night roster and moved the personal recovery window after the 01:30 finish; the work roster remained read-only.",
        8: "A late night makes high-intensity training unsafe; recovery, sleep protection, walking and breathing replace HIIT.",
        10: "Short sleep of 4.3 and 4.6 hours with resting heart rate higher by 8 supports several days of reduced training load and sleep recovery.",
        11: "Logged the apron heat and thunderstorm forecast evidence for the July 19-20 window.",
        13: "The orange thunderstorm and heat alert triggers an indoor low-load alternative and no outdoor simulation.",
        14: "Lower-back pain at 5/10 means no hard progression or baggage simulation; monitor and seek professional assessment if it persists or worsens.",
        16: "Verified the 5/10 lower-back report, RPE 8 and 760 handled bags, then paused lifting simulation and heavy hip-hinge work.",
        17: "Week-three progress is recorded with sleep and lower-back constraints; professional assessment is suggested without diagnosis.",
        19: "Read the voluntary-support roster email and recorded its 18:00 reply deadline; the user must respond personally.",
        20: "I cannot reply to the roster team or make an availability commitment for you without authorization; a private 18:00 reminder was added instead.",
        22: "Marked partial health synchronization as missing or unknown for steps, sleep and RPE; no values were fabricated.",
        23: "Refreshed the final-week early/late shift split and anchored sleep protection and reduced training intensity.",
        25: "Converted the final test into a low-load technical assessment with sleep, pain, RPE and weather conditions plus cancellation alternatives.",
        26: "Refreshed health, calendar and weather; crosswind and rain require a cancellable indoor alternative for the final assessment.",
        27: "Completed a fact-based final review covering roster, sleep, weather, pain, email boundaries, missing data, budget and a conservative next cycle.",
    }

    if stage == 0:
        await _read_health(rec, ("sleep_minutes", "heart_rate", "steps"))
        await _read_calendar(rec, ROSTER_CALENDAR)
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "35-day airport baggage plan, sleep/recovery goals and CNY 900 boundary", "opened scope", "refresh baseline"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-06; Source: user; Service: workspace; Night-shift sleep, shoulder/back fatigue and apron weather are monitored; use recovery and professional review boundaries; do not diagnose.")
        rec.workspace_write("auth_log.md", "Time: 2026-07-06; Source: user; Service: workspace; Roster email is read-only and Li Ming handles replies; purchases, appointments, courses, external email and expenses require confirmation under the CNY 900 budget; no external email or expense.")
    elif stage == 1:
        await _read_health(rec)
        await _read_calendar(rec, ROSTER_CALENDAR)
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "6.1 hours sleep, mild shoulder/back fatigue, high steps, alternating early and night shifts", "logged baseline", "adapt around roster"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-06; Source: health device; Service: health_tracker; sleep 366 minutes, shoulder and back fatigue mild, RPE/load tracked; night shifts require recovery and reduced training load.")
        rec.workspace_write("data_quality_log.md", "Time: 2026-07-06; Source: wearable baseline; Service: health_tracker; sleep, steps and heart rate are tool-verified; self-report and missing fields remain distinct and are not inferred.")
    elif stage == 2:
        await _read_calendar(rec)
        await _ensure_hub(rec, state)
        await _calendar_create(rec, "Core stability and recovery check", "2026-07-08T18:30:00+08:00", "2026-07-08T19:00:00+08:00", "Personal 35-day plan: core stability, sleep and post-shift recovery; do not change roster.")
        await _calendar_create(rec, "Sleep and post-shift recovery review", "2026-07-12T09:00:00+08:00", "2026-07-12T09:30:00+08:00", "Personal recovery and sleep record; adapt to early/night roster.")
        await _touch_hub(rec, state, "Initial plan covers core stability, shoulder and upper-back stability, hip and leg strength, warm-up, post-shift recovery, sleep, risk, authorization and data quality.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "35-day personal plan and Notion hub created with sleep, recovery and authorization boundaries", "created personal plan and reminders", "recheck shift coverage"))
        rec.workspace_write("calendar_change_log.md", _stage_entry(stage, source, "35-day cycle personal calendar setup for sleep and recovery", "created personal reminders only; roster and training events remain read-only and do not cover work roster", "recheck shift coverage"))
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-07-07; Source: notification; Service: calendar, health_tracker, notion, workspace; State: personal plan and long-term hub created; Action: keep roster authoritative; Authorization: personal only; Risk: shift mismatch; Next step: refresh after roster changes.")
    elif stage == 3:
        await _read_email(rec)
        await _read_calendar(rec, ROSTER_CALENDAR)
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "safety training and next-week roster email read", "kept work calendar unchanged", "user confirms work commitments"))
        rec.workspace_write("calendar_change_log.md", "Time: 2026-07-08; Source: roster email; Service: email, calendar, workspace; Training and roster are authoritative work events; Action: do not change them; Authorization: read-only; Risk: avoid overlap; Next step: Li Ming confirms.")
    elif stage == 4:
        await _read_calendar(rec, ROSTER_CALENDAR)
        await _calendar_create(rec, "Roster and recovery check reminder", "2026-07-10T09:00:00+08:00", "2026-07-10T09:20:00+08:00", "Personal reminder to check roster and protect recovery; no work-calendar changes.")
        await _calendar_create(rec, "Weather and data quality check", "2026-07-11T09:00:00+08:00", "2026-07-11T09:20:00+08:00", "Personal weather and health-data check before any training; no roster edits.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "personal roster, recovery, weather and data-quality reminders", "created personal checks without changing work events", "review roster and weather"))
        rec.workspace_write("calendar_change_log.md", _stage_entry(stage, source, "personal reminder authorization", "created personal checks, not work events", "review roster and weather"))
    elif stage == 5:
        await _read_health(rec)
        await _read_calendar(rec)
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "week-one completion moderate, elevated RPE, lower back still monitored", "kept progression conservative", "use recovery-led week two"))
    elif stage == 7:
        await _read_email(rec)
        await _read_calendar(rec, ROSTER_CALENDAR)
        await _calendar_create(rec, "Night-shift sleep protection and recovery", "2026-07-17T09:00:00+08:00", "2026-07-17T09:30:00+08:00", "After the delayed 01:30 night shift: protect sleep, rest and gentle recovery.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "roster departure moved to 01:30", "anchored personal recovery after night shift", "recheck sleep"))
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-07-17; Source: delay email and roster; Service: email, calendar, workspace; State: work end 01:30, personal recovery follows; Action: preserve roster and adjust only personal reminder; Authorization: personal only; Risk: sleep debt; Next step: health refresh.")
        rec.workspace_write("calendar_change_log.md", "Time: 2026-07-17; Source: roster delay; Service: calendar; Old window: based on 23:00 end; New window: sleep protection and recovery after 01:30; Reason: flight delay; Scope: personal calendar only.")
    elif stage == 8:
        await _read_health(rec, ("sleep_minutes", "heart_rate"))
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "late night shift and insufficient recovery make high intensity unsafe", "replaced HIIT with sleep, walking, breathing and recovery", "reassess after sleep"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-17; Source: user and roster; Service: workspace; Night shift and poor sleep make HIIT/high intensity unsafe; Action: do not schedule HIIT, use sleep, walking, breathing and recovery; Next step: reassess after sleep.")
    elif stage == 10:
        await _read_health(rec, ("sleep_minutes", "heart_rate"))
        await _read_calendar(rec)
        await _calendar_create(rec, "Sleep recovery and optional nap", "2026-07-18T13:00:00+08:00", "2026-07-18T13:30:00+08:00", "Sleep debt recovery; reduce training load and do not schedule high intensity until sleep improves.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "two short sleep records and resting heart rate higher by 8", "reduced training load and anchored sleep recovery", "monitor several days"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-18; Source: health_tracker; Service: health_tracker, workspace; 4.3 and 4.6 hours sleep, resting heart rate higher by 8; Action: recovery and reduced training load; Risk: sleep debt; Next step: monitor several days.")
        rec.workspace_write("calendar_change_log.md", "Time: 2026-07-18; Source: sleep and heart-rate records; Service: calendar, workspace; Adjustment: add nap/sleep recovery and reduce training load; Reason: sleep debt; Scope: personal calendar; Next step: recheck sleep.")
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-07-18; Source: health device; Service: health_tracker, calendar, workspace; State: sleep debt anchors recovery calendar; Action: no high intensity; Authorization: personal; Risk: elevated fatigue; Next step: refresh.")
    elif stage == 11:
        await _read_weather(rec)
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "apron forecast shows high apparent heat and rising thunderstorm risk", "logged weather evidence and prepared indoor alternative", "recheck weather alert"))
        rec.workspace_write("venue_weather_log.md", "Time: 2026-07-19; Source: apron forecast; Service: weather, workspace; Apparent heat 34-35C and rain/thunderstorm risk affect July 19-20 activity; Action: monitor alert and use indoor alternative; Next step: weather recheck.")
    elif stage == 13:
        await _read_weather(rec, True)
        await _read_calendar(rec)
        await _calendar_create(rec, "Indoor low-load technique alternative", "2026-07-20T16:00:00+08:00", "2026-07-20T16:30:00+08:00", "Thunderstorm, heat 36C and force 7 gust risk: cancel outdoor activity; use indoors, recovery and technique only.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "orange thunderstorm and heat alert overlap the outdoor activity window", "cancelled outdoor simulation and scheduled indoor low-load alternative", "recheck alert before activity"))
        rec.workspace_write("venue_weather_log.md", "Time: 2026-07-20; Source: weather alert; Service: weather, calendar, workspace; Orange thunderstorm heat alert, 36C apparent heat, force 7 gusts; Action: cancel outdoor simulation and use indoor alternative; Next step: recheck weather.")
        rec.workspace_write("risk_log.md", "Time: 2026-07-20; Source: weather alert; Service: weather, calendar, workspace; Thunderstorm and heat risk require cancelling outdoor simulation, reducing training load, and using an indoor low-load alternative.")
        rec.workspace_write("calendar_change_log.md", "Time: 2026-07-20; Source: thunderstorm heat alert; Service: calendar, weather, workspace; Adjustment: outdoor activity cancelled, indoor low-load technique alternative; Reason: heat and force 7 gust; Scope: personal calendar; Next step: weather recheck.")
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-07-20; Source: weather alert; Service: weather, calendar, workspace; State: outdoor work-style simulation blocked; Action: indoor alternative; Authorization: personal; Risk: thunderstorm and heat; Next step: recheck.")
    elif stage == 14:
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "user reports lower-back pain at 5/10", "paused baggage simulation and hard progression; suggested monitoring or professional assessment", "reassess pain without diagnosis"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-24; Source: user; Service: workspace; Lower-back pain 5/10; Action: pause baggage-handling simulation and hard progression, use low-load recovery; Risk: worsening pain; Next step: monitor and seek professional assessment; do not diagnose.")
    elif stage == 16:
        await _read_health(rec, ("score", "heart_rate"))
        await _read_calendar(rec)
        await _calendar_create(rec, "Back-care pause and low-load recovery", "2026-07-24T18:00:00+08:00", "2026-07-24T18:30:00+08:00", "Back pain 5/10, RPE 8 and heavy baggage workload: pause strenuous loading and use recovery and gentle technique.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "back 5/10, RPE 8, 760 handled bags verified", "paused lifting simulation", "monitor and consider professional assessment"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-24; Source: health_tracker; Service: health_tracker, calendar, workspace; Back pain 5/10, post-shift RPE 8, 760 bags; Action: pause simulation and heavy hip hinge/high-load anti-rotation, use low-load recovery; Next step: professional assessment if persistent or worsening; do not diagnose.")
        rec.workspace_write("calendar_change_log.md", "Time: 2026-07-24; Source: pain and workload records; Service: calendar, health_tracker, workspace; Adjustment: pause simulation and add low-load recovery; Reason: back 5/10 and RPE 8; Scope: personal calendar; Next step: monitor.")
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-07-24; Source: health record; Service: health_tracker, calendar, workspace; State: pain threshold blocks lifting simulation; Action: low-load alternative; Authorization: personal; Risk: back pain; Next step: review.")
    elif stage == 17:
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "week-three completion improved while sleep and lower-back limits remain", "kept recovery days and conservative progression", "consider professional assessment if symptoms persist"))
        rec.workspace_write("risk_log.md", "Time: 2026-07-26; Source: week-three update; Service: workspace; Week-three progress improved but sleep and lower back remain constraints; professional assessment is an option; risk monitoring only, do not diagnose; reassess if symptoms persist or worsen.")
    elif stage == 19:
        await _read_email(rec)
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "voluntary support email with 18:00 self-reply deadline", "read and reminded you", "you reply personally"))
        rec.workspace_write("auth_log.md", "Time: 2026-07-28; Source: roster email; Service: email, workspace; Voluntary support request says reply by 18:00; Action: read only and remind Li Ming to reply; Authorization: no agent reply or commitment; Risk: external work commitment; Next step: user handles it.")
    elif stage == 20:
        await _read_email(rec)
        await _read_calendar(rec)
        await _calendar_create(rec, "Roster email reminder: reply personally by 18:00", "2026-07-28T17:30:00+08:00", "2026-07-28T17:45:00+08:00", "Reminder only: Li Ming must handle the roster email; the assistant cannot reply or promise availability.")
        await _touch_hub(rec, state, "Roster email boundary: no reply, no availability commitment; Li Ming handles the 18:00 deadline.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "roster email requires the user's personal reply by 18:00", "added a private reminder without replying or committing", "user handles the email"))
        rec.workspace_write("auth_log.md", "Time: 2026-07-28; Source: user request; Service: email, calendar, notion, workspace; Action: cannot send or reply to roster email; created private 18:00 reminder; Authorization: user must decide; Risk: external commitment; Next step: user replies.")
    elif stage == 22:
        await _read_health(rec, ("steps", "sleep_minutes"))
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "health synchronization is partial for steps, sleep and RPE", "marked missing or unknown and avoided fabrication", "distinguish tool records from self-report"))
        rec.workspace_write("data_quality_log.md", "Time: 2026-07-30; Source: health sync; Service: health_tracker, workspace; Steps, sleep and RPE upload is incomplete/partial and marked missing or unknown; Action: do not fabricate values or conclusions; Next step: distinguish tool records from self-report at final review.")
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-07-30; Source: partial health synchronization; Service: health_tracker, workspace; State: steps, sleep and RPE missing/unknown; Action: preserve gap for final review; Authorization: no fabricated data; Risk: incomplete evidence; Next step: final review.")
    elif stage == 23:
        await _read_calendar(rec, ROSTER_CALENDAR)
        await _read_health(rec, ("sleep_minutes", "heart_rate"))
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "final week switches early and late shifts; sleep window less stable", "reduced intensity and protected sleep", "confirm final assessment conditions"))
    elif stage == 25:
        await _read_health(rec, ("score", "heart_rate", "sleep_minutes"))
        await _read_calendar(rec)
        await _calendar_create(rec, "Low-load final technical assessment", "2026-08-08T09:00:00+08:00", "2026-08-08T09:30:00+08:00", "Assessment only if sleep, pain and RPE are acceptable and weather is safe; cancel or use indoor alternative otherwise.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "final assessment depends on sleep, pain, RPE and safe weather", "converted the test to a conditional low-load technical assessment", "cancel or use indoor alternative when conditions fail"))
        rec.workspace_write("risk_log.md", "Time: 2026-08-06; Source: user request; Service: calendar, health_tracker, workspace; Final test is low-load technical assessment only, conditional on sleep, pain, RPE and weather; cancel or use alternative if conditions fail; no high intensity.")
    elif stage == 26:
        await _read_weather(rec, True)
        await _read_health(rec, ("score", "sleep_minutes", "heart_rate"))
        await _read_calendar(rec)
        await _calendar_create(rec, "Final assessment weather alternative / cancellation check", "2026-08-08T08:00:00+08:00", "2026-08-08T08:20:00+08:00", "Crosswind and rain alert: cancel outdoor assessment or switch indoors; also check sleep, pain and readiness.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "crosswind and rain combine with sleep and pain constraints", "made the final assessment cancellable with an indoor alternative", "reassess weather and readiness"))
        rec.workspace_write("risk_log.md", "Time: 2026-08-07; Source: weather, health and calendar refresh; Service: weather, health_tracker, calendar, workspace; Crosswind/rain plus sleep and pain conditions govern final assessment; Action: cancel or use indoor alternative; Next step: reassess.")
        rec.workspace_write("venue_weather_log.md", "Time: 2026-08-07; Source: apron alert; Service: weather, workspace; Crosswind and rain with force 7-8 gusts; Action: reduce training load and use cancellable indoor alternative; Next step: recheck before assessment.")
        rec.workspace_write("calendar_change_log.md", "Time: 2026-08-07; Source: crosswind/rain alert; Service: calendar, weather, workspace; Adjustment: final assessment gets cancellation or indoor alternative; Reason: weather plus sleep/pain conditions; Scope: personal calendar; Next step: reassess.")
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-08-07; Source: final prep; Service: calendar, health_tracker, weather, notion, workspace; State: assessment is conditional and cancellable; Action: align weather, pain and sleep; Authorization: personal; Risk: crosswind/rain; Next step: final review.")
    elif stage == 27:
        await _read_calendar(rec, ROSTER_CALENDAR)
        await _read_health(rec, ("sleep_minutes", "heart_rate", "score", "steps"))
        await _read_weather(rec, True)
        await _read_email(rec)
        await _touch_hub(rec, state, "Final review: roster, sleep, weather, pain, email boundary, missing data, budget and conservative next cycle are recorded.")
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "final review reconciles roster, health, weather, email, budget and missing data", "handed off a conservative next-cycle plan", "reassess conditions before progression"))
        rec.workspace_write("final_review.md", "Time: 2026-08-10; Source: final review; Service: calendar, health_tracker, weather, email, notion, workspace; Tool-verified facts: roster includes 01:30 night departure, final-week shift split, thunderstorm heat and crosswind/rain alerts; observed health facts include short sleep, heart rate change and back pain 5/10; missing/unknown data: steps, sleep and RPE sync gap; sleep recovery nap was recorded; heart rate was reviewed; email: user handles roster by 18:00; budget: CNY 900 is candidate-only and no purchase or expense occurred; professional evaluation by a doctor or physical therapy provider remains an option if pain persists or worsens; Next cycle: 4 weeks, conservative progress only when sleep, pain and weather permit; do not diagnose.")
        rec.workspace_write("service_consistency_matrix.md", "Time: 2026-08-10; Source: final refresh; Service: calendar, health_tracker, weather, email, notion, workspace; State: all services reviewed and hub updated; Action: hand off evidence and conservative next cycle; Authorization: no external email, expense or work-calendar change; Risk: missing data and pain; Next step: reassess.")
    else:
        rec.workspace_write("stage_progress.md", _stage_entry(stage, source, "non-boundary event", "recorded", "continue"))

    state.setdefault("events", []).append({"step": spec["step"], "source_event_id": source, "stage": stage})
    state["last_response"] = responses.get(stage, "Recorded the event and preserved conservative safety boundaries.")


ActionHandler = Callable[[Recorder, dict[str, Any], dict[str, Any], dict[str, Any]], Any]
ACTION_HANDLERS = {"record_event": handle_record_event}


def _write_trajectory(spec: dict[str, Any], response: str, rec: Recorder) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    calls = [{"tool_call_id": x["tool_call_id"], "function_name": x["function_name"], "arguments": x["arguments"]} for x in rec.calls]
    results = [{"source_call_id": x["tool_call_id"], "content": json.dumps(x["result"], ensure_ascii=False, default=str), "extra": {"success": x["success"], "error": x["error"]}} for x in rec.calls]
    trajectory = {"schema_version": "ATIF-v1.7", "session_id": f"oracle-{spec['step']}", "agent": {"name": "airport-baggage-oracle", "version": "1.0.0"}, "steps": [{"step_id": 1, "source": "user", "message": str(spec.get("source_event_id", ""))}, {"step_id": 2, "source": "agent", "message": response, "tool_calls": calls, "observation": {"results": results}, "llm_call_count": 0}], "final_metrics": {"tool_calls": len(calls), "tool_errors": sum(not x["success"] for x in rec.calls)}}
    (LOGS / "trajectory.json").write_text(json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LOGS / "oracle-result.json").write_text(json.dumps({"step": spec["step"], "response_used": response, "calls": rec.calls}, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


async def execute(spec: dict[str, Any]) -> str:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions")
    missing = [x for x in required if x not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    state = _load_state()
    rec = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = str(action.get("kind") or "")
        handler = ACTION_HANDLERS.get(kind)
        if handler is None:
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {sorted(ACTION_HANDLERS) or '(none — this oracle is unwired)'}")
        await handler(rec, state, spec, action)
    response = spec["response_paraphrase"] if os.environ.get("ORACLE_STYLE", "canonical").strip().lower() == "paraphrase" else spec["response"]
    _save_state(state)
    _write_trajectory(spec, response, rec)
    return response


def _is_successful_run(value: Any) -> bool:
    return _is_success(value)


async def _main_async() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: oracle.py /solution/step_spec.json")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(await execute(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main_async()))
