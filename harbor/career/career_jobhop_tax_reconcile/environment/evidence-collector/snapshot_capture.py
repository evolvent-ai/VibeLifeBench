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

WORLD_CLOCK_FILE = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
WORLD_CLOCK_REQUIRED = True

USER_ID = "usr_gao_kai"
CALENDAR_ID = "cal_gk_0001"
CHECKING_ACCOUNT = "acct_gk_checking"


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"world_now"}:
            raise ValueError("invalid scenario clock payload")
        return {"schema_version": 1, "step": os.environ.get("HARBOR_STEP_NAME", "unknown"), "now": payload["world_now"]}
    except Exception as exc:
        if WORLD_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {WORLD_CLOCK_FILE}: {exc}"
            ) from exc
        raise RuntimeError(f"required world clock unavailable at {WORLD_CLOCK_FILE}: {exc}") from exc


# IDs used by this task's rubrics and seeded corpus. The rubrics assert on
# these exact ids, so the snapshot must resolve each of them.
TRACKED_JOB_IDS = (
    "job_4f91c2a8d7e3",
    "job_a17e5c903bd4",
    "job_6c2d8f14b9a7",
)

TRACKED_APPLICATION_IDS = (
    "app_000000",
    "app_000001",
)

TRACKED_LEGAL_IDS = {
    "cases": (
        "case_kq_missing_month",
        "case_kq_false_delete",
        "case_kq_net_gross",
    ),
    "statutes": (
        "stat_kq_iit_settlement_admin",
        "stat_kq_admin",
        "stat_kq_iit_law",
        "stat_kq_withholding",
    ),
    "articles": (
        "art_kq_admin_retention",
        "art_kq_period",
        "art_kq_iit_comprehensive",
        "art_kq_annual",
        "art_kq_2025_booking",
        "art_kq_appeal",
        "art_kq_authorization",
        "art_kq_prepare",
        "art_kq_refund_account",
        "art_kq_truth",
        "art_kq_withhold_info",
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


def _banking_transactions(env: Any, account_id: str) -> list[dict[str, Any]]:
    """Flat transaction rows for one account.

    ``list_transactions`` answers with a paged ``{"items": [...]}`` envelope,
    but the rubric evidence fallback reads ``banking.transactions`` verbatim as
    a row list, so the envelope is flattened here at capture time.
    """
    envelope = _call(env, "banking", "list_transactions", account_id=account_id, limit=500)
    rows = envelope.get("items") if isinstance(envelope, dict) else envelope
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


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
    """Verbatim port of the source ``_capture_stage_snapshot``."""
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "job_board": {
            "applications": _call(env, "job_board", "list_applications", user_id=USER_ID),
            "application_details": {
                application_id: _call(
                    env, "job_board", "get_application_status", application_id=application_id
                )
                for application_id in TRACKED_APPLICATION_IDS
            },
            "resumes": _call(env, "job_board", "list_resumes", user_id=USER_ID),
            "saved_jobs": _call(env, "job_board", "list_saved_jobs", user_id=USER_ID),
            "chats": _call(env, "job_board", "list_chats", user_id=USER_ID),
            "jobs": {
                job_id: _call(env, "job_board", "get_job", job_id=job_id)
                for job_id in TRACKED_JOB_IDS
            },
        },
        "banking": {
            "accounts": _call(env, "banking", "list_accounts", user_id=USER_ID),
            "transactions": _banking_transactions(env, CHECKING_ACCOUNT),
        },
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
