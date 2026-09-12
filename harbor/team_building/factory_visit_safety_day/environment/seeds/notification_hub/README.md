# `notification_hub/factory_visit_safety_day`

## Chinese Description

This is the task-local `notification_hub` environment used by the task `team_building/factory_visit_safety_day` (Supply Chain Team Factory Visit Team-Building). It stores the offline synthetic business state available at the start of the scenario, and its environment name is `factory_visit_safety_day`. The scenario window is `2026-07-01` to `2026-07-25`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `notification_hub` environment for `team_building/factory_visit_safety_day` (Supply Chain Factory Visit Team Day). It contains the offline synthetic business state available at scenario start. The environment name is `factory_visit_safety_day`, the scenario window is `2026-07-01` through `2026-07-25`, and the timezone is `Asia/Shanghai`.

## Related Task / Associated Task

- **Task / Task:** `team_building/factory_visit_safety_day`
- **Chinese title / Chinese title:** Supply Chain Team Factory Visit Team-Building
- **English title / English title:** Supply Chain Factory Visit Team Day
- **Service / Service:** `notification_hub`
- **Environment / Environment name:** `factory_visit_safety_day`
- **Scenario window / Scenario window:** `2026-07-01` → `2026-07-25`
- **Timezone / Time zone:** `Asia/Shanghai`

## Scenario Role / Scenario Role

Save notifications, subscriptions, official accounts, and message delivery statuses.

Stores notifications, subscriptions, official accounts, and delivery state.

## Seed Contents / Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business Table / Table | Initial Rows / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `notifications` | 45 |
| `official_account_posts` | 12 |
| `official_account_subscriptions` | 6 |
| `official_accounts` | 6 |
| `price_alerts` | 3 |
| `subscriptions` | 7 |

## Key Entities / Key Entities

Listed below are the major business tables with relatively many rows in the initial snapshot, along with their primary-key fields; they are ordinary scenario entities and do not represent predetermined conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business Table / Table | Initial Rows / Initial Rows | Primary Key |
|---|---:|---|
| `notifications` | 45 | `notification_id` |
| `official_account_posts` | 12 | `post_id` |
| `subscriptions` | 7 | `subscription_id` |
| `official_account_subscriptions` | 6 | `user_id`, `account_id` |
| `official_accounts` | 6 | `account_id` |
| `price_alerts` | 3 | `alert_id` |

## Initial State and Mutations / Initial State and Mutations

`init.*` only describes the initial state before the event timeline is applied。Subsequent state changes must be applied according to the Stage and chronological order in `event.yaml`, and must not be regarded as already existing in the initial seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` has 4 events that update this service / 4 events in `event.yaml` update this service:

| Stage | Time / Time | Kind / Type | Update method / Update method |
|---:|---|---|---|
| 10 | `2026-07-11T08:10:00+08:00` | `mutation` | SQL file `mutation_s10_ppe_alert.sql` |
| 13 | `2026-07-14T08:10:00+08:00` | `mutation` | SQL file `mutation_s13_credential_alert.sql` |
| 20 | `2026-07-21T07:50:00+08:00` | `mutation` | SQL file `mutation_s20_onsite.sql` |
| 22 | `2026-07-22T08:20:00+08:00` | `mutation` | SQL file `mutation_s22_late_needs.sql` |

## File Description / Files

| File / File | Purpose / Purpose | Size / Size |
|---|---|---:|
| `init.sql` | SQLite initial seed / initial SQLite seed | 25231 bytes |
| `mutation_s10_ppe_alert.sql` | Staged update referenced by the event timeline / staged update referenced by the event timeline | 396 bytes |
| `mutation_s13_credential_alert.sql` | Staged update referenced by the event timeline / staged update referenced by the event timeline | 997 bytes |
| `mutation_s20_onsite.sql` | staged update referenced by the event timeline / staged update referenced by the event timeline | 1426 bytes |
| `mutation_s22_late_needs.sql` | staged update referenced by the event timeline / staged update referenced by the event timeline | 386 bytes |

## Loading / Loading

The compatible runtime should bind `notification_hub` to the environment `factory_visit_safety_day` and read data from `envs/notification_hub/factory_visit_safety_day/` within the task directory. This data audit used the `SCHEMA_SQL` provided by the external service implementation to create the tables and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 rows. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files according to the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `notification_hub` to environment `factory_visit_safety_day` and read `envs/notification_hub/factory_visit_safety_day/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy Statement / Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy information and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
