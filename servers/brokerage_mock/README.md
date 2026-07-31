# brokerage-mock

A FastMCP-based mock 个人证券账户 server. Surfaces a retail brokerage
account on top of a SQLite store: portfolio summary, positions, A-share
quotes, orders (market + limit), and an open-end fund catalog with
subscribe / redeem. Transport is **streamable-http only**.

All money is **integer 分** (1 CNY = 100 minor units). Symbols are
6-digit string codes (e.g. `"600519"`). Fund units are stored in
milli-units (1 unit = 1000 milli).

There is no simulated clock, no admin/clock-walk path, and no automatic
drift. State changes between stages are written directly to the
runtime sqlite file by the orchestrator via `mutation` events in
`event.yaml`.

See [SPEC.md](./SPEC.md) for the complete tool / schema / error contract.

## Run directly

```bash
uv sync
uv run brokerage-mock --port 8000 \
    --env ../../envs/brokerage/li_wei_growth
```

Then `POST http://localhost:8000/mcp` with an MCP streamable-http client.

CLI flags:

- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--env PATH` — env dir; `<env>/init.sql` applied on cold start
- `--debug`

Every cold start unlinks `<env>/runtime.db` and recreates it fresh.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Exercises the service layer directly against a fresh DB seeded from
the li_wei_growth env. Asserts `list_accounts`, `get_portfolio`,
`get_quote`, a market `place_order` buy, fund catalog, and
`get_portfolio_perf(30d)`.

## Tool surface

Read-only:
- `list_accounts`, `get_portfolio`, `get_positions`, `get_portfolio_perf`
- `get_quote`
- `list_orders`, `list_funds`, `get_fund_nav`

Mutations:
- `place_order` (market or limit), `cancel_order`
- `subscribe_fund`, `redeem_fund`

All tools return JSON-serialised strings; errors are
`{"error": "...", "code": "..."}`. See SPEC.md §Appendix A for codes.
