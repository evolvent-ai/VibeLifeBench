# notion_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `notion-mock` MCP server.

## 1. Purpose

`notion_mock` is a self-contained, fully-offline mock of Notion's HTTP
API — workspaces, pages, blocks, databases, users — exposed over the
Model Context Protocol so benchmark tasks can read and write a
realistic Notion workspace without a live Notion integration. It
replaces the older Node + Postgres `notion-mcp-server`.

Tool names match Notion's `operationId` convention from
`scripts/notion-openapi.json` (e.g. `API-post-page`), so benchmark
prompts that reference these names continue to work.

The server makes **no** network calls and ships **no** bundled seed
data. State enters through the env directory's `init.sql`.

Non-goals:

- Not a faithful drop-in for every Notion endpoint — only the 12
  highest-traffic operations are fully implemented; the rest stub out
  with `NOT_IMPL` (see §4).
- No auth. Identity is the seeded "bot" user returned by `API-get-self`.
- No file uploads. No real-time updates. No comments threading depth.
- No pagination: tools accept `start_cursor`/`page_size` for API
  parity but every list comes back in a single page (capped at 100).

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`,
  `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.

## 3. Tools — fully implemented

All tools are `async def`, return `json.dumps(value, ensure_ascii=False)`,
and surface errors as `{"error": "...", "code": "..."}` rather than
raising across the MCP boundary. IDs are dashed UUIDs.

### 3.1 Pages

#### `API-post-page(parent, properties?, icon?, cover?, children?) -> str`

Create a new page (or, when `parent.type == "database_id"`, a new
database row). Returns the new page object.

`parent` accepts one of:
- `{"type":"page_id","page_id":"<uuid>"}`
- `{"type":"database_id","database_id":"<uuid>"}`
- `{"type":"workspace","workspace":true}`

`properties` is a Notion-shaped property map. A `title` property of
shape `{"title":[{"type":"text","text":{"content":"..."}}]}` is
extracted and stored on the page's `title` column for fast search.

`children` is an array of block specs appended after creation (recursive
— each child may carry its own `children` array).

Errors: `BAD_PARENT`, `BAD_PROPERTY`, `BAD_ARG`.

#### `API-retrieve-a-page(page_id) -> str`

Return the page object — including `parent`, `properties`,
`created_time`, `last_edited_time`, `archived`, `icon`, `cover`, and a
synthetic Notion-style URL. Also resolves database-row page ids.

Errors: `PAGE_NOT_FOUND`.

#### `API-patch-page(page_id, properties?, icon?, cover?, archived?, in_trash?) -> str`

Update a page's properties (shallow merge), icon, cover, or archive
state. Returns the updated page.

Errors: `PAGE_NOT_FOUND`.

#### `API-retrieve-a-page-property(page_id, property_id) -> str`

Return a single property value. `property_id` may be the property name
(common: `"title"`, `"Status"`) or the synthetic id stored on the
property object.

Errors: `PAGE_NOT_FOUND`, `BAD_PROPERTY`.

### 3.2 Blocks

#### `API-get-block-children(block_id, page_size=100, start_cursor?) -> str`

Returns `{object:"list", results:[...], has_more:false, next_cursor:null, type:"block", block:{}}`.

`block_id` can be either a page id (returns top-level page blocks) or a
parent block id (returns nested children). Archived blocks are
excluded. Order: by `position` ascending.

Errors: `PAGE_NOT_FOUND` (only when the parent id doesn't resolve to
anything we know about — page, block, or DB row).

#### `API-patch-block-children(block_id, children, after?) -> str`

Append blocks. `children` is a non-empty array of block specs of the
shape `{"type":"<type>","<type>":{<content>}}`. Nested `children`
arrays are inserted recursively. Returns the list of just-inserted
blocks (top level only).

`after` is accepted for API parity but ignored — new blocks always
append to the end.

Errors: `BAD_ARG` (empty children), `BAD_BLOCK_TYPE`, `PAGE_NOT_FOUND`.

#### `API-retrieve-a-block(block_id) -> str`

Return one block object.

Errors: `BLOCK_NOT_FOUND`.

#### `API-update-a-block(block_id, body?, **kwargs) -> str`

Update a block. Accepts either the canonical Notion body shape (e.g.
`{"paragraph":{"rich_text":[...]}}`) or flat keyword args. Setting
`archived=true` archives the block. `type` may be changed but content
is preserved.

Errors: `BLOCK_NOT_FOUND`, `BAD_BLOCK_TYPE`.

#### `API-delete-a-block(block_id) -> str`

