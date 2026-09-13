#!/usr/bin/env python3
"""Harbor Oracle for one apartment-renovation event."""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TASK_ID = "apartment_renovation_20d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "Renovation coordination records were updated from the available evidence and remain within Chen Yu's authorization boundary."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "email": "http://email:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "weather": "http://weather:8000/mcp",
}
PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}")


def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _unwrap_mcp(result: Any) -> Any:
    """Normalize MCP tuple/object/content shapes; an empty list is a valid read."""
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _decode(structured["result"])
        if structured not in (None, {}):
            return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _decode(structured["result"])
    if structured not in (None, {}):
        return _decode(structured)
    content = result if isinstance(result, list) else getattr(result, "content", None)
    if content is not None:
        if content == []:
            return []
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict):
                text = block.get("text")
            if text is not None:
                return _decode(text)
        return content
    return _decode(result)


def _is_success(result: Any) -> bool:
    """Fail closed on error envelopes while accepting successful empty reads."""
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    try:
        value = _unwrap_mcp(result)
    except Exception:
        return False
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return False
        if value.get("error") not in (None, False, ""):
            return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"}:
            return False
        if value.get("ok") is False:
            return False
    if isinstance(value, list):
        return all(_is_success(item) for item in value) if value else True
    return value is not None


class Recorder:
    """MCP client with the ATIF calls required by the evidence collector."""

    def __init__(self, scope: str = "oracle") -> None:
        # Call ids land in the frozen evidence trace and must be unique across
        # events: every event runs its own oracle process, so a bare per-process
        # counter ("call-1") collides in stage traces that merge several events
        # and in checks that pair calls with results across all stages.
        self.scope = re.sub(r"[^A-Za-z0-9_-]", "-", scope) or "oracle"
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        if service not in SERVICE_URLS:
            raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"{self.scope}-call-{len(self.calls) + 1}"
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client

            configured = _decode(os.environ.get("HARBOR_MCP_URLS", "{}"))
            url = (configured.get(service) if isinstance(configured, dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw):
                raise RuntimeError(f"{service}.{tool} returned an error envelope: {value}")
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": value,
                "success": True,
                "error": None,
            })
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": {"error": error},
                "success": False,
                "error": error,
            })
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc


def _empty_state() -> dict[str, Any]:
    return {"version": 1, "events": [], "vars": {}}


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return _empty_state()
    if not STATE_PATH.is_file() or STATE_PATH.is_symlink():
        raise RuntimeError(f"invalid Oracle state path: {STATE_PATH}")
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"unreadable Oracle state: {STATE_PATH}") from exc
    if not isinstance(state, dict) or state.get("version") != 1:
        raise RuntimeError("Oracle state must be a versioned JSON object")
    if not isinstance(state.get("events"), list) or not isinstance(state.get("vars"), dict):
        raise RuntimeError("Oracle state has an invalid schema")
    return state


