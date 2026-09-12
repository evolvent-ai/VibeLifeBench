# `email/zhao_meng_litigation`

## Chinese Explanation

This is the task-local `email` environment used by task `litigation/food_safety_dispute_33d` (food-safety online-shopping refund-plus-tenfold-compensation dispute litigation). It stores the offline synthetic business state available at the start of the scenario. The environment is named `zhao_meng_litigation`. The scenario window is `2026-05-20` to `2026-06-22`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `email` environment for `litigation/food_safety_dispute_33d` (Food Safety E-commerce Dispute Litigation — 33 Days). It contains the offline synthetic business state available at scenario start. The environment name is `zhao_meng_litigation`, the scenario window is `2026-05-20` through `2026-06-22`, and the timezone is `Asia/Shanghai`.

## Related Task / Associated Task

- Task: `litigation/food_safety_dispute_33d`
- **Chinese title / Chinese title:** Food Safety Online Shopping Refund Plus Tenfold Compensation Dispute Litigation
- **English title / English title:** Food Safety E-commerce Dispute Litigation — 33 Days
- Service: `email`
- Environment: `zhao_meng_litigation`
- Scenario window: `2026-05-20` → `2026-06-22`
- Timezone: `Asia/Shanghai`

## Scenario Role

Save email folders, messages, conversations, attachments, and draft statuses.

Stores mail folders, messages, threads, attachments, and drafts.

## Initial Data / Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service's SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business Table / Table | Initial Rows / Initial Rows |
|---|---:|
| `_counters` | 1 |
| `account_config` | 1 |
| `attachments` | 0 |
| `drafts` | 0 |
| `folders` | 7 |
| `messages` | 210 |
| `sent_log` | 0 |

## Key Entities

Listed below are the main business tables with relatively large row counts in the initial snapshot, along with their primary key fields; they are ordinary-scenario entities and do not represent preset conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business Table / Table | Initial Rows / Initial Rows | Primary Key / Primary Key |
|---|---:|---|
| `messages` | 210 | `id` |
| `folders` | 7 | `id` |
| `account_config` | 1 | `id` |

## Initial State and Mutations

`init.*` describes only the initial state before the event timeline is applied. Subsequent state changes must be applied according to the Stage and chronological order in `event.yaml` and cannot be treated as already present in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` contains 7 events that update this service / 7 events in `event.yaml` update this service:

| Stage | Time | Kind | Update method |
|---:|---|---|---|
| 7 | `2026-05-30T09:00:00+08:00` | `mutation` | SQL file `mutation_s7_seller_vanish.sql` |
| 8 | `2026-06-01T09:30:00+08:00` | `mutation` | SQL file `mutation_s8_case_accepted.sql` |
| 10 | `2026-06-04T09:00:00+08:00` | `mutation` | SQL file `mutation_s10_seller_defense.sql` |
| 12 | `2026-06-08T09:40:00+08:00` | `mutation` | SQL file `mutation_s12_hearing_notice.sql` |
| 13 | `2026-06-10T09:00:00+08:00` | `mutation` | SQL file `mutation_s13_inspect_conflict.sql` |
| 16 | `2026-06-16T09:50:00+08:00` | `mutation` | SQL file `mutation_s16_judgment_delivery.sql` |
| 18 | `2026-06-18T13:50:00+08:00` | `mutation` | SQL file `mutation_s18_appeal_delivery.sql` |

## File Description / Files

| File | Purpose | Size |
|---|---|---:|
| `init.sql` | SQLite initial seed | 107377 bytes |
| `mutation_s10_seller_defense.sql` | Staged update referenced by the event timeline | 1225 bytes |
| `mutation_s12_hearing_notice.sql` | staged update referenced by the event timeline | 1221 bytes |
| `mutation_s13_inspect_conflict.sql` | staged update referenced by the event timeline | 1129 bytes |
| `mutation_s16_judgment_delivery.sql` | staged update referenced by the event timeline | 1237 bytes |
| `mutation_s18_appeal_delivery.sql` | staged update referenced by the event timeline | 1211 bytes |
| `mutation_s7_seller_vanish.sql` | staged update referenced by the event timeline | 1130 bytes |
| `mutation_s8_case_accepted.sql` | staged update referenced by the event timeline | 1198 bytes |

## Loading Instructions / Loading

A compatible runtime should bind `email` to the `zhao_meng_litigation` environment and read data from `envs/email/zhao_meng_litigation/` within the task directory. This data audit used the `SCHEMA_SQL` provided by the external service implementation to create the tables and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 rows. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files in accordance with the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `email` to environment `zhao_meng_litigation` and read `envs/email/zhao_meng_litigation/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy Statement / Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
