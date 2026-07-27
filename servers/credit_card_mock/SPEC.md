# credit_card_mock — Specification

Status: v1
Audience: implementers / harness integrators.
Scope: a self-contained, fully offline mock of a consumer credit-card backend.

This server simulates the slice of a real card-issuer back-office an agent
might touch on behalf of a cardholder: list cards, read statements, pay
the bill, dispute a charge, freeze a card, peek at rewards. State is held
in a single SQLite file; transport is streamable-HTTP only. The server
has no simulated clock — stage-driven state changes (cycle close,
overdue accrual, point expiry) are applied as SQL mutations by the v3
orchestrator.

It mirrors `hotel_booking_mock`'s code conventions (one service class per
domain, one `register_*_tools` function per tool group, `@handle_errors`
decorator, ISO dates, integer minor units) but uses HTTP instead of stdio
and exposes no admin tool to the agent.

---

## 1. Stack

- Python ≥ 3.12, `mcp[cli] >= 1.11.0`, `fastmcp >= 2.10.5`.
- `sqlite3` stdlib only — no ORM.
- No HTTP-client libraries (`requests` / `httpx` / `aiohttp` / `urllib3`).
- Logging to stderr only; no `print` statements in the package.

## 2. Layout

```
servers/credit_card_mock/
├── pyproject.toml
├── README.md
├── SPEC.md                         # this file
├── Dockerfile
├── .python-version
├── .gitignore
├── LICENSE
├── src/credit_card_mock/
│   ├── __init__.py                 # __version__
│   ├── __main__.py
│   ├── server.py                   # argparse + FastMCP + streamable-http
│   ├── models/{__init__,card}.py
│   ├── backends/
│   │   ├── __init__.py
│   │   ├── db.py                   # PRAGMAs + DDL
│   │   └── seed.py                 # apply_init_sql() — only path for external state
│   ├── services/                   # one class per domain
│   │   ├── card_service.py
│   │   ├── statement_service.py
│   │   ├── payment_service.py
│   │   ├── dispute_service.py
│   │   └── rewards_service.py
│   ├── tools/                      # one register_*_tools per file
│   │   ├── card_tools.py
│   │   ├── statement_tools.py
│   │   ├── payment_tools.py
│   │   ├── dispute_tools.py
│   │   └── rewards_tools.py
│   └── utils/                      # dates, ids, exceptions
env data lives outside the package under `envs/credit_card/<scenario>/`.
```

## 3. Transport

Streamable-HTTP at `/mcp` is the only transport. There is NO stdio
fallback and NO `--transport` flag.

`server.py` calls:

```python
mcp = FastMCP("credit-card-mock", host=args.host, port=args.port)
# ... register tools ...
mcp.run(transport="streamable-http")
```

CLI flags:
- `--env PATH` — required; path to `envs/<server>/<env_name>/`.
- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--debug`

On startup the server unlinks `<env>/runtime.db`, creates the schema,
runs `<env>/init.sql` if present, and binds streamable-HTTP. Every
cold start is a reset.

## 4. State injection

The package ships SCHEMA ONLY. There is no bundled seed JSON / SQL data
inside the package. All state enters via `<env>/init.sql`. The minimal
stateless env is `envs/credit_card/empty/` (empty `init.sql`).

`backends/seed.py` exposes `apply_init_sql(conn, init_sql_path)` — nothing else.

## 5. State evolution across stages

The agent under test never sees a tool that advances time. Cycle closes,
overdue accruals, late-fee postings, and point expirations are all
applied by the task orchestrator as `mutation` events in
`event.yaml` — these are one or more SQL statements run against this
server's runtime DB. There is no management CLI, sweep loop, or runtime
clock.

If a task wants D7 to feel like a cycle has just closed, the task writes
the resulting `statements` rows (and the matching
`statement_lines`/`cards` updates) directly in its stage-N overlay SQL.

## 6. Tools (agent-facing)

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`.
Validation / business errors are returned as
`{"error": "...", "code": "..."}` rather than raised. Money is integer
`分` (CNY minor units). IDs are domain-prefixed strings.

### 6.1 `list_cards(user_id: str) -> str`

Returns a JSON array of card summaries:

```json
[
  {
    "card_id": "card_cmb_white",
    "issuer": "招商银行",
    "product_name": "白领信用卡",
    "masked_no": "****-****-****-4521",
    "type": "Visa",
    "credit_limit_minor": 15000000,
    "available_credit_minor": 14680000,
    "statement_balance_minor": 320000,
    "min_payment_due_minor": 16000,
    "due_date": "2026-05-09",
    "status": "active"
  }
]
```

`status` ∈ `{active, frozen, expired, closed}`.

### 6.2 `get_card(card_id: str) -> str`

Returns the full card detail plus cycle params, APR (basis points), total
points, and the last 5 transactions (newest first, merged across the open
unbilled set and statement_lines).

### 6.3 `list_statements(card_id: str, limit: int = 12) -> str`

Newest first. `status` ∈ `{open, paid, overdue, partial}`. Money fields:
`opening_balance_minor`, `new_charges_minor`, `payments_minor`,
`closing_balance_minor`, `min_payment_due_minor`.

### 6.4 `get_statement(statement_id: str) -> str`

