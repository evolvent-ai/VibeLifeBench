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

# The scenario's protagonist. Every user-scoped mock API takes ``user_id`` as a
# required argument (``list_accounts``, ``list_calendars``, ``list_applications``,
# ``list_resumes``, ``list_saved_jobs``, ``list_chats``, ``list_saved``) and no
# mock exposes a "list users" tool, so this anchor is the one identity capture
# still knows. Everything *under* it — accounts, positions, symbols, jobs, cases,
# statutes, articles, folders, calendars — is enumerated from the list/search
# tools at capture time instead of being listed here.
USER_ID = "usr_gao_kai"

# The helpers probe alternate spellings of the same person; capture every one of
# them so a per-user lookup is answered from evidence instead of falling through.
USER_IDS = ("usr_gao_kai", "gao_kai")


def _rows(payload: Any, *envelope_keys: str) -> list[Any]:
    """Normalise a list/search tool's decoded payload to its list of rows.

    The mock's list tools ``dumps`` a bare JSON array (``list_accounts``,
    ``list_statute_articles``, ``get_positions``) or an object under one plural
    key (``get_folders`` -> ``{"folders": [...]}``); the search tools
    (``search_jobs``, ``search_cases``, ``search_statutes``) return a paginated
    envelope whose rows sit under ``items``. Every case reduces to a list of
    dict rows; anything else — a scalar, or an ``{"error": ...}`` reply — is
    empty here, so the caller's enumeration simply finds no ids rather than
    crashing on a shape it was not expecting.
    """
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in envelope_keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []


def _row_id(row: dict, *keys: str) -> str | None:
    """First non-null identity among ``keys``, coerced to a string."""
    for key in keys:
        value = row.get(key)
        if value is not None:
            return str(value)
    return None


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid world clock payload")
        return {"world_now": payload["world_now"]}
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


class CaptureError(RuntimeError):
    """The world could not be read, so no snapshot may be published."""


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
    """Read one tool, separating a failed read from a legitimately empty one.

    Three outcomes, not two. A transport failure (the call raises) and a
    server-side failure (``isError``, surfaced as ``McpToolError``) both mean
    *the world was not read*, and abort the capture. A call that returns
    normally is data — including an empty list, which is a real answer: a
    healthy server raises ``JobNotFoundError`` for an absent id, so treating
    every empty read as breakage would reject healthy worlds.

    Recording failures into the snapshot instead — the previous contract — put
    them beyond reach of anyone who could act on them: ``{"error": ...}`` and a
    bare error string both degrade to an empty section downstream, so a dead
    server scored as an idle agent. Measured then: four of the seven servers
    could fail at capture and still yield ``status: ok``. An unpublished
    snapshot stops the run with a diagnosis; a plausible-looking broken one is
    frozen, hashed, and scored as fact.
    """
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        raise CaptureError(f"{server}.{tool}: capability is not available")
    try:
        _v = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            _v,
            lambda p: _decode(cap.call_tool(tool, **{**kwargs, 'page': p})),
        )
    except CaptureError:
        raise
    except BaseException as exc:
        raise CaptureError(f"{server}.{tool}: {type(exc).__name__}: {exc}") from exc


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


def _search_all(
    env: Any, server: str, tool: str, *, id_keys: tuple[str, ...], page_size: int = 100, **kwargs: Any
) -> list[Any]:
    """Walk every page of a paginated search tool and merge the rows.

    The search mocks (``search_jobs``, ``search_cases``, ``search_statutes``)
    return an envelope ``{items, total, page, page_size, has_more}`` whose
    ``limit`` is a batch size, not a data-loss cap: the matching set is counted
    in full before the page window is sliced out, so walking pages until
    ``has_more`` is false recovers the whole set. A bare list — a server that
    does not paginate — is returned as-is, since it already holds every row.
    """
    merged: list[Any] = []
    seen: set[str] = set()
    page = 1
    while True:
        payload = _call(env, server, tool, page=page, limit=page_size, **kwargs)
        rows = _rows(payload, "items")
        if not isinstance(payload, dict):
            merged.extend(rows)
            break
        fresh: list[Any] = []
        for row in rows:
            rid = _row_id(row, *id_keys)
            if rid and rid in seen:
                continue
            if rid:
                seen.add(rid)
            fresh.append(row)
        merged.extend(fresh)
        if not payload.get("has_more"):
            break
        if not fresh:
            break  # has_more misreported, or the page only repeated seen rows
        page += 1
    return merged


def _email_listing(env: Any, folder: str) -> Any:
    return _paged_call(
        env, "email", "get_emails",
        rows_key="emails", id_keys=("email_id", "id"), folder=folder,
    )


