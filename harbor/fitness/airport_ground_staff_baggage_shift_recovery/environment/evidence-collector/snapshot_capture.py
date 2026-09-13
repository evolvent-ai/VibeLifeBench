"""Capture the authoritative stage-boundary world through MCP.

The world-controller invokes this module only in its sidecar phase. All world
mutations visible to the step were applied before the agent turn; no trailing
mutation is allowed between response collection and snapshot publication. The
returned dictionary is written directly into the private evidence volume; this
module never materializes historical files in the agent workspace.

The captured sections are this task's own contract — the five services wired in
``docker-compose.yaml`` (calendar, email, health_tracker, notion, weather), read
as user ``li_ming`` — shaped for what ``tests/rubrics/_helpers.py`` reads:

* ``calendar.events`` — rows from BOTH seeded calendars, each keeping its
  ``calendar_id`` (personal planning vs. the authoritative airport roster);
* ``health_tracker`` — every metric type plus the workout log, each row
  projecting its timestamp under ``date``/``timestamp`` (the rubrics window by
  those keys; the mock stores ``recorded_at``/``started_at``);
* ``email`` — folder listings with each message's ``read_email`` body and
  threading headers merged in (the listing is metadata-only, but the rubrics
  match body facts such as reply deadlines against the row blob);
* ``weather.alerts`` — active alerts for the seeded apron location.

Every read lands in the snapshot exactly as the service answered it. A failed
capability read therefore freezes as ``{"error": ...}`` — diagnosable, and the
controller refuses to publish a snapshot that carries one.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

SCENARIO_CLOCK_PATH = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
SCENARIO_CLOCK_REQUIRED = True

USER_ID = "li_ming"
CAL_PERSONAL = "cal_liming_personal"
CAL_ROSTER = "cal_airport_roster"
CALENDARS = (CAL_PERSONAL, CAL_ROSTER)
ALERT_GEO = "pvg_apron"

# The mock accepts exactly these metric types (health_tracker_mock
# _metric_meta.METRIC_TYPES); each is paged in full and merged.
METRIC_TYPES = (
    "weight",
    "steps",
    "heart_rate",
    "sleep_minutes",
    "blood_pressure",
    "body_fat",
    "finger_pain",
    "score",
)

# The rubrics window events across the whole cycle (2026-07 .. 2026-08) and the
# seeded history starts in June, so freeze a superset window; the checks
# re-filter by each row's start/end themselves.
CALENDAR_WINDOW = {
    "time_min": "2026-06-01T00:00:00+08:00",
    "time_max": "2026-09-30T23:59:00+08:00",
    "max_results": 500,
}


def scenario_clock() -> dict[str, Any]:
    try:
        payload = json.loads(SCENARIO_CLOCK_PATH.read_text(encoding="utf-8"))
        if set(payload) != {"world_now"} or not isinstance(payload.get("world_now"), str):
            raise ValueError("invalid scenario clock payload")
        parsed = datetime.fromisoformat(payload["world_now"].replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("scenario clock must include an offset")
        return {"schema_version": 1, "step": "unknown", "now": parsed.isoformat()}
    except Exception as exc:
        if SCENARIO_CLOCK_REQUIRED:
            raise RuntimeError(
                f"required scenario clock unavailable at {SCENARIO_CLOCK_PATH}: {exc}"
            ) from exc
        return {"schema_version": 1, "step": "unknown", "now": ""}


# Workspace files shipped as baseline context. The snapshot excludes them so
# that seeded prose can never be mistaken for the agent's own writing; the
# agent-facing derived ledgers (stage_progress.md, risk_log.md, ...) are
# captured because the rubrics score what the agent durably wrote there.
BASELINE_WORKSPACE_NAMES = {
    "AGENTS.md",
    "BUDGET_AUTH.md",
    "HEALTH_BOUNDARIES.md",
    "IDENTITY.md",
    "PERSONA.md",
    "PRIVACY_AND_AUTH.md",
    "SOUL.md",
    "TOOLS.md",
    "TRAINING_PRINCIPLES.md",
    "USER.md",
}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")


def _decode(value: Any) -> Any:
    """Decode JSON-in-string tool results."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page: Any = None) -> Any:
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value):
        return value
    merged = list(rows)
    page = int(value.get("page") or 1) + 1
    total = value.get("total")
    while value.get("has_more") and fetch_page is not None and (not isinstance(total, int) or len(merged) < total):
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
        page += 1
    if value.get("has_more"):
        value["_pagination_incomplete"] = True
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    """Never raise, record the error.

    A failed capability read must land in the snapshot as ``{"error": ...}``,
    so a broken server produces a snapshot the controller refuses to publish
    with a diagnosable cause instead of silently freezing an empty world.
    """
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        decoded = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(decoded, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
    except BaseException as exc:  # noqa: BLE001 - capture must not abort the sidecar
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(
    env: Any, server: str, tool: str, *, rows_key: str, id_keys: tuple[str, ...], **kwargs: Any
) -> Any:
    """Walk every page of a paginated tool and merge the rows.

    The email mock clamps ``page_size`` to 50 (``utils/validators.py``) and
    signals the clamp only by echoing the applied value, so one large request
    silently returns a prefix. Evidence that never enters the snapshot can
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


def _calendar_snapshot(env: Any) -> dict[str, Any]:
    """Events from both seeded calendars, rows keeping their ``calendar_id``.

    The rubrics address personal planning and the authoritative airport roster
    as separate calendars; capturing a single calendar id would freeze either
    an empty world or a mixed one, and every roster-preservation check would
    read the wrong rows.
    """
    events: list[Any] = []
    for calendar_id in CALENDARS:
        rows = _call(env, "calendar", "list_events", calendar_id=calendar_id, **CALENDAR_WINDOW)
        for row in rows if isinstance(rows, list) else []:
            if isinstance(row, dict):
                row.setdefault("calendar_id", calendar_id)
                events.append(row)
    return {"events": events, "calendar_ids": list(CALENDARS)}


def _health_snapshot(env: Any) -> dict[str, Any]:
    """Every metric type plus the workout log, with a ``date`` projection.

    The mock exposes timestamps as ``recorded_at`` / ``started_at``; the rubrics
    window rows by ``date`` or ``timestamp``, so each frozen row carries the
    same instant under the contract key. Without the projection every
    since/until filter drops every row and all health checks read an empty
    tracker no matter what the agent did.
    """
    metrics: list[Any] = []
    for metric_type in METRIC_TYPES:
        rows = _call(
            env, "health_tracker", "get_metrics",
            user_id=USER_ID, type=metric_type, limit=1000,
        )
        for row in rows if isinstance(rows, list) else []:
            if isinstance(row, dict):
                row.setdefault("date", row.get("recorded_at"))
                row.setdefault("timestamp", row.get("recorded_at"))
                metrics.append(row)
    workouts: list[Any] = []
    workout_rows = _call(env, "health_tracker", "list_workouts", user_id=USER_ID, limit=500)
    for row in workout_rows if isinstance(workout_rows, list) else []:
        if isinstance(row, dict):
            row.setdefault("date", row.get("started_at"))
            row.setdefault("timestamp", row.get("started_at"))
            workouts.append(row)
    return {"metrics": metrics, "workouts": workouts}


def _email_listing(env: Any, folder: str) -> Any:
    return _paged_call(
        env, "email", "get_emails",
        rows_key="emails", id_keys=("email_id", "id"), folder=folder,
    )


def _email_snapshot(env: Any, folder: str) -> dict[str, Any]:
    """Folder listing with per-message bodies merged into the listing rows.

    ``get_emails`` returns metadata only. The rubrics match message facts
    (deadlines, quoted instructions such as the 18:00 reply-by time) against the
    row blob, so the frozen listing must carry each message's ``read_email``
    projection and its threading headers — otherwise every inbox message reads
    as header-only and the email checks fail no matter what the agent did. The
    raw per-message reads are additionally kept under ``details``. A failed
    per-message read is recorded on its row without poisoning the folder (one
    unreadable body must not void the whole stage), so it uses a dedicated key
    rather than the fatal ``{"error": ...}`` shape.
    """
    listing = _email_listing(env, folder)
    details: list[Any] = []
    if isinstance(listing, dict):
        for item in listing.get("emails") or []:
            if not isinstance(item, dict):
                continue
            email_id = item.get("email_id") or item.get("id")
            if email_id is None:
                continue
            detail = _call(env, "email", "read_email", email_id=str(email_id))
            headers = _call(env, "email", "get_email_headers", email_id=str(email_id))
            if isinstance(detail, dict) and "error" not in detail:
                for key in ("body_text", "body_html", "attachments"):
                    if detail.get(key) is not None:
                        item.setdefault(key, detail[key])
            elif isinstance(detail, dict):
                item["detail_capture_error"] = str(detail["error"])
            if isinstance(headers, dict) and "error" not in headers:
                for key in ("in_reply_to", "references"):
                    if headers.get(key) is not None:
                        item.setdefault(key, headers[key])
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


def _weather_snapshot(env: Any) -> dict[str, Any]:
    """Active alerts for the seeded apron location.

    ``weather_alert_matches`` greps the alert rows for id/kind/severity/window
    plus description terms; the apron geo is the seeded location both task
    alerts cover, so the list under ``alerts`` is the whole contract (the
    verifier-side reader answers any geo from this one merged list).
    """
    return {"alerts": _call(env, "weather", "get_alerts", geo=ALERT_GEO)}


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Freeze this stage's five-service world for the rubrics."""
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(),
        "user_id": USER_ID,
        "calendar": _calendar_snapshot(env),
        "email": {
            "inbox": _email_snapshot(env, "INBOX"),
            "sent": _email_snapshot(env, "Sent"),
            "drafts": _paged_call(
                env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id")
            ),
        },
        "health_tracker": _health_snapshot(env),
        "workspace": _workspace_snapshot(env),
        "notion": _notion_snapshot(env),
        "weather": _weather_snapshot(env),
    }
