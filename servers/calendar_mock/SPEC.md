# calendar_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `calendar-mock` MCP server.

## 1. Purpose

`calendar_mock` is a self-contained, fully-offline mock of a
Google-Calendar-style backend — calendars, events, attendees, reminders,
recurring rules. It replaces the legacy Node+PostgreSQL
`Calendar-Autoauth-MCP-Server` with the same agent surface so that
benchmark tasks can exercise an agent's ability to read schedule state,
create/update/delete events, search across events, and react to
deterministic state changes the task orchestrator injects via out-of-band
SQL mutations.

The server makes **no** network calls and ships **no** bundled seed data —
state enters only through `<env>/init.sql` (v3 contract).

Non-goals:

- No real Google Calendar API. Field names mirror the Google shape where
  it's free, but the server is not API-compatible.
- No multi-user permissions or sharing. Identity is whatever the caller
  passes as `user_id` on `list_calendars`.
- No timezone math beyond storing the string. ISO 8601 with an offset is
  the input/output form.
- No i18n.

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`, `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.

## 3. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`,
and surface errors as `{"error": "...", "code": "..."}` rather than raising
across the MCP boundary. Datetimes are ISO 8601 strings; dates are
`YYYY-MM-DD`. IDs are domain-prefixed strings (`cal_…`, `evt_…`).

### 3.1 `list_calendars(user_id) -> str`

```json
[
  {"calendar_id": "cal_000001", "user_id": "usr_li_wei",
   "name": "Personal", "color": "#4285F4", "timezone": "Asia/Shanghai",
   "is_primary": true, "created_at": "2024-01-01T00:00:00Z"},
  ...
]
```

Order: `is_primary DESC, created_at ASC, calendar_id ASC`.

### 3.2 `list_events(time_min?, time_max?, calendar_id?, max_results=20, order_by="startTime") -> str`

Returns events overlapping the half-open window `[time_min, time_max)`.
An event overlaps the window if `end_dt > time_min AND start_dt < time_max`.
Without `time_min`/`time_max` no bound is applied. `calendar_id`, if
present, scopes to a single calendar. `order_by` is one of `startTime`
(ASC) or `updated` (DESC). `max_results` defaults to 20, clamped to 500.

Each item has the same shape as `get_event` below.

### 3.3 `get_event(event_id, calendar_id?) -> str`

Full event detail, attendees + reminders included.

```json
{
  "event_id": "evt_00000001",
  "calendar_id": "cal_000001",
  "summary": "妈妈生日",
  "description": "...",
  "location": "...",
  "start": {"dateTime": "2026-05-08T18:30:00+08:00"},
  "end":   {"dateTime": "2026-05-08T21:00:00+08:00"},
  "all_day": false,
  "status": "confirmed",
  "created_at": "2026-04-01T09:00:00Z",
  "updated_at": "2026-04-01T09:00:00Z",
  "recurrence_rule": null,
  "parent_event_id": null,
  "attendees": [
    {"email": "zhangfang@example.com", "name": "妈妈", "response_status": "accepted"},
    ...
  ],
  "reminders": [
    {"method": "email", "minutes_before": 1440},
    {"method": "popup", "minutes_before": 60}
  ]
}
```

If `calendar_id` is supplied and does not match, returns `EVENT_NOT_FOUND`.

### 3.4 `create_event(summary, start, end, description?, location?, calendar_id?, attendees?, reminders?) -> str`

`start` and `end` are ISO 8601 datetime strings. `end` must be strictly
after `start` (`BAD_TIME_RANGE` otherwise). If `calendar_id` is omitted
the user's primary calendar is used; if no primary exists the oldest
calendar wins. If no calendars exist at all, `BAD_ARG`.

`attendees` is `[{email, name?, response_status?}]` where
`response_status` ∈ `{needsAction, accepted, declined, tentative}`
(default `needsAction`).

`reminders` is `[{minutes_before, method?}]` where `method` ∈
`{popup, email}` (default `popup`) and `minutes_before` is a non-negative
integer.

Returns the same shape as `get_event`.

### 3.5 `update_event(event_id, summary?, start?, end?, description?, location?, calendar_id?, status?) -> str`

Only the supplied fields change. `description` and `location` accept the
empty string to clear the value (the field is overwritten only when the
argument is explicitly provided — `None` means "don't touch"). If both
`start` and `end` are touched they're validated together; if only one is
touched, validation uses the existing value of the other.

`status` ∈ `{confirmed, tentative, cancelled}`. To move an event between
calendars set `calendar_id`. Returns the updated event.

### 3.6 `delete_event(event_id, calendar_id?) -> str`

Hard delete. Cascades to `attendees` and `reminders` via FK. If
`calendar_id` is supplied and does not match, returns `EVENT_NOT_FOUND`.

```json
{"event_id": "evt_...", "deleted": true}
```

### 3.7 `search_events(query, time_min?, time_max?, max_results=50) -> str`

Case-insensitive substring match across `summary`, `description`,
`location`, and joined `attendees.email`/`attendees.name`. Optional
time-window restricts to overlap (same predicate as `list_events`). Same
return shape as `list_events`.

## 4. Storage

SQLite, one file per server (`<env>/runtime.db`). `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL`.

| table        | purpose                                                              |
| ------------ | -------------------------------------------------------------------- |
| `calendars`  | per-user calendars                                                   |
| `events`     | event rows; `recurrence_rule` is stored verbatim (no materialization) |
| `attendees`  | per-event invitee rows; cascade-deleted with the event               |
| `reminders`  | per-event reminders; cascade-deleted with the event                  |
| `_counters`  | atomic seq counters used to mint stable IDs                          |

Indices: `(calendar_id, start_dt)` and `start_dt` on `events`,
`parent_event_id` on `events`, `event_id` on `attendees` / `reminders`.

The server carries no notion of "today"; date comparisons fall back to the
literal datetime strings the agent supplies.

## 5. State injection

On cold start the server writes a fresh `<env>/runtime.db`, applies the
bundled schema, then executes `<env>/init.sql` if present. The package
ships no bundled seed data.

## 6. Stage progression

No in-server clock walk. Date-keyed rows are pre-baked by `init.sql`.
Stage transitions arrive through the orchestrator's event-overlay
channel as raw SQL applied directly against `runtime.db`.

## 7. Logging & ops

- `logging.getLogger(__name__)` everywhere; handler attached to stderr only.
- No `print()` in the package.

## 8. Appendix — error codes

| code                | meaning                                                              |
| ------------------- | -------------------------------------------------------------------- |
| `EVENT_NOT_FOUND`   | `event_id` does not exist (or does not belong to `calendar_id`)      |
| `CALENDAR_NOT_FOUND`| `calendar_id` does not exist                                         |
| `BAD_TIME_RANGE`    | `end` is not strictly after `start`                                  |
| `BAD_DATE`          | non-ISO date/datetime string                                         |
| `OVERLAPPING_EVENT` | reserved (not raised in v1)                                          |
| `BAD_ARG`           | catch-all for malformed inputs                                       |

## 9. Out of scope

- No iCalendar import / export.
- No RRULE expansion. `recurrence_rule` is stored verbatim for round-tripping; the server does not materialize child instances.
- No pagination cursors (`max_results` only).
- No conflict detection between events (the `OVERLAPPING_EVENT` code is
  reserved for a future version).
- No real auth, no permission enforcement beyond `user_id` scoping on
  `list_calendars`.
