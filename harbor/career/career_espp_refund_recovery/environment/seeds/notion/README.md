# `notion/career_espp_refund_recovery`

## [translated source text]

[translated source text]task `career/career_espp_refund_recovery`（departureemployeeESPP redemption[translated source text]reconcile[translated source text]）[translated source text] task-local `notion` environment。[translated source text]save[translated source text]status，environment[translated source text] `career_espp_refund_recovery`。[translated source text] `2026-06-08` [translated source text] `2026-08-25`，[translated source text] `Asia/Shanghai`。

## English Summary

This is the task-local `notion` environment for `career/career_espp_refund_recovery` (ESPP Redemption Reconciliation and Re-employment). It contains the offline synthetic business state available at scenario start. The environment name is `career_espp_refund_recovery`, the scenario window is `2026-06-08` through `2026-08-25`, and the timezone is `Asia/Shanghai`.

## [translated source text]task / Associated Task

- **Task / task:** `career/career_espp_refund_recovery`
- **[translated source text] / Chinese title:** departureemployeeESPP redemption[translated source text]reconcile[translated source text]
- **English title / [translated source text]:** ESPP Redemption Reconciliation and Re-employment
- **Service / [translated source text]:** `notion`
- **Environment / environment[translated source text]:** `career_espp_refund_recovery`
- **Scenario window / [translated source text]:** `2026-06-08` → `2026-08-25`
- **Timezone / [translated source text]:** `Asia/Shanghai`

## [translated source text] / Scenario Role

save[translated source text]、database、[translated source text]record。

Stores pages, databases, blocks, and durable structured records.

## [translated source text]data / Seed Contents

[translated source text] `init.sql`。[translated source text] SQLite schema [translated source text] `init.sql` [translated source text]；[translated source text]，[translated source text]statusboundary。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| [translated source text] / Table | [translated source text] / Initial Rows |
|---|---:|
| `blocks` | 55 |
| `comments` | 0 |
| `counters` | 0 |
| `database_rows` | 0 |
| `databases` | 0 |
| `pages` | 16 |
| `users` | 2 |
| `workspaces` | 1 |

## key[translated source text] / Key Entities

[translated source text]；[translated source text]，[translated source text]。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| [translated source text] / Table | [translated source text] / Initial Rows | [translated source text] / Primary Key |
|---|---:|---|
| `blocks` | 55 | `block_id` |
| `pages` | 16 | `page_id` |
| `users` | 2 | `user_id` |
| `workspaces` | 1 | `workspace_id` |

## [translated source text]status[translated source text] / Initial State and Mutations

`init.*` [translated source text]timeline[translated source text]status。[translated source text]status[translated source text]according to `event.yaml` [translated source text] Stage [translated source text]，must not[translated source text] seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` [translated source text]；[translated source text] Agent [translated source text]status[translated source text]。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## [translated source text] / Files

| File / [translated source text] | Purpose / [translated source text] | Size / [translated source text] |
|---|---|---:|
| `init.sql` | SQLite [translated source text] seed / initial SQLite seed | 18563 bytes |

## [translated source text] / Loading

[translated source text] `notion` [translated source text]environment `career_espp_refund_recovery`，[translated source text]task[translated source text] `envs/notion/career_espp_refund_recovery/` [translated source text]data。[translated source text]data[translated source text] `SCHEMA_SQL` [translated source text]，[translated source text] `init.sql`；SQLite `integrity_check` [translated source text] `ok`，[translated source text] 0 article。[translated source text] `init.json` [translated source text] JSONL [translated source text]，[translated source text]according to[translated source text]data[translated source text]。[translated source text] task-only [translated source text]。

A compatible runtime should bind `notion` to environment `career_espp_refund_recovery` and read `envs/notion/career_espp_refund_recovery/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## data[translated source text] / Data and Privacy

[translated source text]environment[translated source text]、[translated source text]、[translated source text]、[translated source text]、[translated source text]、[translated source text]、price、[translated source text]summary[translated source text]record[translated source text]data。[translated source text]，[translated source text]。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
