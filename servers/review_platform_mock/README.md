# review-mock

A FastMCP-based, fully-offline mock of a merchant-review & booking platform
(大众点评 / 好好住 style): merchant discovery, ratings/reviews + 晒图,
团购套餐 (group-buy deals), and 订座/预约 (reservations). Runs over
**streamable-HTTP** (no stdio) with a local SQLite database. Money is stored
as integer 分 (1/100 元); the example env uses CNY. Ratings are stored as
INTEGER tenths and surfaced as a 1.0–5.0 float.

See [SPEC.md](./SPEC.md) for the full implementer-facing specification.

## Tools (agent-facing)

- `search_merchants(category, city?, area?, min_rating?, price_band?, sort?, limit?)` — `category` ∈ {restaurant, venue, vet, home_service}.
- `get_merchant(merchant_id)` — rating, avg_price_minor, hours, address, phone, private-room info.
- `get_recommendations(category, area?, limit?)` — top-rated merchants in a category.
- `list_reviews(merchant_id, limit?)`
- `write_review(user_id, merchant_id, rating, body, image_captions?)` — `rating` 1–5; recomputes the merchant's aggregate rating.
- `list_merchant_deals(merchant_id)` / `get_deal(deal_id)` — 团购套餐.
- `reserve(user_id, merchant_id, datetime, party_size, deal_id?)` — 订座/预约.
- `list_reservations(user_id)` / `cancel_reservation(reservation_id)`
- `get_merchant_qa(merchant_id)` / `ask_question(user_id, merchant_id, body)`
- `save_merchant(user_id, merchant_id)` / `list_saved_merchants(user_id)` — 收藏.

The server has no simulated clock and no management CLI. Stage-driven state
changes are applied as SQL mutations by the task orchestrator.

## Quick start

```bash
# From this directory
pip install -e .

# Run with an env directory.
review-mock \
  --port 8000 \
  --env ../../envs/review_platform/shanghai_dining_2026
```

On startup the server unlinks any `<env>/runtime.db`, creates the schema,
executes `<env>/init.sql` if present, and binds streamable-HTTP at
`http://<host>:<port>/mcp`.

## CLI flags

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host` (default `0.0.0.0`)
- `--port` (default `8017` for local dev; pass `8000` for Docker/Terrarium parity)
- `--debug` — verbose logging.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess against
`envs/review_platform/shanghai_dining_2026` and round-trips
`search_merchants`, `get_merchant`, `list_reviews`, `list_merchant_deals`,
`reserve`, `write_review`, `list_saved_merchants`, plus an expired-deal
reservation expecting `DEAL_UNAVAILABLE`. Prints `PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`MERCHANT_NOT_FOUND`, `DEAL_NOT_FOUND`, `DEAL_UNAVAILABLE`,
`RESERVATION_NOT_FOUND`, `PARTY_SIZE_EXCEEDED`, `BAD_RATING`,
`BAD_CATEGORY`, `BAD_DATE`, `BAD_ARG`.
