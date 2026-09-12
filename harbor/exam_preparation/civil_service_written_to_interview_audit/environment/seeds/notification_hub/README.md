# `notification_hub/civil_service_written_to_interview_audit`

## translated source textexplanation

translated source text `exam_preparation/civil_service_written_to_interview_audit`（civil servicewritten examtranslated source textinterviewtranslated source textaudittranslated source text）translated source textof task-local `notification_hub` environment。translated source textstoresscenariostartavailableofoffline synthetictranslated source textstatus，environmenttranslated source text `civil_service_written_to_interview_audit`。scenariowindowtranslated source text `2026-07-08` to `2026-08-31`，translated source text `Asia/Shanghai`。

## English Summary

This is the task-local `notification_hub` environment for `exam_preparation/civil_service_written_to_interview_audit` (Civil Service Written Exam to Interview Qualification Audit). It contains the offline synthetic business state available at scenario start. The environment name is `civil_service_written_to_interview_audit`, the scenario window is `2026-07-08` through `2026-08-31`, and the timezone is `Asia/Shanghai`.

## translated source text / Associated Task

- **Task / translated source text:** `exam_preparation/civil_service_written_to_interview_audit`
- **translated source textquestions / Chinese title:** civil servicewritten examtranslated source textinterviewtranslated source textaudittranslated source text
- **English title / translated source textquestions:** Civil Service Written Exam to Interview Qualification Audit
- **Service / service:** `notification_hub`
- **Environment / environmenttranslated source text:** `civil_service_written_to_interview_audit`
- **Scenario window / scenariowindow:** `2026-07-08` → `2026-08-31`
- **Timezone / translated source text:** `Asia/Shanghai`

## scenariotranslated source text / Scenario Role

storesnotice、translated source text、officialaccountandmessagetranslated source textstatus。

Stores notifications, subscriptions, official accounts, and delivery state.

## translated source textdata / Seed Contents

translated source textfiletranslated source text `init.sql`。translated source texttableofrow counttranslated source textservice SQLite schema and `init.sql` oftranslated source textnewtranslated source textload；translated source texttable，according totranslated source textinitial stateboundary。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| translated source texttable / Table | translated source textrow count / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `notifications` | 240 |
| `official_account_posts` | 0 |
| `official_account_subscriptions` | 2 |
| `official_accounts` | 3 |
| `price_alerts` | 0 |
| `subscriptions` | 2 |

## keytranslated source text / Key Entities

belowtranslated source textexittranslated source textrow counttranslated source textoftranslated source texttableandtranslated source textprimary keytranslated source text；translated source textordinaryscenarioentities，does not implypreset outcome。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| translated source texttable / Table | translated source textrow count / Initial Rows | primary keytranslated source text / Primary Key |
|---|---:|---|
| `notifications` | 240 | `notification_id` |
| `official_accounts` | 3 | `account_id` |
| `official_account_subscriptions` | 2 | `user_id`, `account_id` |
| `subscriptions` | 2 | `subscription_id` |

## initial stateandtranslated source text / Initial State and Mutations

`init.*` onlytranslated source texteventtimelineapplybeforeofinitial state。subsequentstate changesmusttranslated source text `event.yaml` of Stage andtranslated source textapply，cannottranslated source textattranslated source text seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` translated source text 6 translated source texteventtranslated source textupdatetranslated source textservice / 6 events in `event.yaml` update this service:

| Stage | Time / translated source text | Kind / translated source text | Update method / updatetranslated source text |
|---:|---|---|---|
| 1 | `2026-07-08T09:00:00+08:00` | `mutation` | inline `upsert` on `notifications` |
| 7 | `2026-07-16T09:00:00+08:00` | `mutation` | inline `upsert` on `notifications` |
| 11 | `2026-08-10T09:00:00+08:00` | `mutation` | inline `upsert` on `notifications` |
| 16 | `2026-08-20T10:00:00+08:00` | `mutation` | inline `upsert` on `notifications` |
| 19 | `2026-08-23T10:00:00+08:00` | `mutation` | inline `upsert` on `notifications` |
| 20 | `2026-08-24T09:30:00+08:00` | `mutation` | inline `upsert` on `notifications` |

## fileexplanation / Files

| File / file | Purpose / translated source text | Size / translated source text |
|---|---|---:|
| `init.sql` | SQLite translated source text seed / initial SQLite seed | 129264 bytes |

## loadexplanation / Loading

translated source text `notification_hub` translated source textenvironment `civil_service_written_to_interview_audit`，fromtranslated source textcatalogtranslated source textof `envs/notification_hub/civil_service_written_to_interview_audit/` translated source textdata。translated source texttimesdatatranslated source textservicetranslated source textof `SCHEMA_SQL` translated source texttable，translated source textload `init.sql`；SQLite `integrity_check` translated source text `ok`，translated source textchecktranslated source text 0 items。translated source textcatalogtranslated source textincludes `init.json` or JSONL file，translated source textserviceofdataloadtranslated source textretaintranslated source textfile。translated source text task-only publishtranslated source textnottranslated source textincludesservicetranslated source textortranslated source text。

A compatible runtime should bind `notification_hub` to environment `civil_service_written_to_interview_audit` and read `envs/notification_hub/civil_service_written_to_interview_audit/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## dataandtranslated source text / Data and Privacy

translated source textenvironmenttranslated source textofpeopletranslated source text、translated source text、account、order、message、place、price、policysummaryandtranslated source textrecordtranslated source textoffline syntheticdata。filenottranslated source textincludestranslated source textpersonaltranslated source text，translated source textnotneedtranslated source textasktranslated source text。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
