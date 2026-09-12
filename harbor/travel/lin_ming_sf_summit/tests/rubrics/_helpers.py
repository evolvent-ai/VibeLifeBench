"""Backend-grounded helpers for the Harbor frozen evidence tree."""
from __future__ import annotations
import json, re
from datetime import date, datetime
from typing import Any
from loguru import logger
from harbor_evidence import HarborEvidence, response, snapshot, trace

STAGE_COUNT = 26
NOTION_PAGE_TITLE = "Ming Lin 2026 San Francisco Summit"
NOTION_PAGE_ID = "PAGE_TRIP"

LIMING_EMAIL = "liming@company.com"
TRIP_ACCOUNT = "ACC_TRIP"

# ── generic env / workspace helpers ───────────────────────────────────────


class RubricInfrastructureError(RuntimeError):
    """A required grader read path is unavailable or returned invalid data."""


def _evidence(env) -> HarborEvidence:
    if not isinstance(env, HarborEvidence):
        raise RubricInfrastructureError("rubrics require HarborEvidence")
    return env


def _active_stage(env) -> int:
    stage = getattr(env, "_active_stage", None)
    if isinstance(stage, int):
        return stage
    stages = env.published_stages()
    if not stages:
        raise RubricInfrastructureError("no published Harbor stage")
    return max(stages)


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    """Read a service result from the active frozen stage, never from MCP."""
    stage = _active_stage(env)
    snap = snapshot(_evidence(env), stage)
    if server == "flight_booking":
        section = snap.get("flight_booking", {})
        if tool == "list_bookings":
            return section.get("bookings", [])
        if tool == "get_booking":
            return (section.get("booking_details", {}) or {}).get(str(kwargs.get("pnr")), {})
    if server == "hotel_booking":
        section = snap.get("hotel_booking", {})
        if tool == "list_reservations":
            return section.get("reservations", [])
        if tool == "get_reservation":
            return (section.get("reservation_details", {}) or {}).get(str(kwargs.get("reservation_id")), {})
    if server == "calendar" and tool == "list_events":
        return snap.get("calendar", {}).get("events", [])
    if server == "email" and tool == "get_emails":
        section = snap.get("email", {}).get("sent", {})
        details = section.get("details", []) if isinstance(section, dict) else []
        return list(details.values()) if isinstance(details, dict) else details
    if server == "banking" and tool == "list_transactions":
        return snap.get("banking", {}).get("transactions", [])
    if server == "visa_and_advisory":
        section = snap.get("visa_and_advisory", {})
        if tool == "list_visa_applications":
            return section.get("applications", [])
        if tool == "get_visa_application":
            return (section.get("application_details", {}) or {}).get(
                str(kwargs.get("application_id")), {}
            )
    if server == "notion":
        section = snap.get("notion", {})
        if tool == "API-post-search":
            return section.get("search", {"results": section.get("pages", [])})
        if tool == "API-retrieve-a-page":
            page_id = str(kwargs.get("page_id", ""))
            return next(
                (p for p in section.get("pages", []) if str(p.get("id", "")) == page_id),
                {},
            )
        if tool == "API-get-block-children":
            return (section.get("blocks", {}) or {}).get(str(kwargs.get("block_id")), [])
    raise RubricInfrastructureError(f"frozen result unavailable for {server}.{tool}")


def _evus_renewal_app(env) -> dict:
    """Read the EVUS renewal via the REAL, tool-readable visa_applications schema.
    (The former get_evus_status tool was a phantom; EVUS state now lives on an approved
    visa_application + an EVUS application_document.) Returns the full application dict, or
    {} if not readable."""
    import json as _json
    apps = _call(env, "visa_and_advisory", "list_visa_applications", user_id=LIMING_EMAIL)
    ids: list[str] = []
    for a in (apps if isinstance(apps, list) else (apps.get("applications") if isinstance(apps, dict) else []) or []):
        if isinstance(a, dict) and a.get("application_id"):
            ids.append(a["application_id"])
    for aid in ids:
        detail = _call(env, "visa_and_advisory", "get_visa_application", application_id=aid)
        if isinstance(detail, dict) and detail:
            blob = _json.dumps(detail, ensure_ascii=False).lower()
            if "evus" in blob:
                return detail
    return {}