Header + `statement_lines`: array of
`{line_id, posted_at, amount_minor, merchant_name, mcc, category, kind}`.
`kind` ∈ `{purchase, refund, payment, fee, interest, adjustment}`. Charge
amounts are positive; refunds and payments are negative.

### 6.5 `list_unbilled(card_id: str) -> str`

Transactions posted since the latest closed statement's `period_end`,
same line shape as 6.4 minus `statement_id`.

### 6.6 `make_payment(card_id, amount_minor, source_hint) -> str`

Applies `amount_minor` (integer 分) to the open statement balance FIRST,
then to unbilled balance. `source_hint` is an opaque string (e.g.
`"acct_checking_main"`) — recorded for audit but not validated. Returns:

```json
{
  "payment_id": "pay_20260512_000051",
  "applied_to_statement_minor": 16000,
  "applied_to_unbilled_minor": 0,
  "new_outstanding_minor": 304000
}
```

Errors: `INVALID_AMOUNT` (≤0 or non-int), `OVERPAYMENT` (> total
outstanding), `CARD_NOT_FOUND`.

Frozen cards still accept payments (this is intentional).

### 6.7 `dispute_transaction(tx_id, reason) -> str`

`tx_id` may be either an unbilled `tx_id` or a billed `line_id`. Starts
in status `"under_review"` with `expected_resolution_date = today + 30`.

```json
{"dispute_id": "dsp_20260512_000001", "status": "under_review", "expected_resolution_date": "2026-06-11"}
```

Errors: `TX_NOT_FOUND`, `DISPUTE_ALREADY_OPEN`.

### 6.8 `list_disputes(card_id, status_filter=None) -> str`

Newest first. `status_filter` ∈ `{under_review, approved, denied,
withdrawn}` when supplied.

### 6.9 `freeze_card(card_id) -> str` / `unfreeze_card(card_id) -> str`

Flip card status between `active` ↔ `frozen`. Frozen cards reject NEW
CHARGES (purchase paths are stubbed since this mock has no public
"charge" tool), but `make_payment` still works on frozen cards.

### 6.10 `get_rewards(card_id) -> str`

Returns `{points_balance, ytd_earned, lifetime_earned, updated_at,
recent_earnings, redemption_options}`. The redemption catalog ships in
`services/rewards_service.py` (`STMT_CREDIT_50`, `STMT_CREDIT_200`,
`MILES_AIR_CHINA`, `GIFT_JD_100`).

### 6.11 `redeem_rewards(card_id, redemption_code) -> str`

Deducts the catalog cost from `points_balance` and writes a `redeem`
ledger row. Errors: `INSUFFICIENT_POINTS`, `BAD_REDEMPTION`.

## 7. Schema (DDL)

See `backends/db.py` for the authoritative SQL. Nine tables:

| table                   | role                                                              |
|-------------------------|-------------------------------------------------------------------|
| `cards`                 | one row per card, all summary fields cached here                  |
| `statements`            | one row per monthly cycle                                         |
| `statement_lines`       | line items belonging to a statement                               |
| `unbilled_transactions` | line items not yet on a statement                                 |
| `payments`              | payment audit trail (one row per `make_payment` call)             |
| `disputes`              | dispute tickets                                                   |
| `rewards_balances`      | one row per card; current points balance + YTD / lifetime earned  |
| `rewards_ledger`        | append-only ledger of point movements                             |
| `_counters`             | tiny key→int counter table backing ID generators                  |

## 8. Error codes (stable)

| code                    | meaning                                                  |
|-------------------------|----------------------------------------------------------|
| `CARD_NOT_FOUND`        | `card_id` does not exist                                 |
| `CARD_FROZEN`           | reserved — see §6.9                                      |
| `OVER_LIMIT`            | reserved for future "charge" tool                        |
| `OVERPAYMENT`           | `make_payment` amount exceeds total outstanding          |
| `INVALID_AMOUNT`        | non-positive or non-integer amount                       |
| `DISPUTE_ALREADY_OPEN`  | active dispute exists for the same tx                    |
| `TX_NOT_FOUND`          | `tx_id` matches neither unbilled nor billed lines        |
| `STATEMENT_NOT_FOUND`   | `statement_id` does not exist                            |
| `INSUFFICIENT_POINTS`   | balance < redemption cost                                |
| `BAD_REDEMPTION`        | unknown `redemption_code`                                |
| `BAD_ARG`               | generic argument validation failure                      |

## 9. Running

### 9.1 Direct (Python)

```bash
pip install -e .
credit-card-mock --host 127.0.0.1 --port 8000 \
    --env ../../envs/credit_card/li_wei_personal
```

Hit `http://127.0.0.1:8000/mcp` with an MCP streamable-http client.

### 9.2 Smoke

```bash
python scripts/smoke_http.py
```

Boots the server on a free local port against
`envs/credit_card/li_wei_personal`, exercises `list_cards` /
`get_card` / `make_payment` (and the `OVERPAYMENT` error branch) /
`freeze_card` / `unfreeze_card` / `list_statements` / `get_rewards`.
Prints `SMOKE PASS` on success.

## 10. Out of scope

- No real authorization or settlement flow — there is no `charge_card`
  tool. The unbilled set is whatever the operator seeds.
- No FX / multi-currency.
- No real merchant network or 3DS.
- Pagination on `list_statements` is just the `limit` kwarg; no cursors.
