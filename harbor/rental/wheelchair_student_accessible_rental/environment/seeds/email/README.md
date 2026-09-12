# `email/wheelchair_student_accessible_rental`

## Chinese Description

This is the task-local `email` environment used by the task `rental/wheelchair_student_accessible_rental` (accessible campus housing for a wheelchair student). It stores the offline synthetic business state available at the start of the scenario. The environment name is `wheelchair_student_accessible_rental`. The scenario window is `2026-07-14` to `2026-08-24`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `email` environment for `rental/wheelchair_student_accessible_rental` (Accessible Campus Housing for a Wheelchair-Using Student). It contains the offline synthetic business state available at scenario start. The environment name is `wheelchair_student_accessible_rental`, the scenario window is `2026-07-14` through `2026-08-24`, and the timezone is `Asia/Shanghai`.

## Associated Task

- **Task / Task:** `rental/wheelchair_student_accessible_rental`
- **Chinese title:** Accessible Campus Housing for a Student Who Uses a Wheelchair
- **English title / English Title:** Accessible Campus Housing for a Wheelchair-Using Student
- **Service / Service:** `email`
- **Environment / Environment Name:** `wheelchair_student_accessible_rental`
- **Scenario window / Scenario Window:** `2026-07-14` → `2026-08-24`
- **Timezone / Time zone:** `Asia/Shanghai`

## Scenario Role

Save email folders, messages, conversations, attachments, and draft statuses.

Stores mail folders, messages, threads, attachments, and drafts.

## Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service’s SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business table | Initial rows |
|---|---:|
| `_counters` | 2 |
| `account_config` | 1 |
| `attachments` | 0 |
| `drafts` | 0 |
| `folders` | 5 |
| `messages` | 178 |
| `sent_log` | 0 |

## Key Entities

Listed below are the major business tables with relatively large row counts in the initial snapshot, along with their primary key fields; they are ordinary scenario entities and do not represent predetermined conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business table | Initial rows | Primary key |
|---|---:|---|
| `messages` | 178 | `id` |
| `folders` | 5 | `id` |
| `account_config` | 1 | `id` |

## Initial State and Mutations

`init.*` describes only the initial state before the event timeline is applied. Subsequent state changes must be applied in the Stage and time order specified by `event.yaml` and must not be treated as already present in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` contains 5 events that update this service / 5 events in `event.yaml` update this service:

| Stage | Time | Kind | Update method |
|---:|---|---|---|
| 7 | `2026-07-21T08:50:00+08:00` | `mutation` | SQL file `stage07_email_replies.sql` |
| 13 | `2026-07-27T08:50:00+08:00` | `mutation` | SQL file `stage13_contract_addendum.sql` |
| 15 | `2026-07-29T08:50:00+08:00` | `mutation` | SQL file `stage15_payment_pressure.sql` |
| 16 | `2026-07-30T08:50:00+08:00` | `mutation` | SQL file `stage16_privacy_request.sql` |
| 21 | `2026-08-08T08:50:00+08:00` | `mutation` | SQL file `stage21_final_clarification.sql` |

## Files

| File | Purpose | Size |
|---|---|---:|
| `init.sql` | SQLite initial seed | 131468 bytes |

## Loading

The compatible runtime should bind `email` to the environment `wheelchair_student_accessible_rental` and read data from `envs/email/wheelchair_student_accessible_rental/` within the task directory. This data audit created the tables using the `SCHEMA_SQL` provided by the external service implementation and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 violations. If the directory contains an `init.json` or JSONL file, the runtime should also retain and read these structured files according to the corresponding service's data-loading conventions. This task-only distribution package does not include the service implementation or execution framework.

A compatible runtime should bind `email` to environment `wheelchair_student_accessible_rental` and read `envs/email/wheelchair_student_accessible_rental/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy information and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