def _email_snapshot(env: Any, folder: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Capture a folder's listing plus per-message detail, keyed by message id.

    Detail merges ``read_email`` (body) with ``get_email_headers``
    (``in_reply_to`` / ``references``). Both calls are required: the mock's
    ``read_email`` projection deliberately omits threading headers, but
    ``_helpers.sent_message_matches`` matches ``thread_message_id`` against
    ``in_reply_to``/``references``. Capturing only ``read_email`` therefore makes
    every threaded-reply check unreachable no matter what the agent does — the
    reply is in Sent, correctly threaded in the database, and still scores zero.

    Bodies are captured for every folder, INBOX included. The rubrics read INBOX
    bodies to reconcile the original grant terms against the company's proposal;
    a listing-only INBOX capture makes that comparison unreachable.

    Returns ``(folder_record, details)`` where details is merged into one
    snapshot-wide id→message map, so a lookup never has to know which folder a
    message lives in.
    """
    listing = _email_listing(env, folder)
    if not isinstance(listing, dict):
        return {"listing": listing}, {}
    details: dict[str, Any] = {}
    for item in listing.get("emails") or []:
        if not isinstance(item, dict):
            continue
        email_id = item.get("email_id") or item.get("id")
        if email_id is None:
            continue
        detail = _call(env, "email", "read_email", email_id=str(email_id))
        headers = _call(env, "email", "get_email_headers", email_id=str(email_id))
        if isinstance(detail, dict):
            merged = dict(item)
            merged.update(detail)
            if isinstance(headers, dict):
                merged.update(headers)
        else:
            merged = dict(item)
        # The helpers resolve a message by email_id, id or message_id; index all
        # three spellings so any of them reaches the same frozen record.
        for key in ("email_id", "id", "message_id"):
            value = merged.get(key)
            if value is not None:
                details[str(value)] = merged
    return {"listing": listing}, details


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


def _banking_snapshot(env: Any) -> dict[str, Any]:
    """Every account the user owns, and its full transaction ledger.

    The account list is read from ``list_accounts`` rather than named: a seed
    that adds a second account (or a rubric that reconciles one) is captured
    without anyone having to remember to extend a hand-written scope. The
    equity-buyback reconciliation matches one exact transaction
    (``tx_gk_severance``) on amount, kind, counterparty, memo and posting time,
    so the ledger is captured per account rather than as a flat list.
    """
    accounts = _call(env, "banking", "list_accounts", user_id=USER_ID)
    account_ids = [
        account_id
        for row in _rows(accounts, "accounts")
        if (account_id := _row_id(row, "account_id", "id"))
    ]
    return {
        "accounts": {
            account_id: _call(env, "banking", "get_account", account_id=account_id)
            for account_id in account_ids
        },
        "transactions": {
            account_id: _call(
                env, "banking", "list_transactions", account_id=account_id, limit=400
            )
            for account_id in account_ids
        },
    }


def _brokerage_snapshot(env: Any) -> dict[str, Any]:
    """Positions per account plus a quote for every symbol the positions name.

    Symbols are derived from the positions themselves, so the valuation chain
    is frozen for whatever the world actually holds — a new position is captured
    without a hand-maintained ``TRACKED_SYMBOLS`` scope.
    """
    accounts = _call(env, "brokerage", "list_accounts", user_id=USER_ID)
    account_ids = [
        account_id
        for row in _rows(accounts, "accounts")
        if (account_id := _row_id(row, "account_id", "id"))
    ]
    positions = {
        account_id: _call(env, "brokerage", "get_positions", account_id=account_id)
        for account_id in account_ids
    }
    symbols: list[str] = []
    seen: set[str] = set()
    for payload in positions.values():
        for row in _rows(payload, "positions"):
            symbol = _row_id(row, "symbol")
            if symbol and symbol not in seen:
                seen.add(symbol)
                symbols.append(symbol)
    return {
        "positions": positions,
        "quotes": {
            symbol: _call(env, "brokerage", "get_quote", symbol=symbol)
            for symbol in symbols
        },
    }


def _calendar_snapshot(env: Any) -> dict[str, Any]:
    """Every calendar the user owns, plus every event on each.

    ``list_calendars`` returns a bare array, so the id list is read with
    ``_rows``; the previous dict-only handling saw a list and fell back to an
    empty scope, capturing only the seeded calendar and scoring an agent that
    booked into a calendar it created as if it had booked nothing.
    """
    calendars = _call(env, "calendar", "list_calendars", user_id=USER_ID)
    calendar_ids = [
        calendar_id
        for row in _rows(calendars, "calendars", "results")
        if (calendar_id := _row_id(row, "calendar_id", "id"))
    ]

    events_by_calendar = {
        calendar_id: _call(
            env, "calendar", "list_events", calendar_id=calendar_id, max_results=500
        )
        for calendar_id in calendar_ids
    }
    event_details: dict[str, Any] = {}
    for payload in events_by_calendar.values():
        for row in _rows(payload, "events", "results"):
            event_id = _row_id(row, "event_id", "id")
            if event_id is None:
                continue
            event_details[event_id] = _call(
                env, "calendar", "get_event", event_id=event_id
            )
    return {
        "calendars": calendars,
        "events_by_calendar": events_by_calendar,
        "event_details": event_details,
    }


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
    """Freeze everything the rubrics can ask for at this stage boundary.

    The shape is the contract ``tests/snapshot_env.py`` reads. It is organised by
    *lookup key* rather than by call site — ledgers keyed by account, messages
    keyed by id, events keyed by calendar — because scoring asks "what did
    account X hold" and not "what did the capture happen to call".

    Coverage is driven by the set of ``(server, tool)`` pairs the rubrics
    actually invoke, extracted from ``tests/rubrics`` rather than assembled by
    hand. A tool the rubrics call but this function never captures is not a
    silent zero: ``SnapshotEnv`` raises, so the gap fails the run loudly.

    Scope is *enumerated*, not named. Every id-scoped section is populated from
    the corresponding list/search tool (``list_accounts``, ``search_jobs``,
    ``search_cases``, ``search_statutes``, ``get_folders``, ``list_calendars``),
    so a seed change — a second account, a new position, an added case — is
    captured without anyone editing a hand-written identity list. The only
    identity carried as a constant is the scenario anchor ``USER_ID`` /
    ``USER_IDS``, which the mock APIs require as an argument.
    """
    # Drafts is captured as a folder as well as through get_drafts: the helpers
    # fall back to the folder listing when the drafts tool returns nothing, and
    # an uncaptured folder would make that fallback unscoreable.
    folder_payload = _call(env, "email", "get_folders")
    folder_names = [
        str(name)
        for row in _rows(folder_payload, "folders")
        if (name := row.get("name"))
    ]
    # The three folders the rubrics read are system folders; ensure they are
    # present even if a seed's get_folders omits one, so the listing fallback is
    # always scoreable.
    for required in ("INBOX", "Sent", "Drafts"):
        if required not in folder_names:
            folder_names.append(required)

    email_folders: dict[str, Any] = {}
    email_details: dict[str, Any] = {}
    for name in folder_names:
        folder_record, details = _email_snapshot(env, name)
        email_folders[name] = folder_record
        email_details.update(details)

    job_search = _search_all(env, "job_board", "search_jobs", id_keys=("job_id", "id"))
    job_ids = [
        job_id
        for row in job_search
        if (job_id := _row_id(row, "job_id", "id"))
    ]

    case_search = _search_all(env, "legal_search", "search_cases", id_keys=("case_id", "id"))
    case_ids = [
        case_id
        for row in case_search
        if (case_id := _row_id(row, "case_id", "id"))
    ]
    statute_search = _search_all(env, "legal_search", "search_statutes", id_keys=("statute_id", "id"))
    statute_ids = [
        statute_id
        for row in statute_search
        if (statute_id := _row_id(row, "statute_id", "id"))
    ]
    article_ids: list[str] = []
    for statute_id in statute_ids:
        article_rows = _call(
            env, "legal_search", "list_statute_articles", statute_id=statute_id
        )
        for row in _rows(article_rows, "articles", "results"):
            article_id = _row_id(row, "article_id", "id")
            if article_id and article_id not in article_ids:
                article_ids.append(article_id)

    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "job_board": {
            "applications_by_user": {
                user_id: _call(env, "job_board", "list_applications", user_id=user_id)
                for user_id in USER_IDS
            },
            # No rubric reads a single application's status: applications are
            # observed through list_applications, so no per-id detail is frozen.
            "application_details": {},
            "resumes": _call(env, "job_board", "list_resumes", user_id=USER_ID),
            "saved_jobs": _call(env, "job_board", "list_saved_jobs", user_id=USER_ID),
            "chats": _call(env, "job_board", "list_chats", user_id=USER_ID),
            "search": job_search,
            "jobs": {
                job_id: _call(env, "job_board", "get_job", job_id=job_id)
                for job_id in job_ids
            },
        },
        "email": {
            "folders": email_folders,
            "details": email_details,
            "drafts": _paged_call(
                env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id")
            ),
        },
        "banking": _banking_snapshot(env),
        "brokerage": _brokerage_snapshot(env),
        "calendar": _calendar_snapshot(env),
        "workspace": _workspace_snapshot(env),
        "notion": _notion_snapshot(env),
        "legal_search": {
            "saved_by_user": {
                user_id: _call(env, "legal_search", "list_saved", user_id=user_id)
                for user_id in USER_IDS
            },
            "search": case_search,
            "statute_search": statute_search,
            "cases": {
                case_id: _call(env, "legal_search", "get_case", case_id=case_id)
                for case_id in case_ids
            },
            "statutes": {
                statute_id: _call(env, "legal_search", "get_statute", statute_id=statute_id)
                for statute_id in statute_ids
            },
            "articles": {
                article_id: _call(env, "legal_search", "get_article", article_id=article_id)
                for article_id in article_ids
            },
        },
    }
