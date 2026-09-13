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
SCENARIO_CLOCK_REQUIRED = True

USER_ID = "user_lin_zeyu"
CALENDAR_ID = "cal_lin_primary"


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid scenario clock payload")
        return {"schema_version": 1, "now": payload["world_now"]}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        raise RuntimeError(f"required world clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}") from exc


# Copied verbatim from the source task.py. The rubrics assert on these exact ids.
# Jobs are inserted progressively by releases, so a tracked id is not guaranteed
# to exist at every stage boundary; the capture records those as null instead of
# failing (NOT_FOUND_CODES below).
TRACKED_JOB_IDS = (
    "portal_retake_notice_2026", "portal_defer_rules_2026",
    "portal_grade_review_rules_2026", "campus_defer_application_2026",
    "portal_room_table_2026", "portal_math_outline_v2", "portal_mock_quiz_0912",
    "portal_seat_table_0915", "portal_score_report_0921",
)

# Mock error codes meaning "this tracked entity does not exist (yet)" — a
# legitimate world state for a speculative capture, not a read failure. Every
# other error stays fail-closed.
NOT_FOUND_CODES = ("NOT_FOUND", "JOB_NOT_FOUND", "APPLICATION_NOT_FOUND")

DECLARED_SERVICES = (
    "job_board", "email", "calendar", "notification_hub", "notion",
)

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
            raise RuntimeError(
                f"paginated capture incomplete: captured {len(merged)} of {total} rows"
            )
    return merged


def _tool_value(
    cap: Any,
    server: str,
    tool: str,
    kwargs: dict[str, Any],
    tolerate_missing: tuple[str, ...] = (),
) -> Any:
    try:
        raw = cap.call_tool(tool, **kwargs)
    except Exception as exc:
        raise RuntimeError(
            f"MCP read failed: {server}.{tool}: {type(exc).__name__}: {exc}"
        ) from exc
    if bool(getattr(raw, "isError", False)) or bool(getattr(raw, "is_error", False)):
        raise RuntimeError(f"MCP read failed: {server}.{tool} returned isError=true")
    value = _decode(raw)
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            raise RuntimeError(f"MCP read failed: {server}.{tool} returned isError=true")
        if value.get("error") not in (None, False, ""):
            if value.get("code") in tolerate_missing:
                return None
            raise RuntimeError(f"MCP read failed: {server}.{tool}: {value['error']}")
    return value


def _call(
    env: Any, server: str, tool: str, tolerate_missing: tuple[str, ...] = (), **kwargs: Any
) -> Any:
    """Read one declared capability and fail closed on read errors."""
    if server not in DECLARED_SERVICES:
        raise RuntimeError(f"undeclared capability requested during capture: {server}")
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        raise RuntimeError(f"missing declared capability: {server}")
    value = _tool_value(cap, server, tool, kwargs, tolerate_missing=tolerate_missing)
    return _unwrap_envelope(
        value,
        lambda p: _tool_value(cap, server, tool, {**kwargs, "page": p}),
    )


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
        if len(merged) < total:
            raise RuntimeError(
                f"MCP read incomplete: {server}.{tool} captured {len(merged)} of {total} rows"
            )
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
    if not isinstance(listing, dict):
        raise RuntimeError(f"email.get_emails returned an invalid {folder} listing")
    if not include_body:
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
            raise RuntimeError("notion search/query returned an invalid result")
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
    """Verbatim port of the source ``_capture_stage_snapshot``."""
    missing = [server for server in DECLARED_SERVICES if getattr(env, f"{server}_mock", None) is None]
    if missing:
        raise RuntimeError(f"missing declared capabilities: {', '.join(missing)}")
    applications = _call(env, "job_board", "list_applications", user_id=USER_ID)
    application_rows = [
        row for row in (applications if isinstance(applications, list) else [])
        if isinstance(row, dict) and row.get("application_id") is not None
    ]
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "job_board": {
            "applications": applications,
            # Details are read for the applications that actually exist in the
            # world; speculatively probing hard-coded ids would only observe
            # APPLICATION_NOT_FOUND for ids no seed or release ever creates.
            "application_details": {
                str(row["application_id"]): _call(
                    env,
                    "job_board",
                    "get_application_status",
                    application_id=str(row["application_id"]),
                )
                for row in application_rows
            },
            "resumes": _call(env, "job_board", "list_resumes", user_id=USER_ID),
            "saved_jobs": _call(env, "job_board", "list_saved_jobs", user_id=USER_ID),
            "chats": _call(env, "job_board", "list_chats", user_id=USER_ID),
            "jobs": {
                job_id: _call(
                    env, "job_board", "get_job", job_id=job_id,
                    tolerate_missing=NOT_FOUND_CODES,
                )
                for job_id in TRACKED_JOB_IDS
            },
        },
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
        "workspace": _workspace_snapshot(env),
        "notion": _notion_snapshot(env),
    }
