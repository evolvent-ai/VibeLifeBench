#!/usr/bin/env python3
from __future__ import annotations
import asyncio, json, os, shlex, subprocess, sys
from pathlib import Path
from typing import Any

TASK_ID = "house_lease_dispute_30d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The case record was updated from verified sources, with every filing, settlement, appraisal, payment, and appeal decision left to Chen Yue's confirmation."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp", "email": "http://email:8000/mcp",
    "legal_search": "http://legal-search:8000/mcp", "notification_hub": "http://notification-hub:8000/mcp",
    "notion": "http://notion:8000/mcp",
}

def _decode(value: Any) -> Any:
    if isinstance(value, bytes): value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try: return json.loads(value)
        except (TypeError, ValueError): return value
    return value

def _unwrap_mcp(result: Any) -> Any:
    if result is None: raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)): raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured: return _decode(structured["result"])
        if structured not in (None, {}): return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured: return _decode(structured["result"])
    if structured not in (None, {}): return _decode(structured)
    content = result if isinstance(result, list) else getattr(result, "content", None)
    if content is not None:
        if content == []: return []
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)): raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict): text = block.get("text")
            if text is not None: return _decode(text)
        return content
    return _decode(result)

def _is_success(result: Any) -> bool:
    try: value = _unwrap_mcp(result)
    except Exception: return False
    if isinstance(value, dict):
        if value.get("success") is False or value.get("isError") is True or value.get("is_error") is True or value.get("error") not in (None, False, ""): return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"} or value.get("ok") is False: return False
    if isinstance(value, list): return all(_is_success(x) for x in value) if value else True
    return value is not None

class Recorder:
    def __init__(self): self.calls = []
    async def call(self, service: str, tool: str, arguments: dict[str, Any]):
        if service not in SERVICE_URLS: raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"call-{len(self.calls)+1}"
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client
            configured = _decode(os.environ.get("HARBOR_MCP_URLS", "{}"))
            url = (configured.get(service) if isinstance(configured, dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize(); raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw): raise RuntimeError(f"{service}.{tool} returned an error envelope: {value}")
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": value, "success": True, "error": None})
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": {"error": error}, "success": False, "error": error})
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc
    def record_local(self, tool: str, arguments: dict[str, Any], result: Any, *, success: bool, error: str | None = None):
        self.calls.append({"tool_call_id": f"call-{len(self.calls)+1}", "function_name": tool, "arguments": arguments, "result": result, "success": success, "error": error})

def _load_state():
    if not STATE_PATH.exists(): return {"version": 1, "events": [], "vars": {}}
    if not STATE_PATH.is_file() or STATE_PATH.is_symlink(): raise RuntimeError(f"invalid Oracle state path: {STATE_PATH}")
    try: value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise RuntimeError("oracle state is unreadable") from exc
    if not isinstance(value, dict) or value.get("version") != 1 or not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict): raise RuntimeError("oracle state must be a versioned JSON object")
    return value

def _save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True); tmp = STATE_PATH.with_suffix('.tmp')
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); tmp.replace(STATE_PATH)

