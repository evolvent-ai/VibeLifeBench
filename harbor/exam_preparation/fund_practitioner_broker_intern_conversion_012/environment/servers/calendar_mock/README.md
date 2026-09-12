# calendar-mock

A FastMCP-based, fully-offline mock of a Google-Calendar-style backend. Runs
over **streamable-HTTP** (no stdio) with a local SQLite database. Replaces
the legacy Node + PostgreSQL `Calendar-Autoauth-MCP-Server` with the same
agent-facing surface.

See [SPEC.md](./SPEC.md) for the full implementer-facing specification.

## Tools (agent-facing)

- `list_calendars(user_id)` — calendars owned by a user.
- `list_events(time_min?, time_max?, calendar_id?, max_results=20, order_by="startTime")`
- `get_event(event_id, calendar_id?)` — full detail incl. attendees + reminders.
- `create_event(summary, start, end, description?, location?, calendar_id?, attendees?, reminders?)`
- `update_event(event_id, summary?, start?, end?, description?, location?, calendar_id?, status?)`
- `delete_event(event_id, calendar_id?)`
- `search_events(query, time_min?, time_max?, max_results=50)` — substring
  match over summary / description / location / attendee email or name.

No admin tool / no clock. Recurring events store an `recurrence_rule` for
round-tripping but are not auto-materialized — env init.sql is responsible
for inserting whichever concrete child rows the task needs.

`start` / `end` are ISO 8601 datetimes (e.g. `2026-05-08T18:30:00+08:00`).

## Quick start

### Direct (Python)

```bash
# From this directory
pip install -e .

# Run against the bundled env.
calendar-mock \
  --port 8000 \
  --env ../../envs/calendar/li_wei_may
```

The server writes a fresh `runtime.db` inside the env directory on every
cold start, applies the bundled schema, then executes
`<env>/init.sql` if present.

### Docker

```bash
docker build -t calendar-mock .
docker run --rm -p 8000:8000 \
  -v $PWD/../../envs/calendar/li_wei_may:/env-seed:ro \
  calendar-mock
```

The streamable-HTTP endpoint is at `http://<host>:<port>/mcp`.

## CLI flags

- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--env PATH` — env directory (`runtime.db` lives inside; optional `init.sql` is applied)
- `--debug` — verbose logging

To boot stateless, point `--env` at `../../envs/calendar/empty`.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess on a free port, applies
`envs/calendar/li_wei_may/init.sql`, and round-trips
`list_calendars`, `list_events`, `get_event`, `search_events`,
`create_event`, `update_event`, `delete_event`, plus error paths. Prints
`PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`EVENT_NOT_FOUND`, `CALENDAR_NOT_FOUND`, `BAD_TIME_RANGE`, `BAD_DATE`,
`OVERLAPPING_EVENT`, `BAD_ARG`.
