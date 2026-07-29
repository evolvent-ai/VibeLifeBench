# banking_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `banking-mock` MCP server.

## 1. Purpose

`banking_mock` is a self-contained, fully-offline mock of a retail banking
backend — accounts, transactions, transfers, payees, scheduled payments. It
exists so benchmark tasks can exercise an agent's ability to read account
state, make transfers, manage payees, schedule recurring debits, and react
to deterministic state changes the task orchestrator injects via
out-of-band SQL mutations.

The server makes **no** network calls and ships **no** bundled seed data —
state enters only through the env-directory `init.sql` script.

Non-goals:

- No real payment authorization. `payee.account_no` is opaque; transfers and
  payments never call an external network.
- No multi-currency FX. The schema has a `currency` column for shape parity,
  but is held constant per env (CNY in the example env).
- No authentication. Identity is whatever the caller passes as `user_id`.
- No i18n.

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`, `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.

## 3. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`,
and surface errors as `{"error": "...", "code": "..."}` rather than raising
across the MCP boundary. Money is integer minor units (分/cents). Dates are
ISO `YYYY-MM-DD`. IDs are domain-prefixed strings.

### 3.1 `list_accounts(user_id) -> str`

```json
[
  {"account_id": "acct_checking_main", "type": "checking",
   "name": "招商银行借记卡 (主账户)", "balance_minor": 3500000,
   "currency": "CNY", "opened_at": "2018-06-15", "frozen": false},
  ...
]
```

`type` ∈ {`checking`, `savings`, `money_market`, `education_fund`}.

### 3.2 `get_account(account_id) -> str`

Full account detail plus a 7-day daily balance trend. The trend is derived
on the fly from `transactions.balance_after_minor`:

```json
{
  "account_id": "acct_checking_main",
  "user_id": "usr_li_wei",
  "type": "checking",
  "name": "...",
  "balance_minor": 3500000,
  "currency": "CNY",
  "opened_at": "2018-06-15",
  "frozen": false,
  "balance_trend_7d": [
    {"date": "2026-04-25", "balance_minor": 3520000},
    {"date": "2026-04-26", "balance_minor": 3520000},
    {"date": "2026-04-27", "balance_minor": 3509200},
    ...
  ]
}
```

### 3.3 `list_transactions(account_id, since?, until?, limit=50, kind_filter?) -> str`

Newest-first. `kind` ∈
`{deposit, withdrawal, transfer_in, transfer_out, payment, fee, interest}`.

```json
[
  {"tx_id": "tx_20260429_000048", "posted_at": "2026-04-29T12:00:00Z",
   "amount_minor": -9200, "kind": "withdrawal",
   "counterparty": "便利店", "memo": "便利店消费",
   "balance_after_minor": 3500000},
   ...
]
```

`amount_minor` is signed from the account's perspective (positive =
inflow, negative = outflow). `limit` defaults to 50 and is clamped to 500.

### 3.4 `transfer(from_account_id, to_account_id, amount_minor, memo?) -> str`

Atomic transfer between two accounts of the same user. For external
recipients use `add_payee` + `pay_payee` instead.

```json
{"tx_id": "tx_...", "from_account_id": "...", "to_account_id": "...",
 "amount_minor": 10000, "from_new_balance_minor": 3490000,
 "to_new_balance_minor": 15010000, "posted_at": "2026-05-01T..."}
```

Errors: `ACCOUNT_NOT_FOUND`, `ACCOUNT_FROZEN`, `INSUFFICIENT_FUNDS`,
`CROSS_USER_TRANSFER`, `BAD_AMOUNT`.

### 3.5 `list_payees(user_id) -> str`

```json
[{"payee_id": "pay_000001", "name": "国家电网",
  "bank_name": "中国工商银行", "account_no_masked": "***************0111",
  "added_at": "2024-01-12T10:00:00Z"}, ...]
```

### 3.6 `add_payee(user_id, name, account_no, bank_name) -> str`

The full `account_no` is stored but only the masked form is returned. Mask
keeps the last 4 characters.

```json
{"payee_id": "pay_000004", "name": "Acme",
 "bank_name": "Bank", "account_no_masked": "************1234",
 "added_at": "2026-05-01T..."}
```

### 3.7 `pay_payee(account_id, payee_id, amount_minor, memo?, scheduled_for?) -> str`

If `scheduled_for` is in the future relative to the server's wall-clock
UTC date, the payment is parked as a `pending_payments` row (status
`pending`) and the account is **not** debited yet. Otherwise debits
immediately. Pending rows are only posted by orchestrator-issued
`mutation` events — the server itself never sweeps them.

```json
// immediate post
{"tx_id": "tx_...", "tx_id_or_pending_id": "tx_...",
 "status": "posted", "amount_minor": 80000,
 "balance_after_minor": 3499200}

// future-dated
{"pending_id": "pend_000001", "tx_id_or_pending_id": "pend_000001",
 "status": "scheduled", "scheduled_for": "2026-06-15",
 "amount_minor": 80000}
```

