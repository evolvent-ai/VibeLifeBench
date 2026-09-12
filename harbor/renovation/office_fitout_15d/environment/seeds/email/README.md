# `email/office_fitout_15d`

## Chinese description

CN-termistask `renovation/office_fitout_15d`（commercial office Fit-out projectCN-text）CN-textof task-local `email` environment。CN-textscenarioCN-textavailableofCN-textstatus，environment namefor `office_fitout_15d`。scenariowindowfor `2026-07-01` to `2026-09-01`，CN-textfor `Asia/Shanghai`。

## English Summary

This is the task-local `email` environment for `renovation/office_fitout_15d` (Commercial Office Fit-Out Project Management). It contains the offline synthetic business state available at scenario start. The environment name is `office_fitout_15d`, the scenario window is `2026-07-01` through `2026-09-01`, and the timezone is `Asia/Shanghai`.

## associated task / Associated Task

- **Task / task:** `renovation/office_fitout_15d`
- **midCN-termtitle / Chinese title:** commercial office Fit-out projectCN-text
- **English title / English title:** Commercial Office Fit-Out Project Management
- **Service / service:** `email`
- **Environment / environment name:** `office_fitout_15d`
- **Scenario window / scenariowindow:** `2026-07-01` → `2026-09-01`
- **Timezone / CN-text:** `Asia/Shanghai`

## scenarioCN-text / Scenario Role

CN-textdocumentCN-term、message、CN-text、CN-textwithdraftstatus。

Stores mail folders, messages, threads, attachments, and drafts.

## CN-textdata / Seed Contents

CN-textdocumentfor `init.json`、`init.sql`。downCN-termoflineCN-textservice SQLite schema with `init.sql` ofCN-textwithinCN-text；CN-text，CN-textstatusCN-text。

Initial files: `init.json`, `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| CN-text / Table | CN-textlineCN-term / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `account_config` | 1 |
| `attachments` | 0 |
| `drafts` | 0 |
| `folders` | 3 |
| `messages` | 4 |
| `sent_log` | 0 |

## CN-text / Key Entities

CN-termdownCN-textfastCN-termmidlineCN-textofCN-textandCN-text；CN-textisordinaryscenarioCN-text，notCN-text。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| CN-text / Table | CN-textlineCN-term / Initial Rows | CN-text / Primary Key |
|---|---:|---|
| `messages` | 4 | `id` |
| `folders` | 3 | `id` |
| `account_config` | 1 | `id` |

## CN-textstatuswithCN-text / Initial State and Mutations

`init.*` CN-termdescriptioneventtimeCN-textbeforeofCN-textstatus。afterCN-termstatusCN-textmustper `event.yaml` of Stage withtimeCN-text，notCN-textforalreadyCN-termatCN-text seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` CN-textserviceofCN-textupdated；CN-termlineCN-text Agent CN-textofstatusCN-textlineCN-text。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## documentdescription / Files

| File / document | Purpose / CN-text | Size / CN-text |
|---|---|---:|
| `init.json` | CN-text seed / structured initial seed | 8466 bytes |
| `init.sql` | SQLite CN-text seed / initial SQLite seed | 7236 bytes |

## CN-textdescription / Loading

CN-textlineCN-textwill `email` CN-textenvironment `office_fitout_15d`，fromtaskCN-textwithinof `envs/email/office_fitout_15d/` CN-textdata。CN-textdataCN-textoutsideCN-termserviceCN-textprovideof `SCHEMA_SQL` CN-text，andCN-text `init.sql`；SQLite `integrity_check` for `ok`，outsideCN-textfor 0 CN-term。CN-textincluding `init.json` or JSONL document，CN-termlineCN-textperCN-textserviceofdataCN-textretainandCN-textdocument。CN-term task-only publishCN-termnotCN-termincludingserviceCN-textorCN-termlineCN-text。

A compatible runtime should bind `email` to environment `office_fitout_15d` and read `envs/email/office_fitout_15d/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## datawithCN-text / Data and Privacy

CN-termenvironmentmidofpeopleCN-term、CN-text、CN-termNo.、CN-text、message、location、price、CN-textsummaryandCN-textrecordCN-termforCN-textdata。documentnotCN-termincludingCN-textpeopleCN-text，CN-termnotrequiredCN-text。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
