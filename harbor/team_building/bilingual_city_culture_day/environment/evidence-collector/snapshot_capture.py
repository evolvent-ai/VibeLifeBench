"""Capture the authoritative stage-boundary world through MCP.

The world-controller invokes this module only in its sidecar phase. All world
mutations visible to the step were applied before the agent turn; no trailing
mutation is allowed between response collection and snapshot publication. The returned dictionary is written directly into the
private evidence volume; this module never materializes historical files in the
agent workspace.

The snapshot must expose every backend the rubric helpers address through
``_helpers.call_tool`` — banking, calendar, email, maps, notification_hub,
notion, review_platform and weather — keyed exactly the way those helpers look
them up (``accounts``/``transactions``/``pending_payments`` under banking,
``events`` under calendar, ``notifications``/``subscriptions`` under
notification_hub, ``reservations``/``saved_merchants``/``deals`` under
review_platform, ``pages`` under notion). A backend missing from this dict makes
``_server_snapshot`` raise "snapshot has no <server> backend", which aborts the
whole trial as a verifier infrastructure error instead of scoring the agent.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

WORLD_CLOCK_PATH = Path(
    os.environ.get("WORLD_CLOCK_PATH", "/world-clock/current.json")
)
WORLD_CLOCK_REQUIRED = os.environ.get("WORLD_CLOCK_REQUIRED", "0") == "1"

USER_ID = "usr_gn_m4xqpa"
CALENDAR_ID = "cal_gz_w9rkmq"

# Vendors whose Q&A and deals the rubric helpers trace back into the snapshot.
TRACKED_MERCHANT_IDS = (
    "mer_yuexiu_bilingual_walk",
    "mer_huifu_dim_sum_studio",
)
# Deals referenced by the guide/dim-sum holds; get_deal lookups resolve from
# this map (release-000 inserts the first two, the seed ships the dim-sum one).
TRACKED_DEAL_IDS = (
    "deal_yuexiu_walk_group33",
    "deal_yuexiu_stepfree_review",
    "deal_huifu_dim_sum_group33",
)
# Places along the candidate route (office -> Yuexiu assembly point).
TRACKED_PLACE_IDS = ("pl_gz_office", "pl_yuexiu_route")
# Weather location the scenario uses (geo_key yuexiu_old_city / city name).
WEATHER_GEO = "Guangzhou Yuexiu"


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_PATH.read_text(encoding="utf-8"))
        if not isinstance(payload.get("step"), str) or not isinstance(payload.get("now"), str):
            raise ValueError("invalid scenario clock payload")
        return {"schema_version": 1, "step": payload["step"], "now": payload["now"]}
    except Exception as exc:
        if WORLD_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {WORLD_CLOCK_PATH}: {exc}"
            ) from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}


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
        return _decode(cap.call_tool(tool, **kwargs))
    except BaseException as exc:  # noqa: BLE001 - parity with source behaviour
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(
    env: Any,
    server: str,
    tool: str,
    *,
    rows_key: str,
    id_keys: tuple[str, ...],
    page_size_kw: str = "page_size",
    page_size: int = 200,
    **kwargs: Any,
) -> Any:
    """Walk every page of a paginated tool and merge the rows.

    The email mock clamps ``page_size`` to 50 (``utils/validators.py``) and
    signals the clamp only by echoing the applied value, so one large request
    silently returns a prefix: the seeded INBOX holds 48 messages, of which a
    single small request would capture only a prefix. Evidence that never enters
    the snapshot can never be scored, so the walk continues until the accumulated
    rows reach the reported total. Rows are merged back into the first page's
    envelope, leaving the stored shape unchanged for consumers.

    ``page_size_kw`` adapts the walk to each mock's own spelling of the page
    size argument (email uses ``page_size``; banking uses ``limit``).
    """
    size_kw = {page_size_kw: page_size}
    first = _call(env, server, tool, page=1, **size_kw, **kwargs)
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
    applied = int(first.get("page_size") or first.get("limit") or 0) or max(len(merged), 1)
    raw_total = first.get("total_results", first.get("total"))
    total = int(raw_total) if isinstance(raw_total, (int, float)) else None
    seen = {_row_id(row) for row in merged}
    page = 2
    # The folder cannot need more pages than it has rows; +1 tolerates a total
    # that grew between calls rather than silently stopping short.
    max_pages = ((total + applied - 1) // applied + 1) if total else 1
    while total is not None and len(merged) < total and page <= max_pages:
        nxt = _call(env, server, tool, page=page, **{page_size_kw: applied}, **kwargs)
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


def _banking_snapshot(env: Any) -> dict[str, Any]:
    """Accounts, payees, pending payments and the merged transaction log.

    ``_helpers.banking_transactions`` asks for ``list_transactions`` per account
    and flattens the rows itself, so the snapshot stores one flat row list under
    ``transactions``; a per-account nested dict would defeat ``_rows``.
    """
    accounts = _call(env, "banking", "list_accounts", user_id=USER_ID)
    transactions: list[Any] = []
    for account in accounts if isinstance(accounts, list) else []:
        account_id = account.get("account_id") if isinstance(account, dict) else None
        if not account_id:
            continue
        rows = _paged_call(
            env, "banking", "list_transactions",
            rows_key="items", id_keys=("tx_id",), page_size_kw="limit",
            account_id=account_id,
        )
        if isinstance(rows, dict):
            transactions.extend(row for row in rows.get("items") or [] if isinstance(row, dict))
    return {
        "accounts": accounts,
        "payees": _call(env, "banking", "list_payees", user_id=USER_ID),
        "pending_payments": _paged_call(
            env, "banking", "list_pending_payments",
            rows_key="items", id_keys=("pending_id",), page_size_kw="limit",
            user_id=USER_ID,
        ),
        "transactions": transactions,
    }


def _review_platform_snapshot(env: Any) -> dict[str, Any]:
    """Saved merchants, reservations, plus per-vendor deals/QA lookups.

    ``_helpers.call_tool`` resolves ``get_deal`` against the ``deals`` mapping,
    so deals are stored keyed by deal id — seeded holds and the release-inserted
    guide/step-free deals alike. ``list_merchant_deals`` for the tracked vendors
    also feeds the map, so a deal added by a release is never missed.
    """
    deal_ids = list(TRACKED_DEAL_IDS)
    for merchant_id in TRACKED_MERCHANT_IDS:
        listing = _call(env, "review_platform", "list_merchant_deals", merchant_id=merchant_id)
        rows = listing if isinstance(listing, list) else (listing or {}).get("items") if isinstance(listing, dict) else []
        for row in rows or []:
            if isinstance(row, dict) and row.get("deal_id"):
                deal_id = str(row["deal_id"])
                if deal_id not in deal_ids:
                    deal_ids.append(deal_id)
    deals = {
        deal_id: _call(env, "review_platform", "get_deal", deal_id=deal_id)
        for deal_id in deal_ids
    }
    return {
        "saved_merchants": _call(env, "review_platform", "list_saved_merchants", user_id=USER_ID),
        "reservations": _call(env, "review_platform", "list_reservations", user_id=USER_ID),
        "deals": deals,
        "merchants": {
            merchant_id: _call(env, "review_platform", "get_merchant", merchant_id=merchant_id)
            for merchant_id in TRACKED_MERCHANT_IDS
        },
        "merchant_qa": {
            merchant_id: _call(env, "review_platform", "get_merchant_qa", merchant_id=merchant_id)
            for merchant_id in TRACKED_MERCHANT_IDS
        },
    }


def _maps_snapshot(env: Any) -> dict[str, Any]:
    """Route places with live alerts plus the driving route between them."""
    return {
        "places": {
            place_id: _call(env, "maps", "get_place_details", place_id=place_id)
            for place_id in TRACKED_PLACE_IDS
        },
        "directions": _call(
            env, "maps", "directions",
            origin="pl_gz_office", dest="pl_yuexiu_route", mode="driving",
        ),
    }


def _weather_snapshot(env: Any) -> dict[str, Any]:
    """Active severe-weather alerts for the scenario location."""
    return {"alerts": _call(env, "weather", "get_alerts", geo=WEATHER_GEO)}


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Freeze every scored backend of this task at the stage boundary."""
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "email": {
            "inbox": _email_snapshot(env, "INBOX", include_body=False),
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
        "banking": _banking_snapshot(env),
        "review_platform": _review_platform_snapshot(env),
        "maps": _maps_snapshot(env),
        "weather": _weather_snapshot(env),
        "workspace": _workspace_snapshot(env),
        "notion": _notion_snapshot(env),
    }
