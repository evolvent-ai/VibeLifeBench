# `calendar/zhao_meng_litigation`

## Chinese Explanation

This is the task-local `calendar` environment used by task `litigation/food_safety_dispute_33d` (food-safety online-shopping refund-plus-tenfold-compensation dispute litigation). It stores the offline synthetic business state available at the start of the scenario. The environment is named `zhao_meng_litigation`. The scenario window is `2026-05-20` to `2026-06-22`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `calendar` environment for `litigation/food_safety_dispute_33d` (Food Safety E-commerce Dispute Litigation — 33 Days). It contains the offline synthetic business state available at scenario start. The environment name is `zhao_meng_litigation`, the scenario window is `2026-05-20` through `2026-06-22`, and the timezone is `Asia/Shanghai`.

## Related Task / Associated Task

- Task: `litigation/food_safety_dispute_33d`
- **Chinese title / Chinese title:** Food Safety Online Shopping Refund Plus Tenfold Compensation Dispute Litigation
- **English title / English title:** Food Safety E-commerce Dispute Litigation — 33 Days
- Service: `calendar`
- Environment: `zhao_meng_litigation`
- Scenario window: `2026-05-20` → `2026-06-22`
- Timezone: `Asia/Shanghai`

## Scenario Role

Save schedules, time windows, participants, reminders, and conflict information.

Stores events, time windows, attendees, reminders, and scheduling conflicts.

## Initial Data / Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service's SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business Table / Table | Initial Rows / Initial Rows |
|---|---:|
| `_counters` | 3 |
| `attendees` | 0 |
| `calendars` | 1 |
| `events` | 205 |
| `reminders` | 0 |

## Key Entities

Listed below are the main business tables with relatively large row counts in the initial snapshot, along with their primary key fields; they are ordinary-scenario entities and do not represent preset conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business Table / Table | Initial Rows / Initial Rows | Primary Key / Primary Key |
|---|---:|---|
| `events` | 205 | `event_id` |
| `calendars` | 1 | `calendar_id` |

## Initial State and Mutations

`init.*` describes only the initial state before the event timeline is applied. Subsequent state changes must be applied according to the Stage and chronological order in `event.yaml` and cannot be treated as already present in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` contains 4 events that update this service / 4 events in `event.yaml` update this service:

| Stage | Time | Kind | Update method |
|---:|---|---|---|
| 8 | `2026-06-01T09:30:00+08:00` | `mutation` | SQL file `mutation_s8_case_deadlines.sql` |
| 12 | `2026-06-08T09:40:00+08:00` | `mutation` | SQL file `mutation_s12_hearing_event.sql` |
| 13 | `2026-06-10T09:00:00+08:00` | `mutation` | SQL file `mutation_s13_inspection_replan.sql` |
| 18 | `2026-06-18T13:50:00+08:00` | `mutation` | SQL file `mutation_s18_appeal_deadlines.sql` |

## File Description / Files

| File | Purpose | Size |
|---|---|---:|
| `database.sqlite` | task-local environment data file | 0 bytes |
| `init.sql` | SQLite initial seed | 105471 bytes |
| `mutation_s12_hearing_event.sql` | Staged update referenced by the event timeline | 942 bytes |
| `mutation_s13_inspection_replan.sql` | staged update referenced by the event timeline | 872 bytes |
| `mutation_s18_appeal_deadlines.sql` | staged update referenced by the event timeline | 882 bytes |
| `mutation_s8_case_deadlines.sql` | Staged update referenced by the event timeline | 1301 bytes |

## Loading Instructions / Loading

A compatible runtime should bind `calendar` to the `zhao_meng_litigation` environment and read data from `envs/calendar/zhao_meng_litigation/` within the task directory. This data audit used the `SCHEMA_SQL` provided by the external service implementation to create the tables and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 rows. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files in accordance with the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `calendar` to environment `zhao_meng_litigation` and read `envs/calendar/zhao_meng_litigation/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy Statement / Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
