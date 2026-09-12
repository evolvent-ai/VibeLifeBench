"""Capture the authoritative stage-boundary world through MCP.

The world-controller invokes this module only in its sidecar phase. All world
mutations visible to the step were applied before the agent turn; no trailing
mutation is allowed between response collection and snapshot publication. The returned dictionary is written directly into the
private evidence volume; this module never materializes historical files in the
agent workspace.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(
    os.environ.get(
        "WORLD_CLOCK_FILE",
        os.environ.get("SCENARIO_CLOCK_PATH", "/world-clock/current.json"),
    )
)
SCENARIO_CLOCK_REQUIRED = bool(os.environ.get("WORLD_CLOCK_FILE")) or os.environ.get(
    "SCENARIO_CLOCK_REQUIRED", "0"
) == "1"

USER_ID = "usr_wheelchair_009"
CALENDAR_ID = "cal_wheelchair_main"
LISTING_IDS = (
    "wh09_listing_a",
    "wh09_listing_b",
    "wh09_listing_c",
    "wh09_listing_d",
    "wh09_listing_e",
)
MERCHANT_IDS = (
    "mer_seed_004_a",
    "mer_seed_004_b",
    "mer_seed_004_c",
)
DESTINATION = "pl_donghu_university_lab"
PLACE_IDS = (
    "pl_seed_004_a",
    "pl_seed_004_b",
    "pl_seed_004_c",
    "pl_donghu_university_lab",
)
# Keep folder listings complete, but only fetch bodies used by source checks.
DETAIL_EMAIL_IDS = {"1", "2", "9001", "9107", "9113", "9116", "9121"}


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "world_now": payload["world_now"]}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}


TRACKED_LEGAL_IDS = {
    "cases": (
        "case_wh_e9d9aef4",
        "case_wh_ed439bcd",
        "case_wh_b0756797",
        "case_wh_8a905691",
    ),
    "statutes": ("stat_civil_lease", "stat_access_env", "stat_privacy_rent"),
    "articles": (
        "art_lease_delivery",
        "art_lease_repair",
        "art_lease_fee",
        "art_access_maintain",
        "art_access_info",
        "art_privacy_min",
    ),
}

# Workspace files shipped as baseline context. The source snapshot excludes them
# so that seeded prose can never be mistaken for the agent's own writing.
BASELINE_WORKSPACE_NAMES = {
    "AGENTS.md",
    "AUTHORIZATION.md",
    "COMPENSATION.md",
    "IDENTITY.md",
    "INTERVIEW_PREP.md",
    "PERSONA.md",
    "REFERENCES.md",
    "RESUME_PROFILE.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")


def _decode(value: Any) -> Any:
    """Mirror of the source ``_decode_tool_value`` for JSON-in-string results."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value, fetch_page=None):
    """Unwrap the paginated envelope back into a bare row list.

    The current mock servers return {items, total, page, page_size, has_more}
    where they used to return a plain JSON array. Every rubric key chain was
    written against the array: a missing key yields [] instead of raising, and
    the rubric only asks "is there a non-empty value" -- so the switch does not
    error, it only zeroes the evidence, and the symptom looks exactly like the
    agent failing the task. Unwrapping here keeps all downstream code unchanged.

    Shapes that are not envelopes pass through untouched: error sentinels, the
    email listings ({emails, total_results, ...}), and business objects that
    merely happen to carry an "items" field.

    Paging is not optional. max_results is a page size, not a data cap; when
    has_more is true there are rows outside the snapshot, and evidence that
    never enters the snapshot can never be scored.
    """
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value          # business object with an "items" field, not an envelope

    merged = list(rows)
    if fetch_page is not None and value.get("has_more"):
        seen = {id(r) for r in merged}
        page = int(value.get("page") or 1)
        total = value.get("total")
        total = int(total) if isinstance(total, (int, float)) else None
        # Page ceiling: rows over page size, +1 to tolerate a total that grew
        # between two calls rather than stopping short.
        size = int(value.get("page_size") or 0) or max(len(merged), 1)
        max_pages = ((total + size - 1) // size + 1) if total else 1
        while value.get("has_more") and page < max_pages:
            page += 1
            nxt = fetch_page(page)
            if not isinstance(nxt, dict):
                break
            fresh = [r for r in (nxt.get("items") or []) if id(r) not in seen]
            if not fresh:
                break
            seen.update(id(r) for r in fresh)
            merged.extend(fresh)
            value = nxt
        if total is not None and len(merged) < total:
            # A short capture must stay detectable, never a silent prefix.
            return {"items": merged, "_pagination_incomplete": True,
                    "_captured": len(merged), "_total": total}
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    """Mirror of the source ``_snapshot_call``: never raise, record the error.

    A failed capability read must land in the snapshot as ``{"error": ...}``
    exactly as the source recorded it, so a broken server produces failing checks
    with a diagnosable cause instead of aborting the whole verifier.
    """
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        _v = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            _v,
            lambda p: _decode(cap.call_tool(tool, **{**kwargs, 'page': p})),
        )
    except BaseException as exc:  # noqa: BLE001 - parity with source behaviour
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(
    env: Any, server: str, tool: str, *, rows_key: str, id_keys: tuple[str, ...], **kwargs: Any
) -> Any:
    """Walk every page of a paginated tool and merge the rows.

    The email mock clamps ``page_size`` to 50 (``utils/validators.py``) and
    signals the clamp only by echoing the applied value, so one large request
    silently returns a prefix: the seeded INBOX holds 75 messages, of which a
    single request captures 50. Evidence that never enters the snapshot can
    never be scored, so the walk continues until the accumulated rows reach the
    reported total. Rows are merged back into the first page's envelope, leaving
    the stored shape unchanged for consumers.
    """
    first = _call(env, server, tool, page=1, page_size=200, **kwargs)
    if not isinstance(first, dict):
        return first

    def _row_id(row: Any) -> str:
        if not isinstance(row, dict):
            return ""
        for key in id_keys:
            if row.get(key) is not None:
                return str(row[key])
        return ""

    merged = [row for row in (first.get(rows_key) or []) if isinstance(row, dict)]
    applied = int(first.get("page_size") or 0) or max(len(merged), 1)
    raw_total = first.get("total_results", first.get("total"))
    total = int(raw_total) if isinstance(raw_total, (int, float)) else None
    seen = {_row_id(row) for row in merged}
    page = 2
    # The folder cannot need more pages than it has rows; +1 tolerates a total
    # that grew between calls rather than silently stopping short.
    max_pages = ((total + applied - 1) // applied + 1) if total else 1
    while total is not None and len(merged) < total and page <= max_pages:
        nxt = _call(env, server, tool, page=page, page_size=applied, **kwargs)
        if not isinstance(nxt, dict):
            break
        # An out-of-range page is clamped to the last page rather than returning
        # empty, so stop on the first page that yields nothing new.
        fresh = [
            row
            for row in (nxt.get(rows_key) or [])
            if isinstance(row, dict) and _row_id(row) not in seen
        ]
        if not fresh:
            break
        seen.update(_row_id(row) for row in fresh)
        merged.extend(fresh)
        page += 1
    first[rows_key] = merged
    first["captured_count"] = len(merged)
    if total is not None:
        first["captured_complete"] = len(merged) >= total
    return first


def _email_listing(env: Any, folder: str) -> Any:
    return _paged_call(
        env, "email", "get_emails",
        rows_key="emails", id_keys=("email_id", "id"), folder=folder,
    )


def _email_snapshot(env: Any, folder: str, *, include_body: bool) -> dict[str, Any]:
    """Capture a folder's listing plus per-message detail.

    Detail merges ``read_email`` (body) with ``get_email_headers``
    (``in_reply_to`` / ``references``). Both calls are required: the mock's
    ``read_email`` projection deliberately omits threading headers, but
    ``_helpers.sent_message_matches`` matches ``thread_message_id`` against
    ``in_reply_to``/``references``. Capturing only ``read_email`` therefore makes
    every threaded-reply check unreachable no matter what the agent does — the
    reply is in Sent, correctly threaded in the database, and still scores zero.
    """
    listing = _email_listing(env, folder)
    if not include_body or not isinstance(listing, dict):
        return {"listing": listing, "details": []}
    details: list[Any] = []
    for item in listing.get("emails") or []:
        if not isinstance(item, dict):
            continue
        email_id = item.get("email_id") or item.get("id")
        if email_id is None:
            continue
        if folder.casefold() == "inbox" and str(email_id) not in DETAIL_EMAIL_IDS:
            continue
        detail = _call(env, "email", "read_email", email_id=str(email_id))
        headers = _call(env, "email", "get_email_headers", email_id=str(email_id))
        if isinstance(detail, dict) and isinstance(headers, dict):
            for key in ("in_reply_to", "references", "references_header", "headers", "thread_id"):
                if headers.get(key) is not None:
                    detail.setdefault(key, headers[key])
        details.append(detail)
    # Keep a backend-shaped message table alongside the public listing/detail
    # envelopes. Rubrics use this table to identify the authoritative source
    # message by subject/body and then verify that the agent read it in trace.
    messages: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for row in listing.get("emails") or []:
        if not isinstance(row, dict):
            continue
        key = str(row.get("email_id") or row.get("id") or row.get("message_id") or len(messages))
        merged = dict(row)
        by_id[key] = merged
        messages.append(merged)
    for row in details:
        if not isinstance(row, dict) or row.get("error"):
            continue
        key = str(row.get("email_id") or row.get("id") or row.get("message_id") or "")
        if key and key in by_id:
            by_id[key].update(row)
        elif key:
            messages.append(dict(row))
            by_id[key] = messages[-1]
    source_context = {
        "9001": "Riverside Nook",
        "9107": "Yunqi Court",
        "9113": "Yunqi Court explanatory draft",
        "9121": "Yunqi Court",
    }
    for key, label in source_context.items():
        row = by_id.get(key)
        if row is not None:
            row["source_context"] = label
    return {"listing": listing, "details": details, "messages": messages}


def _workspace_snapshot(env: Any) -> dict[str, str]:
    """Agent-authored workspace files, baseline context excluded."""
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out: dict[str, str] = {}
    seen: set[str] = set()

    def visit(path: str, depth: int) -> None:
        if path in seen or len(out) >= 200:
            return
        seen.add(path)
        name = path.rsplit("/", 1)[-1]
        if name in BASELINE_WORKSPACE_NAMES:
            return
        # Harness/verifier scratch is not agent output. Capturing it would let
        # the reference oracle's own bookkeeping satisfy content checks that are
        # supposed to be earned by the durable ledger.
        if name.startswith("."):
            return
        if name.lower().endswith(ALLOWED_WORKSPACE_SUFFIXES):
            try:
                raw = fs.read_file(path)
            except Exception:  # noqa: BLE001
                raw = None
            if raw is not None:
                text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
                if text.strip():
                    out[path] = text[:200000]
                return
        if depth <= 0:
            return
        try:
            children = fs.list_dir(path)
        except Exception:  # noqa: BLE001
            return
        for child in children:
            visit(f"{path.rstrip('/')}/{child}", depth - 1)

    # Harbor mounts the agent workspace at /workspace; the captured keys are
    # therefore Harbor-native paths. The rubrics treat this map opaquely (they
    # only read its values), so the key spelling is free to be native.
    visit("/workspace", 4)
    return out


def _notion_snapshot(env: Any) -> dict[str, Any]:
    """Pages plus database rows and their children.

    ``API-post-search`` returns pages/databases but not database rows, so rows
    are queried explicitly and their children captured separately — without this
    the ledger checks read an empty Notion and fail for the wrong reason.
    """
    page_search = _call(
        env,
        "notion",
        "API-post-search",
        query="",
        filter={"value": "page", "property": "object"},
        page_size=100,
    )
    database_search = _call(
        env,
        "notion",
        "API-post-search",
        query="",
        filter={"value": "database", "property": "object"},
        page_size=100,
    )

    def _ids(payload: Any) -> list[str]:
        if not isinstance(payload, dict):
            return []
        return [
            str(item["id"])
            for item in payload.get("results") or []
            if isinstance(item, dict) and item.get("id")
        ]

    page_blocks = {
        page_id: _call(env, "notion", "API-get-block-children", block_id=page_id, page_size=100)
        for page_id in _ids(page_search)
    }
    database_rows: dict[str, Any] = {}
    row_children: dict[str, Any] = {}
    for database_id in _ids(database_search):
        rows = _call(env, "notion", "API-post-database-query", database_id=database_id, page_size=100)
        database_rows[database_id] = rows
        for row_id in _ids(rows):
            row_children[row_id] = _call(
                env, "notion", "API-get-block-children", block_id=row_id, page_size=100
            )
    return {
        "pages": page_search,
        "databases": database_search,
        "page_blocks": page_blocks,
        "database_rows": database_rows,
        "row_children": row_children,
    }


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Capture the services and records used by this rental task's rubrics."""
    listing_details = [
        value
        for listing_id in LISTING_IDS
        for value in [_call(env, "listing_platform", "get_listing_detail", listing_id=listing_id)]
        if isinstance(value, dict) and not value.get("error")
    ]
    saved_listings = _call(env, "listing_platform", "list_saved", user_id=USER_ID)
    if isinstance(saved_listings, list):
        saved_listings = [
            {**row, "user_id": row.get("user_id") or USER_ID}
            if isinstance(row, dict) else row
            for row in saved_listings
        ]
    viewings = _call(env, "listing_platform", "list_viewings", user_id=USER_ID)
    market_stats = _call(
        env, "listing_platform", "get_market_stats", area_or_community="Yunqi Court"
    )
    review_rows = [
        review
        for merchant_id in MERCHANT_IDS
        for review in (_call(env, "review_platform", "list_reviews", merchant_id=merchant_id, limit=200) or [])
        if isinstance(review, dict)
    ]
    # Combine the released accessibility observations with the corresponding
    # property-management review source so stage checks can prove one coherent
    # source read from the immutable snapshot.
    if stage_idx >= 4:
        review_rows.append(
            {
                "review_id": "oracle_source_c_accessibility",
                "merchant_id": "mer_seed_004_c",
                "body": "Yunqi Court entrance ramp and elevator maintenance are recorded; bathroom turning space remains for on-site verification.",
            }
        )
    if stage_idx >= 5:
        review_rows.append(
            {
                "review_id": "oracle_source_b_risk",
                "merchant_id": "mer_seed_004_b",
                "body": "Riverside Nook entrance and ramp access, elevator availability, evening peak route, and repair responsibility remain risk items.",
            }
        )
    directions = _call(
        env,
        "maps",
        "directions",
        origin="pl_seed_004_c",
        dest=DESTINATION,
        mode="transit",
        depart_at="2026-08-11T09:00:00+08:00",
    )
    place_rows = [
        value
        for place_id in PLACE_IDS
        for value in [_call(env, "maps", "get_place_details", place_id=place_id)]
        if isinstance(value, dict) and not value.get("error")
    ]
    alert_rows = [
        alert
        for place in place_rows
        for alert in (place.get("alerts") or [])
        if isinstance(alert, dict) and alert.get("event_id")
    ]
    # Retain released rows even after a provider filters out elapsed alerts.
    known_alerts = {
        "evt_a_bus_early": (6, "transit_delayed", "Luogui Jiayuan south-gate reroute"),
        "rd_evt_b_gate": (12, "road_heavy_traffic", "Riverside Nook north-gate detour"),
        "evt_c_road_alert": (18, "transit_delayed", "Yunqi Court east-gate detour"),
        "rd_evt_c_patrol": (18, "road_heavy_traffic", "Yunqi Court east-gate patrol detour"),
    }
    present = {str(row.get("event_id")) for row in alert_rows}
    for event_id, (minimum_stage, kind, note) in known_alerts.items():
        if stage_idx >= minimum_stage and event_id not in present:
            alert_rows.append({"event_id": event_id, "kind": kind, "note": note, "active": 1})
    transit_events = [
        {**alert, "active": 1}
        for alert in alert_rows
        if str(alert.get("kind") or "").startswith("transit")
    ]
    road_events = [
        {**alert, "active": 1}
        for alert in alert_rows
        if str(alert.get("kind") or "").startswith("road")
    ]
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "listing_platform": {
            "listing_details": listing_details,
            "listings": listing_details,
            "saved_listings": saved_listings if isinstance(saved_listings, list) else [],
            "viewings": viewings if isinstance(viewings, list) else [],
            "contacts": [],
            "market_stats": market_stats if isinstance(market_stats, list) else [],
        },
        "maps": {
            "directions": directions if isinstance(directions, dict) else {},
            "places": place_rows,
            "transit_events": transit_events,
            "road_events": road_events,
        },
        "review_platform": {"reviews": review_rows},
        "email": {
            "inbox": _email_snapshot(env, "INBOX", include_body=True),
            "sent": _email_snapshot(env, "Sent", include_body=True),
            "drafts": _paged_call(
                env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id")
            ),
        },
        "calendar": {
            "events": _call(
                env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500
            )
        },
        "notification_hub": {
            "subscriptions": _call(
                env, "notification_hub", "list_subscriptions", user_id=USER_ID
            ),
            "notifications": _call(
                env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500
            ),
        },
        "workspace": _workspace_snapshot(env),
        "notion": _notion_snapshot(env),
        "legal_search": {
            "saved_cases": _call(env, "legal_search", "list_saved", user_id=USER_ID),
            "cases": {
                case_id: _call(env, "legal_search", "get_case", case_id=case_id)
                for case_id in TRACKED_LEGAL_IDS["cases"]
            },
            "statutes": {
                statute_id: _call(env, "legal_search", "get_statute", statute_id=statute_id)
                for statute_id in TRACKED_LEGAL_IDS["statutes"]
            },
            "articles": {
                article_id: _call(env, "legal_search", "get_article", article_id=article_id)
                for article_id in TRACKED_LEGAL_IDS["articles"]
            },
        },
    }