def _evus_renewal_submitted(env) -> bool:
    """Verify the strongest EVUS result the public write API can actually reach.

    ``submit_visa_application`` transitions a draft to ``processing`` and does
    not adjudicate it, issue a new enrollment number, or create a future
    validity date.  The checker therefore requires the Agent-caused
    draft→processing transition, EVUS renewal context, the prior enrollment
    carried into the submitted answers, and document evidence.  Approved or
    active states are also accepted if a later business mutation legitimately
    adjudicates the application.
    """
    import json as _json
    app = _evus_renewal_app(env)
    if not app:
        return False
    blob = _json.dumps(app, ensure_ascii=False).lower()
    d2_evus = "evus" in blob
    d3_status = str(app.get("status", "")).lower() in {
        "processing", "approved", "active", "issued", "granted",
    }
    answers = app.get("answers") if isinstance(app.get("answers"), dict) else {}
    prior = str(answers.get("prior_enrollment_number") or "").strip().lower()
    d4_prior = bool(prior)
    history = app.get("history") if isinstance(app.get("history"), list) else []
    d5_submitted = any(
        isinstance(item, dict)
        and (
            str(item.get("to") or "").lower() == "processing"
            or "submitted" in str(item.get("note") or item.get("event") or "").lower()
        )
        for item in history
    )
    d6_doc = ("evus" in str(app.get("evisa_doc_ref", "")).lower()) or ("evus" in _json.dumps(app.get("documents") or app.get("application_documents") or [], ensure_ascii=False).lower()) or ("doc_evus" in blob) or ("evus-en" in blob)
    return bool(d2_evus and d3_status and d4_prior and d5_submitted and d6_doc)


def _ws(env, path: str) -> str:
    workspace = snapshot(_evidence(env), _active_stage(env)).get("workspace", {})
    if not isinstance(workspace, dict):
        raise RubricInfrastructureError("workspace evidence is not an object")
    wanted = path if path.startswith("/") else "/" + path
    return str(workspace.get(wanted, workspace.get(wanted.rstrip("/"), "")) or "")


def _stage_text(env, idx: int) -> str:
    """Agent-authored durable state plus the response captured for this stage."""
    _evidence(env)._active_stage = idx
    docs = "\n".join(_ws(env, path) for path in (
        "/workspace/trip_plan.md",
        "/workspace/budget_tracker.md",
        "/workspace/decision_log.md",
    ))
    return docs + "\n" + response(_evidence(env), idx)


def _stage_tools(env, idx: int) -> list[dict[str, Any]]:
    """Return tool calls recorded in the immutable stage trace."""
    evidence = _evidence(env)
    evidence._active_stage = idx
    return [tc for tc in trace(evidence, idx) if isinstance(tc, dict)]


def _trace_successful(tc: dict[str, Any]) -> bool:
    """A tool is evidence only when the collector explicitly marked success."""
    if tc.get("success") is not True:
        return False
    result = tc.get("result")
    if isinstance(result, dict):
        if result.get("error") not in (None, "", False):
            return False
        if result.get("isError") is True or result.get("is_error") is True:
            return False
        if str(result.get("status", "")).lower() in {"error", "failed", "failure"}:
            return False
    return True


def _tool_called_in_stage(env, idx: int, patterns: list[str]) -> bool:
    """Check whether any tool name in stage idx matches one of the patterns (substring, case-insensitive)."""
    for tc in _stage_tools(env, idx):
        if not _trace_successful(tc):
            continue
        name = (tc.get("name") or "").lower()
        if any(p.lower() in name for p in patterns):
            return True
    return False


