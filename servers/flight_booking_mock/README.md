# flight-booking-mock

FastMCP **streamable-HTTP** server that emulates Amadeus-style flight search /
booking / order-management APIs. **Pure local mock** — no network egress, no
upstream GDS, all state in a single SQLite file.

Source of truth: [`SPEC.md`](./SPEC.md).

## Install

```bash
uv sync
```

Requires Python ≥ 3.12.

## Run

```bash
uv run flight-booking-mock \
    --env ../../envs/flight_booking/japan_20d_may \
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

Every boot is a fresh DB. There is no clock advancement; date-keyed rows
(`flights.depart_dt`, `flight_status.date`, …) are queried by literal
date as supplied by the agent's tool calls.

## Empty env

`envs/flight_booking/empty/init.sql` is an empty file; the smallest env
that boots the server with no data:

```bash
flight-booking-mock --env ../../envs/flight_booking/empty --port 18099
```

## Smoke test

```bash
uv run python scripts/smoke_http.py
```

Boots the server on a free port pointed at the japan_20d_may env,
exercises `search_flights`, `get_flight_offer`, `create_booking`,
`get_booking`, and prints `SMOKE PASS` on success.

## Agent-facing tools

| tool                      | purpose                                              |
| ------------------------- | ---------------------------------------------------- |
| `search_flights`          | search offers for a route/date(s)                    |
| `get_flight_offer`        | fetch full fare rules + segments for an offer_id     |
| `get_seat_map`            | seat map for an offer or booking segment             |
| `price_offer`             | reprice an offer                                     |
| `create_booking`          | issue a PNR                                          |
| `get_booking`             | fetch a PNR                                          |
| `list_bookings`           | list PNRs for a user/email                           |
| `cancel_booking`          | cancel a PNR                                         |
| `change_booking`          | exchange segments for a new offer                    |
| `check_in`                | online check-in                                      |
| `get_flight_status`       | live status for a flight                             |
| `subscribe_flight_status` | push subscription (local notifications table)        |

## Layout

```
src/flight_booking_mock/
  server.py     # FastMCP wiring, streamable-HTTP transport
  config.py     # argparse → AppConfig
  tools/        # register_*_tools entry points
  services/     # business logic
  models/       # dataclasses
  backends/     # SQLite repo
  utils/        # ids, timewin, exceptions
```

See `SPEC.md` for error codes and schema.
