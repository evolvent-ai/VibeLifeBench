# notion-mock

A FastMCP-based, fully-offline mock of Notion's HTTP API. Runs over
**streamable-HTTP** (no stdio) with a local SQLite database. Tool names
match Notion's `operationId` convention (`API-post-page`,
`API-get-block-children`, …) so existing benchmark tasks keep working
when this server replaces the legacy Node + Postgres implementation.

See [SPEC.md](./SPEC.md) for the implementer-facing spec.

## Tools (agent-facing)

### Fully implemented (12)

- **Pages**: `API-post-page`, `API-retrieve-a-page`, `API-patch-page`,
  `API-retrieve-a-page-property`.
- **Blocks**: `API-get-block-children`, `API-patch-block-children`,
  `API-retrieve-a-block`, `API-update-a-block`, `API-delete-a-block`.
- **Database**: `API-post-database-query`.
- **Search**: `API-post-search`.
- **Users**: `API-get-self`.

### Stubs (return `{"error":"NOT_IMPLEMENTED","code":"NOT_IMPL"}`)

`API-create-a-database`, `API-retrieve-a-database`,
`API-update-a-database`, `API-create-a-comment`, `API-retrieve-a-comment`,
`API-get-user`, `API-get-users`.

There is **no** admin tool exposed over MCP. There is no out-of-band
admin module either — stage mutations are applied by the orchestrator
writing direct SQL against `<env>/runtime.db`.

## Quick start

```bash
notion-mock \
  --host 127.0.0.1 \
  --port 8000 \
  --env "$(git rev-parse --show-toplevel)/envs/notion/li_wei_workspace"
```

The streamable-HTTP endpoint is at `http://<host>:<port>/mcp`.

## CLI flags

- `--host` (default `0.0.0.0`)
- `--port` (pass `8000` for Docker/Terrarium parity)
- `--env PATH` — env directory containing an optional `init.sql`. On
  cold start the server unlinks any leftover `runtime.db`, creates the
  schema, runs `init.sql` if present, and serves MCP.
- `--debug` — verbose logging

## IDs

Object ids are deterministic dashed UUID-shaped strings generated from
a per-kind counter (`counters` table) + `sha256("<kind>:<n>")`. No
`random` or `uuid.uuid4()` is used anywhere in the package.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server on a free port against a temp copy of
`envs/notion/li_wei_workspace`, round-trips the core 5 tools, prints
`PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable
codes:

`PAGE_NOT_FOUND`, `BLOCK_NOT_FOUND`, `DATABASE_NOT_FOUND`,
`USER_NOT_FOUND`, `BAD_PARENT`, `BAD_PROPERTY`, `BAD_BLOCK_TYPE`,
`NOT_IMPL`, `BAD_ARG`.
