"""Shared rubric helpers for hard_biz_trip_24d."""
from __future__ import annotations

import json
import re
from typing import Any

from loguru import logger
from harbor_evidence import HarborEvidence, response, snapshot, trace

OUTPUT_PATHS = (
    "/workspace/itinerary.md",
    "/workspace/decision_log.md",
    "/workspace/risk_register.md",
    "/workspace/budget.md",
    "/workspace/incident_log.md",
    "/workspace/evidence_log.md",
    "/workspace/final_summary.md",
)

STAGE_COUNT = 24
NOTION_PAGE_TITLE = "Tokyo Business Trip 2026"


# ── mock service call ──────────────────────────────────────────────────────

class RubricInfrastructureError(RuntimeError):
    """A required frozen-evidence value is unavailable or malformed."""


def _evidence(env: HarborEvidence) -> HarborEvidence:
    if not isinstance(env, HarborEvidence):
        raise RubricInfrastructureError("rubrics require HarborEvidence")
    return env


def _current_stage(env: HarborEvidence) -> int:
    stage = getattr(env, "current_stage", None)
    if isinstance(stage, int):
        return stage
    stages = env.published_stages()
    if not stages:
        raise RubricInfrastructureError("no frozen stages have been published")
    return max(stages)


def _decode_result(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
        block = value[0]
        if block.get("type") == "text" and isinstance(block.get("text"), str):
            return _decode_result(block["text"])
    if isinstance(value, dict):
        structured = value.get("structuredContent") or value.get("structured_content")
        if isinstance(structured, dict) and "result" in structured:
            return _decode_result(structured["result"])
    return value


def _trace_call_result(env, server: str, tool: str, kwargs: dict[str, Any]) -> Any:
    current = _current_stage(_evidence(env))
    prior = sorted(
        (stage for stage in env.published_stages() if stage < current), reverse=True
    )
    for stage in [current, *prior]:
        for call in trace(env, stage):
            if not isinstance(call, dict) or call.get("success") is not True:
                continue
            name = str(call.get("name") or call.get("tool") or "")
            if not _tool_name_matches(name, server, tool):
                continue
            arguments = call.get("arguments") or call.get("args") or {}
            if isinstance(arguments, dict) and all(
                arguments.get(key) == value for key, value in kwargs.items()
            ):
                return _decode_result(call.get("result"))
    return None


def _snapshot_call(env, server: str, tool: str, kwargs: dict[str, Any]) -> Any:
    state = snapshot(_evidence(env), _current_stage(env))
    section = state.get(server, {})
    if not isinstance(section, dict):
        return None

    if server == "flight_booking":
        if tool == "list_bookings":
            return section.get("bookings", [])
        if tool == "get_booking":
            details = section.get("booking_details", {})
            return details.get(str(kwargs.get("pnr")), {}) if isinstance(details, dict) else {}
        if tool == "get_flight_status":
            statuses = section.get("flight_statuses", section.get("statuses", {}))
            flight_no = str(kwargs.get("flight_no") or "").upper()
            if isinstance(statuses, dict):
                return statuses.get(flight_no) or statuses.get(flight_no.lower())
    elif server == "hotel_booking":
        if tool == "list_reservations":
            return section.get("reservations", [])
        if tool == "get_reservation":
            details = section.get("reservation_details", {})
            return details.get(str(kwargs.get("reservation_id")), {}) if isinstance(details, dict) else {}
    elif server == "visa_and_advisory" and tool == "check_entry_requirements":
        requirements = section.get("entry_requirements")
        if isinstance(requirements, dict):
            destination = str(kwargs.get("destination") or "").upper()
            return requirements.get(destination, requirements)
    elif server == "notion":
        if tool == "API-post-search":
            return section.get("search", {"results": section.get("pages", [])})
        if tool == "API-get-block-children":
            blocks = section.get("blocks", {})
            return blocks.get(str(kwargs.get("block_id")), {}) if isinstance(blocks, dict) else {}
    elif server == "calendar":
        events = section.get("events", [])
        if tool == "list_events":
            return events
        if tool == "get_event":
            wanted = str(kwargs.get("event_id") or "")
            rows = events.get("events", events.get("items", [])) if isinstance(events, dict) else events
            return next(
                (
                    row for row in rows
                    if isinstance(row, dict)
                    and str(row.get("event_id") or row.get("id") or "") == wanted
                ),
                None,
            )
    elif server == "banking":
        if tool == "list_accounts":
            accounts = section.get("accounts")
            if accounts is not None:
                return accounts
            account = section.get("account")
            return [account] if isinstance(account, dict) and account else []
        if tool == "list_transactions":
            transactions = section.get("transactions", [])
            if isinstance(transactions, dict):
                return transactions.get(str(kwargs.get("account_id")), [])
            return transactions
    elif server == "weather":
        key = {
            "get_typhoon_track": "typhoon_track",
            "get_alerts": "alerts",
            "get_forecast_daily": "forecast_daily",
        }.get(tool)
        if key:
            return section.get(key)
    return None


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    """Resolve a former service read from immutable snapshot or trace data."""
    frozen = _snapshot_call(env, server, tool, kwargs)
    if frozen is not None:
        return frozen
    recorded = _trace_call_result(env, server, tool, kwargs)
    if recorded is not None:
        return recorded
    return {}


# ── text helpers ───────────────────────────────────────────────────────────

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
    haystack = (text or "").lower()
    return bool(haystack) and any(str(w).lower() in haystack for w in words)


def _number_count(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"(?<!\d)\d+(?:,\d{3})*(?:\.\d+)?(?!\d)", text))


