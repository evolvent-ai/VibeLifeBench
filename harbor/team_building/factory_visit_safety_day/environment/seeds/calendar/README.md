# `calendar/factory_visit_safety_day`

## Chinese Description

This is the task-local `calendar` environment used by the task `team_building/factory_visit_safety_day` (Supply Chain Team Factory Visit Team-Building). It stores the offline synthetic business state available at the start of the scenario, and its environment name is `factory_visit_safety_day`. The scenario window is `2026-07-01` to `2026-07-25`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `calendar` environment for `team_building/factory_visit_safety_day` (Supply Chain Factory Visit Team Day). It contains the offline synthetic business state available at scenario start. The environment name is `factory_visit_safety_day`, the scenario window is `2026-07-01` through `2026-07-25`, and the timezone is `Asia/Shanghai`.

## Related Task / Associated Task

- **Task / Task:** `team_building/factory_visit_safety_day`
- **Chinese title / Chinese title:** Supply Chain Team Factory Visit Team-Building
- **English title / English title:** Supply Chain Factory Visit Team Day
- **Service / Service:** `calendar`
- **Environment / Environment name:** `factory_visit_safety_day`
- **Scenario window / Scenario window:** `2026-07-01` → `2026-07-25`
- **Timezone / Time zone:** `Asia/Shanghai`

## Scenario Role / Scenario Role

Save schedules, time windows, participants, reminders, and conflict information.

Stores events, time windows, attendees, reminders, and scheduling conflicts.

## Seed Contents / Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business Table / Table | Initial Rows / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `attendees` | 0 |
| `calendars` | 1 |
| `events` | 36 |
| `reminders` | 0 |

## Key Entities / Key Entities

Listed below are the major business tables with relatively many rows in the initial snapshot, along with their primary-key fields; they are ordinary scenario entities and do not represent predetermined conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business Table / Table | Initial Rows / Initial Rows | Primary Key |
|---|---:|---|
| `events` | 36 | `event_id` |
| `calendars` | 1 | `calendar_id` |

## Initial State and Mutations / Initial State and Mutations

`init.*` only describes the initial state before the event timeline is applied。Subsequent state changes must be applied according to the Stage and chronological order in `event.yaml`, and must not be regarded as already existing in the initial seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` does not declare stage updates that directly write to this service; state changes produced by Agent tool calls during runtime are still persisted by the compatible runtime。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## File Description / Files

| File / File | Purpose / Purpose | Size / Size |
|---|---|---:|
| `init.sql` | SQLite initial seed / initial SQLite seed | 13699 bytes |

## Loading / Loading

The compatible runtime should bind `calendar` to the environment `factory_visit_safety_day` and read data from `envs/calendar/factory_visit_safety_day/` within the task directory. This data audit used the `SCHEMA_SQL` provided by the external service implementation to create the tables and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 rows. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files according to the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `calendar` to environment `factory_visit_safety_day` and read `envs/calendar/factory_visit_safety_day/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy Statement / Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy information and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
