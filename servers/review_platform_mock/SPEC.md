# review_platform_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `review-mock` MCP server.

## 1. Purpose

`review_platform_mock` is a self-contained, fully-offline mock of a
merchant-review & booking platform (大众点评 / 好好住 style) — merchant
discovery, ratings/reviews + 晒图, 团购套餐 (group-buy deals), 订座/预约
(reservations), merchant Q&A, and 收藏 (saved merchants). It exists so
benchmark tasks can exercise an agent's ability to discover and compare
merchants (e.g. picking a 团建 venue), read reviews/deals, make bookings,
and react to deterministic state changes injected via out-of-band SQL
mutations.

The server makes **no** network calls and ships **no** bundled seed data —
state enters only through the env-directory `init.sql` script.

Non-goals:

- No real payment. Deals/reservations never call an external network.
- No inventory/capacity ledger beyond a per-merchant `max_party_size` guard
  and per-deal `status`.
- No authentication. Identity is whatever the caller passes as `user_id`.
- No geocoding/maps; `area` is a free-text district label.

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`, `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.

## 3. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`,
and surface errors as `{"error": "...", "code": "..."}` rather than raising
across the MCP boundary. Money is integer minor units (分). Ratings are
stored as INTEGER tenths and surfaced as a 1.0–5.0 float. Dates are ISO
`YYYY-MM-DD`; datetimes ISO `YYYY-MM-DDTHH:MM[:SS]`. IDs are
domain-prefixed strings.

### 3.1 `search_merchants(category, city?, area?, min_rating?, price_band?, sort=rating, limit=20) -> str`

`category` ∈ {`restaurant`, `venue`, `vet`, `home_service`} (required).
`price_band` ∈ {`$`, `$$`, `$$$`, `$$$$`}. `sort` ∈ {`rating`, `price_asc`,
`price_desc`, `review_count`}. `min_rating` is a 1.0–5.0 float. `limit`
defaults 20, clamped to 100. Returns a list of merchant summaries:

```json
[{"merchant_id": "mer_venue_0001", "name": "云端宴会厅 (陆家嘴店)",
  "category": "venue", "city": "上海", "area": "浦东新区",
  "rating": 4.8, "review_count": 3, "avg_price_minor": 58000,
  "price_band": "$$$$", "has_private_room": true, "max_party_size": 200,
  "tags": ["宴会厅","团建","年会","江景","可定制"]}, ...]
```

Errors: `BAD_CATEGORY`, `BAD_ARG`.

### 3.2 `get_merchant(merchant_id) -> str`

Full merchant detail (summary fields + `address`, `phone`, `hours`).
Errors: `MERCHANT_NOT_FOUND`.

### 3.3 `get_recommendations(category, area?, limit=5) -> str`

Top-rated merchants in a category (optionally scoped to `area`), sorted by
rating then review_count. `limit` defaults 5, clamped to 50. Returns
merchant summaries. Errors: `BAD_CATEGORY`, `BAD_ARG`.

### 3.4 `list_reviews(merchant_id, limit=20) -> str`

Newest-first. `limit` defaults 20, clamped to 200.

```json
[{"review_id": "rev_00000003", "merchant_id": "mer_rest_0001",
  "user_id": "usr_li_wei", "rating": 4, "body": "...",
  "image_captions": [], "created_at": "2026-05-03T12:40:00Z"}, ...]
```

Errors: `MERCHANT_NOT_FOUND`.

### 3.5 `write_review(user_id, merchant_id, rating, body, image_captions?) -> str`

`rating` is an integer 1–5; `body` required; `image_captions` an optional
list. Inserts the review and **recomputes** the merchant's aggregate rating
(`rating_tenths`) and `review_count` in a single SAVEPOINT.

```json
{"review_id": "rev_00000041", "merchant_id": "mer_rest_0001",
 "user_id": "usr_li_wei", "rating": 5, "created_at": "...",
 "merchant_new_rating": 4.8, "merchant_review_count": 4}
```

Errors: `BAD_RATING`, `MERCHANT_NOT_FOUND`, `BAD_ARG`.

### 3.6 `list_merchant_deals(merchant_id) -> str`

```json
[{"deal_id": "deal_00000005", "merchant_id": "mer_venue_0001",
  "title": "云端宴会厅团建包场", "description": "...",
  "price_minor": 680000, "list_price_minor": 800000, "serves": 100,
  "valid_until": "2026-12-31", "status": "active"}, ...]
```

`status` ∈ {`active`, `sold_out`, `expired`}. Errors: `MERCHANT_NOT_FOUND`.

### 3.7 `get_deal(deal_id) -> str`

Single deal in the same shape. Errors: `DEAL_NOT_FOUND`.

### 3.8 `reserve(user_id, merchant_id, datetime, party_size, deal_id?) -> str`

