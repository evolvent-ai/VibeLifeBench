# hotel-booking-mock

Local FastMCP mock of a hotel booking aggregator (Booking.com Demand /
Expedia Rapid / Hotels.com look-alike). Streamable-HTTP transport, SQLite
state under the env directory, no external traffic.

See [SPEC.md](./SPEC.md) for the schema and tool surface.

## Install

```bash
uv sync
```

Python ≥ 3.12.

## Run

```bash
uv run hotel-booking-mock \
    --env ../../envs/hotel_booking/japan_20d_may \
    --host 0.0.0.0 --port 8000
```

The server listens at `http://<host>:<port>/mcp` (streamable-HTTP).

### CLI flags

| flag       | default     | meaning                                                          |
| ---------- | ----------- | ---------------------------------------------------------------- |
| `--env`    | (required)  | Path to an env directory. The dir's `init.sql` is loaded on boot. |
| `--host`   | `0.0.0.0`   | HTTP bind host                                                   |
| `--port`   | recommended `8000` for Docker/Terrarium parity | HTTP bind port             |
| `--debug`  | `False`     | Enable debug logging                                             |

On cold start the server:

1. Deletes any stale `<env>/runtime.db` (and `-wal` / `-shm` sidecars).
2. Creates the schema.
3. If `<env>/init.sql` exists, executes it.
4. Opens MCP streamable-HTTP.

Every boot is a fresh DB. Rate plans / inventory / reservations are
queried by literal date — the server has no notion of "today".

## Empty env

`envs/hotel_booking/empty/init.sql` is an empty file; the smallest env
that boots the server with no data.

## Smoke test

```bash
uv run python scripts/smoke_http.py
```

Boots the server pointed at the japan_20d_may env, exercises
`search_hotels` → `get_room_availability` → `create_reservation` →
`cancel_reservation`, prints `PASS` on success.

## Agent-facing tools

| tool                         | purpose                                            |
| ---------------------------- | -------------------------------------------------- |
| `search_hotels`              | hotels in a city / geo for a date window           |
| `get_hotel_details`          | full hotel profile incl. policies                  |
| `get_room_availability`      | per-room-type rate plans for a stay window         |
| `create_reservation`         | book a rate_plan_id for a guest profile            |
| `get_reservation`            | fetch a reservation                                |
| `list_reservations`          | list reservations by user_id                       |
| `modify_reservation`         | shift dates / change room type                     |
| `cancel_reservation`         | cancel, returns refund + penalty                   |
| `request_late_checkout`      | request late checkout (auto-approval logic)        |
| `submit_special_request`     | open a request ticket                              |
| `get_user_bookings_summary`  | aggregate user stats                               |

## Layout

```
src/hotel_booking_mock/
  server.py    # FastMCP wiring, streamable-HTTP transport
  tools/       # register_*_tools entry points
  services/    # business logic
  backends/    # SQLite repo
  utils/       # ids, dates, pricing (haversine), exceptions
```
