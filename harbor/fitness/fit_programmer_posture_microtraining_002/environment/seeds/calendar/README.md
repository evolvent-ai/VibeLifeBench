# calendar env for fit_programmer_posture_microtraining_002

## Scenario Use

Work blocks, deployment windows, Wednesday recurring meetings, incident review meetings, and subsequent hotfix mutations.

## Time Range and Time Zone

2026-07-01 to 2026-07-28, Asia/Shanghai, all times use `+08:00`.

## Key Objects

- User: `user_zou_ming` / `zou.ming@example.invalid`
- task/env: `fit_programmer_posture_microtraining_002`
- Key object IDs are provided only for reviewer reconciliation; the agent needs to discover them by querying through MCP tools.

## Relationship to task/rubric

This env is a task-local seed. The rubric will assess long-term consistency using the MCP final state, tool trace, workspace files, and response text.

## Status Enumeration and Amount Conventions

Amounts are expressed in cents; calendar statuses follow the server schema; the initial Sent field for email is empty; course and product authorization is governed by the user's boundaries in the workspace.

## Loading and Smoke Test

The corresponding server schema can be used to load `init.sql`; this generation script will perform basic SQLite schema + init.sql validation.

## Core Business Table Audit

| Table Name | Core | Initial Row Count | Dependent Capability Axis/check | Interference Strategy | Meets Standard |
|---|---|---:|---|---|---|
| `calendars` | No | 1 | Single-user default calendar container | Configuration container table, not a retrieval/filter entry point and does not carry primary-flow or safety-critical facts | Not applicable |
| `events` | Yes | 210 | Work conflicts, microtraining scheduling, mutation recovery and final refresh / `chk_s02_release_window`, `chk_s03_microbreak_series`, `chk_s06_calendar_mutation_discovered`, `chk_s06_diff_refresh_calendar_after_mutation`, `chk_s19_work_conflict_split`, `chk_final_diff_latest_refresh_before_review` | Work blocks, rollout on-call coverage, Wednesday recurring meetings, hotfixes, incident review meetings, personal matters, and unrelated reminders coexist; near key conflicts, interference is retained from nearby dates, nearby time periods, and unrelated events | Yes |

## Data Source

Synthetic data, for offline benchmark use only; it contains no real personal sensitive information.