### 3.8 `list_pending_payments(user_id, account_id?, status_filter?, limit=50) -> str`

Returns future-dated one-off payments owned by `user_id`, ordered by
`scheduled_for`. `account_id` and `status_filter` (`pending`, `posted`, or
`cancelled`) are optional; `limit` is capped at 500. Each row includes the
pending ID, source account, payee identity, amount, memo, date, and status.

```json
[{"pending_id": "pend_000001", "account_id": "acct_checking_main",
  "payee_id": "pay_000001", "payee_name": "Acme", "amount_minor": 80000,
  "memo": "deposit", "scheduled_for": "2026-06-15", "status": "pending"}]
```

### 3.9 `schedule_recurring(account_id, payee_id, amount_minor, freq, start_date, end_date?) -> str`

`freq` ∈ `{daily, weekly, monthly}`. Returns `{schedule_id, next_run_date,
amount_minor, freq, status: "active"}`. `next_run_date` starts equal to
`start_date`.

### 3.10 `cancel_recurring(schedule_id) -> str`

Returns `{schedule_id, status: "cancelled"}`. `SCHEDULE_NOT_FOUND` if the
id is unknown. Idempotent: cancelling an already-cancelled schedule still
returns `cancelled`.

### 3.11 `list_recurring(user_id, status_filter?) -> str`

`status` ∈ `{active, paused, cancelled, ended}`.

```json
[{"schedule_id": "sch_000001", "account_id": "acct_checking_main",
  "payee_id": "pay_000001", "payee_name": "国家电网",
  "amount_minor": 80000, "freq": "monthly",
  "next_run_date": "2026-05-05", "status": "active"}, ...]
```

## 4. Storage

SQLite, one file per server. `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL`.

| table                   | purpose                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| `accounts`              | user accounts with current balance and frozen flag                                            |
| `transactions`          | append-only ledger, signed `amount_minor`, carries `balance_after_minor`                      |
| `payees`                | per-user external payees; stores both raw + masked account_no                                 |
| `recurring_payments`    | active/paused/cancelled/ended schedules with `next_run_date` cursor                           |
| `pending_payments`      | future-dated single payments (orchestrator posts them via mutation events)                    |
| `_counters`             | atomic seq counters used to mint stable ids                                                   |

Indices: `(account_id, posted_at)` on `transactions`; `next_run_date` on
`recurring_payments`; `(scheduled_for, status)` on `pending_payments`.

## 5. State injection

No JSON seed. The server takes `--env <dir>` and on cold start:

1. Unlinks `<env>/runtime.db` (and WAL sidecars).
2. Creates the schema.
3. `executescript`s `<env>/init.sql` if present.
4. Opens streamable-HTTP on `<host>:<port>/mcp`.

The minimal stateless env is `envs/banking/empty/` (empty `init.sql`).

## 6. State evolution across stages

The task orchestrator drives state changes through `mutation` events in
each task's `event.yaml`. A mutation is one or more SQL statements
against this server's runtime DB; the dispatch path is identical to a
caller running raw SQL.

This server has no management CLI, no sweep loop, no interest accrual,
and no runtime clock. If a task needs recurring payments to post on a given stage,
the task writes the resulting `transactions` rows directly (or executes
the `pay_payee` flow via an explicit SQL `INSERT` on `pending_payments`
followed by a stage-N mutation that posts the debit and flips the
status).

## 7. Logging & ops

- `logging.getLogger(__name__)` everywhere; handler attached to stderr
  only (FastMCP itself does not use stdout for streamable-HTTP, but we
  preserve the convention).
- No `print()` in the package.

## 8. Appendix — error codes

| code                    | meaning                                                              |
| ----------------------- | -------------------------------------------------------------------- |
| `ACCOUNT_NOT_FOUND`     | `account_id` does not exist                                          |
| `ACCOUNT_FROZEN`        | a debit was attempted on a `frozen=1` account                        |
| `INSUFFICIENT_FUNDS`    | debit would push `balance_minor` below 0                             |
| `PAYEE_NOT_FOUND`       | `payee_id` does not exist or belongs to a different user             |
| `SCHEDULE_NOT_FOUND`    | `schedule_id` does not exist                                         |
| `CROSS_USER_TRANSFER`   | `from` and `to` accounts belong to different `user_id`s              |
| `BAD_DATE`              | non-ISO date string                                                  |
| `BAD_FREQ`              | `freq` not in `{daily, weekly, monthly}`                             |
| `BAD_AMOUNT`            | `amount_minor` not a positive integer                                |
| `BAD_ARG`               | catch-all for malformed inputs                                       |

## 9. Out of scope

- No multi-leg / multi-currency FX.
- No interest types beyond simple daily on `savings`.
- No pagination cursors (`limit` only).
- No batch / bulk endpoints.
- No real auth, no per-user permission enforcement beyond the same-user
  guard on `transfer`.
