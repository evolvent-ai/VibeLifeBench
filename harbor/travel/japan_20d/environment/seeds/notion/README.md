# li_wei_workspace

Seed for Li Wei's personal Notion workspace, with a reference date of
`2026-05-01`. The shape was chosen to support the `travel/japan_20d`
benchmark task, but stands on its own as a small, plausible workspace.

## What's in it

- **1 user** (`22222222-…`, "Li Wei") + 1 bot integration (`11111111-…`).
- **1 workspace** ("Li Weitranslated content") owned by Li Wei.
- **5 top-level pages**:
  - `Japan Trip Journal (2026-05)` — anchor doc the agent edits across
    the trip; pre-populated with a heading, intro paragraph, two
    to-do items, and two checklist bullets.
  - `Reading List` — small carry-over personal page.
  - `Project Goals 2026` — annual planning doc.
  - `Notes` — parent page with 2 child pages:
    - `Tokyo Restaurants` (bullets)
    - `Meeting Notes 2026-04` (paragraph)
- **2 databases**:
  - `Tasks` — title / status / done / due. 3 seeded rows (passport
    check done, medical kit in-progress, Hakone Free Pass todo).
  - `Books` — title / author / rating. 2 seeded rows.

## IDs

All ids are real (dashed) UUIDs so they round-trip through normal
`uuid.UUID(...)` parsing used by clients. The fixed
prefixes are:

| Prefix | Class |
|---|---|
| `aaaaaaaa-…` | Pages |
| `bbbbbbbb-…` | Databases |
| `cccccccc-…` | Database rows |
| `dddddddd-…` | Blocks |
| `1111…` / `2222…` | Users |
| `0000…` | Workspace |

## Usage

```bash
notion-mock \
  --env ../../envs/notion/li_wei_workspace \
  --host 0.0.0.0 --port 8000
```

Or via Docker:

```bash
docker build -t notion-mock .
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/notion/li_wei_workspace:/env-seed:ro" \
  vibe-agent-benchmark/notion_mock:latest
```
