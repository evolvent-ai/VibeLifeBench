# `notion/pharmacist_western_registration_shift_prep`

## translated business textdescription

thistranslated business texttask `exam_preparation/pharmacist_western_registration_shift_prep`（licensed pharmacistWestern medicineregistrationtranslated business text、legitimate coursetranslated business textandtranslated business textexam preparation）translated business text task-local `notion` environment。translated business textstoresscenario startavailabletranslated business textofflinesynthetictranslated business textstatus，environmenttranslated business textis `pharmacist_western_registration_shift_prep`。scenariowindowis `2026-08-01` translated business text `2026-10-11`，timezoneis `Asia/Shanghai`。

## English Summary

This is the task-local `notion` environment for `exam_preparation/pharmacist_western_registration_shift_prep` (Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation). It contains the offline synthetic business state available at scenario start. The environment name is `pharmacist_western_registration_shift_prep`, the scenario window is `2026-08-01` through `2026-10-11`, and the timezone is `Asia/Shanghai`.

## translated business texttask / Associated Task

- **Task / task:** `exam_preparation/pharmacist_western_registration_shift_prep`
- **translated business text / Chinese title:** licensed pharmacistWestern medicineregistrationtranslated business text、legitimate coursetranslated business textandtranslated business textexam preparation
- **English title / translated business text:** Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation
- **Service / service:** `notion`
- **Environment / environmenttranslated business text:** `pharmacist_western_registration_shift_prep`
- **Scenario window / scenariowindow:** `2026-08-01` → `2026-10-11`
- **Timezone / timezone:** `Asia/Shanghai`

## scenariotranslated business text / Scenario Role

storestranslated business text、datatranslated business text、translated business textwithandtranslated business textrecord。

Stores pages, databases, blocks, and durable structured records.

## initialdata / Seed Contents

initialfileis `init.sql`。translated business textservice SQLite schema and `init.sql` translated business textload；translated business text，withtranslated business textinitial stateboundary。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| translated business text / Table | initialtranslated business text / Initial Rows |
|---|---:|
| `blocks` | 216 |
| `comments` | 0 |
| `counters` | 4 |
| `database_rows` | 0 |
| `databases` | 0 |
| `pages` | 5 |
| `users` | 1 |
| `workspaces` | 1 |

## translated business text / Key Entities

withtranslated business textinitialtranslated business textandtranslated business textfield；translated business textordinaryscenarioentities，does not implypreset outcome。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| translated business text / Table | initialtranslated business text / Initial Rows | translated business textfield / Primary Key |
|---|---:|---|
| `blocks` | 216 | `block_id` |
| `pages` | 5 | `page_id` |
| `counters` | 4 | `key` |
| `users` | 1 | `user_id` |
| `workspaces` | 1 | `workspace_id` |

## initial stateanddynamic changes / Initial State and Mutations

`init.*` translated business textdescriptiontranslated business textunitstranslated business textinitial state。later state changestranslated business text `event.yaml` translated business text Stage andtranslated business text，translated business textisalreadytranslated business textattranslated business textinitial seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` notstatementtranslated business textrecordedtranslated business textservicetranslated business text；during runtimetranslated business text Agent tool callstranslated business textstatustranslated business textpersisted。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## filedescription / Files

| File / file | Purpose / purpose | Size / translated business text |
|---|---|---:|
| `init.sql` | SQLite initial seed / initial SQLite seed | 70034 bytes |

## loaddescription / Loading

translated business textwill `notion` translated business textenvironment `pharmacist_western_registration_shift_prep`，translated business texttaskdirectorytranslated business text `envs/notion/pharmacist_western_registration_shift_prep/` readdata。thistranslated business textdatatranslated business textservicetranslated business textnowtranslated business text `SCHEMA_SQL` translated business text，andload `init.sql`；SQLite `integrity_check` is `ok`，translated business textis 0 translated business text。translated business textdirectorytranslated business text `init.json` or JSONL file，translated business textservicetranslated business textdataloadtranslated business textretainandreadthistranslated business textfile。translated business text task-only translated business textcontains noservicetranslated business textnowortranslated business text。

A compatible runtime should bind `notion` to environment `pharmacist_western_registration_shift_prep` and read `envs/notion/pharmacist_western_registration_shift_prep/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## dataandprivacystatement / Data and Privacy

thisenvironmenttranslated business textpeopletranslated business text、translated business text、translated business text、translated business text、translated business text、location、price、policytranslated business textrecordtranslated business textisofflinesyntheticdata。filecontains nogenuineitemspeopleprivacy，translated business textrequires internet access。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
