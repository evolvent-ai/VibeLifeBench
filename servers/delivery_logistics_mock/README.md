# delivery-logistics-mock

A FastMCP-based mock express shipping server (顺丰 / 京东物流 / 中通 style),
backed by SQLite, runs entirely offline. Transport is **streamable-HTTP only**
(no stdio fallback). Money is integer 分 (CNY minor units).

See [SPEC.md](./SPEC.md) for the full tool / schema / error reference.

## Run directly (host)

```bash
# From this directory, after `pip install -e .` (or `uv sync`):
delivery-logistics-mock \
  --host 0.0.0.0 \
  --port 8000 \
  --env ../../envs/delivery_logistics/li_wei_inflight
```

The MCP endpoint is exposed at `http://HOST:PORT/mcp`. On cold start the
server writes a fresh `runtime.db` inside the env directory, applies the
bundled schema, then executes `init.sql` if it exists.

CLI flags:

- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--env PATH` — env directory (`runtime.db` lives inside; optional `init.sql` is applied)
- `--debug` — verbose logging

To run stateless against an empty env: `--env ../../envs/delivery_logistics/empty`.

## Run in Docker

```bash
docker build -t delivery-logistics-mock .
docker run --rm -p 8000:8000 \
  -v $PWD/../../envs/delivery_logistics/li_wei_inflight:/env-seed:ro \
  delivery-logistics-mock
```

## Smoke test

```bash
python scripts/smoke_http.py
```

Boots the server on a random local port using
`envs/delivery_logistics/li_wei_inflight`, opens an MCP client over
streamable-HTTP, and exercises `track_package`, `list_shipments`,
`reschedule_delivery`, and `request_pickup`.

## Agent-facing tools

- `track_package`, `list_shipments`, `get_shipment`, `estimate_delivery`
- `request_pickup`
- `reschedule_delivery`, `change_address`, `cancel_shipment`
- `report_issue`, `list_issues`
- `subscribe_status`, `unsubscribe`

All return JSON-serialised strings. Errors use the shape
`{"error": "...", "code": "..."}`; see `SPEC.md` for the full code list.
