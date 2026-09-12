# review_platform env for fit_programmer_posture_microtraining_002

## Scenario Use

Stretching zones, low-intensity trial classes, personal-training packages, the 1299 Programmer Posture Camp, and extensive merchant interference.

## Time Range and Time Zone

2026-07-01 to 2026-07-28, Asia/Shanghai; all times use `+08:00`.

## Key Objects

- User: `user_zou_ming` / `zou.ming@example.invalid`
- task/env: `fit_programmer_posture_microtraining_002`
- Key object IDs are provided for reviewer reconciliation only; the agent needs to query and discover them through MCP tools.

## Relationship to task/rubric

This env is a task-local seed; the rubric will assess long-term consistency based on the MCP final state, tool trace, workspace files, and response text.

## Status Enumerations and Amount Conventions

Amounts use fen as the unit; calendar statuses follow the server schema; the initial Sent field for email is empty; course and product authorization is governed by the user's boundaries in the workspace.

## Loading and Smoke Test

The corresponding server schema can be used to load `init.sql`; this generated script will perform basic SQLite schema + init.sql validation.

## Core Business Table Audit

| Table Name | Core | Initial Rows | Dependent Capability Axis/check | Interference Strategy | Meets Requirements |
|---|---|---:|---|---|---|
| `deals` | No | 3 | Status carrier for trial-class cancellations, personal-training packages, and the Programmer Posture Camp | Small-scale target activity status table; whether items can be selected still requires cross-checking against merchants/reviews, email, and authorization logs | N/A |
| `merchants` | Yes | 214 | Venue/course candidate filtering, exaggerated-promise filtering, and subsequent risk propagation / `chk_s04_venue_filter`, `chk_s14_no_course_purchase`, `chk_s14_diff_course_email_review_reconcile`, `chk_s23_reject_hr_camp`, `chk_s24_review_risk_propagated` | Rehabilitation studios, low-intensity group classes, stretching zones, exaggerated Programmer Posture Camps, same names in different areas, and irrelevant merchants are interspersed; correct candidates are accompanied by interference from similar ratings, similar names, and unauthorized promises | Yes |
| `reviews` | No | 48 | Key merchant review summaries and supplementary risks | Detailed reviews supporting target-merchant assessment, not the primary directory search entry point; 2-3 similar but non-equivalent positive/negative reviews interfere near key risks | N/A |

## Data Source

Synthetic data, for offline benchmark use only; does not contain real personal sensitive information.