`datetime` ISO `YYYY-MM-DDTHH:MM[:SS]`. `party_size` a positive int and must
not exceed the merchant's `max_party_size` (when > 0). `deal_id` optionally
attaches a deal that must belong to the merchant and be `active`.

```json
{"reservation_id": "resv_000003", "user_id": "usr_li_wei",
 "merchant_id": "mer_rest_0006", "merchant_name": "海底捞...",
 "datetime": "2026-05-24T19:00:00", "party_size": 8,
 "deal_id": "deal_00000003", "status": "confirmed", "created_at": "..."}
```

Errors: `BAD_DATE`, `MERCHANT_NOT_FOUND`, `PARTY_SIZE_EXCEEDED`,
`DEAL_NOT_FOUND`, `DEAL_UNAVAILABLE`, `BAD_ARG`.

### 3.9 `list_reservations(user_id) -> str`

Newest-first, joined with `merchant_name`. `status` ∈ {`confirmed`,
`cancelled`}.

### 3.10 `cancel_reservation(reservation_id) -> str`

Returns `{reservation_id, status: "cancelled"}`. Idempotent. Errors:
`RESERVATION_NOT_FOUND`.

### 3.11 `get_merchant_qa(merchant_id) -> str`

Newest-first list of `{qa_id, merchant_id, user_id, question, answer,
answered_by, created_at}` (`answer`/`answered_by` may be null). Errors:
`MERCHANT_NOT_FOUND`.

### 3.12 `ask_question(user_id, merchant_id, body) -> str`

Creates a Q&A entry with `answer=null`. Errors: `MERCHANT_NOT_FOUND`,
`BAD_ARG`.

### 3.13 `save_merchant(user_id, merchant_id) -> str`

Idempotent upsert into `saved_merchants`. Returns `{user_id, merchant_id,
saved: true, saved_at}`. Errors: `MERCHANT_NOT_FOUND`, `BAD_ARG`.

### 3.14 `list_saved_merchants(user_id) -> str`

Newest-first list of saved-merchant summaries, each with a `saved_at` field.

## 4. Storage

SQLite, one file per server. `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL`.

| table              | purpose                                                            |
| ------------------ | ------------------------------------------------------------------ |
| `merchants`        | discoverable merchants; `rating_tenths`, `avg_price_minor`, hours  |
| `reviews`          | per-merchant reviews (rating 1–5) with optional 晒图 captions      |
| `deals`            | 团购套餐 with `price_minor`/`list_price_minor` and status          |
| `reservations`     | 订座/预约 with party_size and optional deal_id                     |
| `merchant_qa`      | merchant Q&A threads                                               |
| `saved_merchants`  | per-user 收藏 set (composite PK)                                   |
| `_counters`        | atomic seq counters used to mint stable ids                        |

## 5. State injection

No JSON seed. The server takes `--env <dir>` and on cold start:

1. Unlinks `<env>/runtime.db` (and WAL sidecars).
2. Creates the schema.
3. `executescript`s `<env>/init.sql` if present.
4. Opens streamable-HTTP on `<host>:<port>/mcp`.

The minimal stateless env is `envs/review_platform/empty/`.

## 6. State evolution across stages

The task orchestrator drives state changes through `mutation` events. A
mutation is one or more SQL statements against this server's runtime DB; the
dispatch path is identical to a caller running raw SQL. This server has no
management CLI, no sweep loop, and no runtime clock — e.g. a deal selling
out is a stage-N `UPDATE deals SET status='sold_out'`.

## 7. Logging & ops

- `logging.getLogger(__name__)` everywhere; handler attached to stderr only.
- No `print()` in the package.

## 8. Appendix — error codes

| code                  | meaning                                                       |
| --------------------- | ------------------------------------------------------------- |
| `MERCHANT_NOT_FOUND`  | `merchant_id` does not exist                                  |
| `DEAL_NOT_FOUND`      | `deal_id` does not exist                                      |
| `DEAL_UNAVAILABLE`    | attached deal is not `active`, or not for this merchant       |
| `RESERVATION_NOT_FOUND` | `reservation_id` does not exist                             |
| `PARTY_SIZE_EXCEEDED` | `party_size` exceeds the merchant's `max_party_size`          |
| `BAD_RATING`          | review `rating` not an integer 1–5                            |
| `BAD_CATEGORY`        | `category` not in the allowed set                             |
| `BAD_DATE`            | non-ISO date/datetime string                                  |
| `BAD_ARG`             | catch-all for malformed inputs                                |

## 9. Out of scope

- No real capacity/table inventory beyond `max_party_size`.
- No pagination cursors (`limit` only).
- No geocoding, distance ranking, or maps.
- No auth or per-user permission enforcement.
