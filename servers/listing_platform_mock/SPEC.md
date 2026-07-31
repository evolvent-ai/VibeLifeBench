# listing_platform_mock — Implementer SPEC

## Purpose

Offline mock of a classified-listings marketplace (链家/贝壳/58/闲鱼/汽车之家
style): heterogeneous, non-standard listings (rentals, resale houses, used
cars, secondhand goods) with human agents, viewing appointments, user saved
sets, user self-listing, market statistics, and saved searches.

## Non-goals

- Not a standardized SKU/cart store (that is `ecommerce_mock`).
- No payments, escrow, contracts, or messaging threads beyond a single recorded
  contact message.
- No clock, RNG, uuid, or admin CLI. No background jobs.

## Stack

- Transport: streamable-HTTP only, path `/mcp`.
- Framework: FastMCP (`from mcp.server.fastmcp import FastMCP`).
- Storage: stdlib `sqlite3` (WAL, autocommit, FK on). Schema in
  `backends/db.py`; seeds via env `init.sql`.
- Money: integer minor units (分). Layering: tools → services → backends/utils.

## Tables

- `listings(listing_id PK, category, title, city, district, community,
  price_minor, area_sqm, rooms, metro, attrs_json, description, photos_json,
  agent_id FK→agents, owner_user_id, status, listed_at)`
- `agents(agent_id PK, name, agency, phone, rating, deals_count, service_area)`
- `saved_listings(user_id, listing_id FK, saved_at, PK(user_id, listing_id))`
- `viewings(viewing_id PK, user_id, listing_id FK, agent_id, scheduled_at,
  status, created_at)`
- `contacts(contact_id PK, user_id, listing_id FK, agent_id, message, created_at)`
- `market_stats(stat_id PK, area, city, category, avg_price_minor, unit,
  sample_size, period)`
- `search_subscriptions(subscription_id PK, user_id, query_json, created_at)`
- `_counters(key PK, value)` — sequences: `listing_seq`, `viewing_seq`,
  `contact_seq`, `subscription_seq`, `saved_seq`.

Enums: `category ∈ {rent, sale_house, used_car, secondhand}`;
`status ∈ {active, delisted}` (listings) / `{scheduled, cancelled}` (viewings);
`market_stats.unit ∈ {per_month, total, per_sqm}`.

## Tool JSON shapes

All responses are JSON strings (`ensure_ascii=False`). Errors:
`{"error": str, "code": str}`.

### search_listings
Req: `{category, city?, district?, min_price_minor?, max_price_minor?,
min_rooms?, max_rooms?, keyword?, sort?, limit?}`
`sort ∈ {price_asc, price_desc, newest, area_desc}` (default `newest`), limit
default 20 / max 200.
Resp: `[listing_summary, ...]` where listing_summary =
`{listing_id, category, title, city, district, community, price_minor,
area_sqm, rooms, metro, agent_id, status, listed_at}`.
Errors: `BAD_CATEGORY`, `BAD_ARG`.

### get_listing
Req: `{listing_id}` → listing_summary. Errors: `LISTING_NOT_FOUND`.

### get_listing_detail
Req: `{listing_id}` → listing_summary + `{attrs: object, photos: [str],
description, owner_user_id, agent: agent_view | null}`. Errors:
`LISTING_NOT_FOUND`.

### get_agent
Req: `{agent_id}` → `{agent_id, name, agency, phone, rating, deals_count,
service_area}`. Errors: `AGENT_NOT_FOUND`.

### contact_agent
Req: `{user_id, listing_id, message}` → `{contact_id, listing_id, agent_id,
agent, message, created_at, status:"sent"}`. Errors: `LISTING_NOT_FOUND`,
`LISTING_DELISTED`, `BAD_ARG`.

### save_listing / unsave_listing / list_saved
- save Req `{user_id, listing_id}` → `{user_id, listing_id, saved_at,
  status:"saved"}`. Errors `LISTING_NOT_FOUND`, `ALREADY_SAVED`.
- unsave Req `{user_id, listing_id}` → `{..., status:"unsaved"}`. Errors
  `NOT_SAVED`.
- list_saved Req `{user_id}` → `[listing_summary + {saved_at}]` oldest-first.

### schedule_viewing / list_viewings / cancel_viewing
- schedule Req `{user_id, listing_id, datetime}` (`datetime` ISO-8601 w/ tz) →
  `{viewing_id, user_id, listing_id, agent_id, scheduled_at, status:"scheduled",
  created_at}`. Errors `LISTING_NOT_FOUND`, `LISTING_DELISTED`, `BAD_DATE`.
- list_viewings Req `{user_id}` → `[{viewing_id, listing_id, listing_title,
  listing_community, agent_id, scheduled_at, status, created_at}]` earliest-first.
- cancel Req `{viewing_id}` → `{viewing_id, status:"cancelled"}`. Errors
  `VIEWING_NOT_FOUND`.

### post_listing
Req: `{user_id, category, title, price_minor, city, district?, community?,
area_sqm?, rooms?, metro?, description?, attrs?, photos?}` → listing_detail of
the created row (`agent_id=null`, `owner_user_id=user_id`,
`listing_id=lst_<8d>`). Errors `BAD_CATEGORY`, `BAD_PRICE`, `BAD_ARG`.

### delist
Req: `{listing_id, user_id?}` → `{listing_id, status:"delisted"}`. If `user_id`
present it must equal `owner_user_id` else `NOT_OWNER`. Errors
`LISTING_NOT_FOUND`.

### subscribe_search
Req: `{user_id, query_json}` (`query_json` a JSON string) → `{subscription_id,
user_id, query, created_at}`. Errors `BAD_ARG` (invalid JSON).

### get_market_stats
Req: `{area_or_community}` → `[{stat_id, area, city, category, avg_price_minor,
unit, sample_size, period}]` (exact `area` match first, then substring). Errors
`STATS_NOT_FOUND`.

## Error-code contract

`BAD_ARG`, `BAD_DATE`, `BAD_CATEGORY`, `BAD_PRICE`, `LISTING_NOT_FOUND`,
`LISTING_DELISTED`, `AGENT_NOT_FOUND`, `VIEWING_NOT_FOUND`, `ALREADY_SAVED`,
`NOT_SAVED`, `NOT_OWNER`, `STATS_NOT_FOUND`.
