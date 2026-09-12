# chen_yu_workspace

Seed for Chen Yu's personal Notion workspace for the Bali 22-day task.

## What this env represents

- **User**: Chen Yu (Chen Yu), Shanghai-based backend engineer.
- **Reference date**: 2026-06-01.
- **Anchor page**: "Bali Trip 2026 -- Journal" -- the agent edits this
  across the trip run.

## What's in it

- **1 user** + 1 bot integration.
- **1 workspace** ("Chen Yu's workspace") owned by Chen Yu.
- **4 top-level pages**:
  - `Bali Trip 2026 -- Journal` -- anchor doc, mostly empty for agent
  - `Game Dev Notes` -- work notes
  - `Reading List` -- personal
  - `Trip Research` -- Bali research links
- **1 database**: `Tasks` with 3 seeded rows:
  - Book flights (todo)
  - Research Bali activities (in_progress)
  - Get travel insurance (todo)

## IDs

| Prefix | Class |
|--------|-------|
| aaaaaaaa-... | Pages |
| bbbbbbbb-... | Databases |
| cccccccc-... | Database rows |
| dddddddd-... | Blocks |
| 1111.../2222... | Users |
| 0000... | Workspace |

## How to load

```bash
notion-mock \
  --env ../../envs/notion/chen_yu_workspace \
  --host 0.0.0.0 --port 8000
```
