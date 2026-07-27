# notification-hub-mock

A FastMCP-based, fully-offline mock of a **cross-platform subscription +
notification hub** (订阅中心 / 价格提醒 / 关键词提醒 / 公众号 feed). Runs over
**streamable-HTTP** (no stdio) with a local SQLite database.

It is the connective tissue across 备考(政策更新) / 购物(盯价盯新品) /
理财(价格监控) / 租房(盯房源): each platform's local `subscribe_*` is single-purpose,
whereas this hub aggregates subscriptions, a unified notification inbox,
price alerts, and 公众号 feeds for one user.

## No clock, no auto-generation

The server has **no runtime clock and no RNG**. Notifications are pre-seeded
historical/static rows. Creating a subscription or price alert only records
*intent* — it never fabricates a time-based notification. New notifications (and
status changes like an alert flipping to `triggered`) arrive **out-of-band** as
SQL mutations injected by the orchestrator during a task. IDs come from a
`_counters` table.

## Tools (agent-facing)

Subscriptions:
- `list_subscriptions(user_id, status?)` — status ∈ active/paused/deleted; default excludes deleted.
- `get_subscription(subscription_id)`
- `create_subscription(user_id, source, type, target, condition_json?)` — type ∈ price_drop/restock/policy_update/new_content/price_target/keyword; `condition_json` is a JSON string.
- `update_subscription(subscription_id, target?, source?, condition_json?)` — at least one field.
- `pause_subscription(subscription_id)`
- `resume_subscription(subscription_id)`
- `delete_subscription(subscription_id)` — soft delete.

Notification inbox:
- `list_notifications(user_id, unread_only?, source?, since?, limit?)` — newest first; `since` is YYYY-MM-DD; limit ≤ 500.
- `get_notification(notification_id)`
- `mark_read(notification_id)`
- `mark_all_read(user_id)` — returns count newly flipped.

Price alerts:
- `create_price_alert(user_id, item_ref, target_price_minor)` — price in 分 (CNY minor units), positive.
- `list_price_alerts(user_id)`

Official accounts (公众号):
- `subscribe_official_account(user_id, account_id)`
- `list_official_accounts(user_id)`
- `get_account_feed(account_id, limit?)` — newest first; limit ≤ 200.

(16 tools total.) Optional params are marked `?`.

## Quick start

```
notification-hub-mock --host 0.0.0.0 --port 8005 \
                      --env <repo>/envs/notification_hub/li_wei_alerts_2026
```

The server creates a fresh `runtime.db` in the env dir, applies the schema,
then runs the env's `init.sql`. MCP endpoint is at `/mcp`.

## CLI flags

| flag      | default   | meaning                                   |
| --------- | --------- | ----------------------------------------- |
| `--env`   | required  | path to `envs/notification_hub/<env>/`    |
| `--host`  | `0.0.0.0` | bind host                                 |
| `--port`  | `8005`    | bind port (Docker image uses 8000)        |
| `--debug` | off       | DEBUG-level logging                       |

## Smoke test

```
uv run python servers/notification_hub_mock/scripts/smoke_http.py
```

Boots the server against `li_wei_alerts_2026`, round-trips
list/create/subscribe/feed/mark-all-read plus one expected error path, and
prints `PASS`/`FAIL`.

## Errors

Every tool returns `{"error": <msg>, "code": <CODE>}` on failure. Stable codes:

| code                     | when                                              |
| ------------------------ | ------------------------------------------------- |
| `BAD_ARG`                | missing/invalid argument (incl. bad limit/JSON)   |
| `BAD_DATE`               | `since` not `YYYY-MM-DD`                           |
| `BAD_TYPE`               | subscription `type` not in the enum               |
| `BAD_AMOUNT`             | `target_price_minor` not a positive integer       |
| `SUBSCRIPTION_NOT_FOUND` | unknown subscription_id                           |
| `NOTIFICATION_NOT_FOUND` | unknown notification_id                           |
| `ACCOUNT_NOT_FOUND`      | unknown official account_id                       |
| `ALREADY_SUBSCRIBED`     | user already subscribes to that official account  |