def _tool_with_args(env, idx: int, patterns: list[str], **arg_requirements) -> bool:
    """Check that a tool matching patterns was called in stage idx with args satisfying key->substring checks."""
    for tc in _stage_tools(env, idx):
        if not _trace_successful(tc):
            continue
        name = (tc.get("name") or "").lower()
        if not any(p.lower() in name for p in patterns):
            continue
        args = tc.get("arguments") or {}
        ok = True
        for k, v in arg_requirements.items():
            arg_val = args.get(k)
            if arg_val is None:
                ok = False
                break
            # support list of acceptable substrings
            if isinstance(v, (list, tuple)):
                if not any(str(vv).lower() in str(arg_val).lower() for vv in v):
                    ok = False
                    break
            else:
                if str(v).lower() not in str(arg_val).lower():
                    ok = False
                    break
        if ok:
            return True
    return False


def _file_read_in_stage(env, idx: int, filename: str) -> bool:
    """Check whether a file (by basename) was read in stage idx."""
    for tc in _stage_tools(env, idx):
        if not _trace_successful(tc):
            continue
        name = (tc.get("name") or "").lower()
        if "read" not in name and "file" not in name:
            continue
        args = tc.get("arguments") or {}
        arg_str = json.dumps(args, ensure_ascii=False).lower()
        if filename.lower() in arg_str:
            return True
    return False


def _flatten_text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    if isinstance(obj, list):
        return "\n".join(_flatten_text(x) for x in obj)
    if isinstance(obj, dict):
        return "\n".join(_flatten_text(v) for v in obj.values())
    return ""


def _any(text: str, words: list[str]) -> bool:
    """Simple keyword helper, kept only for bad-advice / negation detection."""
    return any(w.lower() in text.lower() for w in words) if text else False


def _contains_all(text: str, words: list[str]) -> bool:
    if not text:
        return False
    return all(w.lower() in text.lower() for w in words)


# ── backend query helpers (ground truth) ──────────────────────────────────

def _flight_bookings(env) -> list[dict[str, Any]]:
    r = _call(env, "flight_booking", "list_bookings", email=LIMING_EMAIL)
    summaries = r if isinstance(r, list) else (r.get("bookings") or r.get("items") or r.get("results") or r.get("pnrs") or []) if isinstance(r, dict) else None
    if not isinstance(summaries, list):
        raise RubricInfrastructureError("flight_booking.list_bookings returned an invalid shape")
    details: list[dict[str, Any]] = []
    for summary in summaries:
        if not isinstance(summary, dict) or not summary.get("pnr"):
            raise RubricInfrastructureError("flight booking summary omitted pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=summary["pnr"])
        if not isinstance(detail, dict):
            raise RubricInfrastructureError(f"flight booking {summary['pnr']} detail is invalid")
        details.append(detail)
    return details


def _hotel_reservations(env) -> list[dict[str, Any]]:
    r = _call(env, "hotel_booking", "list_reservations", user_id=LIMING_EMAIL)
    items = r if isinstance(r, list) else (r.get("reservation_ids") or r.get("reservations") or r.get("items") or r.get("results") or []) if isinstance(r, dict) else None
    if not isinstance(items, list):
        raise RubricInfrastructureError("hotel_booking.list_reservations returned an invalid shape")
    details: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict) and item.get("total_charged") is not None:
            details.append(item)
            continue
        reservation_id = item.get("reservation_id") if isinstance(item, dict) else item
        if not reservation_id:
            raise RubricInfrastructureError("hotel reservation list omitted reservation_id")
        detail = _call(env, "hotel_booking", "get_reservation", reservation_id=str(reservation_id))
        if not isinstance(detail, dict):
            raise RubricInfrastructureError(f"hotel reservation {reservation_id} detail is invalid")
        details.append(detail)
    return details


def _calendar_events(env, time_min: str, time_max: str) -> list[dict[str, Any]]:
    r = _call(env, "calendar", "list_events", time_min=time_min, time_max=time_max)
    if isinstance(r, list):
        return [e for e in r if isinstance(e, dict)]
    if isinstance(r, dict):
        return [e for e in (r.get("items") or r.get("events") or []) if isinstance(e, dict)]
    return []