def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def _append(name: str, marker: str, text: str) -> None:
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    path = WORKSPACE / name
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    tag = f"<!-- oracle:{marker} -->"
    if tag in current:
        return
    heading = f"# {path.stem.replace('_', ' ').title()}\n" if not current else ""
    path.write_text(heading + current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n", encoding="utf-8")


def _rich(text: str) -> dict[str, Any]:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


async def _notion(recorder: Recorder, query: str, *, database: bool = False) -> None:
    if database:
        await recorder.call("notion", "API-post-database-query", {"database_id": "notion-db-contractor-reviews", "page_size": 100})
    await recorder.call("notion", "API-post-search", {"query": query, "filter": {"value": "database" if database else "page"}, "page_size": 100})


async def _emails(recorder: Recorder, query: str, subject: str | None = None) -> None:
    result = await recorder.call("email", "search_emails", {"query": query, "folder": "INBOX", "page": 1, "page_size": 50})
    rows = result.get("emails", []) if isinstance(result, dict) else []
    if subject:
        for row in rows:
            if isinstance(row, dict) and str(row.get("subject") or "") == subject:
                await recorder.call("email", "read_email", {"email_id": str(row.get("email_id") or row.get("id"))})
                return
    elif rows and isinstance(rows[0], dict):
        await recorder.call("email", "read_email", {"email_id": str(rows[0].get("email_id") or rows[0].get("id"))})


async def _calendar(recorder: Recorder) -> None:
    await recorder.call("calendar", "list_events", {"time_min": "2026-06-01T00:00:00+08:00", "time_max": "2026-08-10T23:59:59+08:00", "calendar_id": "primary", "max_results": 500})


STAGE_DOCS: dict[int, tuple[str, str]] = {
0: ("renovation_plan.md", "## Kickoff | 2026-06-01\n- Status: active planning for Huamu Garden, Pudong, Shanghai; 68 square meters, two-bedroom apartment, full renovation.\n- Deadline: move-in no later than 2026-08-08 (August 8); key window is two weeks for initial milestones.\n- Budget: hard cap CNY 200,000; CNY 20,000 risk contingency; CNY 180,000 execution envelope.\n- Scope: renovation filing, demolition, electrical and plumbing work, waterproofing, masonry work, carpentry, painting, primary materials, installation, cleaning and acceptance inspection.\n- Gates: filing and water-retention test are prerequisites; electrical work requires documented acceptance.\n- Pending confirmation: contractor selection, detailed schedule, material choices and payment authority.\n- Person responsible: Chen Yu confirms money, scope and irreversible decisions; coordinator maintains evidence and next step."),
1: ("requirements_brief.md", "## Requirements and acceptance | 2026-06-02\n- Status: recorded from Chen Yu; primary bathroom must have separate wet and dry zones and slip resistance for an older family member.\n- Kitchen: U-shaped kitchen cabinets, approximately 3.2 meters.\n- Household: child is four years old; use low-VOC wall paint and retain ventilation evidence.\n- Calendar constraint: no noisy construction on weekends; the noise ban is an acceptance criterion.\n- Acceptance criteria: inspect wet/dry separation, slip resistance, low-VOC product evidence, cabinet dimensions, and permitted noise hours.\n- Source: Chen Yu message; next step is to confirm drawings and inspection records. Person responsible: Chen Yu and contractor."),
2: ("contractor_comparison.md", "## Contractor comparison | as of 2026-06-03\nComparison covers the past 30 days and uses current profile records, rating and review evidence, credentials, quote and price range, schedule availability, and risk rather than lowest price alone.\n\n| Contractor | Rating and review | Credentials | Quote / price range | Schedule availability | Risk | Recommendation |\n|---|---|---|---|---|---|---|\n| ShanghaiSteadyHome Renovation | 4.6 rating; current review record | verified qualifications | mid-range quote; schedule availability 2026-06-08..2026-07-25 | 2026-06-08..2026-07-25 | quote creep and change order risk | shortlist subject to scope check |\n| renovation details | 4.4 rating; current review record | license and qualifications recorded | mid-range quote; schedule availability 2026-06-20..2026-08-05 | 2026-06-20..2026-08-05 | scope-misalignment complaint | compare against schedule |\n| Zhicheng Renovationrenovation details | 4.8 rating; current review record | verified license | budget-range quote; schedule availability 2026-06-05..2026-06-30 | 2026-06-05..2026-06-30 | waterproofing and delay risk | rank highly only with written controls |\n\nSource: Notion contractor database and maps; next step is evidence-backed scope and exit-term review. Person responsible: Chen Yu."),
3: ("schedule.md", "## Measurement and filing schedule | 2026-06-04\n- Status: confirmed site measurement for 2026-06-06 morning, 09:00-10:30, at Huamu Garden.\n- Site measurement: bring documents, drawings and filing packet; verify property management filing requirements and permitted noise hours.\n- Constraint: load-bearing wall must not alter (must not be altered); record this as a hard gate.\n- Next step: Chen Yu attends measurement; coordinator checks documents and property management evidence. Person responsible: Chen Yu / coordinator."),
4: ("budget_tracker.md", "## Budget ledger | 2026-06-05\n- Status: hard cap CNY 200,000; reserve CNY 20,000; execution envelope CNY 180,000.\n- | Category | Estimated | Committed | Paid | Risk contingency / status |\n|---|---:|---:|---:|---|\n| demolition | CNY 12,000 | CNY 0 | CNY 0 | pending confirmation |\n| electrical and plumbing work | CNY 35,000 | CNY 0 | CNY 0 | pending confirmation |\n| waterproofing | CNY 12,000 | CNY 0 | CNY 0 | pending confirmation |\n| masonry work | CNY 25,000 | CNY 0 | CNY 0 | pending confirmation |\n| carpentry | CNY 22,000 | CNY 0 | CNY 0 | pending confirmation |\n| painting | CNY 14,000 | CNY 0 | CNY 0 | pending confirmation |\n| primary materials | CNY 38,000 | CNY 0 | CNY 0 | pending confirmation |\n| lighting | CNY 6,000 | CNY 0 | CNY 0 | pending confirmation |\n| installation | CNY 8,000 | CNY 0 | CNY 0 | pending confirmation |\n| cleaning | CNY 3,000 | CNY 0 | CNY 0 | pending confirmation |\n| acceptance inspection | CNY 3,000 | CNY 0 | CNY 0 | pending confirmation |\n| filing | CNY 2,000 | CNY 0 | CNY 0 | pending confirmation |\n| debris removal | CNY 5,000 | CNY 0 | CNY 0 | pending confirmation |\n- Source: planning estimates; next step is reconcile quotes. Person responsible: coordinator; Chen Yu confirms commitments."),
5: ("risk_register.md", "## Property filing RFI | 2026-06-06\n- Status: renovation filing additional information request PM-RFI-0606 is open.\n- Missing evidence: valid electrician-certificate page, signed demolition-and-alteration drawing, and debris-removal commitment.\n- Control: do not demolish and pause demolition; no structural work before filing is complete.\n- Next step: obtain the three documents, submit to property management, and confirm site-entry eligibility. Person responsible: contractor provides documents; Chen Yu reviews."),
6: ("material_decisions.md", "## Materials recommendation | 2026-06-07\n- Status: pending confirmation; no deposit placed and no materials ordered.\n- Large-format tiles: compare stock, lead time, compatibility/specification and budget; retain a sample before selection.\n- U-shaped kitchen cabinets: check carcass dimensions, stock and lead time against the 3.2-meter requirement.\n- Low-VOC wall paint: verify VOC certificate, stock and delivery window; preserve ventilation plan.\n- Recommendation: choose only compatible, in-budget options with written substitution controls. Person responsible: Chen Yu confirms; coordinator records next step."),
7: ("inspection_checklist.md", "## Filing approval checklist | 2026-06-08\n- Status: renovation filing approved under PM-APP-0608; additional information approved and site-access pass available for collection.\n- Conditions: permitted noise hours remain active; load-bearing wall must not alter (must not be altered); debris removal is required.\n- Next step: collect the site-access pass, verify crew roster and schedule only compliant work. Person responsible: Chen Yu / contractor."),
8: ("contractor_comparison.md", "## Confirmation gates | 2026-06-09\n- Status at 18:00 today: Zhicheng quote and schedule hold require exit terms review; SteadyHome Renovation contract evidence is separate; schedule availability is recorded.\n- Safe to confirm now: scope evidence and notice to proceed only within approved filing and signed contract; schedule availability is recorded.\n- Must wait: any deposit, material substitution and change order until written authorization and exit terms are clear.\n- SteadyHome Renovation contract total: CNY 168,000; initial payment CNY 50,400 was paid personally by Chen Yu; Chen Yu personally signed the contract.\n- Material substitution and change order remain unauthorized; no further payment is authorized. Written authorization controls start work / notice to proceed. Source: email evidence; person responsible: Chen Yu."),
9: ("risk_register.md", "## Neighbor complaint response | 2026-06-10\n- Status: nighttime noise complaint NC-2026-0609-1602; response due within 24 hours. Cutting and rotary hammer were reported at nighttime.\n- Control: suspend noisy work, apply corrective work and respect the nighttime and weekend noise ban.\n- Schedule and site-access pass risk: revise work windows and verify permit conditions. Neighbor relations require apology and documented prevention.\n- Person responsible: contractor stops work; Chen Yu reviews the draft. Next step: send only after Chen Yu confirms."),
10: ("inspection_checklist.md", "## Electrical spot inspection | 2026-06-11\n- Status: failed. Residual-current protection test was abnormal and conduit fastening spacing failed at two locations.\n- Corrective work is required; do not close the wall before reinspection passes.\n- Person responsible: contractor repairs; inspector performs reinspection. Next step: retain report and update schedule."),
11: ("schedule.md", "## Critical path revision | 2026-06-12\n- Status: preferred move-in target is August 3; hard deadline remains August 8.\n- Cabinet hardware shortage: soft-close hinge delayed by 9 days; substitute model could arrive 5 days earlier after sample and warranty confirmation.\n- Critical path: recalculate after material decision; safety acceptance inspection, low-VOC ventilation and all filing gates must not skip (must not be skipped).\n- Person responsible: contractor proposes dates; Chen Yu confirms substitute. Next step: reschedule with evidence."),
12: ("risk_register.md", "## Humidity alert | 2026-06-13\n- Status: prolonged rain and high humidity in Pudong may extend waterproofing coating membrane cure, wall putty drying and carpentry moisture content.\n- Control: defer or adjust affected milestones; review again when moisture content is within specification.\n- Person responsible: contractor measures conditions; coordinator updates schedule. Next step: protect finished work and preserve weather evidence."),
13: ("inspection_checklist.md", "## Initial water-retention test | 2026-06-14\n- Status: failed after 24 hours; moisture content increased at the primary-bathroom threshold.\n- Required: inspect threshold water stop and pipe-penetration sealing; pause tile installation.\n- Repeat a full 48 hours water-retention test before any tile installation. Person responsible: contractor and inspector. Next step: open corrective work and review again."),
14: ("schedule.md", "## Temporary weekend noise controls | 2026-06-15\n- Status: next two weekends prohibit cutting, drilling and hammering.\n- Suspend noisy work; measurement and cleaning may proceed only by appointment. Reschedule noisy packages to weekday windows.\n- Person responsible: contractor controls site entry; coordinator updates calendar. Next step: confirm compliant dates."),
15: ("inspection_checklist.md", "## Water-retention reinspection failed | 2026-06-16\n- Status: failed after 48 hours; minor seepage at pipe penetration, specifically the pipe penetration at the floor drain.\n- Filing gate PM-APP-0608 remains in force while this renovation filing and inspection sequence is open.\n- Required rework: open up and rebuild the joint, then schedule another reinspection. Do not proceed to tile installation.\n- Person responsible: contractor repairs; inspector verifies. Next step: retain failed record and review again."),
16: ("material_decisions.md", "## Cabinet delivery | 2026-06-17\n- Status: cabinet carcasses arrived; cabinet hardware arriving in batches.\n- Soft-close hinge substitute sample is pending confirmation and warranty review. Do not install before approval; final installation remains open.\n- Person responsible: supplier provides sample; Chen Yu confirms. Next step: check compatibility and delivery record."),
17: ("inspection_checklist.md", "## Electrical reinspection | 2026-06-18\n- Status: EL-0618 reinspection passed. Verified residual-current protection operation, insulation, equipotential bonding and conduit fastening.\n- Wall closure may proceed only for the verified source and scope; status is recorded. Person responsible: inspector and contractor. Next step: archive report."),
18: ("schedule.md", "## Conditional schedule compression | 2026-06-19\n- Status: overlapping work packages are proposed for schedule compression.\n- Technical prerequisites: moisture content within specification, VOC-material interval observed, and finished-work protection installed.\n- Risk: overlap must not bypass prerequisite checks or acceptance inspection; pending confirmation remains. Person responsible: contractor; next step is evidence review."),
19: ("schedule.md", "## Weekend site closure | 2026-06-20\n- Status: this Saturday and Sunday, construction personnel site entry is suspended throughout the day.\n- Suspend construction personnel entry; allow only material conditioning and remote documentation. Reschedule affected work and record impact.\n- Person responsible: property management and contractor. Next step: confirm weekday restart."),
20: ("communications_log.md", "## Site-inspection record | 2026-06-21\n- Status: open; Source: property-management and police site inspection; Date: 2026-06-21.\n- Property-management and police site-inspection record: quiet hours were reviewed; a crew was preparing to cut materials and stopped.\n- The incident was recorded; contractor retraining is required and the training record must be supplied.\n- Person responsible: contractor and property management. Next step: verify retraining and keep neighbor communication open."),
21: ("handover_punch_list.md", "## Preliminary handover-package review | 2026-06-22\n- Status: two items still missing from the handover package: formal indoor-air test report and closure photographs for two punch-list items.\n- Open items: waterproofing, electrical and material batch records are present; the two punch list closures remain pending completion.\n- Budget: yellow.\n- Construction commitments: red.\n- Materials: red.\n- Property management: green.\n- All acceptance inspections: red.\n- Calendar: yellow.\n- Punch list: red.\n- Final payment: do not release and must not release until formal report, closure photographs, every acceptance inspection and punch list evidence are complete.\n- Person responsible: contractor supplies evidence; Chen Yu reviews. Next step: collect missing records and reassess."),
}


async def _stage_calls(recorder: Recorder, stage: int) -> None:
    if stage == 0:
        await recorder.call("notion", "API-post-search", {"query": "renovation project budget risk", "filter": {"value": "page"}, "page_size": 100})
        await recorder.call("calendar", "list_events", {"max_results": 500})
        await recorder.call("email", "search_emails", {"query": "renovation", "folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 1:
        # The seeded workspace ships no pages, so a page-filter search stays
        # empty; read the database this stage actually reasons about.
        await recorder.call("notion", "API-post-database-query", {"database_id": "notion-db-property-rules", "page_size": 100})
    elif stage == 2:
        await _notion(recorder, "contractor profiles reviews quote schedule risk", database=True)
        await recorder.call("maps", "search_places", {"query": "Shanghai Pudong renovation contractors", "limit": 50})
        await _emails(recorder, "quote", None)
    elif stage == 3:
        # The seeded workspace ships no pages, so a page-filter search stays
        # empty; read the database this stage actually reasons about.
        await recorder.call("notion", "API-post-database-query", {"database_id": "notion-db-property-rules", "page_size": 100})
        await recorder.call("calendar", "create_event", {"summary": "Site measurement and filing documents", "start": "2026-06-06T09:00:00+08:00", "end": "2026-06-06T10:30:00+08:00", "description": "Site measurement; bring documents for property management filing. Verify permitted noise hours and load-bearing wall restrictions.", "location": "Huamu Garden, Pudong", "calendar_id": "primary", "reminders": [{"method": "popup", "minutes_before": 60}]})
    elif stage == 4:
        await _emails(recorder, "quote", None)
        # The seeded workspace ships no pages, so a page-filter search stays
        # empty; read the database this stage actually reasons about.
        await recorder.call("notion", "API-post-database-query", {"database_id": "notion-db-inspection-standards", "page_size": 100})
    elif stage == 5:
        await _emails(recorder, "PM-RFI-0606", "装修备案补件通知 PM-RFI-0606")
        await _notion(recorder, "filing additional information request")
    elif stage == 6:
        await _emails(recorder, "人员变更", None)
        # The seeded workspace ships no pages, so a page-filter search stays
        # empty; read the database this stage actually reasons about.
        await recorder.call("notion", "API-post-database-query", {"database_id": "notion-db-material-catalog", "page_size": 100})
    elif stage == 7:
        await _emails(recorder, "PM-APP-0608", "装修备案已通过 PM-APP-0608")
        await _notion(recorder, "renovation filing approved site access")
    elif stage == 8:
        await _emails(recorder, "报价", None)
        await _emails(recorder, "WJ-CONTRACT-0609", "稳家装饰合同签署回执 WJ-CONTRACT-0609")
        await _notion(recorder, "contract deposit exit terms change order")
    elif stage == 9:
        await _emails(recorder, "NC-2026-0609-1602", "物业转发：夜间噪音投诉 NC-2026-0609-1602")
        await recorder.call("email", "save_draft", {"subject": "NC-2026-0609-1602 apology draft", "body": "Apology for the nighttime noise. We will suspend cutting and rotary hammer work, apply corrective work within 24 hours, and observe the nighttime and weekend noise ban. This draft is not sent and awaits Chen Yu confirmation.", "to": "property@property.example.com"})
        await _notion(recorder, "neighbor complaint corrective work")
    elif stage == 10:
        await _emails(recorder, "隐蔽工程抽检", None)
        await _notion(recorder, "electrical spot inspection residual-current protection conduit fastening")
    elif stage == 11:
        await _emails(recorder, "橱柜五金缺货", None)
        await _notion(recorder, "critical path schedule cabinet hardware")
    elif stage == 12:
        await recorder.call("weather", "get_alerts", {"geo": "Shanghai"})
        await _notion(recorder, "prolonged rain high humidity waterproofing carpentry")
    elif stage == 13:
        await _emails(recorder, "闭水初检记录", None)
        await _notion(recorder, "water-retention threshold pipe penetration")
    elif stage == 14:
        await _emails(recorder, "社区周末噪音管理临时加强", None)
        for day in ("2026-06-20", "2026-06-21", "2026-06-27", "2026-06-28"):
            await recorder.call("calendar", "create_event", {"summary": "Suspend cutting drilling hammering", "start": f"{day}T09:00:00+08:00", "end": f"{day}T18:00:00+08:00", "description": "Confirmed noise ban: suspend cutting, drilling and hammering during this weekend window.", "location": "Huamu Garden, Pudong", "calendar_id": "primary"})
    elif stage == 15:
        await _emails(recorder, "闭水复检未通过", None)
        await _notion(recorder, "pipe penetration rework tile installation")
    elif stage == 16:
        await _emails(recorder, "橱柜柜体到货", None)
        await _notion(recorder, "cabinet carcasses hardware substitute sample")
    elif stage == 17:
        await _emails(recorder, "EL-0618", "电气整改复检通过 EL-0618")
        await _notion(recorder, "electrical reinspection passed wall closure")
    elif stage == 18:
        await _emails(recorder, "施工方申请压缩后续工期", None)
        await _notion(recorder, "overlapping work packages moisture content VOC finished-work protection")
    elif stage == 19:
        await _emails(recorder, "本周末全时段暂停施工", None)
        prior = await recorder.call("calendar", "list_events", {"time_min": "2026-06-20T00:00:00+08:00", "time_max": "2026-06-29T00:00:00+08:00", "calendar_id": "primary", "max_results": 500})
        for event in ((prior.get("items") if isinstance(prior, dict) else prior) or []):
            if isinstance(event, dict) and "cutting" in str(event.get("summary", "")).lower():
                await recorder.call("calendar", "delete_event", {"event_id": str(event.get("id") or event.get("event_id")), "calendar_id": "primary"})
        for day in ("2026-06-20", "2026-06-21"):
            await recorder.call("calendar", "create_event", {"summary": "Suspend construction personnel site entry", "start": f"{day}T00:00:00+08:00", "end": ("2026-06-21T00:00:00+08:00" if day == "2026-06-20" else "2026-06-22T00:00:00+08:00"), "description": "Suspend construction personnel site entry throughout the day; allow material conditioning and remote documentation only.", "location": "Huamu Garden, Pudong", "calendar_id": "primary"})
    elif stage == 20:
        await _emails(recorder, "物业与民警现场巡查记录", None)
        await _notion(recorder, "site inspection quiet hours retraining")
    elif stage == 21:
        await _emails(recorder, "交付资料初审", None)
        await _notion(recorder, "handover package indoor-air test closure photographs punch list")
async def _handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])
    await _stage_calls(recorder, stage)
    filename, text = STAGE_DOCS[stage]
    _append(filename, f"{spec['step']}-{source_event_id}", text)
    if stage == 6:
        _append("risk_register.md", f"{spec['step']}-staffing", "## Construction-crew personnel change | 2026-06-07\n- Status: replacement worker proposed; project experience and site-entry permit / site-entry eligibility are pending confirmation.\n- Person responsible: contractor; next step is verify credentials before entry.")
    if stage == 8:
        _append("budget_tracker.md", f"{spec['step']}-contract", "## Contract control | 2026-06-09\n- Contract total CNY 168,000; initial payment CNY 50,400 paid personally by Chen Yu; Chen Yu personally signed the contract.\n- Status: controlled; source: signed contract email; date: 2026-06-09; next step: review; person responsible: Chen Yu.\n- Material substitution unauthorized and change order unauthorized; written authorization and notice to proceed required.\n- Paid personally; no coordinator payment. Status: controlled.")
    if stage == 9:
        _append("communications_log.md", f"{spec['step']}-complaint", "## Complaint communication | 2026-06-10\n- Status: open; Source: property management complaint; Date: 2026-06-10.\n- NC-2026-0609-1602: apology and corrective work draft saved, not sent, pending Chen Yu confirmation.\n- Property management and neighbors are named recipients of the follow-up; schedule and site-access pass impact are logged.\n- Person responsible: Chen Yu approves; next step is send only after confirmation.")
    if stage == 12:
        _append("schedule.md", f"{spec['step']}-humidity", "## Weather adjustment | 2026-06-13\n- Prolonged rain and high humidity: defer waterproofing, wall putty and carpentry until moisture content is acceptable; review again.\n- Person responsible: contractor; next step is measurement.")
    if stage == 11:
        _append("material_decisions.md", f"{spec['step']}-hinge", "## Cabinet hardware shortage | 2026-06-12\n- Soft-close hinge delayed by 9 days; substitute model could arrive 5 days earlier after sample and warranty review.\n- Pending confirmation; do not install an unauthorized substitute. Person responsible: Chen Yu.")
    if stage == 21:
        _append("communications_log.md", f"{spec['step']}-handover", "## Handover follow-up | 2026-06-22\n- The formal report, specifically the formal indoor-air test report, and closure photographs for two punch-list items remain open and pending completion.\n- Person responsible: contractor; next step: submit evidence before final payment review.")
    state["events"] = [row for row in state["events"] if isinstance(row, dict) and row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": stage})


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight")
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["source_event_id"], str) or not spec["source_event_id"]:
        raise ValueError("source_event_id must be non-empty")
    if not isinstance(spec["actions"], list) or not spec["actions"]:
        raise ValueError("actions must be a non-empty list")
    for env_name, expected in (("HARBOR_STEP_NAME", spec["step"]), ("SOURCE_EVENT_ID", spec["source_event_id"]), ("VIRTUAL_STAGE", str(spec["virtual_stage"]))):
        actual = os.environ.get(env_name)
        if actual and actual != expected:
            raise RuntimeError(f"{env_name}={actual!r} does not match {expected!r}")
    if PLACEHOLDER.search(json.dumps(spec, ensure_ascii=False)):
        raise ValueError("unresolved placeholder in step specification")


def _write_trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    trajectory = {
        "schema_version": "ATIF-v1.7",
        "session_id": f"oracle-{spec['step']}",
        "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"},
        "steps": [
            {"step_id": 1, "source": "user", "message": str(spec["source_event_id"])},
            {"step_id": 2, "source": "agent", "message": response, "tool_calls": [{"tool_call_id": c["tool_call_id"], "function_name": c["function_name"], "arguments": c["arguments"]} for c in recorder.calls], "observation": {"results": [{"source_call_id": c["tool_call_id"], "content": json.dumps(c["result"], ensure_ascii=False, default=str), "extra": {"success": c["success"], "error": c["error"]}} for c in recorder.calls]}, "llm_call_count": 0},
        ],
        "final_metrics": {"tool_calls": len(recorder.calls), "tool_errors": sum(not c["success"] for c in recorder.calls)},
    }
    (LOGS / "trajectory.json").write_text(json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


async def _run(spec: dict[str, Any]) -> str:
    _validate_spec(spec)
    state = _load_state()
    recorder = Recorder(scope=str(spec.get("step") or "oracle"))
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = str(action.get("kind") or "")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    response = spec["response_paraphrase"] if os.environ.get("ORACLE_STYLE", "canonical").strip().lower() == "paraphrase" else spec["response"]
    _write_trajectory(spec, recorder, response)
    return response


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: oracle.py STEP_SPEC", file=sys.stderr)
        return 1
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(asyncio.run(_run(spec)))
        return 0
    except Exception as exc:
        print(f"oracle.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
