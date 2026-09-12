# `maps_mock` — Specification

Local mock **Maps MCP server** (FastMCP, streamable-HTTP, SQLite).
Provides the subset of Google Maps Platform APIs a travel/logistics
agent needs: geocoding, places, directions, distance matrix, transit
schedule, and traffic estimates.

Code lives under `servers/maps_mock/` and follows the repository's
Terrarium capability contract:

- Streamable-HTTP only (no stdio).
- No admin / clock / mutation tool on the MCP surface. State changes
  between stages are written directly to the runtime sqlite file by
  the orchestrator via `event.yaml` `mutation` events.
- Schema-only package; the env directory's `init.sql` ships the state.
- No `MCP_EXPOSE_*` toggles, no bundled JSON seed, no drift.

---

## 1. Transport & CLI

`server.py` runs

```python
mcp.run(transport="streamable-http")
```

after binding `mcp.settings.host` / `mcp.settings.port`. Endpoint is
`/mcp`.

Flags accepted by `maps-mock` (argparse, in `server.py`):

| flag      | default     | meaning                                                       |
| --------- | ----------- | ------------------------------------------------------------- |
| `--host`  | `0.0.0.0`   | Bind address                                                  |
| `--port`  | `8000` for Docker/Terrarium parity | TCP port                                |
| `--env`   | required    | Path to env dir. `<env>/init.sql` is applied on cold start.   |
| `--debug` | off         | Verbose logging                                               |

Every cold start unlinks `<env>/runtime.db` and recreates it fresh.

---

## 2. Directory Layout

```
servers/maps_mock/
├── pyproject.toml
├── README.md
├── SPEC.md
├── Dockerfile
├── LICENSE
├── scripts/
│   └── smoke_http.py
└── src/
    └── maps_mock/
        ├── __init__.py
        ├── __main__.py
        ├── server.py          # streamable-HTTP entrypoint, takes --env
        ├── models/            # dataclasses
        ├── backends/
        │   ├── sqlite_backend.py
        │   └── seed.py        # apply_init_sql()
        ├── services/          # one class per logical group
        ├── tools/             # one register_*_tools(mcp, service) per file
        └── utils/
```

---

## 3. Agent-facing tools

Eight tools, all `async def`, all returning JSON-serializable dicts/lists
(or `{"error", "code"}` on failure). All are registered on the shared
`FastMCP("maps-mock")` instance in `server.py`.

### 3.1 `geocode(address: str) -> dict`
Forward-geocode a free-form address to coordinates + place_id.

### 3.2 `reverse_geocode(lat: float, lng: float) -> dict`
Nearest-neighbor place lookup. Returns `{"place_id": null, ...}` if no
known place is within 500 m.

### 3.3 `search_places(query, geo=None, radius_m=5000, category=None, limit=10) -> list[dict]`
Places Nearby + text search hybrid. Sorts by distance when `geo` is
provided, else by `rating DESC, name ASC`.

### 3.4 `get_place_details(place_id: str) -> dict`
Full detail view. Surfaces an `alerts` array if active road or transit
events touch the place.

### 3.5 `directions(origin: str, dest: str, mode="driving", depart_at=None) -> dict`
Routing across `driving | walking | transit | bicycling`. Origin and
dest accept `place_id`, free-form address, or `"lat,lng"`. Active
`road_events` inflate driving duration and add `warnings`.

### 3.6 `distance_matrix(origins, dests, mode="driving") -> dict`
Batch distance/duration grid. `|origins| × |dests| ≤ 100`.

### 3.7 `get_transit(origin: str, dest: str, depart_at: str) -> list[dict] | dict`
Scheduled transit itineraries (up to 3). Snaps endpoints to nearest
`transit_stops` within 1.5 km; otherwise returns `{"error": "NO_TRANSIT_NEARBY"}`.
Itineraries touching an active `transit_events(kind='suspended')` row
are dropped; if none remain, returns `{"disruptions": [...]}`.

### 3.8 `get_traffic_estimate(origin, dest, depart_at=None) -> dict`
Driving-only normal vs. with-traffic comparison. Derives `severity` from
the ratio: <1.10 light, 1.10–1.30 moderate, 1.30–1.60 heavy, >1.60 severe.

There is **no admin tool** exposed over MCP.

---

## 4. State model — SQLite schema

Single file. Schema is shipped in `backends/sqlite_backend.py` and
applied idempotently on every startup. Tables:

- `places` — POIs with `lat/lng/city/country/rating/price_level/hours_json`.
- `place_reviews` — sampled reviews per place.
- `roads` — sparse road segments referenced by road_events.
- `transit_stops`, `transit_lines`, `transit_schedule` — line/stop graph
  and departure-time grid.
- `road_events`, `transit_events` — incident windows with an `active`
  flag. Whatever is in `init.sql` is what's seen; the orchestrator
  flips `active` via direct SQL when a stage opens/closes an incident.
- `notifications` — ops-channel rows.

---

## 5. State changes between stages

There is no sim clock. The orchestrator opens the runtime sqlite file
directly and applies `mutation` events from `event.yaml` (inline SQL
or `sql_file` overlays). The server is not in the loop.

---

## 6. Quality contract

- Tools never raise across the MCP boundary; they return `{"error","code"}`.
- All logging goes to stderr (`logging.getLogger(__name__)`). No `print`.
- Schema creation is idempotent. The server starts cleanly against an
  empty DB (every list-tool returns `[]`).
- `scripts/smoke_http.py` spawns the server on a free port against the
  Japan-20d env and exercises `geocode`, `search_places`, `directions`,
  `distance_matrix` over streamable-HTTP. Exit 0 on PASS.

---

## Appendix — Error codes

| code               | when                                                              |
| ------------------ | ----------------------------------------------------------------- |
| `INVALID_REQUEST`  | malformed args (bad enum, list too long, missing required field)  |
| `ZERO_RESULTS`     | geocode / directions cannot resolve an endpoint                   |
| `NO_TRANSIT_NEARBY`| `get_transit` endpoint > 1.5 km from any stop                     |
| `INTERNAL_ERROR`   | uncaught exception (logged with traceback)                        |