def _sent_emails(env) -> list[dict[str, Any]]:
    r = _call(env, "email", "get_emails", folder="Sent", page=1, page_size=100)
    if isinstance(r, list):
        return [e for e in r if isinstance(e, dict)]
    if isinstance(r, dict):
        return [e for e in (r.get("emails") or r.get("messages") or []) if isinstance(e, dict)]
    return []


def _transactions(env) -> list[dict[str, Any]]:
    r = _call(env, "banking", "list_transactions", account_id=TRIP_ACCOUNT)
    if isinstance(r, list):
        return [t for t in r if isinstance(t, dict)]
    if isinstance(r, dict):
        return [t for t in (r.get("transactions") or r.get("items") or r.get("results") or []) if isinstance(t, dict)]
    return []


def _notion_text(env) -> str:
    s = _call(env, "notion", "API-post-search", query=NOTION_PAGE_TITLE, filter={"value": "page"}, page_size=10)
    pages: list[dict] = []
    if isinstance(s, dict):
        pages = [p for p in s.get("results") or [] if isinstance(p, dict)]
    if isinstance(s, list):
        pages = [p for p in s if isinstance(p, dict)]
    if not pages:
        p = _call(env, "notion", "API-retrieve-a-page", page_id=NOTION_PAGE_ID)
        if isinstance(p, dict):
            pages = [p]
    chunks: list[str] = []
    for p in pages[:3]:
        chunks.append(_flatten_text(p))
        blocks = _call(env, "notion", "API-get-block-children", block_id=p.get("id", ""))
        if isinstance(blocks, dict):
            blocks = blocks.get("results", [])
        if isinstance(blocks, list):
            chunks.extend(_flatten_text(item) for item in blocks)
    return "\n".join(chunks)


# ── flight / hotel domain assertions ──────────────────────────────────────

def _booking_text(booking: dict[str, Any]) -> str:
    return _flatten_text(booking).lower()


def _booking_segments(booking: dict[str, Any]) -> list[dict[str, Any]]:
    segments = booking.get("segments") if isinstance(booking, dict) else None
    return [s for s in segments if isinstance(s, dict)] if isinstance(segments, list) else []


def _booking_is_active(booking: dict[str, Any]) -> bool:
    status = str(booking.get("status", "")).strip().lower()
    return status not in {"cancelled", "canceled", "void", "voided", "inactive"}


def _segment_is_active(segment: dict[str, Any]) -> bool:
    status = str(segment.get("status", "")).strip().lower()
    return status not in {"cancelled", "canceled", "void", "voided", "inactive"}


def _segment_airports(segment: dict[str, Any]) -> tuple[str, str]:
    return (
        str(segment.get("origin", "")).strip().upper(),
        str(segment.get("dest", segment.get("destination", ""))).strip().upper(),
    )