Soft-delete by setting `archived=true`. The block is still resolvable
via retrieve but is hidden from child listings.

Errors: `BLOCK_NOT_FOUND`.

### 3.3 Database

#### `API-post-database-query(database_id, filter?, sorts?, page_size=100, start_cursor?) -> str`

Run a filter/sort over a database's rows. Returns
`{object:"list", results:[<page>...], has_more:false, next_cursor:null, type:"page_or_database", page_or_database:{}}`.

Filter support:
- Combinators: `and`, `or` (arbitrary nesting).
- String-y types (`rich_text`, `title`, `url`, `email`,
  `phone_number`, `select`, `status`): `equals`, `contains`,
  `starts_with`, `ends_with`, `is_empty`, `is_not_empty`.
- `checkbox`: `equals`.
- `number`: `equals`, `greater_than`, `less_than`,
  `greater_than_or_equal_to`, `less_than_or_equal_to`.

Sort support: `[{property|timestamp, direction}]` — `direction` is
`"ascending"` or `"descending"`; `timestamp` is `"created_time"` or
`"last_edited_time"`.

Errors: `DATABASE_NOT_FOUND`, `BAD_ARG`.

### 3.4 Search

#### `API-post-search(query?, filter?, sort?, page_size=100, start_cursor?) -> str`

Substring search across page titles, page properties text, and
database titles. `filter={"value":"page"}` or `{"value":"database"}`
narrows the object kind. `sort={"direction":..., "timestamp":...}`
orders the result list. Empty `query` returns everything.

### 3.5 Users

#### `API-get-self() -> str`

Return the bot user representing this integration. Prefers
`type='bot'` rows; falls back to the first user. Always returns the
same object across calls in a given env.

Errors: `USER_NOT_FOUND`.

## 4. Stubbed tools

The following are registered so the agent gets a clean error rather
than "unknown tool":

- `API-create-a-database`, `API-retrieve-a-database`,
  `API-update-a-database`
- `API-create-a-comment`, `API-retrieve-a-comment`
- `API-get-user`, `API-get-users`

All return `{"error":"NOT_IMPLEMENTED","code":"NOT_IMPL"}`.

## 5. Storage

SQLite (WAL mode, FK on). Plain table names (no `notion.*` schema
prefix). Schema is created by `init_schema(conn)` on startup; no
bundled seed.

### 5.1 Tables

- `users(user_id PK, name, avatar_url, email, type)` — `type ∈ {person, bot}`.
- `workspaces(workspace_id PK, name, owner_user_id)`.
- `pages(page_id PK, parent_type, parent_id, title, archived,
  created_time, last_edited_time, properties_json, icon, cover)` —
  `parent_type ∈ {workspace, page_id, database_id}`.
- `databases(database_id PK, parent_type, parent_id, title,
  schema_json, archived, created_time, last_edited_time)`.
- `database_rows(row_id PK, database_id FK, properties_json,
  created_time, last_edited_time, archived)` — `row_id` is also a
  page_id (Notion treats DB rows as pages).
- `blocks(block_id PK, parent_block_id, parent_page_id, type,
  content_json, has_children, archived, position, created_time,
  last_edited_time)` — exactly one of `parent_block_id` /
  `parent_page_id` is set per row.
- `comments(comment_id PK, parent_page_id, discussion_id,
  content_json, created_by, created_time)` — present for schema parity;
  not exercised by any implemented tool.
- `counters(key PK, value)` — backing store for deterministic id
  generation (`utils.ids.next_uuid`).

JSON-shaped columns store the raw Notion JSON as TEXT and are
re-parsed on every read.

## 6. Clock

There is **no** simulated clock. Newly-written rows are stamped with
`utils.dates.DEFAULT_WRITE_TIME` (`2026-01-01T00:00:00.000Z`). Tasks
that care about per-stage `last_edited_time` set it via event-yaml
mutations against `runtime.db`.

## 7. Appendix — error codes

| Code | When |
|---|---|
| `PAGE_NOT_FOUND` | Page id doesn't resolve to a page or DB row. |
| `BLOCK_NOT_FOUND` | Block id doesn't resolve. |
| `DATABASE_NOT_FOUND` | Database id doesn't resolve. |
| `USER_NOT_FOUND` | No users seeded. |
| `BAD_PARENT` | `parent` malformed or its target doesn't exist. |
| `BAD_PROPERTY` | Property id/name not on the page. |
| `BAD_BLOCK_TYPE` | Block `type` missing or unknown. |
| `NOT_IMPL` | Stubbed tool — see §4. |
| `BAD_ARG` | Generic validation failure. |
