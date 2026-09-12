# notion env for fit_programmer_posture_microtraining_002

## Scenario Use

Initial Notion control center page and numerous interference pages; agent must append long-term state itself.

## Time Range and Time Zone

2026-07-01 to 2026-07-28, Asia/Shanghai, all times use `+08:00`.

## Key Objects

- User: `user_zou_ming` / `zou.ming@example.invalid`
- task/env: `fit_programmer_posture_microtraining_002`
- Key object IDs are provided only for reviewer reconciliation; agent needs to discover them through MCP tool queries.

## Relationship to task/rubric

This env is a task-local seed; rubric will assess long-term consistency based on the MCP final state, tool trace, workspace files, and response text.

## Status Enumeration and Monetary Convention

Monetary amounts use fen as the unit; calendar statuses follow the server schema; initial Sent for email is empty; course and product authorization follows the user's boundaries in the workspace.

## Loading and smoke test

The corresponding server schema can be used to load `init.sql`; this generation script will perform basic validation of the SQLite schema + init.sql.

## Core Business Table Audit

| Table name | Core? | Initial row count | Dependency capability axis/check | Interference strategy | Meets criteria? |
|---|---|---:|---|---|---|
| `blocks` | No | 1 | Initial page block container | Single-page initial block, not an archive search entry; agent may append persistent assets during execution | N/A |
| `pages` | Yes | 211 | Long-term Notion control center, course exclusion, and risk/budget/authorization synchronization and final/cross consistency / `chk_s00_initial_logs`, `chk_cross_stage_progress`, `chk_cross_service_consistency`, `chk_quiet_gap_checks`, `chk_final_review_evidence`, `chk_final_diff_latest_refresh_before_review` | Posture training, office health, courses, equipment, and unrelated work pages are mixed together; nearby titles, old drafts, and unrelated review pages interfere with the key Notion control center | Yes |
| `users` | No | 1 | Notion user configuration | Single-user configuration table, not a search/filter entry point | N/A |
| `workspaces` | No | 1 | Notion workspace configuration | Single-workspace configuration table, does not carry mainline or safety-critical decisions | N/A |

## Data Source

Synthetic data, for offline benchmark only; does not contain real personally sensitive information.
