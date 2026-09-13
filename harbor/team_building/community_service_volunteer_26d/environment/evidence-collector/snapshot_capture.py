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

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"

USER_ID = "usr_csr_maya"
CALENDAR_ID = "cal_csr_volunteer"


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        value = payload.get("world_now")
        if set(payload) != {"world_now"} or not isinstance(value, str):
            raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "now": value}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        return {"schema_version": 1, "now": ""}


# Copied verbatim from the source task.py. The rubrics assert on these exact ids.
TRACKED_JOB_IDS = (
    "job_mj_214",
    "job_yr_098",
    "job_qs_507",
    "job_lh_332",
    "job_jh_126",
    "job_ba_773",
    "job_eb2508",
    "job_4437d4",
    "job_08caa9",
    "job_fbc2b6",
    "job_86f824",
    "job_361030",
    "job_541371",
    "job_adcf31",
)

TRACKED_APPLICATION_IDS = (
    "app_mj_001",
    "app_39f15c",
    "app_9cfb94",
    "app_a935d7",
    "app_b323c6",
    "app_ca54c7",
    "app_308e6e",
    "app_0a108f",
    "app_6ebad5",
    "app_bc0d7e",
)

TRACKED_LEGAL_IDS = {
    "cases": (
        "case_noncompete_comp",
        "case_probation_salary",
        "case_employee_work",
        "case_customer_data",
        "case_clause_scope",
        "case_confidentiality",
        "case_0b9fb5e5",
        "case_91df21d0",
        "case_32e71e2d",
        "case_c202b143",
        "case_9e37bba0",
    ),
    "statutes": (
        "stat_labor_contract",
        "stat_personal_info",
        "stat_civil_code",
        "stat_52e9ebd7",
        "stat_b8e3b12b",
        "stat_aa45041c",
        "stat_53e861d3",
        "stat_8f9c2ba0",
        "stat_fdb02184",
        "stat_fb08641d",
    ),
    "articles": (
        "art_labor_19",
        "art_labor_20",
        "art_labor_23",
        "art_labor_24",
        "art_pipl_6",
        "art_civil_privacy",
        "art_87d7abfc",
        "art_4cb3c589",
        "art_314eb23c",
        "art_41be0315",
        "art_a67caa73",
        "art_c6e4419e",
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
INBOX_DETAIL_IDS = {
    "101", "469", "582", "1201", "1202", "1203", "1204", "1205", "1206",
    "1211", "1212", "1213", "1214",
}


def _decode(value: Any) -> Any:
    """Mirror of the source ``_decode_tool_value`` for JSON-in-string results."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page: Any = None) -> Any:
    """Unwrap paginated MCP envelopes and merge subsequent pages."""
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value):
        return value
    merged = list(rows)
    total = value.get("total")
    page = int(value.get("page") or 1) + 1
    size = int(value.get("page_size") or len(rows) or 1)
    while value.get("has_more") and fetch_page is not None:
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            value["_pagination_incomplete"] = True
            break
        fresh = nxt["items"]
        merged.extend(fresh)
        value = nxt
        page += 1
        if total is not None and len(merged) >= int(total):
            break
    if value.get("has_more"):
        value["_pagination_incomplete"] = True
    return merged


# Auto-continuation re-issues the same tool with the applied page size. Each
# mock names that parameter differently; forwarding "page_size" to a tool whose
# signature declares "limit"/"max_results" would fail the call outright.
_CONTINUATION_SIZE_PARAMS: dict[tuple[str, str], str] = {
    ("banking", "list_transactions"): "limit",
    ("calendar", "list_events"): "max_results",
    ("calendar", "search_events"): "max_results",
    ("car_rental", "search_vehicle_offers"): "max_results",
    ("content_platform", "search_notes"): "limit",
    ("delivery_logistics", "list_shipments"): "limit",
    ("ecommerce", "list_orders"): "limit",
    ("ecommerce", "search_products"): "limit",
    ("notification_hub", "list_notifications"): "limit",
    ("review_platform", "search_merchants"): "limit",
}


def _continuation_size_param(server: str, tool: str) -> str:
    return _CONTINUATION_SIZE_PARAMS.get((server, tool), "page_size")


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
        value = _decode(cap.call_tool(tool, **kwargs))
        size_param = _continuation_size_param(server, tool)
        return _unwrap_envelope(
            value,
            lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page, size_param: value.get("page_size")})),
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
        if folder.upper() == "INBOX" and str(email_id) not in INBOX_DETAIL_IDS:
            continue
        detail = _call(env, "email", "read_email", email_id=str(email_id))
        headers = _call(env, "email", "get_email_headers", email_id=str(email_id))
        if isinstance(detail, dict) and isinstance(headers, dict):
            for key in ("in_reply_to", "references", "references_header", "headers", "thread_id"):
                if headers.get(key) is not None:
                    detail.setdefault(key, headers[key])
        details.append(detail)
    return {"listing": listing, "details": details}


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
    """Capture every task service and the private workspace at a boundary."""
    order_headers = _call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=500)
    orders = [
        _call(env, "ecommerce", "get_order", order_id=row["order_id"])
        for row in order_headers if isinstance(row, dict) and row.get("order_id")
    ] if isinstance(order_headers, list) else order_headers
    shipment_headers = _call(
        env, "delivery_logistics", "list_shipments", user_id=USER_ID, limit=500
    )
    shipments = [
        _call(env, "delivery_logistics", "get_shipment", shipment_id=row["shipment_id"])
        for row in shipment_headers if isinstance(row, dict) and row.get("shipment_id")
    ] if isinstance(shipment_headers, list) else shipment_headers
    product_ids = (
        "prod_hygiene_kit_standard", "prod_towel_pack_gray", "prod_plain_label_roll",
        "prod_fresh_food_box", "prod_vitamin_supplement", "prod_gift_card_200",
        "prod_used_tablet",
    )
    offer_ids = ("offer_vol_small_16", "offer_vol_bus_28", "offer_vol_van_12")
    merchant_ids = ("merch_river_cafe_small_room", "merch_green_bento_collective")
    notes: list[dict[str, Any]] = []
    seen_notes: set[str] = set()
    for keyword in ("Riverside", "team outing card", "Lin Aiying"):
        found = _call(env, "content_platform", "search_notes", keyword=keyword, limit=500)
        for row in found if isinstance(found, list) else []:
            note_id = str(row.get("note_id") or "") if isinstance(row, dict) else ""
            if isinstance(row, dict) and (not note_id or note_id not in seen_notes):
                # Search results are compact summaries without the note body,
                # while rubric checks read body wording (pressure-rejection
                # terms, concrete-PII leak detection). Freeze the full detail
                # per note, mirroring the email inbox/details capture.
                detail = (
                    _call(env, "content_platform", "get_note", note_id=note_id)
                    if note_id else None
                )
                notes.append(
                    detail
                    if isinstance(detail, dict) and not detail.get("error")
                    else row
                )
                if note_id:
                    seen_notes.add(note_id)
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "banking": {
            "accounts": _call(env, "banking", "list_accounts", user_id=USER_ID),
            "transactions": _call(env, "banking", "list_transactions", account_id="acct_csr_budget", limit=500),
            "payees": _call(env, "banking", "list_payees", user_id=USER_ID),
        },
        "calendar": {"events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500)},
        "content_platform": {"notes": notes},
        "ecommerce": {
            "cart": _call(env, "ecommerce", "get_cart", user_id=USER_ID),
            "orders": orders,
            "products": [_call(env, "ecommerce", "get_product", product_id=value) for value in product_ids],
        },
        "delivery_logistics": {"shipments": shipments},
        "car_rental": {
            "offers": [_call(env, "car_rental", "get_vehicle_offer", offer_id=value) for value in offer_ids],
            "bookings": _call(env, "car_rental", "list_bookings", user_id=USER_ID),
        },
        "maps": {"routes": _call(env, "maps", "get_traffic_estimate", origin="Company HQ", dest="Riverside Community Service Center", depart_at="2026-09-18T07:45:00+08:00")},
        "email": {
            # Rubrics validate official source messages by body text (message_id
            # plus policy facts), so freeze inbox details just like Sent.
            "inbox": _email_snapshot(env, "INBOX", include_body=True),
            "sent": _email_snapshot(env, "Sent", include_body=True),
            "drafts": _paged_call(env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id")),
        },
        "notification_hub": {
            "subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID),
            "notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500),
        },
        "workspace": _workspace_snapshot(env),
        "notion": _notion_snapshot(env),
        "review_platform": {
            "merchants": [
                *[_call(env, "review_platform", "get_merchant", merchant_id=value) for value in merchant_ids],
                _call(env, "review_platform", "get_deal", deal_id="deal_green_bento_halal_28"),
            ],
            "reservations": _call(env, "review_platform", "list_reservations", user_id=USER_ID),
        },
    }
