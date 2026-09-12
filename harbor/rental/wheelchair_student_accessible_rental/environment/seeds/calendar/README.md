# `calendar/wheelchair_student_accessible_rental`

## Chinese Description

This is the task-local `calendar` environment used by the task `rental/wheelchair_student_accessible_rental` (accessible campus housing for a wheelchair student). It stores the offline synthetic business state available at the start of the scenario. The environment name is `wheelchair_student_accessible_rental`. The scenario window is `2026-07-14` to `2026-08-24`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `calendar` environment for `rental/wheelchair_student_accessible_rental` (Accessible Campus Housing for a Wheelchair-Using Student). It contains the offline synthetic business state available at scenario start. The environment name is `wheelchair_student_accessible_rental`, the scenario window is `2026-07-14` through `2026-08-24`, and the timezone is `Asia/Shanghai`.

## Associated Task

- **Task / Task:** `rental/wheelchair_student_accessible_rental`
- **Chinese title:** Accessible Campus Housing for a Student Who Uses a Wheelchair
- **English title / English Title:** Accessible Campus Housing for a Wheelchair-Using Student
- **Service / Service:** `calendar`
- **Environment / Environment Name:** `wheelchair_student_accessible_rental`
- **Scenario window / Scenario Window:** `2026-07-14` → `2026-08-24`
- **Timezone / Time zone:** `Asia/Shanghai`

## Scenario Role

Save schedules, time windows, participants, reminders, and conflict information.

Stores events, time windows, attendees, reminders, and scheduling conflicts.

## Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service’s SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business table | Initial rows |
|---|---:|
| `_counters` | 1 |
| `attendees` | 54 |
| `calendars` | 1 |
| `events` | 225 |
| `reminders` | 132 |

## Key Entities

Listed below are the major business tables with relatively large row counts in the initial snapshot, along with their primary key fields; they are ordinary scenario entities and do not represent predetermined conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business table | Initial rows | Primary key |
|---|---:|---|
| `events` | 225 | `event_id` |
| `reminders` | 132 | `id` |
| `attendees` | 54 | `id` |
| `calendars` | 1 | `calendar_id` |

## Initial State and Mutations

`init.*` describes only the initial state before the event timeline is applied. Subsequent state changes must be applied in the Stage and time order specified by `event.yaml` and must not be treated as already present in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` contains 1 event that updates this service / 1 events in `event.yaml` update this service:

| Stage | Time | Kind | Update method |
|---:|---|---|---|
| 10 | `2026-07-24T08:50:00+08:00` | `mutation` | SQL file `stage10_calendar_conflict.sql` |

## Files

| File | Purpose | Size |
|---|---|---:|
| `init.sql` | SQLite initial seed | 148664 bytes |

## Loading

The compatible runtime should bind `calendar` to the environment `wheelchair_student_accessible_rental` and read data from `envs/calendar/wheelchair_student_accessible_rental/` within the task directory. This data audit uses the external service implementation's `SCHEMA_SQL` to create the tables and loads `init.sql`; SQLite `integrity_check` is `ok`, and the foreign key check returned 0 violations. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files according to the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `calendar` to environment `wheelchair_student_accessible_rental` and read `envs/calendar/wheelchair_student_accessible_rental/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy information and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
