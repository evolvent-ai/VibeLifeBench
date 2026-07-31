# notification_hub_mock — implementer spec

## Purpose

Offline mock of a cross-platform **subscription + notification hub**: unified
订阅中心, 价格/关键词/库存/政策 提醒, and 公众号 feed. Aggregation layer over the
other servers' single-purpose `subscribe_*` tools; the connective tissue for
备考 / 购物 / 理财 / 租房 tasks.

## Non-goals

- No clock, no RNG, no uuid, no admin CLI.
- **Never fabricates notifications.** Notification rows are static seed history.
  `create_subscription` / `create_price_alert` record intent only. New
  notifications + status transitions arrive as out-of-band SQL mutations.
- Not a payment/booking system; it only watches and inboxes.

## Stack

FastMCP (`mcp.server.fastmcp`) streamable-HTTP at `/mcp`; stdlib `sqlite3`
(WAL, autocommit, FK on); IDs from `_counters`; money in 分 (CNY minor units);
timestamps ISO-8601 `...Z`; `json.dumps(ensure_ascii=False)`.

## Tables

- `subscriptions(subscription_id PK, user_id, source, type, target, condition_json, status, created_at, updated_at)`
  — type ∈ price_drop/restock/policy_update/new_content/price_target/keyword;
  status ∈ active/paused/deleted.
- `notifications(notification_id PK, user_id, source, type, subscription_id FK?, title, body, payload_json, created_at, read)`.
- `price_alerts(alert_id PK, user_id, item_ref, target_price_minor, currency, status, created_at)`
  — status ∈ active/triggered/cancelled.
- `official_accounts(account_id PK, name, category, description)`.
- `official_account_subscriptions(user_id, account_id) PK(user_id, account_id)`.
- `official_account_posts(post_id PK, account_id FK, title, summary, url, published_at)`.
- `_counters(key PK, value)` — keys: `subscription_seq`, `notification_seq`, `alert_seq`.

ID formats: `sub_%06d`, `ntf_%08d`, `alr_%06d`.

## Tools — request / response

JSON-text responses (a stringified JSON object/array). `condition` and
`payload` are returned **parsed** (objects), not as raw JSON strings.

### list_subscriptions(user_id, status?)
→ `[Subscription]`. status ∈ {active,paused,deleted}; omitted → excludes deleted.
Sorted by created_at asc.

### get_subscription(subscription_id) → `Subscription`
Errors `SUBSCRIPTION_NOT_FOUND`.

`Subscription` = `{subscription_id, user_id, source, type, target, condition, status, created_at, updated_at}`.

### create_subscription(user_id, source, type, target, condition_json?)
→ `Subscription` (status `active`). Validates `type` enum (`BAD_TYPE`), requires
user_id/source/target (`BAD_ARG`); `condition_json` must parse as JSON if given.

### update_subscription(subscription_id, target?, source?, condition_json?)
→ `Subscription`. ≥1 field required (`BAD_ARG`). Bumps `updated_at`.

### pause_subscription / resume_subscription / delete_subscription(subscription_id)
→ `Subscription` with status paused/active/deleted respectively. Idempotent.

### list_notifications(user_id, unread_only?, source?, since?, limit?)
→ `[Notification]` newest-first. `unread_only` bool; `source` exact match;
`since` `YYYY-MM-DD` keeps created_at ≥ since (`BAD_DATE` if malformed);
`limit` default 50, clamped to 500 (`BAD_ARG` if < 1).

### get_notification(notification_id) → `Notification`
Errors `NOTIFICATION_NOT_FOUND`.

`Notification` = `{notification_id, user_id, source, type, subscription_id, title, body, payload, created_at, read}`.

### mark_read(notification_id) → `Notification` (read=true). Idempotent.

### mark_all_read(user_id) → `{user_id, marked_read}` (count newly flipped).

### create_price_alert(user_id, item_ref, target_price_minor)
→ `PriceAlert` (status `active`). `target_price_minor` positive int (`BAD_AMOUNT`).

### list_price_alerts(user_id) → `[PriceAlert]`
`PriceAlert` = `{alert_id, user_id, item_ref, target_price_minor, currency, status, created_at}`.

### subscribe_official_account(user_id, account_id)
→ `OfficialAccount` + `subscribed_at`. Errors `ACCOUNT_NOT_FOUND`, `ALREADY_SUBSCRIBED`.

### list_official_accounts(user_id) → `[OfficialAccount + subscribed_at]`.

### get_account_feed(account_id, limit?)
→ `[Post]` newest-first, limit default 20 / max 200. Errors `ACCOUNT_NOT_FOUND`.
`Post` = `{post_id, account_id, title, summary, url, published_at}`.

## Error-code contract

`BAD_ARG`, `BAD_DATE`, `BAD_TYPE`, `BAD_AMOUNT`, `SUBSCRIPTION_NOT_FOUND`,
`NOTIFICATION_NOT_FOUND`, `ACCOUNT_NOT_FOUND`, `ALREADY_SUBSCRIBED`. All surfaced
as `{"error": msg, "code": CODE}`; unexpected exceptions map to `BAD_ARG`.
