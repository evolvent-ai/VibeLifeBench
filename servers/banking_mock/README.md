# banking-mock

A FastMCP-based, fully-offline mock of a retail banking backend. Runs over
**streamable-HTTP** (no stdio) with a local SQLite database. Money is stored
as integer 分 (cents); the example env uses CNY.

See [SPEC.md](./SPEC.md) for the full implementer-facing specification.

## Tools (agent-facing)

- `list_accounts(user_id)`
- `get_account(account_id)` — includes a 7-day daily balance trend.
- `list_transactions(account_id, since?, until?, limit?, kind_filter?)`
- `transfer(from_account_id, to_account_id, amount_minor, memo?)`
- `list_payees(user_id)` / `add_payee(user_id, name, account_no, bank_name)`
- `list_pending_payments(user_id, account_id?, status_filter?, limit?)`
- `pay_payee(account_id, payee_id, amount_minor, memo?, scheduled_for?)`
- `schedule_recurring(account_id, payee_id, amount_minor, freq, start_date, end_date?)`
- `list_recurring(user_id, status_filter?)` / `cancel_recurring(schedule_id)`

The server has no simulated clock and no management CLI. Stage-driven state
changes are applied as SQL mutations by the task orchestrator.

## Quick start

```bash
# From this directory
pip install -e .

# Run with an env directory.
banking-mock \
  --port 8000 \
  --env ../../envs/banking/li_wei_personal
```

On startup the server unlinks any `<env>/runtime.db`, creates the schema,
executes `<env>/init.sql` if present, and binds streamable-HTTP at
`http://<host>:<port>/mcp`.

## CLI flags

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--debug` — verbose logging.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess against
`envs/banking/li_wei_personal` and round-trips `list_accounts`,
`transfer`, `list_transactions`, `list_payees`, plus a frozen-source
transfer expecting `ACCOUNT_FROZEN`. Prints `PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`ACCOUNT_NOT_FOUND`, `ACCOUNT_FROZEN`, `INSUFFICIENT_FUNDS`,
`PAYEE_NOT_FOUND`, `SCHEDULE_NOT_FOUND`, `CROSS_USER_TRANSFER`,
`BAD_DATE`, `BAD_FREQ`, `BAD_AMOUNT`, `BAD_ARG`.
