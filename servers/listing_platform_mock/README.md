# listing-mock

A FastMCP-based, fully-offline mock of a 链家/贝壳/58/闲鱼/汽车之家 style
classified-listings marketplace (non-standard listings + agents + viewings +
user self-listing). Runs over **streamable-HTTP** (no stdio) with a local
SQLite database. Distinct from the ecommerce server (standardized SKU cart
shopping): here listings are heterogeneous (rentals, resale houses, used cars,
secondhand goods) with flexible per-category attributes, human agents, and
viewing appointments.

The server has **no clock, no RNG, no admin CLI**. IDs are issued from a
`_counters` table; tool-created timestamps are deterministic. All state enters
through the env's `init.sql`; state changes mid-task arrive as out-of-band SQL
mutations from the orchestrator — the server is oblivious to them.

Money is in integer minor units (分; ¥1 = 100). For `rent` listings
`price_minor` is the **monthly rent**; for `sale_house` / `used_car` /
`secondhand` it is the **total price**. Dates are ISO `YYYY-MM-DD`; timestamps
are ISO-8601 with timezone.

## Tools (agent-facing)

Discovery & detail
- `search_listings(category, city?, district?, min_price_minor?, max_price_minor?, min_rooms?, max_rooms?, keyword?, sort?, limit?)` — category ∈ {rent, sale_house, used_car, secondhand}; sort ∈ {price_asc, price_desc, newest, area_desc}; limit default 20, max 200.
- `get_listing(listing_id)` — summary view.
- `get_listing_detail(listing_id)` — full attrs, photo captions (text), description, owner, embedded agent.

Agents
- `get_agent(agent_id)` — agent profile (name, agency, phone, rating, deals_count, service_area).
- `contact_agent(user_id, listing_id, message)` — record a message to a listing's agent.

Saved listings
- `save_listing(user_id, listing_id)`
- `unsave_listing(user_id, listing_id)`
- `list_saved(user_id)`

Viewings
- `schedule_viewing(user_id, listing_id, datetime)` — `datetime` ISO-8601 w/ tz.
- `list_viewings(user_id)`
- `cancel_viewing(viewing_id)`

Self-listing & subscriptions
- `post_listing(user_id, category, title, price_minor, city, district?, community?, area_sqm?, rooms?, metro?, description?, attrs?, photos?)`
- `delist(listing_id, user_id?)` — if `user_id` given it must own the listing.
- `subscribe_search(user_id, query_json)` — save a search; `query_json` must be valid JSON.

Market
- `get_market_stats(area_or_community)` — avg transaction price rows; matches `area` exactly then by substring.

Optional params are marked `?`. Every tool returns a JSON string
(`ensure_ascii=False` so Chinese stays readable) or `{"error", "code"}`.

## Quick start

```bash
pip install -e .
listing-platform-mock --env ../../envs/listing_platform/shanghai_rent_2026 --port 8016
# MCP endpoint: http://127.0.0.1:8016/mcp
```

## CLI flags

| Flag      | Default   | Meaning                                            |
| --------- | --------- | -------------------------------------------------- |
| `--env`   | required  | Path to `envs/listing_platform/<env_name>/` dir.   |
| `--host`  | `0.0.0.0` | Bind host.                                         |
| `--port`  | `8016`    | Bind port (dev). Docker image uses `8000`.         |
| `--debug` | off       | DEBUG-level logging.                               |

## Smoke test

```bash
python servers/listing_platform_mock/scripts/smoke_http.py
```
Boots the server on a free port against `shanghai_rent_2026`, round-trips a
handful of tools (incl. an expected error path), asserts on seeded values, and
prints `PASS` / `FAIL`.

## Errors

Every tool may return `{"error": <msg>, "code": <CODE>}`. Stable codes:

| Code               | Meaning                                                  |
| ------------------ | -------------------------------------------------------- |
| `BAD_ARG`          | Missing/invalid argument (also catch-all for internals). |
| `BAD_DATE`         | Malformed ISO date / datetime.                           |
| `BAD_CATEGORY`     | `category` not in the allowed set.                       |
| `BAD_PRICE`        | `price_minor` not a positive integer.                    |
| `LISTING_NOT_FOUND`| Unknown `listing_id`.                                    |
| `LISTING_DELISTED` | Action requires an active listing.                       |
| `AGENT_NOT_FOUND`  | Unknown `agent_id`.                                      |
| `VIEWING_NOT_FOUND`| Unknown `viewing_id`.                                    |
| `ALREADY_SAVED`    | Listing already in the user's saved set.                 |
| `NOT_SAVED`        | Listing not in the user's saved set.                     |
| `NOT_OWNER`        | `delist` user_id does not own the listing.               |
| `STATS_NOT_FOUND`  | No market stats match the area/community.                |
