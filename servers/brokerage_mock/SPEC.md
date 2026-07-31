# brokerage-mock — Specification

A self-contained mock of a personal A-share brokerage. Stack: Python
3.12, FastMCP, SQLite (stdlib `sqlite3`). Transport is **streamable-http
only** on `/mcp`.

## 1. Conventions

- **Currency**: CNY for all positions, orders, and funds.
- **Money unit**: integer 分 (`*_minor`) — 1 CNY = 100 minor.
- **Symbols**: 6-digit code strings (e.g. `"600519"`, `"000333"`).
- **Dates**: ISO `YYYY-MM-DD`.
- **Fund units**: stored in milli-units; 1 fund unit = 1000 milli.
- **Order qty**: agents pass whole-share integers; internally stored as
  `qty_milli` (`qty * 1000`) so stocks and fractional funds share one
  column.
- **Tool returns**: JSON strings via `json.dumps(..., ensure_ascii=False)`.
- **Errors**: `{"error": "<msg>", "code": "<CODE>"}` (never raises across
  the MCP boundary).

## 2. Tools

### 2.1 `list_accounts(user_id) -> [Account]`

Lists all brokerage accounts owned by `user_id`.

```
[{account_id, broker, account_type, opened_at, status}]
```

`account_type` ∈ `{cash, margin}` (only `cash` in v1).

### 2.2 `get_portfolio(account_id) -> Portfolio`

```
{account_id, cash_minor, positions_value_minor, total_value_minor,
 todays_pnl_minor, as_of_date}
```

`todays_pnl_minor` = Σ over positions of `qty * (last_close - prev_close)`,
computed in minor units.

### 2.3 `get_positions(account_id) -> [Position]`

```
[{symbol, name, kind, qty, avg_cost_minor, current_price_minor,
  market_value_minor, unrealized_pnl_minor}]
```

`kind` ∈ `{stock, fund}`. `qty` is whole shares for stocks, fractional
(rounded to 3 decimals) for funds.

### 2.4 `get_quote(symbol) -> Quote`

```
{symbol, name, bid_minor, ask_minor, last_minor, prev_close_minor,
 day_change_bp, as_of_date}
```

`day_change_bp` is in basis points: `(last - prev_close) / prev_close * 10000`.
Bid/ask are synthesized from a 5 bp half-spread around `last`.

### 2.5 `list_orders(account_id, status_filter?, limit=50) -> [Order]`

```
[{order_id, symbol, side, qty, order_type, limit_price_minor, status,
  placed_at, filled_at, fill_price_minor}]
```

`status` ∈ `{pending, filled, cancelled, rejected}`. Newest first.

### 2.6 `place_order(account_id, symbol, side, qty, order_type, limit_price_minor?, tif="day") -> Ack`

`side` ∈ `{buy, sell}`. `order_type` ∈ `{market, limit}`. `qty` is a
positive integer (whole shares).

- **Market order**: fills immediately at the latest available close
  (`last_minor`). Cash / shares are debited / credited atomically.
- **Limit order**: if the limit crosses the latest available price,
  fills immediately at `last_minor`. Otherwise queues with status
  `pending`. There is no automatic fill engine; a task that wants the
  order to fill later must write the fill row from a `mutation` event.

Buy orders validate `cash_minor >= qty * ref_price`. Sell orders
validate `held_qty >= qty`.

Returns `{order_id, status, fill_price_minor?}`.

### 2.7 `cancel_order(order_id) -> Ack`

Cancels a pending order. Errors if the order is in any non-pending
status. Returns `{order_id, status: "cancelled"}`.

### 2.8 `list_funds(category?) -> [Fund]`

```
[{fund_code, fund_name, category, nav_minor, ytd_return_bp, risk_level}]
```

`category` ∈ `{money_market, bond, equity, mixed, index}` or null.

### 2.9 `get_fund_nav(fund_code, lookback_days=30) -> [NavRow]`

```
[{date, nav_minor}]  -- newest first
```

### 2.10 `subscribe_fund(account_id, fund_code, amount_minor) -> Ack`

