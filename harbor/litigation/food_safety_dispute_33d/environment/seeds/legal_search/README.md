# `legal_search/food_safety_2026`

## Chinese Explanation

This is the task-local `legal_search` environment used by task `litigation/food_safety_dispute_33d` (food-safety online-shopping refund-plus-tenfold-compensation dispute litigation). It stores the offline synthetic business state available at the start of the scenario. The environment is named `food_safety_2026`. The scenario window is `2026-05-20` to `2026-06-22`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `legal_search` environment for `litigation/food_safety_dispute_33d` (Food Safety E-commerce Dispute Litigation — 33 Days). It contains the offline synthetic business state available at scenario start. The environment name is `food_safety_2026`, the scenario window is `2026-05-20` through `2026-06-22`, and the timezone is `Asia/Shanghai`.

## Related Task / Associated Task

- Task: `litigation/food_safety_dispute_33d`
- **Chinese title / Chinese title:** Food Safety Online Shopping Refund Plus Tenfold Compensation Dispute Litigation
- **English title / English title:** Food Safety E-commerce Dispute Litigation — 33 Days
- Service: `legal_search`
- Environment: `food_safety_2026`
- Scenario window: `2026-05-20` → `2026-06-22`
- Timezone: `Asia/Shanghai`

## Scenario Role

Save laws and regulations, policies, cases, search indexes, and saved-item records.

Stores statutes, policies, cases, search indexes, and saved legal records.

## Initial Data / Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service's SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business Table / Table | Initial Rows / Initial Rows |
|---|---:|
| `_counters` | 2 |
| `cases` | 210 |
| `citations` | 220 |
| `courts` | 6 |
| `saved_cases` | 2 |
| `statute_articles` | 12 |
| `statutes` | 4 |

## Key Entities

Listed below are the main business tables with relatively large row counts in the initial snapshot, along with their primary key fields; they are ordinary-scenario entities and do not represent preset conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business Table / Table | Initial Rows / Initial Rows | Primary Key / Primary Key |
|---|---:|---|
| `citations` | 220 | `citation_id` |
| `cases` | 210 | `case_id` |
| `statute_articles` | 12 | `article_id` |
| `courts` | 6 | `court_id` |
| `statutes` | 4 | `statute_id` |
| `saved_cases` | 2 | `saved_id` |

## Initial State and Mutations

`init.*` describes only the initial state before the event timeline is applied. Subsequent state changes must be applied according to the Stage and chronological order in `event.yaml` and cannot be treated as already present in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` does not declare any stage updates that directly write to this service; status changes produced by Agent tool calls during runtime are still persisted by the compatible runtime.

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## File Description / Files

| File | Purpose | Size |
|---|---|---:|
| `init.sql` | SQLite initial seed | 336843 bytes |

## Loading Instructions / Loading

A compatible runtime should bind `legal_search` to the `food_safety_2026` environment and read data from `envs/legal_search/food_safety_2026/` within the task directory. This data audit used the `SCHEMA_SQL` provided by the external service implementation to create the tables and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 rows. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files in accordance with the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `legal_search` to environment `food_safety_2026` and read `envs/legal_search/food_safety_2026/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy Statement / Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
