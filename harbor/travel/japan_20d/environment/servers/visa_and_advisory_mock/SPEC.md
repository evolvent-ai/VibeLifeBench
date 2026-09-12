# visa-and-advisory-mock — SPEC

Local, hermetic FastMCP mock for travel compliance workflows: entry
requirements, eVisa application lifecycle, and travel advisories. The
server is offline, uses SQLite, and exposes streamable-HTTP at `/mcp`.

## Boot Contract

Terrarium/Docker runs the container on port `8000` and mounts an env
scenario at `/env-seed`; the Dockerfile copies that data to `/env` before
starting the server:

```bash
visa-and-advisory-mock --host 0.0.0.0 --port 8000 --env /env
```

For direct local runs, pass any env directory explicitly:

```bash
visa-and-advisory-mock \
  --host 0.0.0.0 \
  --port 8000 \
  --env ../../envs/visa_and_advisory/japan_20d_may
```

On every cold start the server deletes `<env>/runtime.db` and sidecars,
creates the schema, executes `<env>/init.sql` if present, then opens
streamable-HTTP. There is no bundled seed, no clock, no admin path, and
no MCP mutation tool. Stage changes are applied by the task orchestrator
as out-of-band SQL mutations against the runtime DB.

## CLI Flags

| flag | meaning |
|---|---|
| `--env` | required env directory containing `init.sql` |
| `--host` | bind host |
| `--port` | bind port; pass `8000` for Docker/Terrarium parity |
| `--debug` | verbose stderr logging |

## Agent-Facing Tools

| tool | summary |
|---|---|
| `check_entry_requirements` | Look up visa rules for a nationality, destination, and purpose. |
| `list_visa_products` | List visa products for a nationality and destination. |
| `get_visa_product` | Return product details, fees, processing time, and required documents. |
| `start_visa_application` | Create a draft application for a user/product. |
| `upload_document` | Attach a document reference to an application. |
| `submit_visa_application` | Submit a draft or RFI application. |
| `get_visa_application` | Return application state, documents, and history. |
| `list_visa_applications` | List applications for a user, newest first. |
| `get_advisory` | Return advisory level and text for a country. |
| `subscribe_advisory` | Subscribe an opaque sink to advisory updates. |

All tools return JSON strings. Business errors are returned as
`{"error": "...", "code": "..."}` instead of uncaught exceptions.

## State Model

Schema is created in `src/visa_and_advisory_mock/backends/sqlite_backend.py`.
The main tables are:

- `entry_requirements`
- `visa_products`
- `visa_applications`
- `application_documents`
- `advisories`
- `advisory_subscriptions`
- `notifications`
- `_counters`

The package ships schema only. Scenario data lives under
`envs/visa_and_advisory/<scenario>/init.sql`; the `empty` scenario is the
minimal bootable state.

## Stage Progression

The agent never sees a clock-walk or management mutation tool. If a task
needs an advisory raise, rule update, or visa status transition at a later
stage, `event.yaml` carries an explicit `mutation` entry and the
Terrarium task applies it directly to `runtime.db`.

## Smoke Test

```bash
python scripts/smoke_http.py
```

The smoke test starts the server on a free local port and exercises the
core visa/advisory flows over streamable-HTTP.
