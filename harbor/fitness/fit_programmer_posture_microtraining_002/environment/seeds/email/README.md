# email env for fit_programmer_posture_microtraining_002

## Scenario Purpose

Launch emails, HR benefits emails, nuisance emails, and follow-up course promotion mutation; Sent is initially empty.

## Time Range and Time Zone

2026-07-01 to 2026-07-28, Asia/Shanghai, with all times using `+08:00`.

## Key Objects

- User: `user_zou_ming` / `zou.ming@example.invalid`
- task/env: `fit_programmer_posture_microtraining_002`
- Key object IDs are provided only for reviewer reconciliation; the agent needs to query and discover them through MCP tools.

## Relationship to task/rubric

This env is a task-local seed; the rubric will assess long-term consistency based on the MCP final state, tool trace, workspace files, and response text.

## Status Enumerations and Amount Conventions

Amounts are expressed in fen; calendar statuses follow the server schema; Sent is initially empty; course and product authorization is governed by the user's boundaries in the workspace.

## Loading and Smoke Test

The corresponding server schema can be used to load `init.sql`; this generated script will perform basic validation of the SQLite schema + init.sql.

## Core Business Table Audit

| Table Name | Core? | Initial Row Count | Dependent Capability Axis/check | Interference Strategy | Meets Requirements? |
|---|---|---:|---|---|---|
| `account_config` | No | 1 | Email account configuration | Single-account configuration table; not an email-search entry point and does not carry primary workflow state | N/A |
| `folders` | No | 3 | Inbox/Drafts/Sent containers | Folder enumeration table; the agent completes business assessment through messages and draft status | N/A |
| `messages` | Yes | 203 | Launch notifications, course promotions, HR posture camp, manager drafts, and the draft-only boundary / `chk_s02_release_window`, `chk_s14_diff_course_email_review_reconcile`, `chk_s20_email_draft_only`, `chk_s23_reject_hr_camp`, `chk_final_auth_statement` | Work emails, benefits notifications, course marketing, noise emails, and follow-up mutation emails are interleaved; nearby subjects, similar senders, and unrelated promotional interference appear alongside key threads | Yes |

## Data Source

Synthetic data, for offline benchmark use only; contains no real personal sensitive information.