Buy a fund with cash. Acquired units = `amount / nav` rounded **down**
to 2 decimal places (stored as 4-decimal-equivalent integer
milli-units, multiples of 10 milli). Cash debited equals
`units_acquired * nav`, which may be slightly less than `amount_minor`
due to rounding (the residual stays in cash).

Returns `{order_id, status: "filled", units_acquired_milli}`.

### 2.11 `redeem_fund(account_id, fund_code, units_milli) -> Ack`

Symmetric: sell `units_milli` of fund at current NAV.

Returns `{order_id, status: "filled", units_redeemed_milli, proceeds_minor}`.

### 2.12 `get_portfolio_perf(account_id, period) -> Perf`

```
{period_return_bp, max_drawdown_bp, start_value_minor, end_value_minor}
```

`period` ∈ `{1d, 7d, 30d, ytd}`. The window ends at the most recent
`portfolio_snapshots.date` for the account. If the account has no
snapshots, all four fields are 0.

## 3. Schema

```sql
accounts(account_id PK, user_id, broker, account_type CHECK,
         cash_minor, opened_at, status)
positions(position_id PK AUTO, account_id FK, symbol, kind CHECK,
          qty_milli, avg_cost_minor, UNIQUE(account_id, symbol))
orders(order_id PK, account_id FK, symbol, side CHECK,
       qty_milli, order_type CHECK, limit_price_minor, tif,
       status CHECK, placed_at, filled_at, fill_price_minor)
symbols(symbol PK, name, kind CHECK)
quotes_daily(symbol, date, open_minor, close_minor, high_minor,
             low_minor, volume, PK(symbol, date))
funds(fund_code PK, fund_name, category CHECK, current_nav_minor,
      ytd_return_bp, risk_level, manager, inception)
fund_navs(fund_code FK, date, nav_minor, PK(fund_code, date))
portfolio_snapshots(account_id FK, date, cash_minor,
                    positions_value_minor, total_value_minor,
                    PK(account_id, date))
_counters(name PK, value)
```

`symbols.symbol` must be unique across stocks and funds: do **not**
reuse a 6-digit code for both kinds in the same DB.

## 4. State changes between stages

There is no simulated clock and no admin path. When a stage opens, the
orchestrator opens the runtime sqlite file directly and applies the
SQL from `event.yaml` `mutation` events (inline statements or
`sql_file` overlays). The server is not in the loop. Pre-baked
`quotes_daily`, `fund_navs`, and `portfolio_snapshots` rows in the
env's `init.sql` provide whatever historical depth the task needs.

## 5. Out of scope (v1)

- Margin accounts, short selling, leverage.
- Intraday quotes / Level-2 / order book depth.
- Fractional stock shares (only fund subscription is fractional).
- Multi-currency, FX, foreign symbols.
- Realized P/L reporting (only `unrealized_pnl_minor` is computed).
- Tax lots, wash sales.

## Appendix A: Error codes

| Code                    | When                                                     |
|-------------------------|----------------------------------------------------------|
| `ACCOUNT_NOT_FOUND`     | `account_id` does not exist                              |
| `SYMBOL_NOT_FOUND`      | `symbol` has no quote data (or empty)                    |
| `INSUFFICIENT_CASH`     | Buy / subscribe exceeds `cash_minor`                     |
| `INSUFFICIENT_SHARES`   | Sell / redeem exceeds held quantity                      |
| `ORDER_NOT_FOUND`       | `order_id` does not exist                                |
| `ORDER_NOT_PENDING`     | `cancel_order` on a non-pending order                    |
| `BAD_SIDE`              | `side` is not `buy` or `sell`                            |
| `BAD_ORDER_TYPE`        | `order_type` is not `market` or `limit`                  |
| `FUND_NOT_FOUND`        | `fund_code` does not exist                               |
| `INVALID_AMOUNT`        | Subscribe amount too small, bad category, bad NAV        |
| `BAD_ARG`               | Generic validation failure (qty, period, etc.)           |