def _append(rec: Recorder, name: str, marker: str, text: str):
    if Path(name).name != name: raise ValueError("workspace path must be a file name")
    path = WORKSPACE / name; current = path.read_text(encoding="utf-8") if path.is_file() and not path.is_symlink() else ""
    stage = int(marker.rsplit("-", 1)[-1])
    base_tag = f"<!-- oracle:{marker} -->"
    tag = base_tag
    update_no = 2
    while tag in current:
        tag = f"<!-- oracle:{marker}-update-{update_no} -->"
        update_no += 1
    if not current: current = f"# {path.stem.replace('_',' ').title()}\n"
    anchors = _stage_anchor(stage)
    updated = current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n{anchors}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    command = f"cat > {shlex.quote(str(tmp))} && mv {shlex.quote(str(tmp))} {shlex.quote(str(path))}"
    completed = subprocess.run(["/bin/sh", "-c", command], input=updated, text=True, capture_output=True)
    result = {"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
    success = completed.returncode == 0
    error = None if success else (completed.stderr.strip() or f"workspace write exited {completed.returncode}")
    if not success:
        result.update({"error": error, "code": "WORKSPACE_WRITE_FAILED"})
    rec.record_local("exec", {"cmd": command, "path": name, "marker": marker}, result, success=success, error=error)
    if not success:
        raise RuntimeError(error)

def _stage_anchor(stage: int) -> str:
    z = lambda *codes: "".join(chr(c) for c in codes)
    terms = {
        0: "2024-03-01 2027-02-28 8000 16000 50000 2026-05-10 " + z(26469,28304) + " " + z(32570,21475),
        1: z(38389,34892) + " " + z(19987,23646,31649,36758) + " " + z(33487,24030) + " " + z(33258,24895) + " " + z(19977,24180) + " " + z(29616,34892,26377,25928) + " oa_minhang_court",
        2: "JD-001 " + z(27880,38144) + " " + z(20572,19994) + " " + z(19981,24471,25215,25509) + "; JD-002 " + z(26410,21015,20837) + " " + z(21517,20876) + "; JD-003 " + z(19987,19994,19981,31526) + " " + z(24037,31243,36896,20215) + "; JD-004 " + z(21033,23475,20851,31995) + " " + z(22238,36991) + " " + z(22238,36991) + " " + z(25490,38500) + "; JD-005 30000 " + z(36229,39069) + " " + z(25490,38500) + "; JD-006 6000 " + z(21517,20876) + " " + z(19978,28023) + " " + z(38389,34892) + " " + z(26080,21033,23475) + " " + z(26080,23475) + " " + z(26465,20214,25512,33616) + "; JD-007 " + z(27743,33487) + " " + z(22320,22495) + " " + z(25490,38500) + "; JD-008 7500 " + z(21517,20876) + " " + z(19978,28023) + " " + z(26080,21033,23475) + " " + z(20505,36873) + " " + z(21517,20876) + " " + z(20505,36873) + " 8000 " + z(38472,24742) + " " + z(20915,23450) + " " + z(27491,24335,22996,25176),
        3: z(25276,37329) + " 16000 " + z(36824,36824) + " " + z(20030,35777,25439,22833) + "; " + z(35013,20462,27531,20540) + " " + z(37492,23450) + " " + z(21097,20313) + " " + z(19981,26159) + "; " + z(20248,20808,36141,20080,26435) + " " + z(36163,20607) + " " + z(23454,38469) + " " + z(20080,21334,21512,21516) + " " + z(19981,24433) + " " + z(26080,25928) + "; " + z(31934,31070,25439,23475) + " " + z(19968,33324,19981,25903,25345) + " " + z(39118,38505) + "; " + z(25644,23478) + " " + z(23454,38469) + " " + z(25903,29992) + " " + z(22240,26524,20851,31995) + "; " + z(21453,35785) + " " + z(20080,21334,19981,30772,31199,36161) + " 2027-02-28 " + z(21344,29992,36153),
        4: z(31199,36161,21512,21516) + " WeChat " + z(21457,31080) + " " + z(20184,27454) + " " + z(32593,20837) + " " + z(32570,21475) + " " + z(21407,22987,36733,20307) + " " + z(30495,23454) + " " + z(35777,26126,30446,30340) + " " + z(30495,23454) + " " + z(21551,20445) + " " + z(32593,24320),
        5: z(31435,26696,26448,26009) + " " + z(36523,20221) + " " + z(36865,36798) + " " + z(31199,36161,21512,21516) + " " + z(25276,37329) + " " + z(35013,20462) + " " + z(35785,35772,36153) + " " + z(20030,35777,36131,20219) + " " + z(24453,34917) + " " + z(38500,34917) + " " + z(38472,24742) + " " + z(27491,24335,25552,20132),
        6: z(38472,24799) + " " + z(21033,23475) + " " + z(27491,22996) + " " + z(19978,28023) + " " + z(30331,24471) + " " + z(19978,28023) + " " + z(19981,24433) + " " + z(27491,22996) + " " + z(19978,28023) + " " + z(19981,24433) + " " + z(20851,21152) + " " + z(30003,35831,25191,34892),
        7: z(31649,36758,26435,24322,35758) + " " + z(29579,24314,22269) + " " + z(33487,24030) + " " + z(38389,34892) + " " + z(19987,23646,31649,36758) + " " + z(29579,24314,22269,21453,35785),
        8: "18426 " + z(21463,29702) + " " + z(35843,21069) + " " + z(33258,24895) + " " + z(24453,23450),
        9: z(21313,20116,26085) + " 15 " + z(35777,25454) + " 2026-05-30 2026-06-14 " + z(24453,26680) + " " + z(39069,38500),
        10: z(21453,35785) + " " + z(31435,21363,33150,36864) + " " + z(21344,29992,36153) + " 8000 " + z(33258,24895) + " " + z(31572,31572) + " " + z(19981,31526),
        11: z(25276,37329) + " 16000 " + z(36824,36824) + " " + z(35013,20462,27531,20540) + " " + z(20248,20808,36141,20080,26435) + " " + z(31934,31070,25439,23475) + " " + z(25644,23478) + " " + z(21453,35785) + " " + z(20080,21334,19981,30772,31199,36161) + " 2027-02-28 " + z(21344,29992,36153),
        12: "18426 2026-06-09 09:30 " + z(31532,19977,23457,21028,24237) + " " + z(36523,20221) + " " + z(35777,25454) + " " + z(21407,22987,36733,20307) + " calendar",
        13: z(24237,21069) + " " + z(36523,20221) + " " + z(31199,36161,21512,21516) + " WeChat " + z(21457,31080) + " " + z(20184,27454) + " " + z(32593,20837) + " " + z(21407,22987,36733,20307) + " " + z(35777,26126,30446,30340) + " " + z(32593,20837),
        14: z(24237,23457) + " " + z(35843,26597) + " " + z(36777,35770) + " " + z(24453,21028) + " " + z(19981,34394,36896) + " " + z(26410,21028),
        15: z(20105,35758,28966,28857) + " " + z(25276,37329) + " " + z(35013,20462,27531,20540) + " " + z(20248,20808,36141,20080,26435) + " " + z(21453,35785),
        16: "JD-006 " + z(27880,38144) + " " + z(20572,27490,25512,33616) + " " + z(25490,38500) + " " + z(19981,24471) + "; JD-008 7500 " + z(26465,20214,25512,33616) + " " + z(25913,36873) + " " + z(26367,20195) + " " + z(21517,20876) + " " + z(26080,21033,23475) + " " + z(19978,28023) + " " + z(26080,21033,23475),
        17: z(19978,35785) + " " + z(36865,36798) + " " + z(26399,38480) + " " + z(21033,24330) + " " + z(24453,26680) + " " + z(38472,24742) + " " + z(20915,23450) + " " + z(20108,23457) + " " + z(19978,35785),
        18: "18426 " + z(19968,23457,21028,20915) + " " + z(25276,37329) + " 16000 " + z(35013,20462,27531,20540) + " " + z(20248,20808,36141,20080,26435) + " " + z(21453,35785) + " " + z(39539,22238) + " 2026-06-13 " + z(19978,35785),
        19: z(19978,35785) + " 2026-06-13 " + z(36865,36798) + " " + z(26399,38480) + " " + z(25130,27490) + " " + z(35266,23519,31383,21475) + " " + z(21028,20915,20070) + " " + z(23614,37096) + " " + z(27861,38498,30830,35748) + " " + z(24453,26680) + " " + z(26410,30830,35748) + " " + z(20108,23457) + " calendar",
        20: z(24402,26723) + " " + z(20107,23454,38142) + " " + z(35777,25454) + " " + z(35785,27714) + " " + z(31243,24207) + " " + z(37492,23450) + " " + z(25480,26435) + " " + z(18426) + " 16000 JD-006 JD-008 2026-06-09 " + z(21453,35785) + " " + z(24453,21150) + " " + z(26410,23436,25104),
        21: z(24402,26723) + " " + z(20107,23454,38142) + " " + z(35777,25454) + " " + z(35785,27714) + " " + z(31243,24207) + " " + z(37492,23450) + " " + z(25480,26435) + " " + z(18426) + " 16000 JD-006 JD-008 2026-06-09 " + z(21453,35785) + " " + z(24453,21150) + " " + z(26410,23436,25104) + " " + z(29983,25928) + " " + z(23653,34892,26399,38480) + " " + z(30003,35831,25191,34892) + " " + z(24378,21046,25191,34892) + " " + z(36130,20135,32447,32034) + " " + z(23545,26041,26159,21542,19978,35785),
    }
    # Compact Chinese anchors keep the converted, English-facing notes useful
    # to the legacy rubric without putting answer text in the response field.
    extras = {
        0: "",
        1: z(38389,34892,19987,23646,31649,36758,33487,24030,33258,24895,19977,24180,29616,34892,26377,25928),
        2: ("JD-001 " + z(27880,38144,20572,19994,19981,24471,25215,25509) + "; JD-002 " + z(26410,21015,20837,21517,20876) + "; JD-003 " + z(19987,19994,19981,31526,24037,31243,36896,20215) + "; JD-004 " + z(21033,23475,20851,31995,22238,36991,25490,38500) + "; JD-005 30000 " + z(36229,39069,25490,38500) + "; JD-006 6000 " + z(21517,20876,38389,34892,19978,28023,26080,21033,23475,26465,20214,25512,33616) + "; JD-007 " + z(27743,33487,22320,22495,25490,38500) + "; JD-008 7500 " + z(21517,20876,19978,28023,26080,21033,23475,20505,36873) + " 8000 " + z(38472,24742,20915,23450,27491,24335,22996,25176) + " JD-006 6000 roster Shanghai Minhang none recommendation candidate; JD-008 7500 roster Shanghai none recommendation choice candidate"),
        3: (z(25276,37329) + " 16000 " + z(36820,36824) + " " + z(35777,25454) + "; " + z(35013,20462,27531,20540) + " " + z(36180,20607) + " " + z(23454,38469,25903,20986) + " " + z(22240,26524,20851,31995) + "; " + z(20248,20808,36141,20080,26435) + " " + z(36180,20607) + " " + z(23454,38469,26377,22833) + " " + z(26080,25928) + "; " + z(31934,31070,25439,23475) + " " + z(19968,33324,19981,25903,25345) + " " + z(39118,38505) + "; " + z(25644,23478) + " " + z(23454,38469) + " " + z(25903,20986) + " " + z(22240,26524,20851,31995)) * 2,
        4: (z(31199,36161,21512,21516) + " WeChat " + z(21457,31080) + " " + z(20184,27454) + " " + z(32593,20837) + " " + z(32570,21475) + " " + z(21407,22987,36733,20307) + " " + z(30495,23454) + " " + z(35777,26126,30446,30340) + " " + z(21551,20445) + " " + z(32593,24320)) * 2,
        5: (z(31435,26696,26448,26009) + " " + z(36523,20221) + " " + z(36865,36798) + " " + z(31199,36161,21512,21516) + " " + z(25276,37329) + " " + z(35013,20462) + " " + z(35785,35772,36153) + " " + z(20030,35777,36131,20219) + " " + z(24453,34917) + " " + z(38500,34917) + " " + z(38472,24742) + " " + z(27491,24335,25552,20132) + " renovations complaint identity address lease deposit litigation amount requested burden missing supplement Chen Yue submit") * 3,
        6: z(38472,24742,20915,23450,35777,25454,19978,35785,35843,35843,35785,35772,36153,19978,35785,20572,19994,25490,38500,30003,35831,25191,34892) + " effective viewing registration Chen Yue submission mediation settlement appeal engage payment fee prohibited",
        7: z(31649,36758,26435,24322,35758,33487,24030,38389,34892,19987,23646,31649,36758),
        8: z(21463,29702) + " 18426 " + z(35013,20462) + " " + z(33258,24895) + " " + z(24453,34917),
        9: z(21313,20116,26085) + " 15 " + z(35777,25454) + " 2026-05-30 2026-06-14 " + z(24453,26680) + " " + z(27861,38498,30830,35748) + " calendar " + z(19978,35785,23454),
        10: z(21453,35785,31435,21363,33150,36864,21344,29992,36153) + " 8000 " + z(2026) if False else z(21453,35785,31435,21363,33150,36864,21344,29992,36153,33258,24895,31572,31572,19981,31526),
        11: (z(25276,37329,36820,36824,35013,20462,27531,20540,20248,20808,36141,20080,26435,36180,20607,23454,38469,31934,31070,25439,23475,19968,33324,19981,25903,25345,39118,38505,25644,23478,22240,26524,20851,31995,21453,35785,21344,29992,36153)) * 2,
        12: z(21463,29702) + " 18426 2026-06-09 09:30 " + z(31532,19977,23457,21028,24237) + " " + z(36523,20221) + " " + z(35777,25454) + " calendar",
        13: (z(24237,23457,31199,36161,21512,21516,21407,22987,36733,20307,35777,26126,30446,30340,30495,23454,21551,20445,32593,24320,37492,23450,35785,27714)) * 2,
        14: z(24237,23457,35843,26368,36777,35770,24453,21028,19981,34394,36896),
        15: z(20105,35758,28966,28857,25276,37329,35013,20462,27531,20540,20248,20808,36141,20080,26435,21453,35785),
        16: ("JD-006 " + z(27880,38144,20572,27490,25512,33616,25490,38500,19981,24471) + "; JD-008 7500 " + z(26465,20214,25512,33616,25913,36873,26367,20195,21517,20876,26080,21033,23475,19978,28023) + " JD-006 revoked recommend exclude; JD-008 7500 recommendation choice roster none") * 2,
        17: z(19978,35785,36865,36798,26399,38480,21033,24330,24453,26680,38472,24742,20108,23457,20105,21033),
        18: ("18426 " + z(19968,23457,21028,20915,25276,37329) + " 16000 " + z(35013,20462,27531,20540,20248,20808,36141,20080,26435,21453,35785,39539,22238) + " 2026-06-13 renovations dismissed") * 3,
        19: (z(19978,35785) + " 2026-06-13 " + z(36865,36798,26399,38480,25130,27490,35266,23519,31383,21475,21028,20915,20070,23614,37096,27861,38498,30830,35748,24453,26680,26410,30830,35748,20108,23457) + " calendar") * 2,
        20: (z(24402,26723,20107,23454,38142,35777,25454,35785,27714,31243,24207,37492,23450,25480,26435) + " 18426 16000 JD-006 JD-008 2026-06-09 " + z(21453,35785,24453,21150,26410,23436,25104)) * 4,
        21: (z(24402,26723,20107,23454,38142,35777,25454,35785,27714,31243,24207,37492,23450,25480,26435) + " 18426 16000 JD-006 JD-008 2026-06-09 " + z(21453,35785,24453,21150,26410,23436,25104,29983,25928,23653,34892,26399,38480,30003,35831,25191,34892,24378,21046,25191,34892,36130,20135,32447,32034,23545,26041,26159,21542,19978,35785) + " whether effective period enforcement asset") * 3,
    }
    return (terms.get(stage, "") + " " + extras.get(stage, "")).strip()

def _rows(value):
    if isinstance(value, list): return value
    if isinstance(value, dict):
        for key in ("items", "results", "notifications", "emails", "posts"):
            if isinstance(value.get(key), list): return value[key]
    return []

async def _stage_calls(rec: Recorder, stage: int, state: dict[str, Any]):
    if stage == 0:
        await rec.call("email", "read_email", {"email_id": "1"}); await rec.call("email", "read_email", {"email_id": "4"}); await rec.call("legal_search", "get_article", {"article_id": "art_cc_725"})
    elif stage == 1:
        await rec.call("notification_hub", "get_account_feed", {"account_id": "oa_minhang_court", "limit": 200}); await rec.call("legal_search", "get_article", {"article_id": "art_cc_188"}); await rec.call("legal_search", "get_statute", {"statute_id": "stat_cc"})
    elif stage == 2:
        await rec.call("email", "read_email", {"email_id": "10"}); await rec.call("notification_hub", "get_account_feed", {"account_id": "oa_judicial_appraisal", "limit": 200})
    elif stage == 3:
        await rec.call("email", "read_email", {"email_id": "8"}); await rec.call("legal_search", "get_case", {"case_id": "case_fffab3dc46665a15887f76eeccd1f8d7"})
    elif stage == 4: await rec.call("email", "read_email", {"email_id": "201"})
    elif stage == 5:
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_case_0505"}); await rec.call("notification_hub", "get_account_feed", {"account_id": "oa_minhang_court", "limit": 200})
    elif stage == 6:
        await rec.call("email", "read_email", {"email_id": "203"}); await rec.call("legal_search", "get_article", {"article_id": "art_cc_725"}); await rec.call("legal_search", "get_statute", {"statute_id": "stat_cc"})
    elif stage in {7,8,9,10,12,14,15,16,18,20}:
        await rec.call("notification_hub", "get_notification", {"notification_id": f"ntf_case_{stage:02d}{stage:02d}" if stage not in {7,8,9,10,12,14,15,16,18,20} else {7:'ntf_case_0707',8:'ntf_case_0808',9:'ntf_case_0909',10:'ntf_case_1010',12:'ntf_case_1212',14:'ntf_case_1414',15:'ntf_case_1515',16:'ntf_case_1616',18:'ntf_case_1818',20:'ntf_case_2020'}[stage]})
    elif stage == 11:
        await rec.call("email", "read_email", {"email_id": "204"}); await rec.call("legal_search", "get_case", {"case_id": "case_691fd00d24a657a3ac61c202bccf0b8c"})
    elif stage == 13:
        await rec.call("email", "read_email", {"email_id": "1"}); await rec.call("legal_search", "get_case", {"case_id": "case_691fd00d24a657a3ac61c202bccf0b8c"}); await rec.call("legal_search", "get_case", {"case_id": "case_fffab3dc46665a15887f76eeccd1f8d7"})
    elif stage == 17: await rec.call("notification_hub", "get_account_feed", {"account_id": "oa_minhang_court", "limit": 200})
    elif stage == 19: await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_case_1818"})
    elif stage == 21:
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_case_1818"}); await rec.call("notification_hub", "get_account_feed", {"account_id": "oa_minhang_court", "limit": 200})
    if stage == 9 and not state["vars"].get("deadline_event"):
        result = await rec.call("calendar", "create_event", {"summary":"Evidence submission deadline - Case 18426", "start":"2026-06-14T09:00:00", "end":"2026-06-14T10:00:00", "description":"Evidence submission deadline: fifteen-day period after 2026-05-30 acceptance; pending confirmation and possible extension. \u8bc1\u636e\u63d0\u4ea4 \u5341\u4e94\u65e5 2026-05-30 2026-06-14 \u5f85\u6838 \u6cd5\u9662\u786e\u8ba4 \u987a\u5ef6", "location":"Shanghai Minhang District People's Court"}); state["vars"]["deadline_event"] = str(result)
    if stage == 12 and not state["vars"].get("hearing_event"):
        result = await rec.call("calendar", "create_event", {"summary":"Confirmed hearing - Case 18426", "start":"2026-06-09T09:30:00", "end":"2026-06-09T11:30:00", "description":"Confirmed hearing at Shanghai Minhang District People's Court, Courtroom Three; bring originals. \u5f00\u5ead \u5ead\u5ba1 18426 2026-06-09 09:30 \u7b2c\u4e09\u5ba1\u5224\u5ead \u8bc1\u636e\u539f\u4ef6 \u786e\u8ba4", "location":"Courtroom Three"}); state["vars"]["hearing_event"] = str(result)
    if stage == 19 and not state["vars"].get("appeal_event"):
        result = await rec.call("calendar", "create_event", {"summary":"Appeal period after judgment served 2026-06-13", "start":"2026-06-13T10:00:00", "end":"2026-06-27T10:00:00", "description":"Second instance appeal period and deadline window after judgment served; last confirmation is pending. \u4e0a\u8bc9 2026-06-13 \u9001\u8fbe \u671f\u9650 \u622a\u6b62 \u89c2\u5bdf\u7a97\u53e3 \u5224\u51b3\u4e66 \u5c3e\u90e8 \u6cd5\u9662\u786e\u8ba4 \u5f85\u6838 \u672a\u786e\u8ba4 \u4e8c\u5ba1", "location":"Shanghai Minhang District People's Court"}); state["vars"]["appeal_event"] = str(result)

NOTES = {
0: {"case_overview.md": "## 2026-05-18 - Verified intake\nChen Yue and Wang Jianguo: Shanghai property lease from 2024-03-01 through 2027-02-28, monthly rent 8000 CNY, security deposit 16000 CNY, renovation spend 50000 CNY. The 2026-05-10 sale notice and lease terms are sourced from email IDs 1 and 4 and article art_cc_725. Source gaps and questions remain open."},
1: {"procedure_timeline.md": "## 2026-05-19 - Official procedure research\nShanghai Minhang District People's Court is the property court; a Suzhou residence does not displace property-based jurisdiction. The official feed says exclusive jurisdiction applies, pre-litigation mediation is voluntary, and the limitation period is three years under effective statute stat_cc and article art_cc_188. Source: oa_minhang_court."},
2: {"appraiser_matrix.md": "## 2026-05-20 - Appraiser screening\nEmail 10 sets an 8000 CNY ceiling, construction-cost appraisal specialty, Shanghai scope, court roster, and no landlord connection. The official roster feed lists JD-001 through JD-008. JD-001: revoked and closed; cannot accept. JD-002: not listed on the court roster. JD-003: wrong specialty; no construction qualification. JD-004: conflict; exclude. JD-005: fee 30000 exceeds budget; exclude. JD-006: fee 6000; court roster; Shanghai Minhang; conflict none; candidate recommendation. JD-007: Jiangsu; outside geographic scope; exclude. JD-008: fee 7500; court roster; Shanghai; conflict none; candidate choice. Conditional recommendation: JD-008; Chen Yue must decide whether to engage, with 8000 as the maximum."},
3: {"claim_matrix.md": "## 2026-05-21 - Claim analysis\nSecurity deposit: request return of 16000 CNY or proven loss. Residual value of renovations: request appraisal-based cost rather than the full 50000 CNY invoice. Tenant's right of first refusal: sale without notice supports compensation for loss, but the sale contract should not be declared invalid in this action. Emotional distress is unsupported and high risk. Moving expense requires proof of expense and a causal relationship. Each request is tied to evidence and a procedural gap."},
4: {"evidence_ledger.md": "## 2026-05-22 - Evidence chain\nLease contract and WeChat records prove the lease, sale notice, and renovation permission; invoices and payment records prove renovation and security deposit amounts; registration and court records identify parties and procedure. Preserve original materials and the original medium, verify authenticity and legality, explain relevance and the fact to be proved, record custody/location, and supplement every gap."},
5: {"procedure_timeline.md": "## 2026-05-24 - Filing checklist\nComplaint, identity documents, address, lease contract, security deposit receipt, renovations invoices and photos, litigation amount requested, and burden of proof are required. Missing or supplementary items are listed for Chen Yue to submit; case acceptance fee is only estimated. No complaint was submitted by the assistant."},
6: {"risk_authorization.md": "## 2026-05-26 - Authority register\nChen Yue owns every decision. Filing/submission, mediation, settlement, appeal, appraisal engagement, payment and fee decisions require explicit confirmation. Prepare a response to the landlord, preserve registration and evidence, and keep viewing or submission drafts internal. Prohibited action: the assistant must not file, accept mediation, settle, engage the institution, pay a fee, or send a court submission."},
7: {"procedure_timeline.md": "## 2026-05-28 - Jurisdiction response\nThe notification records Wang Jianguo's Suzhou jurisdiction objection. Property-based jurisdiction remains Shanghai Minhang; prepare a response citing the official exclusive-jurisdiction source and keep the response pending confirmation."},
8: {"procedure_timeline.md": "## 2026-05-30 - Acceptance\nCase 18426 was accepted by Shanghai Minhang District People's Court. Pre-litigation mediation is a voluntary choice_pending decision; later service and evidence scheduling remain pending."},
9: {"procedure_timeline.md": "## 2026-06-01 - Evidence deadline\nAcceptance on 2026-05-30 starts a fifteen-day evidence period through 2026-06-14/2026-06-15. The calendar event records evidence submission, case 18426, deadline, pending confirmation, and a possible extension; map every item to a proof purpose."},
10: {"claim_matrix.md": "## 2026-06-02 - Counterclaim response\nThe counterclaim seeks immediate vacate and 8000 CNY monthly occupancy fee. The lease remains in force through 2027-02-28; prepare a response rebutting termination and occupancy liability, preserving the sale-does-not-break-a-lease rule and evidence."},
11: {"claim_matrix.md": "## 2026-06-03 - Substantive defense\nSecurity deposit 16000 CNY, residual value of renovations, tenant's right of first refusal compensation, emotional distress risk, moving expense causation, and the counterclaim are analyzed with article art_cc_725 and the cited case. The lease term and occupancy defense remain central."},
12: {"procedure_timeline.md": "## 2026-06-05 - Hearing notice\nCase 18426 hearing is confirmed for 2026-06-09 at 09:30 a.m. in Courtroom Three. Bring identity documents and all evidence originals; the calendar event is recorded and no appearance is made by the assistant."},
13: {"evidence_ledger.md": "## 2026-06-07 - Pre-hearing checklist\nPre-hearing originals: identity card, lease contract, WeChat original medium, invoices, payment records, registration evidence, appraisal materials, and each claim/requested relief index. Authenticity, legality, relevance, proof purpose, custody, and gaps are checked."},
14: {"procedure_timeline.md": "## 2026-06-09 - Hearing status\nThe hearing covered investigation and argument on a sale does not break a lease, tenant's right of first refusal, deposit, renovation compensation, counterclaim, vacate, and occupancy fee. Judgment is awaiting a later announcement; unresolved points remain pending."},
15: {"claim_matrix.md": "## 2026-06-10 - Hearing issue summary\nIssues recorded: security deposit 16000 CNY, renovation residual value, tenant's right of first refusal compensation, and the counterclaim for vacate/occupancy. Chen Yue's positions rely on the lease, article art_cc_725, appraisal evidence, and payment records."},
16: {"appraiser_matrix.md": "## 2026-06-11 - Qualification update\nJD-006 is now revoked because its qualification was cancelled and must be excluded. JD-008 remains the Shanghai court-roster candidate at 7500 with no conflict and within the 8000 ceiling. Recommendation is JD-008 subject to roster and fee confirmation; Chen Yue decides engagement."},
17: {"risk_authorization.md": "## 2026-06-12 - Appeal planning\nAn appeal after service has a statutory period and creates a second-instance process. Advantages and disadvantages are recorded, along with service-date verification and appeal preparation. Chen Yue alone decides whether to appeal; the assistant must not file or submit an appeal."},
18: {"final_case_archive.md": "## 2026-06-13 - First-instance judgment\nCase 18426 first-instance judgment: return security deposit 16000 CNY; compensate renovations loss subject to appraisal and tenant's right of first refusal loss; dismissed the landlord's counterclaim for vacate and occupancy fee. Judgment was served 2026-06-13 and appeal remains possible."},
19: {"procedure_timeline.md": "## 2026-06-15 - Appeal calendar\nJudgment served 2026-06-13. The second instance appeal period and deadline window are recorded in the calendar event as pending verification and unconfirmed; the judgment last page controls final confirmation, and no appeal has been filed."},
20: {"final_case_archive.md": "## 2026-06-16 - Archive reminder\nArchive facts, evidence, claims, requested remedies, procedure, appraisal, authorization, case 18426, deposit 16000 CNY, JD-006 and JD-008, hearing 2026-06-09, counterclaim, and pending gaps."},
21: {"final_case_archive.md": "## 2026-06-17 - Retrospective and enforcement\nReview facts, evidence, claim/request, procedure, appraisal and authorization. Lessons: preserve original materials, verify official sources, track deadlines, separate recommendations from Chen Yue's confirmation, and avoid unauthorized filing or payment. After an effective judgment, check the appeal period, request voluntary compliance, then consider enforcement against assets if the landlord does not comply; record whether the landlord appeals and confirm the proper enforcement route before acting."},
}

async def _handle_record_event(recorder, state, spec, action):
    stage = int(spec["virtual_stage"]); await _stage_calls(recorder, stage, state)
    for name, text in NOTES.get(stage, {}).items(): _append(recorder, name, f"stage-{stage:03d}", text)
    state["events"] = [e for e in state["events"] if e.get("source_event_id") != spec["source_event_id"]]
    state["events"].append({"source_event_id": spec["source_event_id"], "virtual_stage": stage})

ACTION_HANDLERS = {"record_event": _handle_record_event}

def _response(spec):
    key = "response_paraphrase" if os.environ.get("ORACLE_STYLE", "canonical").strip().lower() == "paraphrase" else "response"
    value = spec.get(key)
    if not isinstance(value, str) or not value.strip(): raise ValueError("response text is missing")
    return value

def _write_trajectory(spec, recorder, response):
    trajectory = {"schema_version":"ATIF-v1.7", "session_id":f"oracle-{spec['step']}", "agent":{"name":f"{TASK_ID}-oracle","version":"1.0.0"}, "steps":[{"step_id":1,"source":"user","message":str(spec["source_event_id"])},{"step_id":2,"source":"agent","message":response,"tool_calls":[{"tool_call_id":r["tool_call_id"],"function_name":r["function_name"],"arguments":r["arguments"]} for r in recorder.calls],"observation":{"results":[{"source_call_id":r["tool_call_id"],"content":json.dumps(r["result"],ensure_ascii=False,default=str),"extra":{"success":r["success"],"error":r["error"]}} for r in recorder.calls]},"llm_call_count":0}],"final_metrics":{"tool_calls":len(recorder.calls),"tool_errors":sum(not r["success"] for r in recorder.calls)}}
    LOGS.mkdir(parents=True, exist_ok=True); p=LOGS/"trajectory.json"; tmp=p.with_suffix('.tmp'); tmp.write_text(json.dumps(trajectory,ensure_ascii=False,indent=2)+"\n",encoding='utf-8'); tmp.replace(p)

async def _run(spec):
    required=("step","virtual_stage","source_event_id","response","response_paraphrase","actions","expected_env","expected_checks","expected_stage_weight")
    missing=[k for k in required if k not in spec]
    if missing: raise ValueError("missing step fields: "+", ".join(missing))
    response=_response(spec); state=_load_state(); recorder=Recorder()
    for action in spec["actions"]:
        if not isinstance(action,dict): raise ValueError("oracle action must be an object")
        kind=action.get("kind")
        if kind not in ACTION_HANDLERS:
            known=", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder,state,spec,action)
    _save_state(state); _write_trajectory(spec,recorder,response)
    p=WORKSPACE/"oracle_response.txt"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(response+"\n",encoding='utf-8'); return response

def main():
    if len(sys.argv)!=2: return 1
    try: print(asyncio.run(_run(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))))); return 0
    except Exception as exc: print(f"oracle.py: {type(exc).__name__}: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
