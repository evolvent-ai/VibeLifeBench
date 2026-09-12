# `calendar/civil_service_written_to_interview_audit`

## translated source textexplanation

translated source text `exam_preparation/civil_service_written_to_interview_audit`（civil servicewritten examtranslated source textinterviewtranslated source textaudittranslated source text）translated source textof task-local `calendar` environment。translated source textstoresscenariostartavailableofoffline synthetictranslated source textstatus，environmenttranslated source text `civil_service_written_to_interview_audit`。scenariowindowtranslated source text `2026-07-08` to `2026-08-31`，translated source text `Asia/Shanghai`。

## English Summary

This is the task-local `calendar` environment for `exam_preparation/civil_service_written_to_interview_audit` (Civil Service Written Exam to Interview Qualification Audit). It contains the offline synthetic business state available at scenario start. The environment name is `civil_service_written_to_interview_audit`, the scenario window is `2026-07-08` through `2026-08-31`, and the timezone is `Asia/Shanghai`.

## translated source text / Associated Task

- **Task / translated source text:** `exam_preparation/civil_service_written_to_interview_audit`
- **translated source textquestions / Chinese title:** civil servicewritten examtranslated source textinterviewtranslated source textaudittranslated source text
- **English title / translated source textquestions:** Civil Service Written Exam to Interview Qualification Audit
- **Service / service:** `calendar`
- **Environment / environmenttranslated source text:** `civil_service_written_to_interview_audit`
- **Scenario window / scenariowindow:** `2026-07-08` → `2026-08-31`
- **Timezone / translated source text:** `Asia/Shanghai`

## scenariotranslated source text / Scenario Role

storesdaytranslated source text、translated source textwindow、translated source textandpeople、reminderandtranslated source textinformation。

Stores events, time windows, attendees, reminders, and scheduling conflicts.

## translated source textdata / Seed Contents

translated source textfiletranslated source text `init.sql`。translated source texttableofrow counttranslated source textservice SQLite schema and `init.sql` oftranslated source textnewtranslated source textload；translated source texttable，according totranslated source textinitial stateboundary。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| translated source texttable / Table | translated source textrow count / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `attendees` | 0 |
| `calendars` | 1 |
| `events` | 229 |
| `reminders` | 0 |

## keytranslated source text / Key Entities

belowtranslated source textexittranslated source textrow counttranslated source textoftranslated source texttableandtranslated source textprimary keytranslated source text；translated source textordinaryscenarioentities，does not implypreset outcome。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| translated source texttable / Table | translated source textrow count / Initial Rows | primary keytranslated source text / Primary Key |
|---|---:|---|
| `events` | 229 | `event_id` |
| `calendars` | 1 | `calendar_id` |

## initial stateandtranslated source text / Initial State and Mutations

`init.*` onlytranslated source texteventtimelineapplybeforeofinitial state。subsequentstate changesmusttranslated source text `event.yaml` of Stage andtranslated source textapply，cannottranslated source textattranslated source text seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` translated source textdirect writestranslated source textserviceoftranslated source textupdate；during runtimetranslated source text Agent tool callstranslated source textofstate changestranslated source textpersisted。

No staged event directly writes this service in `event.yaml`; state changes caused by agent tool calls are still persisted by the compatible runtime.

## fileexplanation / Files

| File / file | Purpose / translated source text | Size / translated source text |
|---|---|---:|
| `init.sql` | SQLite translated source text seed / initial SQLite seed | 109549 bytes |

## loadexplanation / Loading

translated source text `calendar` translated source textenvironment `civil_service_written_to_interview_audit`，fromtranslated source textcatalogtranslated source textof `envs/calendar/civil_service_written_to_interview_audit/` translated source textdata。translated source texttimesdatatranslated source textservicetranslated source textof `SCHEMA_SQL` translated source texttable，translated source textload `init.sql`；SQLite `integrity_check` translated source text `ok`，translated source textchecktranslated source text 0 items。translated source textcatalogtranslated source textincludes `init.json` or JSONL file，translated source textserviceofdataloadtranslated source textretaintranslated source textfile。translated source text task-only publishtranslated source textnottranslated source textincludesservicetranslated source textortranslated source text。

A compatible runtime should bind `calendar` to environment `civil_service_written_to_interview_audit` and read `envs/calendar/civil_service_written_to_interview_audit/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## dataandtranslated source text / Data and Privacy

translated source textenvironmenttranslated source textofpeopletranslated source text、translated source text、account、order、message、place、price、policysummaryandtranslated source textrecordtranslated source textoffline syntheticdata。filenottranslated source textincludestranslated source textpersonaltranslated source text，translated source textnotneedtranslated source textasktranslated source text。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
