# visa_and_advisory_mock

Local, hermetic FastMCP mock for travel-compliance workflows: visa entry
requirements, eVisa application lifecycle, and government travel
advisories. Backed by a single SQLite file. Pure Python + stdlib
`sqlite3`. No network calls.

Transport: **streamable-HTTP only**. Terrarium/Docker runs it on container port
`8000`. There is no
admin / clock / mutation tool on the MCP surface — state changes between
stages are written directly to the runtime sqlite file by the
orchestrator via `event.yaml` `mutation` events.

## Install

```bash
uv sync   # or: pip install -e .
```

## Run (HTTP)

```bash
visa-and-advisory-mock \
    --host 0.0.0.0 \
    --port 8000 \
    --env ../../envs/visa_and_advisory/japan_20d_may
```

CLI flags:

| flag      | default   | meaning                                                       |
| --------- | --------- | ------------------------------------------------------------- |
| `--host`  | `0.0.0.0` | bind host                                                     |
| `--port`  | recommended `8000` for Docker/Terrarium parity | bind port              |
| `--env`   | required  | Path to env dir. `<env>/init.sql` is applied on cold start.   |
| `--debug` | off       | verbose logging to stderr                                     |

Every cold start unlinks `<env>/runtime.db` and recreates it fresh.
The package ships no seed data — the env's `init.sql` provides
everything (visa products, entry rules, advisories, applications-in-flight).

## Tools

Agent-facing (all returned via `tools/list`):

| tool                       | summary |
| -------------------------- | ------- |
| `check_entry_requirements` | Look up visa rules + transit advice for a (nationality, destination, purpose) triple. |
| `list_visa_products`       | List visa products for a (nationality, destination) pair. |
| `get_visa_product`         | Full product details, including form schema. |
| `start_visa_application`   | Create a draft application. |
| `upload_document`          | Attach a document reference to an application. |
| `submit_visa_application`  | Submit a draft (or RFI'd) application; transitions to processing. |
| `get_visa_application`     | Full application state, documents, and history. |
| `list_visa_applications`   | All applications for a user (most recent first). |
| `get_advisory`             | Travel advisory level (1-4) and text for a country. |
| `subscribe_advisory`       | Subscribe an opaque sink to advisory updates. |

## Example env

See [`envs/visa_and_advisory/japan_20d_may/`](../../envs/visa_and_advisory/japan_20d_may/) for the
Japan 20-day (May 2026) snapshot.

```bash
visa-and-advisory-mock --env ../../envs/visa_and_advisory/japan_20d_may
```

## Smoke test

```bash
python scripts/smoke_http.py
# prints "PASS" and exits 0
```

The script starts the server in a subprocess on a free port and
exercises `list_visa_products`, `start_visa_application`,
`upload_document`, `submit_visa_application`, `get_advisory`, and a
`product_not_found` negative path over real streamable-HTTP.

## Conventions

- Country codes: ISO 3166-1 alpha-2 uppercase.
- Currency codes: ISO 4217.
- Fees: integers in major currency units (3000 means 3000 JPY).
- Dates on the wire: `YYYY-MM-DD` ISO strings.
- Wall-clock timestamps in stored rows: ISO-8601 UTC strings.
- IDs are deterministic sequence counters backed by the `_counters` table.