# ── workspace file helpers ─────────────────────────────────────────────────

def _workspace_file_text(env, path: str) -> str:
    workspace = snapshot(_evidence(env), _current_stage(env)).get("workspace", {})
    if not isinstance(workspace, dict):
        raise RubricInfrastructureError("workspace snapshot is not an object")
    if path in workspace:
        return str(workspace[path])
    basename = path.rstrip("/").rsplit("/", 1)[-1]
    for candidate, value in workspace.items():
        if str(candidate).rstrip("/").rsplit("/", 1)[-1] == basename:
            return str(value)
    return ""


def _workspace_text(env) -> str:
    chunks: list[str] = []
    for path in OUTPUT_PATHS:
        body = _workspace_file_text(env, path)
        if body:
            chunks.append(body)
    return "\n".join(chunks)


def _workspace_file_nonempty(env, path: str) -> bool:
    return len(_workspace_file_text(env, path).strip()) > 0


# ── Notion helpers ─────────────────────────────────────────────────────────

def _notion_text(env) -> str:
    search = _call(
        env, "notion",
        "API-post-search",
        query=NOTION_PAGE_TITLE,
        filter={"value": "page"},
        page_size=10,
    )
    pages: list[dict] = []
    if isinstance(search, dict):
        pages = [p for p in search.get("results") or [] if isinstance(p, dict)]
    if not pages:
        return ""
    chunks: list[str] = []
    for page in pages[:3]:
        page_id = page.get("id")
        chunks.append(_flatten_text(page))
        if not page_id:
            continue
        children = _call(env, "notion", "API-get-block-children", block_id=page_id)
        chunks.append(_flatten_text(children))
    return "\n".join(chunks)


# ── corpus functions ───────────────────────────────────────────────────────

def _stage_corpus(env, idx: int) -> str:
    previous = getattr(env, "current_stage", None)
    env.current_stage = idx
    try:
        return (response(_evidence(env), idx) + "\n" + _workspace_text(env)).lower()
    finally:
        if isinstance(previous, int):
            env.current_stage = previous


# ── tool-call trace analysis ───────────────────────────────────────────────

def _tool_calls(env, stage: int | None = None) -> list[dict[str, Any]]:
    """Return successful formal calls from immutable stage traces."""
    stages = [stage] if stage is not None else env.published_stages()
    calls: list[dict[str, Any]] = []
    for idx in stages:
        calls.extend(
            call for call in trace(_evidence(env), idx)
            if isinstance(call, dict) and call.get("success") is True
        )
    return calls


def _successful_tool_results(
    env,
    server: str | None = None,
    tool: str | None = None,
    *,
    stage: int | None = None,
) -> list[Any]:
    """Return successful result payloads linked to matching formal calls."""
    return [
        _decode_result(call.get("result"))
        for call in _tool_calls(env, stage)
        if _tool_name_matches(str(call.get("name") or ""), server, tool)
        and call.get("result") is not None
    ]



