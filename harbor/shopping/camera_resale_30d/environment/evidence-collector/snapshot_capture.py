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
    os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json")
)
SCENARIO_CLOCK_REQUIRED = True

USER_ID = "usr_zhan_peng"
CALENDAR_ID = "cal_rscam_task"

# The snapshot-backed rubrics (tests/rubrics/shared/_helpers.py) project each
# historical read onto named channels under the owning service's section; the
# channel keys in ``capture_stage_snapshot`` must match that mapping. These are
# the identifiers the frozen channels are read with.
MAIN_ORDER_ID = "ord_rscam_0001"
SALE_ORDER_ID = "ord_rscam_0002"
MAIN_PRODUCT_ID = "prod_rscam_main"
LISTING_ID = "lst_rscam_0001"
CARD_ID = "card_rscam_01"
ORIGINAL_TRACKING_NO = "SF3521520001CN"
SALE_TRACKING_NO = "YTOSCAM5520002CN"
WEATHER_GEO = "Guangzhou City"


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid world clock payload")
        return {"schema_version": 1, "now": payload["world_now"]}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        raise RuntimeError(f"required world clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}") from exc


# Workspace files shipped as baseline context. The source snapshot excludes them
# so that seeded prose can never be mistaken for the agent's own writing.
BASELINE_WORKSPACE_NAMES = {
    "AGENTS.md",
    "IDENTITY.md",
    "PERSONA.md",
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


def _unwrap_envelope(value: Any, fetch_page: Any = None) -> Any:
    """Flatten the common paginated MCP envelope, fetching every page."""
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value):
        return value
    merged = list(rows)
    total = value.get("total")
    page = int(value.get("page") or 1)
    size = int(value.get("page_size") or len(rows) or 1)
    while value.get("has_more") and fetch_page is not None:
        page += 1
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            value["_pagination_incomplete"] = True
            break
        fresh = nxt["items"]
        if not fresh:
            value["_pagination_incomplete"] = True
            break
        merged.extend(fresh)
        value = nxt
        if total is not None and len(merged) >= int(total):
            break
    if total is not None and len(merged) < int(total):
        value["_pagination_incomplete"] = True
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
        decoded = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            decoded,
            lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
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


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Freeze all eight resale services and durable workspace at a boundary.

    Every channel mirrors one rubric read channel in
    ``tests/rubrics/shared/_helpers.py::_BACKEND_CHANNELS`` — e.g. the cart
    channel exists so ``s8_optimal`` sees the live cart instead of a malformed
    payload, and the two shipment reads sit under ``shipments`` so
    ``track_package`` lookups resolve either tracking number.
    """
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "ecommerce": {
            "main_order": _call(env, "ecommerce", "get_order", order_id=MAIN_ORDER_ID),
            "acceptance_order": _call(env, "ecommerce", "get_order", order_id=SALE_ORDER_ID),
            "main_product": _call(env, "ecommerce", "get_product", product_id=MAIN_PRODUCT_ID),
            "cart": _call(env, "ecommerce", "get_cart", user_id=USER_ID),
        },
        "delivery_logistics": {
            "shipments": [
                _call(env, "delivery_logistics", "track_package", tracking_no=ORIGINAL_TRACKING_NO),
                _call(env, "delivery_logistics", "track_package", tracking_no=SALE_TRACKING_NO),
            ],
        },
        "credit_card": {
            "cards": _call(env, "credit_card", "get_card", card_id=CARD_ID),
            "unbilled": _call(env, "credit_card", "list_unbilled", card_id=CARD_ID),
            "disputes": _call(env, "credit_card", "list_disputes", card_id=CARD_ID),
        },
        "email": {
            "inbox": _email_snapshot(env, "INBOX", include_body=False),
            "sent": _email_snapshot(env, "Sent", include_body=True),
            "drafts": _paged_call(
                env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id")
            ),
        },
        "calendar": {
            "calendars": _call(env, "calendar", "list_calendars", user_id=USER_ID),
            "events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500),
        },
        "notification_hub": {
            "subscriptions": _call(
                env, "notification_hub", "list_subscriptions", user_id=USER_ID
            ),
            "notifications": _call(
                env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500
            ),
        },
        "listing_platform": {
            "settlement": _call(env, "listing_platform", "get_listing_detail", listing_id=LISTING_ID),
        },
        "weather": {
            "current": _call(env, "weather", "get_current_weather", geo=WEATHER_GEO),
            "forecast": _call(env, "weather", "get_forecast_daily", geo=WEATHER_GEO, days=10),
            "alerts": _call(env, "weather", "get_alerts", geo=WEATHER_GEO),
        },
        "workspace": _workspace_snapshot(env),
    }