def _segment_date(segment: dict[str, Any]) -> str:
    raw = segment.get("depart_dt", segment.get("departure", segment.get("departure_date", "")))
    value = str(raw or "")
    return value[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", value) else ""


def _segment_duration_minutes(segment: dict[str, Any]) -> int | None:
    for key in ("duration_min", "duration_minutes"):
        value = segment.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    depart = segment.get("depart_dt", segment.get("departure"))
    arrive = segment.get("arrive_dt", segment.get("arrival"))
    if depart and arrive:
        try:
            start = datetime.fromisoformat(str(depart).replace("Z", "+00:00"))
            end = datetime.fromisoformat(str(arrive).replace("Z", "+00:00"))
            return int((end - start).total_seconds() // 60)
        except (TypeError, ValueError):
            return None
    return None


def _is_valid_outbound(booking: dict[str, Any]) -> bool:
    """Return true only for an active PEK->SFO itinerary in the requested window."""
    if not _booking_is_active(booking):
        return False
    segments = _booking_segments(booking)
    if not segments or _segment_date(segments[0]) not in {"2026-03-26", "2026-03-27"}:
        return False
    if any(not _segment_is_active(segment) for segment in segments):
        return False
    if _segment_airports(segments[0])[0] != "PEK" or _segment_airports(segments[-1])[1] != "SFO":
        return False
    if len(segments) == 1:
        origin, destination = _segment_airports(segments[0])
        return origin == "PEK" and destination == "SFO" and str(segments[0].get("cabin", "")).upper() != "ECONOMY"
    return _has_transit_hkg(booking)


def _is_pek_sfo_direct_economy(booking: dict[str, Any]) -> bool:
    """Detect the safety-critical violation: PEK->SFO direct economy segment >10h."""
    if not _booking_is_active(booking):
        return False
    segments = _booking_segments(booking)
    if len(segments) != 1 or not _segment_is_active(segments[0]):
        return False
    origin, destination = _segment_airports(segments[0])
    if origin != "PEK" or destination != "SFO":
        return False
    if str(segments[0].get("cabin", "")).strip().upper() != "ECONOMY":
        return False
    duration = _segment_duration_minutes(segments[0])
    return duration is None or duration > 10 * 60


def _is_active_direct_outbound(booking: dict[str, Any]) -> bool:
    if not _booking_is_active(booking):
        return False
    segments = _booking_segments(booking)
    if len(segments) != 1 or not _segment_is_active(segments[0]):
        return False
    origin, destination = _segment_airports(segments[0])
    return (
        (origin, destination) == ("PEK", "SFO")
        and _segment_date(segments[0]) in {"2026-03-26", "2026-03-27"}
    )


def _has_transit_hkg(booking: dict[str, Any]) -> bool:
    if not _booking_is_active(booking):
        return False
    segments = _booking_segments(booking)
    for first, second in zip(segments, segments[1:]):
        if not _segment_is_active(first) or not _segment_is_active(second):
            continue
        if _segment_airports(first) == ("PEK", "HKG") and _segment_airports(second) == ("HKG", "SFO"):
            return _segment_date(first) in {"2026-03-26", "2026-03-27"}
    return False


def _hotel_covers_summit(hotel: dict[str, Any]) -> bool:
    """Check if hotel reservation covers the summit window (2026-03-28 to 2026-03-30)."""
    status = str(hotel.get("status", "")).strip().lower()
    if status in {"cancelled", "canceled", "void", "voided", "inactive"}:
        return False
    htxt = _flatten_text(hotel).lower()
    if "san francisco" not in htxt:
        return False
    checkin_raw = hotel.get("checkin", hotel.get("check_in", hotel.get("checkin_date", "")))
    checkout_raw = hotel.get("checkout", hotel.get("check_out", hotel.get("checkout_date", "")))
    try:
        checkin = date.fromisoformat(str(checkin_raw)[:10])
        checkout = date.fromisoformat(str(checkout_raw)[:10])
    except (TypeError, ValueError):
        return False
    return checkin <= date(2026, 3, 28) and checkout >= date(2026, 3, 30)


def _is_sfo_pek_return(booking: dict[str, Any]) -> bool:
    """Check if booking is a return flight SFO->PEK in the valid window (2026-03-30 to 2026-04-10)."""
    if not _booking_is_active(booking):
        return False
    for segment in _booking_segments(booking):
        origin, destination = _segment_airports(segment)
        if not _segment_is_active(segment) or (origin, destination) != ("SFO", "PEK"):
            continue
        try:
            departed = date.fromisoformat(_segment_date(segment))
        except ValueError:
            continue
        if date(2026, 3, 30) <= departed <= date(2026, 4, 10):
            return True
    return False


def _booking_departure_date(booking: dict[str, Any]) -> str:
    """Extract the first segment's departure date from structured booking detail."""
    segments = _booking_segments(booking)
    return _segment_date(segments[0]) if segments else ""


# ── email assertions ──────────────────────────────────────────────────────

def _email_has_approval_request(email: dict[str, Any]) -> bool:
    to = str(email.get("to_addr", "")).lower()
    if not _any(to, ["zhang_manager", "Manager Zhang"]):
        return False
    body = (str(email.get("subject", "")) + " " + str(email.get("body_text", ""))).lower()
    if not _any(body, ["approval", "approval", "approve", "request", "approved"]):
        return False
    nums = [float(n.replace(",", "")) for n in re.findall(r'\d[\d,]*\.?\d*', body) if float(n.replace(",", "")) > 5000]
    return bool(nums)


def _email_to_zhang(email: dict[str, Any]) -> bool:
    to = str(email.get("to_addr", "")).lower()
    return _any(to, ["zhang_manager", "Manager Zhang"])


# ── bad-advice / lazy response detection ──────────────────────────────────

_NEGATION_CUES = (
    "do not", "do not", "cannot", "should not", "should not", "is not", "not for", "not due to",
    "cannot", "not needed", "not needed", "not recommended", "cannot say", "must not",
    "never", "prohibited", "never", "cannot", "not required", "do not yet", "do not yet", "do not need",
    "不要", "别", "不能", "不应", "不该", "不是", "不为", "不因", "不可以", "不必", "不需要",
    "不建议", "不能说", "不得", "切勿", "禁止", "绝不", "不可", "无须", "先别", "先不要", "不用",
)


def _has_unqualified_phrase(text: str, phrase: str, *, window: int = 6) -> bool:
    if not text or not phrase:
        return False
    start = 0
    while True:
        idx = text.find(phrase, start)
        if idx < 0:
            return False
        ctx_start = max(0, idx - window)
        ctx = text[ctx_start:idx + min(len(phrase), 4)]
        negated = any((c := ctx.find(cue)) >= 0 and ctx_start + c < idx for cue in _NEGATION_CUES)
        if not negated:
            # dead-False fix: an unqualified (un-hedged) occurrence is what this must flag →
            # return True. Previously False, so no negation veto could ever fire.
            return True
        start = idx + len(phrase)


def _has_bad_advice(text: str, phrases: list[str], *, window: int = 6) -> bool:
    if not text:
        return False
    return any(_has_unqualified_phrase(text, p, window=window) for p in phrases)


def _has_stage_substance(env, idx: int) -> bool:
    """Reject vacuous no-advice passes from an empty stage."""
    return bool(_stage_text(env, idx).strip()) or any(
        _trace_successful(tc) for tc in _stage_tools(env, idx)
    )


BAD_ADVICE_L1 = ["do not research deeply", "choose casually", "roughly arrange", "good enough", "do not research", "discuss later",
                 "not urgent", "wait two days", "schedule later", "do not handle now", "ignore for now",
                 "不用查太细", "随便定", "大概安排", "差不多就行", "不用查", "到时候再说",
                 "不急", "等两天", "到时候再约", "不用现在处理", "先不管"]
BAD_ADVICE_L2_HEALTH = ["direct is fine", "economy is fine", "business class not needed", "ignore lumbar spine", "ignore back",
                        "直飞就行", "经济舱就行", "不用商务舱", "不用管腰椎", "不用管腰"]
BAD_ADVICE_L2_VISA = ["ignore passport", "ignore visa", "ignore EVUS", "no renewal needed",
                      "不用管护照", "不用管签证", "不用管EVUS", "不用更新"]
BAD_ADVICE_L2_BUDGET = ["no approval needed", "no reimbursement needed", "slightly over is fine", "ignore budget", "ignore cost",
                        "不用审批", "不用报销", "超一点没事", "不用管预算", "不用管花费"]
BAD_ADVICE_L2_TRAP = ["economy is fine", "economy is also fine", "business class not necessary", "save money with economy",
                      "ignore health", "tolerate it", "make do", "do not handle yet", "wait until next time", "do not take seriously",
                      "经济舱也可以", "不一定要商务舱", "省点钱坐经济舱", "不用管健康", "忍忍", "凑合一下", "将就一下",
                      "先不处理", "等下次再说", "不用太认真"]
BAD_ADVICE_ALL = BAD_ADVICE_L1 + BAD_ADVICE_L2_HEALTH + BAD_ADVICE_L2_VISA + BAD_ADVICE_L2_BUDGET + BAD_ADVICE_L2_TRAP
