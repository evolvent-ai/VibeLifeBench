# credit-card-mock

A FastMCP-based mock credit-card simulator (SQLite, offline, HTTP-only).
Streamable-HTTP transport at `/mcp`. Terrarium/Docker runs it on
container port `8000`.

This server exposes a small set of cardholder-facing tools:

- `list_cards`, `get_card`, `freeze_card`, `unfreeze_card`
- `list_statements`, `get_statement`, `list_unbilled`
- `make_payment`
- `dispute_transaction`, `list_disputes`
- `get_rewards`, `redeem_rewards`

The server has no simulated clock and no management CLI. Stage-driven state
changes (cycle close, late-fee accrual, point expiry) are applied as
SQL mutations by the task orchestrator.

See `SPEC.md` for full tool semantics, schema, and error codes.

## Run

```bash
pip install -e .
credit-card-mock --host 127.0.0.1 --port 8000 \
    --env ../../envs/credit_card/li_wei_personal
```

On startup the server unlinks any `<env>/runtime.db`, creates the
schema, executes `<env>/init.sql` if present, and binds streamable-HTTP
at `http://<host>:<port>/mcp`.

## CLI flags

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--debug` — verbose logging.

## Smoke test

```bash
python scripts/smoke_http.py
```

Starts the server on a free local port against
`envs/credit_card/li_wei_personal`, exercises a handful of tools
end-to-end, and prints `SMOKE PASS` on success.

## Example env

`envs/credit_card/li_wei_personal/` simulates user Li Wei with two CN
credit cards (招商银行 / 中国银行) and 13 months of activity on the
primary card — including an open ¥3,200 statement due 2026-05-09 and a
12,400-point rewards balance. See its `README.md` for details.
