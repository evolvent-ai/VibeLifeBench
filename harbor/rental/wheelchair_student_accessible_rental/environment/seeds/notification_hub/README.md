# `notification_hub/wheelchair_student_accessible_rental`

## Chinese Description

This is the task-local `notification_hub` environment used by the task `rental/wheelchair_student_accessible_rental` (campus-accessible housing for wheelchair-using students). It stores the offline synthetic business state available at the start of the scenario, and its environment name is `wheelchair_student_accessible_rental`. The scenario window is `2026-07-14` to `2026-08-24`, in the `Asia/Shanghai` time zone.

## English Summary

This is the task-local `notification_hub` environment for `rental/wheelchair_student_accessible_rental` (Accessible Campus Housing for a Wheelchair-Using Student). It contains the offline synthetic business state available at scenario start. The environment name is `wheelchair_student_accessible_rental`, the scenario window is `2026-07-14` through `2026-08-24`, and the timezone is `Asia/Shanghai`.

## Associated Task

- **Task / Task:** `rental/wheelchair_student_accessible_rental`
- **Chinese title:** Accessible Campus Housing for a Student Who Uses a Wheelchair
- **English title / English Title:** Accessible Campus Housing for a Wheelchair-Using Student
- **Service / Service:** `notification_hub`
- **Environment / Environment Name:** `wheelchair_student_accessible_rental`
- **Scenario window / Scenario Window:** `2026-07-14` → `2026-08-24`
- **Timezone / Time zone:** `Asia/Shanghai`

## Scenario Role

Save notifications, subscriptions, official accounts, and message delivery statuses.

Stores notifications, subscriptions, official accounts, and delivery state.

## Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service’s SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business table | Initial rows |
|---|---:|
| `_counters` | 3 |
| `notifications` | 98 |
| `official_account_posts` | 3 |
| `official_account_subscriptions` | 3 |
| `official_accounts` | 3 |
| `price_alerts` | 0 |
| `subscriptions` | 2 |

## Key Entities

Listed below are the major business tables with relatively large row counts in the initial snapshot, along with their primary key fields; they are ordinary scenario entities and do not represent predetermined conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business table | Initial rows | Primary key |
|---|---:|---|
| `notifications` | 98 | `notification_id` |
| `official_account_posts` | 3 | `post_id` |
| `official_account_subscriptions` | 3 | `user_id`, `account_id` |
| `official_accounts` | 3 | `account_id` |
| `subscriptions` | 2 | `subscription_id` |

## Initial State and Mutations

`init.*` describes only the initial state before the event timeline is applied. Subsequent state changes must be applied in the Stage and time order specified by `event.yaml` and must not be treated as already present in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` contains 1 event that updates this service / 1 events in `event.yaml` update this service:

| Stage | Time | Kind | Update method |
|---:|---|---|---|
| 18 | `2026-08-01T08:50:00+08:00` | `mutation` | SQL file `stage18_notification_late_route.sql` |

## Files

| File | Purpose | Size |
|---|---|---:|
| `init.sql` | SQLite initial seed | 52108 bytes |

## Loading

The compatible runtime should bind `notification_hub` to the environment `wheelchair_student_accessible_rental` and read data from `envs/notification_hub/wheelchair_student_accessible_rental/` within the task directory. This data audit created the tables using the `SCHEMA_SQL` provided by the external service implementation and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 violations. If the directory contains an `init.json` or JSONL file, the runtime should also retain and read these structured files according to the corresponding service's data-loading conventions. This task-only distribution package does not include the service implementation or execution framework.

A compatible runtime should bind `notification_hub` to environment `wheelchair_student_accessible_rental` and read `envs/notification_hub/wheelchair_student_accessible_rental/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy information and do not require internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