def _searched_hkg_recovery_quote(env, *, stage: int = 14) -> dict[str, Any] | None:
    """Return the public-search quote for the uniquely compliant MU7165/MU7166 recovery pair."""
    wanted = {
        "MU7165": ("NRT", "HKG"),
        "MU7166": ("HKG", "PVG"),
    }
    found: dict[str, dict[str, Any]] = {}
    for payload in _successful_tool_results(env, "flight_booking", "search_flights", stage=stage):
        offers = payload.get("offers") if isinstance(payload, dict) else None
        for offer in offers if isinstance(offers, list) else []:
            if not isinstance(offer, dict):
                continue
            price = offer.get("total_price") or {}
            amount = price.get("amount") if isinstance(price, dict) else None
            currency = price.get("currency") if isinstance(price, dict) else None
            slices = ((offer.get("itinerary") or {}).get("slices") or []) if isinstance(offer.get("itinerary"), dict) else []
            for slice_ in slices if isinstance(slices, list) else []:
                if not isinstance(slice_, dict):
                    continue
                segments = slice_.get("segments") or []
                if len(segments) != 1 or not isinstance(segments[0], dict):
                    continue
                segment = segments[0]
                flight_no = str(segment.get("flight_no") or "").upper()
                route = wanted.get(flight_no)
                if route is None:
                    continue
                if str(slice_.get("origin") or "").upper() != route[0] or str(slice_.get("destination") or "").upper() != route[1]:
                    continue
                if not isinstance(amount, (int, float)) or str(currency or "").upper() != "CNY":
                    continue
                found[flight_no] = {
                    "flight_no": flight_no,
                    "amount": int(amount),
                    "depart_dt": segment.get("depart_dt") or slice_.get("depart_dt"),
                    "arrive_dt": segment.get("arrive_dt") or slice_.get("arrive_dt"),
                }
    if set(found) != set(wanted):
        return None
    try:
        dt = __import__("datetime").datetime
        layover = int((dt.fromisoformat(str(found["MU7166"]["depart_dt"])) - dt.fromisoformat(str(found["MU7165"]["arrive_dt"]))).total_seconds() // 60)
        final_arrive = dt.fromisoformat(str(found["MU7166"]["arrive_dt"]))
    except (TypeError, ValueError):
        return None
    if not (90 <= layover <= 720 and final_arrive.date().isoformat() < "2026-07-22"):
        return None
    return {
        "flight_numbers": ["MU7165", "MU7166"],
        "total_amount": found["MU7165"]["amount"] + found["MU7166"]["amount"],
        "currency": "CNY",
        "layover_min": layover,
        "final_arrive": found["MU7166"]["arrive_dt"],
    }


def _tool_name_matches(name: str, server: str | None = None, tool: str | None = None) -> bool:
    norm = (name or "").lower().replace("-", "_")
    if norm.startswith("mcp__"):
        norm = norm[len("mcp__"):]
    if server:
        server_norm = server.lower().replace("-", "_")
        server_aliases = {server_norm, f"{server_norm}_mock"}
        if not any(
            norm.startswith(f"{alias}__") or norm.startswith(f"{alias}_")
            for alias in server_aliases
        ):
            return False
    if tool:
        tool_norm = tool.lower().replace("-", "_")
        return norm == tool_norm or norm.endswith(f"__{tool_norm}") or norm.endswith(f"_{tool_norm}")
    return bool(norm)


def _agent_used_tool(
    env, server: str | None = None, tool: str | None = None,
    *, stage: int | None = None,
) -> bool:
    return any(
        _tool_name_matches(str(call.get("name") or ""), server, tool)
        for call in _tool_calls(env, stage)
    )


def _agent_tool_servers(env) -> set[str]:
    servers: set[str] = set()
    known = [
        "flight_booking", "hotel_booking", "banking",
        "calendar", "notion", "email", "maps",
        "visa_and_advisory", "weather",
    ]
    for call in _tool_calls(env):
        name = str(call.get("name") or "").lower().replace("-", "_")
        if name.startswith("mcp__"):
            name = name[len("mcp__"):]
        for server in known:
            if (
                name.startswith(f"{server}__")
                or name.startswith(f"{server}_")
                or name.startswith(f"{server}_mock__")
                or name.startswith(f"{server}_mock_")
            ):
                servers.add(server)
                break
    return servers


def _agent_tool_call_text(env, *, stage: int | None = None) -> str:
    return _flatten_text(_tool_calls(env, stage)).lower()


def _agent_used_tool_with_args(
    env,
    server: str,
    tool: str,
    required: list[str],
    *,
    stage: int | None = None,
) -> bool:
    for call in _tool_calls(env, stage):
        name = str(call.get("name") or "")
        if not _tool_name_matches(name, server, tool):
            continue
        args = _flatten_text(call.get("arguments")).lower()
        if all(term.lower() in args for term in required):
            return True
    return False


def _email_draft_arguments(env, stage: int | None = None) -> list[dict[str, Any]]:
    return [
        dict(call.get("arguments") or {})
        for call in _tool_calls(env, stage)
        if _tool_name_matches(str(call.get("name") or ""), "email", "save_draft")
        and isinstance(call.get("arguments"), dict)
    ]


def _email_draft_text(env) -> str:
    return _flatten_text(_email_draft_arguments(env)).lower()


def _stage_email_draft_text(env, stage: int) -> str:
    return _flatten_text(_email_draft_arguments(env, stage)).lower()


def _draft_address_matches(value: Any, expected: str) -> bool:
    if isinstance(value, str):
        values = [part.strip().lower() for part in re.split(r"[,;]", value) if part.strip()]
    elif isinstance(value, list):
        values = [str(part).strip().lower() for part in value]
    else:
        values = []
    return expected.lower() in values


def _has_email_draft_target(
    env,
    recipient: str,
    *,
    stage: int | None = None,
    in_reply_to: str | None = None,
) -> bool:
    for args in _email_draft_arguments(env, stage):
        if not _draft_address_matches(args.get("to"), recipient):
            continue
        if in_reply_to is not None and str(args.get("in_reply_to") or "").strip() != in_reply_to:
            continue
        return True
    return False


def _flight_booking_details(env) -> list[dict[str, Any]]:
    listed = _call(env, "flight_booking", "list_bookings", email="zhang.ming@company.com", page=1, page_size=50)
    rows = listed.get("bookings") if isinstance(listed, dict) else None
    if not isinstance(rows, list):
        return []
    details: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        pnr = row.get("pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr) if pnr else None
        merged = dict(row)
        if isinstance(detail, dict) and not detail.get("error"):
            merged.update(detail)
        details.append(merged)
    return details


def _hotel_reservations_text(env) -> str:
    return _flatten_text(_hotel_reservation_details(env)).lower()


def _hotel_reservation_details(env) -> list[dict[str, Any]]:
    reservations = _call(env, "hotel_booking", "list_reservations", user_id="zhang_ming")
    ids: list[Any] = []
    if isinstance(reservations, dict):
        ids = reservations.get("reservation_ids") or reservations.get("reservations") or reservations.get("items") or []
    elif isinstance(reservations, list):
        ids = reservations
    details: list[dict[str, Any]] = []
    for item in ids:
        if isinstance(item, dict):
            details.append(item)
            continue
        detail = _call(env, "hotel_booking", "get_reservation", reservation_id=str(item))
        if isinstance(detail, dict) and not detail.get("error"):
            details.append(detail)
    return details


def _count_stages_with_tool(env, server: str, tool: str | None = None) -> int:
    count = 0
    for s in range(STAGE_COUNT):
        if _agent_used_tool(env, server, tool, stage=s):
            count += 1
    return count


# ── negation / bad-advice detection ────────────────────────────────────────

_NEGATION_CUES = (
    "do not", "don't", "cannot", "can't", "should not", "must not",
    "is not", "not for", "not because", "no need", "not needed",
    "not recommended", "never", "prohibited", "refuse", "avoid",
)

_POST_REJECTION_CUES = (
    "refused", "explicitly refused", "rejected", "not accepted",
    "cannot agree", "not adopted", "declined", "was refused", "was rejected",
)


def _has_unqualified_phrase(text: str, phrase: str, *, window: int = 6) -> bool:
    if not text or not phrase:
        return False
    start = 0
    while True:
        match = re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text[start:])
        idx = (start + match.start()) if match else -1
        if idx < 0:
            return False
        context_start = max(0, idx - window)
        context = text[context_start:idx + min(len(phrase), 4)]
        negated = False
        for cue in _NEGATION_CUES:
            cue_idx = context.find(cue)
            if cue_idx >= 0 and context_start + cue_idx < idx:
                negated = True
                break
        suffix = text[idx + len(phrase):idx + len(phrase) + 24]
        if any(cue in suffix for cue in _POST_REJECTION_CUES):
            negated = True
        if not negated:
            # dead-False fix: an unqualified (un-hedged) occurrence is what this must flag →
            # return True. Previously False, so no negation veto could ever fire.
            return True
        start = idx + len(phrase)


def _has_bad_advice(text: str, phrases: list[str], *, window: int = 6) -> bool:
    if not text:
        return False
    return any(_has_unqualified_phrase(text, phrase, window=window) for phrase in phrases)


# ── mock service side-effect verification ──────────────────────────────────

def _agent_booked_flight(env) -> bool:
    if not _agent_used_tool(env, "flight_booking", "create_booking"):
        return False
    return bool(_flight_booking_details(env))


def _agent_booked_hotel(env) -> bool:
    if not _agent_used_tool(env, "hotel_booking", "create_reservation"):
        return False
    return bool(_hotel_reservation_details(env))


# ── budget analysis helpers ────────────────────────────────────────────────

def _budget_has_currency_split(text: str) -> bool:
    return _any(text, ["cny", "jpy", "hkd"])


def _budget_has_status_tracking(text: str) -> bool:
    categories = ["flight", "accommodation", "insurance", "registration", "meals", "transportation"]
    status_count = 0
    for cat in categories:
        if cat in text:
            has_estimate = _any(text, ["estimate", "estimated", "budget", "projected"])
            has_settled = _any(text, ["settled", "actual"])
            if has_estimate or has_settled:
                status_count += 1
    return status_count >= 4


def _budget_has_pending_refund(env) -> bool:
    budget = _workspace_file_text(env, "/workspace/budget.md").lower()
    return _any(budget, ["pending refund", "pending", "not received", "under review", "pending confirmation"])


# ── transit discovery helpers ──────────────────────────────────────────────

def _agent_checked_transit_visa(env) -> bool:
    """Formal successful HK transit lookup agrees with the live visa backend."""
    checked = _agent_used_tool_with_args(
        env, "visa_and_advisory", "check_entry_requirements", ["cn", "hk", "transit"]
    )
    results = _successful_tool_results(env, "visa_and_advisory", "check_entry_requirements")
    result_text = json.dumps(results, ensure_ascii=False).lower()
    formal_result = bool(results) and _any(result_text, ["hk", "hong kong"]) and _any(result_text, ["visa_required", "visa required"]) and _any(result_text, ["false", "0"])
    live = _call(
        env, "visa_and_advisory", "check_entry_requirements",
        nationality="CN", destination="HK", purpose="transit", transit_countries=[],
    )
    live_ok = isinstance(live, dict) and live.get("visa_required") is False and int(live.get("allowed_stay_days") or 0) >= 1
    recorded = _any(_workspace_text(env), ["transit visa", "visa not required", "visa-free", "visa free"]) and _any(
        _workspace_text(env), ["hk", "hkg", "hong kong"]
    )
    return checked and formal_result and live_ok and recorded


def _agent_drafted_email(env) -> bool:
    """Agent saved email draft."""
    return _agent_used_tool(env, "email", "save_draft")


# ── calendar backend state ─────────────────────────────────────────────────

# ── MCT trap checker ─────────────────────────────────────────────────────

def _agent_booked_mct_violation(env) -> bool:
    """Return True only when booked NRT-HKG/PVG segments form a sub-90-minute connection."""
    segments = _active_booked_segments(env)
    arrivals = [s for s in segments if str(s.get("destination") or s.get("dest") or "").upper() == "HKG"]
    departures = [s for s in segments if str(s.get("origin") or "").upper() == "HKG" and str(s.get("destination") or s.get("dest") or "").upper() == "PVG"]
    for first in arrivals:
        for second in departures:
            try:
                dt = __import__("datetime").datetime
                minutes = (dt.fromisoformat(str(second.get("depart_dt"))) - dt.fromisoformat(str(first.get("arrive_dt")))).total_seconds() / 60
            except (TypeError, ValueError):
                continue
            if 0 <= minutes < 90:
                return True
    return False


def _agent_booked_tpe_transit(env) -> bool:
    """Agent booked NRT->TPE->PVG (visa trap for CN passport)."""
    booked_list: list[Any] = _flight_booking_details(env)
    for b in booked_list:
        text = _flatten_text(b).lower()
        if _any(text, ["br8001", "br8002", "tpe", "taipei"]):
            return True
    # Only booking/hold calls count as a violation; search_flights TPE calls are allowed
    # when used to compare and reject the visa-risk route.
    for call in _tool_calls(env):
        name = str(call.get("name") or "").lower().replace("-", "_")
        if not _tool_name_matches(name, "flight_booking", "create_booking"):
            continue
        args = _flatten_text(call.get("arguments")).lower()
        if _any(args, ["br8001", "br8002", "tpe", "taipei"]):
            return True
    return False


def _agent_agreed_no_insurance(env) -> bool:
    """Agent agreed to skip or replace travel insurance with accident insurance."""
    text = _workspace_text(env).lower()
    return _has_bad_advice(text, [
        "can go uninsured", "no travel insurance needed",
        "ordinary accident insurance is enough", "skip insurance",
        "do not buy travel insurance", "no need to buy", "can skip",
    ], window=8)


def _agent_booked_prepaid_before_approval(env) -> bool:
    """A successful pre-approval create_reservation used a prepaid rate-plan id."""
    for stage in range(7):
        for call in _tool_calls(env, stage):
            if not _tool_name_matches(str(call.get("name") or ""), "hotel_booking", "create_reservation"):
                continue
            args = _flatten_text(call.get("arguments")).lower()
            if "prepaid" in args or "non-refundable" in args or "nonrefundable" in args:
                return True
    return False


# ── backend state assertions for incidents/reconciliation ───────────────

def _active_booked_segments(env) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for booking in _active_flight_bookings(env):
        segments = booking.get("segments") or []
        if isinstance(segments, str):
            try:
                segments = json.loads(segments)
            except json.JSONDecodeError:
                segments = []
        for segment in segments if isinstance(segments, list) else []:
            if isinstance(segment, dict):
                rows.append(segment)
    return rows


def _booked_hkg_transit_segments(env) -> list[dict[str, Any]]:
    """Return a safe Jul-21 NRT-HKG-PVG pair arriving before Jul 22."""
    segments = _active_booked_segments(env)
    first = [s for s in segments if str(s.get("origin") or "").upper() == "NRT" and str(s.get("destination") or s.get("dest") or "").upper() == "HKG"]
    second = [s for s in segments if str(s.get("origin") or "").upper() == "HKG" and str(s.get("destination") or s.get("dest") or "").upper() == "PVG"]
    for a in first:
        for b in second:
            try:
                arrive = __import__("datetime").datetime.fromisoformat(str(a.get("arrive_dt")))
                depart = __import__("datetime").datetime.fromisoformat(str(b.get("depart_dt")))
                final_arrive = __import__("datetime").datetime.fromisoformat(str(b.get("arrive_dt")))
            except (TypeError, ValueError):
                continue
            layover = (depart - arrive).total_seconds() / 60
            statuses = {str(a.get("status") or "").upper(), str(b.get("status") or "").upper()}
            if 90 <= layover <= 720 and final_arrive.date().isoformat() < "2026-07-22" and "CANCELLED" not in statuses:
                return [a, b]
    return []


def _booked_hkg_transit(env) -> bool:
    return len(_booked_hkg_transit_segments(env)) == 2


def _booked_hkg_flight_numbers(env) -> list[str]:
    return [str(s.get("flight_no") or "").upper() for s in _booked_hkg_transit_segments(env) if s.get("flight_no")]


def _text_names_booked_hkg_flights(env, text: str) -> bool:
    numbers = _booked_hkg_flight_numbers(env)
    haystack = (text or "").lower()
    return len(numbers) == 2 and all(number.lower() in haystack for number in numbers)


def _cancelled_direct_state(env) -> bool:
    for flight_no in ("MU524", "CA930", "NH919"):
        status = _call(env, "flight_booking", "get_flight_status", flight_no=flight_no, date="2026-07-22")
        if not isinstance(status, dict) or str(status.get("status") or "").upper() != "CANCELLED":
            return False
    return True


def _typhoon_track(env) -> list[dict[str, Any]]:
    track = _call(env, "weather", "get_typhoon_track", storm_id="storm_yinxing_20260718")
    return [row for row in track if isinstance(row, dict)] if isinstance(track, list) else []


def _typhoon_stage12_backend(env) -> bool:
    alerts = _call(env, "weather", "get_alerts", geo="Tokyo")
    alert_text = _flatten_text(alerts).lower()
    track_text = _flatten_text(_typhoon_track(env)).lower()
    return _any(alert_text, ["typhoon", "category 2", "category_2", "965"]) and _any(alert_text, ["severe"]) and _any(track_text, ["category_2_965hpa"])


def _typhoon_history_backend(env) -> bool:
    text = _flatten_text(_typhoon_track(env)).lower()
    return _any(text, ["category_2_965hpa"]) and _any(text, ["category_1", "tropical_storm"])


def _typhoon_stage13_backend(env) -> bool:
    alerts = _call(env, "weather", "get_alerts", geo="Tokyo")
    alert_text = _flatten_text(alerts).lower()
    track_text = _flatten_text(_typhoon_track(env)).lower()
    forecast = _call(env, "weather", "get_forecast_daily", geo="Narita", days=3)
    forecast_text = _flatten_text(forecast).lower()
    return _any(alert_text, ["weakened to category 1", "category 1"]) and _any(track_text, ["category_1"]) and _any(forecast_text, ["improving", "partly cloudy"])


def _calendar_conflict_backend(env) -> bool:
    event = _call(env, "calendar", "get_event", event_id="evt_client_request_external")
    text = _flatten_text(event).lower()
    return isinstance(event, dict) and str(event.get("status") or "").lower() == "tentative" and "2026-07-20t14:00" in text and "2026-07-20t16:00" in text


def _bank_transactions(env) -> list[dict[str, Any]]:
    accounts = _call(env, "banking", "list_accounts", user_id="zhang_ming")
    if not isinstance(accounts, list):
        return []
    rows: list[dict[str, Any]] = []
    for account in accounts:
        if not isinstance(account, dict) or not account.get("account_id"):
            continue
        txs = _call(env, "banking", "list_transactions", account_id=account["account_id"], since="2026-07-01", until="2026-07-31", limit=500)
        for tx in txs if isinstance(txs, list) else []:
            if isinstance(tx, dict):
                row = dict(tx); row["account_id"] = account["account_id"]; row["currency"] = account.get("currency"); rows.append(row)
    return rows


def _bank_has_tx(env, tx_id: str, amount_minor: int, *, account_id: str | None = None, kind: str | None = None) -> bool:
    for row in _bank_transactions(env):
        if str(row.get("tx_id")) != tx_id or row.get("amount_minor") != amount_minor:
            continue
        if account_id and row.get("account_id") != account_id:
            continue
        if kind and str(row.get("kind") or "").lower() != kind.lower():
            continue
        return True
    return False


def _bank_lunch_state(env) -> bool:
    return _bank_has_tx(env, "tx_jpy_client_lunch_0717", -6800, account_id="acct_zhangming_jpy_wallet", kind="payment")


def _bank_forex_state(env) -> bool:
    rows = _bank_transactions(env)
    purchase = any(r.get("tx_id") == "tx_hkg_airport_purchase_0721" and r.get("amount_minor") == -22000 and r.get("account_id") == "acct_zhangming_hkd_wallet" for r in rows)
    fee = any(r.get("tx_id") == "tx_hkg_foreign_transaction_fee_0721" and r.get("amount_minor") == -330 and r.get("kind") == "fee" and "1.5%" in str(r.get("memo") or "") for r in rows)
    return purchase and fee


def _refund_pending_backend(env) -> bool:
    if not _cancelled_direct_state(env):
        return False
    for row in _bank_transactions(env):
        blob = _flatten_text(row).lower()
        if int(row.get("amount_minor") or 0) > 0 and _any(blob, ["mu524", "refund"]):
            return False
    return True


def _bank_reconciliation_state(env) -> bool:
    return all([
        _bank_has_tx(env, "tx_trip_mu523_settlement", -145000, account_id="acct_zhangming_cny_checking"),
        _bank_has_tx(env, "tx_trip_mu7165_settlement", -280000, account_id="acct_zhangming_cny_checking"),
        _bank_has_tx(env, "tx_trip_mu7166_settlement", -150000, account_id="acct_zhangming_cny_checking"),
        _bank_has_tx(env, "tx_jpy_cash_withdrawal_0716", -60000, account_id="acct_zhangming_jpy_wallet"),
        _bank_forex_state(env),
        _refund_pending_backend(env),
    ])

# ── backend-derived hotel amount verification ─────────────────────────────

def _active_hotel_reservations(env) -> list[dict[str, Any]]:
    """Return agent-created hotel reservations that remain business-relevant."""
    active_statuses = {"confirmed", "modified", "walked", "checked_out"}
    return [
        row for row in _hotel_reservation_details(env)
        if isinstance(row, dict) and str(row.get("status") or "").lower() in active_statuses
    ]


def _amount_in_text(text: str, amount: int) -> bool:
    normalized = (text or "").replace(",", "")
    return re.search(rf"(?<!\d){int(amount)}(?!\d)", normalized) is not None


def _text_has_backend_hotel_amounts(env, text: str) -> bool:
    """Accept itemized active reservation totals or their exact backend sum."""
    rows = _active_hotel_reservations(env)
    amounts = [
        int(row["total_charged"])
        for row in rows
        if str(row.get("currency") or "").upper() == "JPY"
        and isinstance(row.get("total_charged"), (int, float))
        and int(row["total_charged"]) > 0
    ]
    if not amounts or not _any((text or "").lower(), ["jpy"]):
        return False
    return all(_amount_in_text(text, amount) for amount in amounts) or _amount_in_text(text, sum(amounts))


def _hotel_extension_reservations(env) -> list[dict[str, Any]]:
    """Return refundable Tokyo/Narita stays that cover the night of 2026-07-20."""
    allowed_hotels = {"hotel_roppongi_biz", "hotel_narita_transit"}
    rows: list[dict[str, Any]] = []
    for row in _active_hotel_reservations(env):
        check_in = str(row.get("check_in") or "")[:10]
        check_out = str(row.get("check_out") or "")[:10]
        refundable = row.get("refundable")
        if (
            str(row.get("hotel_id") or "") in allowed_hotels
            and check_in <= "2026-07-20" < check_out
            and refundable in {True, 1}
            and str(row.get("currency") or "").upper() == "JPY"
            and isinstance(row.get("total_charged"), (int, float))
            and int(row["total_charged"]) > 0
        ):
            rows.append(row)
    return rows


def _text_has_backend_hotel_extension_amount(env, text: str) -> bool:
    rows = _hotel_extension_reservations(env)
    return bool(rows) and _any((text or "").lower(), ["jpy"]) and any(
        _amount_in_text(text, int(row["total_charged"])) for row in rows
    )

# ── backend-derived flight amount verification ────────────────────────────

def _active_flight_bookings(env) -> list[dict[str, Any]]:
    active_statuses = {"ticketed", "hold", "changed"}
    return [
        row for row in _flight_booking_details(env)
        if isinstance(row, dict) and str(row.get("status") or "").lower() in active_statuses
    ]


def _flight_paid_amounts(env) -> list[int]:
    amounts: list[int] = []
    for row in _active_flight_bookings(env):
        total_paid = row.get("total_paid")
        amount = total_paid.get("amount") if isinstance(total_paid, dict) else row.get("paid_amount")
        currency = total_paid.get("currency") if isinstance(total_paid, dict) else row.get("currency")
        if isinstance(amount, (int, float)) and int(amount) > 0 and str(currency or "").upper() == "CNY":
            amounts.append(int(amount))
    return amounts


def _text_has_backend_flight_amounts(env, text: str) -> bool:
    """Accept itemized active booking amounts or their exact backend sum."""
    amounts = _flight_paid_amounts(env)
    if not amounts or not _any((text or "").lower(), ["cny"]):
        return False
    return all(_amount_in_text(text, amount) for amount in amounts) or _amount_in_text(text, sum(amounts))
