# maps-mock

Local, deterministic mock of Google Maps Platform APIs (geocode, places,
directions, distance matrix, transit schedule, traffic) for the Toolathlon
benchmark. **FastMCP + streamable-HTTP + SQLite. No network, no Google billing.**

State enters via the env directory's `init.sql`. The package ships
schema only — no bundled seed data.

See `SPEC.md` for the full behaviour spec.

## Install

```
uv sync       # or: pip install .
```

## Run (HTTP MCP server)

```
maps-mock \
  --host 0.0.0.0 \
  --port 8000 \
  --env ../../envs/maps/japan_20d_may
```

Endpoint: `http://<host>:<port>/mcp` (streamable-HTTP).

| flag       | default     | description                                                |
|------------|-------------|------------------------------------------------------------|
| `--host`   | `0.0.0.0`   | Bind address                                               |
| `--port`   | recommended `8000` for Docker/Terrarium parity | TCP port              |
| `--env`    | required    | Path to env dir. `<env>/init.sql` is applied on cold start.|
| `--debug`  | off         | Verbose logging                                            |

Every cold start unlinks `<env>/runtime.db` and recreates it fresh.

## Tools (agent-facing)

- `geocode(address)`
- `reverse_geocode(lat, lng)`
- `search_places(query, geo?, radius_m?, category?, limit?)`
- `get_place_details(place_id)`
- `directions(origin, dest, mode?, depart_at?)`
- `distance_matrix(origins, dests, mode?)`
- `get_transit(origin, dest, depart_at)`
- `get_traffic_estimate(origin, dest, depart_at?)`

There is no admin / clock / mutation tool over MCP. State changes
between stages are performed by the orchestrator writing directly to
the runtime SQLite file via `mutation` events in `event.yaml`.

## Example env

See [`envs/maps/japan_20d_may/`](../../envs/maps/japan_20d_may/) for
the Japan 20-day (May 2026) snapshot.

```bash
maps-mock \
  --env ../../envs/maps/japan_20d_may
```

## Smoke test

```
python scripts/smoke_http.py
```

Spawns the server on a free port against the Japan-20d env and
exercises `geocode`, `search_places`, `directions`, `distance_matrix`
over the streamable-HTTP endpoint. Prints `PASS` / `FAIL`.

## Schedule encoding

Each `transit_schedule` row records a **departure** time at a specific stop.
`transit_lines.segment_minutes_json` carries the minutes between consecutive
stops along a line, used to derive arrival times and segment distances on the
fly in `transit_service`.
