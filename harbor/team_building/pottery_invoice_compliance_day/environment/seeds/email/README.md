# `email/pottery_invoice_compliance_day`

## Chinese Explanation

This is the task-local `email` environment used by the task `team_building/pottery_invoice_compliance_day` (indoor pottery team-building preparation). It stores the offline synthetic business state available at the start of the scenario. The environment name is `pottery_invoice_compliance_day`. The scenario window is `2026-07-01` to `2026-07-30`, and the time zone is `Asia/Shanghai`.

## English Summary

This is the task-local `email` environment for `team_building/pottery_invoice_compliance_day` (Indoor Pottery Team-Building Planning). It contains the offline synthetic business state available at scenario start. The environment name is `pottery_invoice_compliance_day`, the scenario window is `2026-07-01` through `2026-07-30`, and the timezone is `Asia/Shanghai`.

## Related Task / Associated Task

- **Task / task:** `team_building/pottery_invoice_compliance_day`
- **Chinese title / Chinese title:** Indoor Pottery Team-Building Preparation
- **English title / English title:** Indoor Pottery Team-Building Planning
- **Service / service:** `email`
- **Environment / environment name:** `pottery_invoice_compliance_day`
- **Scenario window / scene window:** `2026-07-01` → `2026-07-30`
- **Timezone / time zone:** `Asia/Shanghai`

## Scenario Role / Scenario Role

Store email folders, messages, conversations, attachments, and draft statuses.

Stores mail folders, messages, threads, attachments, and drafts.

## Seed Contents / Seed Contents

The initial file is `init.sql`. The row counts in the table below come from a fresh in-memory load of the corresponding service's SQLite schema and `init.sql`; empty tables are included to clearly define the initial-state boundary.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| Business Table / Table | Initial Row Count / Initial Rows |
|---|---:|
| `_counters` | 2 |
| `account_config` | 1 |
| `attachments` | 0 |
| `drafts` | 0 |
| `folders` | 3 |
| `messages` | 240 |
| `sent_log` | 0 |

## Key Entities / Key Entities

Listed below are the major business tables with relatively large row counts in the initial snapshot and their primary-key fields; they are ordinary-scenario entities and do not represent predetermined conclusions.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| Business Table / Table | Initial Row Count / Initial Rows | Primary Key Field / Primary Key |
|---|---:|---|
| `messages` | 240 | `id` |
| `folders` | 3 | `id` |
| `account_config` | 1 | `id` |

## Initial State and Mutations / Initial State and Mutations

`init.*` describes only the initial state before applying the event timeline. Subsequent state changes must be applied in the Stage and time order of `event.yaml` and cannot be treated as already existing in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

There are 10 events in `event.yaml` that will update this service / 10 events in `event.yaml` update this service:

| Stage / Stage | Time / Time | Kind / Kind | Update method / Update method |
|---:|---|---|---|
| 1 | `2026-07-02T09:50:00+08:00` | `mutation` | SQL file `mut_s01_hr_approval.sql` |
| 3 | `2026-07-04T10:45:00+08:00` | `mutation` | SQL file `mut_s03_admin_requirements.sql` |
| 6 | `2026-07-07T09:45:00+08:00` | `mutation` | SQL file `mut_s06_finance_policy.sql` |
| 7 | `2026-07-08T16:00:00+08:00` | `mutation` | SQL file `mut_s07_approver_criteria.sql` |
| 11 | `2026-07-12T08:00:00+08:00` | `mutation` | SQL file `mut_glaze_composition.sql` |
| 15 | `2026-07-16T08:45:00+08:00` | `mutation` | SQL file `mut_s15_private_payment_request.sql` |
| 16 | `2026-07-17T13:50:00+08:00` | `mutation` | SQL file `mut_s16_approval_decision.sql` |
| 19 | `2026-07-20T18:20:00+08:00` | `mutation` | SQL file `mut_s19_onsite_handoff.sql` |
| 21 | `2026-07-22T10:50:00+08:00` | `mutation` | SQL file `mut_s21_followup_request.sql` |
| 23 | `2026-07-23T13:50:00+08:00` | `mutation` | SQL file `mut_s23_invoice_reconciliation.sql` |

## File Description / Files

| File / File | Purpose / Purpose | Size / Size |
|---|---|---:|
| `init.sql` | SQLite initial seed / initial SQLite seed | 161208 bytes |
| `mut_glaze_composition.sql` | task-local environment data file / task-local environment data file | 618 bytes |
| `mut_s01_hr_approval.sql` | task-local environment data file / task-local environment data file | 633 bytes |
| `mut_s03_admin_requirements.sql` | task-local environment data file / task-local environment data file | 641 bytes |
| `mut_s06_finance_policy.sql` | task-local environment data file / task-local environment data file | 678 bytes |
| `mut_s07_approver_criteria.sql` | task-local environment data file / task-local environment data file | 629 bytes |
| `mut_s15_private_payment_request.sql` | task-local environment data file / task-local environment data file | 609 bytes |
| `mut_s16_approval_decision.sql` | task-local environment data file / task-local environment data file | 629 bytes |
| `mut_s19_onsite_handoff.sql` | task-local environment data file / task-local environment data file | 651 bytes |
| `mut_s21_followup_request.sql` | task-local environment data file / task-local environment data file | 629 bytes |
| `mut_s23_invoice_reconciliation.sql` | task-local environment data file / task-local environment data file | 680 bytes |

## Loading Instructions / Loading

The compatible runtime should bind `email` to the environment `pottery_invoice_compliance_day` and read data from `envs/email/pottery_invoice_compliance_day/` within the task directory. This data audit used the `SCHEMA_SQL` provided by the external service implementation to create the tables and loaded `init.sql`; SQLite `integrity_check` was `ok`, and the foreign-key check returned 0 rows. If the directory contains `init.json` or JSONL files, the runtime should also retain and read these structured files in accordance with the corresponding service's data-loading conventions. This task-only release package does not include the service implementation or execution framework.

A compatible runtime should bind `email` to environment `pottery_invoice_compliance_day` and read `envs/email/pottery_invoice_compliance_day/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## Data and Privacy Statement / Data and Privacy

The people, organizations, accounts, orders, messages, locations, prices, policy summaries, and business records in this environment are all offline synthetic data. The files contain no real personal privacy and do not require access to the internet.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
