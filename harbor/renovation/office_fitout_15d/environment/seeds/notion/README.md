# `notion/office_fitout_15d`

## Chinese description

CN-termistask `renovation/office_fitout_15d`（commercial office Fit-out projectCN-text）CN-textof task-local `notion` environment。CN-textscenarioCN-textavailableofCN-textstatus，environment namefor `office_fitout_15d`。scenariowindowfor `2026-07-01` to `2026-09-01`，CN-textfor `Asia/Shanghai`。

## English Summary

This is the task-local `notion` environment for `renovation/office_fitout_15d` (Commercial Office Fit-Out Project Management). It contains the offline synthetic business state available at scenario start. The environment name is `office_fitout_15d`, the scenario window is `2026-07-01` through `2026-09-01`, and the timezone is `Asia/Shanghai`.

## associated task / Associated Task

- **Task / task:** `renovation/office_fitout_15d`
- **midCN-termtitle / Chinese title:** commercial office Fit-out projectCN-text
- **English title / English title:** Commercial Office Fit-Out Project Management
- **Service / service:** `notion`
- **Environment / environment name:** `office_fitout_15d`
- **Scenario window / scenariowindow:** `2026-07-01` → `2026-09-01`
- **Timezone / CN-text:** `Asia/Shanghai`

## scenarioCN-text / Scenario Role

CN-text、dataCN-term、CN-textandCN-textofCN-textrecord。

Stores pages, databases, blocks, and durable structured records.

## CN-textdata / Seed Contents

CN-textdocumentfor `init.json`、`init.sql`。downCN-termoflineCN-textservice SQLite schema with `init.sql` ofCN-textwithinCN-text；CN-text，CN-textstatusCN-text。

Initial files: `init.json`, `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| CN-text / Table | CN-textlineCN-term / Initial Rows |
|---|---:|
| `blocks` | 0 |
| `comments` | 0 |
| `counters` | 0 |
| `database_rows` | 1060 |
| `databases` | 8 |
| `pages` | 0 |
| `users` | 2 |
| `workspaces` | 1 |

## CN-text / Key Entities

CN-termdownCN-textfastCN-termmidlineCN-textofCN-textandCN-text；CN-textisordinaryscenarioCN-text，notCN-text。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| CN-text / Table | CN-textlineCN-term / Initial Rows | CN-text / Primary Key |
|---|---:|---|
| `database_rows` | 1060 | `row_id` |
| `databases` | 8 | `database_id` |
| `users` | 2 | `user_id` |
| `workspaces` | 1 | `workspace_id` |

## CN-textstatuswithCN-text / Initial State and Mutations

`init.*` CN-termdescriptioneventtimeCN-textbeforeofCN-textstatus。afterCN-termstatusCN-textmustper `event.yaml` of Stage withtimeCN-text，notCN-textforalreadyCN-termatCN-text seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` CN-textserviceofCN-textupdated；CN-termlineCN-text Agent CN-textofstatusCN-textlineCN-text。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## documentdescription / Files

| File / document | Purpose / CN-text | Size / CN-text |
|---|---|---:|
| `contractor_review_rows.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 585055 bytes |
| `contractor_reviews.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 370038 bytes |
| `databases.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 6190 bytes |
| `init.json` | CN-text seed / structured initial seed | 3756514 bytes |
| `init.sql` | SQLite CN-text seed / initial SQLite seed | 1918962 bytes |
| `inspection_standards.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 140826 bytes |
| `issue_tracker.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 8679 bytes |
| `material_catalog.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 693978 bytes |
| `material_price_points.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 138181 bytes |
| `project_status.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 10142 bytes |
| `property_rules.jsonl` | task-local CN-textrecordCN-term / task-local structured record set | 186138 bytes |

## CN-textdescription / Loading

CN-textlineCN-textwill `notion` CN-textenvironment `office_fitout_15d`，fromtaskCN-textwithinof `envs/notion/office_fitout_15d/` CN-textdata。CN-textdataCN-textoutsideCN-termserviceCN-textprovideof `SCHEMA_SQL` CN-text，andCN-text `init.sql`；SQLite `integrity_check` for `ok`，outsideCN-textfor 0 CN-term。CN-textincluding `init.json` or JSONL document，CN-termlineCN-textperCN-textserviceofdataCN-textretainandCN-textdocument。CN-term task-only publishCN-termnotCN-termincludingserviceCN-textorCN-termlineCN-text。

A compatible runtime should bind `notion` to environment `office_fitout_15d` and read `envs/notion/office_fitout_15d/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## datawithCN-text / Data and Privacy

CN-termenvironmentmidofpeopleCN-term、CN-text、CN-termNo.、CN-text、message、location、price、CN-textsummaryandCN-textrecordCN-termforCN-textdata。documentnotCN-termincludingCN-textpeopleCN-text，CN-termnotrequiredCN-text。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
