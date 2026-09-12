# `notification_hub/pharmacist_western_registration_shift_prep`

## translated business textdescription

thistranslated business texttask `exam_preparation/pharmacist_western_registration_shift_prep`（licensed pharmacistWestern medicineregistrationtranslated business text、legitimate coursetranslated business textandtranslated business textexam preparation）translated business text task-local `notification_hub` environment。translated business textstoresscenario startavailabletranslated business textofflinesynthetictranslated business textstatus，environmenttranslated business textis `pharmacist_western_registration_shift_prep`。scenariowindowis `2026-08-01` translated business text `2026-10-11`，timezoneis `Asia/Shanghai`。

## English Summary

This is the task-local `notification_hub` environment for `exam_preparation/pharmacist_western_registration_shift_prep` (Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation). It contains the offline synthetic business state available at scenario start. The environment name is `pharmacist_western_registration_shift_prep`, the scenario window is `2026-08-01` through `2026-10-11`, and the timezone is `Asia/Shanghai`.

## translated business texttask / Associated Task

- **Task / task:** `exam_preparation/pharmacist_western_registration_shift_prep`
- **translated business text / Chinese title:** licensed pharmacistWestern medicineregistrationtranslated business text、legitimate coursetranslated business textandtranslated business textexam preparation
- **English title / translated business text:** Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation
- **Service / service:** `notification_hub`
- **Environment / environmenttranslated business text:** `pharmacist_western_registration_shift_prep`
- **Scenario window / scenariowindow:** `2026-08-01` → `2026-10-11`
- **Timezone / timezone:** `Asia/Shanghai`

## scenariotranslated business text / Scenario Role

storesnotice、translated business text、official accountandtranslated business textstatus。

Stores notifications, subscriptions, official accounts, and delivery state.

## initialdata / Seed Contents

initialfileis `init.sql`。translated business textservice SQLite schema and `init.sql` translated business textload；translated business text，withtranslated business textinitial stateboundary。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| translated business text / Table | initialtranslated business text / Initial Rows |
|---|---:|
| `_counters` | 3 |
| `notifications` | 1 |
| `official_account_posts` | 220 |
| `official_account_subscriptions` | 2 |
| `official_accounts` | 3 |
| `price_alerts` | 0 |
| `subscriptions` | 2 |

## translated business text / Key Entities

withtranslated business textinitialtranslated business textandtranslated business textfield；translated business textordinaryscenarioentities，does not implypreset outcome。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| translated business text / Table | initialtranslated business text / Initial Rows | translated business textfield / Primary Key |
|---|---:|---|
| `official_account_posts` | 220 | `post_id` |
| `official_accounts` | 3 | `account_id` |
| `official_account_subscriptions` | 2 | `user_id`, `account_id` |
| `subscriptions` | 2 | `subscription_id` |
| `notifications` | 1 | `notification_id` |

## initial stateanddynamic changes / Initial State and Mutations

`init.*` translated business textdescriptiontranslated business textunitstranslated business textinitial state。later state changestranslated business text `event.yaml` translated business text Stage andtranslated business text，translated business textisalreadytranslated business textattranslated business textinitial seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` translated business texthas 10 itemstranslated business textunitstranslated business textservice / 10 events in `event.yaml` update this service:

| Stage | Time / translated business text | Kind / translated business text | Update method / translated business text |
|---:|---|---|---|
| 1 | `2026-08-03T08:59:00+08:00` | `mutation` | SQL file `stage_1_registration_notice.sql` |
| 6 | `2026-08-15T08:00:00+08:00` | `mutation` | SQL file `stage_6_schema_org_code.sql` |
| 10 | `2026-08-24T10:20:00+08:00` | `mutation` | SQL file `stage_10_law_update_post.sql` |
| 13 | `2026-08-30T20:51:00+08:00` | `mutation` | SQL file `stage_13_submission_pending.sql` |
| 15 | `2026-09-04T09:00:00+08:00` | `mutation` | SQL file `stage_15_review_reject.sql` |
| 16 | `2026-09-04T21:26:00+08:00` | `mutation` | SQL file `stage_16_resubmitted.sql` |
| 20 | `2026-09-18T09:00:00+08:00` | `mutation` | SQL file `stage_20_payment_open.sql` |
| 21 | `2026-09-18T21:11:00+08:00` | `mutation` | SQL file `stage_21_payment_complete.sql` |
| 26 | `2026-10-06T08:00:00+08:00` | `mutation` | SQL file `stage_26_ticket_open.sql`; SQL file `stage_26_ticket_window_post.sql` |
| 27 | `2026-10-08T09:00:00+08:00` | `mutation` | SQL file `stage_27_ticket_ready.sql` |

## filedescription / Files

| File / file | Purpose / purpose | Size / translated business text |
|---|---|---:|
| `init.sql` | SQLite initial seed / initial SQLite seed | 76147 bytes |

## loaddescription / Loading

translated business textwill `notification_hub` translated business textenvironment `pharmacist_western_registration_shift_prep`，translated business texttaskdirectorytranslated business text `envs/notification_hub/pharmacist_western_registration_shift_prep/` readdata。thistranslated business textdatatranslated business textservicetranslated business textnowtranslated business text `SCHEMA_SQL` translated business text，andload `init.sql`；SQLite `integrity_check` is `ok`，translated business textis 0 translated business text。translated business textdirectorytranslated business text `init.json` or JSONL file，translated business textservicetranslated business textdataloadtranslated business textretainandreadthistranslated business textfile。translated business text task-only translated business textcontains noservicetranslated business textnowortranslated business text。

A compatible runtime should bind `notification_hub` to environment `pharmacist_western_registration_shift_prep` and read `envs/notification_hub/pharmacist_western_registration_shift_prep/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## dataandprivacystatement / Data and Privacy

thisenvironmenttranslated business textpeopletranslated business text、translated business text、translated business text、translated business text、translated business text、location、price、policytranslated business textrecordtranslated business textisofflinesyntheticdata。filecontains nogenuineitemspeopleprivacy，translated business textrequires internet access。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
