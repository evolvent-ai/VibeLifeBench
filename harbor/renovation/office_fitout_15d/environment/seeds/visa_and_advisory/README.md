# `visa_and_advisory/office_fitout_15d`

## Chinese description

CN-termistask `renovation/office_fitout_15d`（commercial office Fit-out projectCN-text）CN-textof task-local `visa_and_advisory` environment。CN-textscenarioCN-textavailableofCN-textstatus，environment namefor `office_fitout_15d`。scenariowindowfor `2026-07-01` to `2026-09-01`，CN-textfor `Asia/Shanghai`。

## English Summary

This is the task-local `visa_and_advisory` environment for `renovation/office_fitout_15d` (Commercial Office Fit-Out Project Management). It contains the offline synthetic business state available at scenario start. The environment name is `office_fitout_15d`, the scenario window is `2026-07-01` through `2026-09-01`, and the timezone is `Asia/Shanghai`.

## associated task / Associated Task

- **Task / task:** `renovation/office_fitout_15d`
- **midCN-termtitle / Chinese title:** commercial office Fit-out projectCN-text
- **English title / English title:** Commercial Office Fit-Out Project Management
- **Service / service:** `visa_and_advisory`
- **Environment / environment name:** `office_fitout_15d`
- **Scenario window / scenariowindow:** `2026-07-01` → `2026-09-01`
- **Timezone / CN-text:** `Asia/Shanghai`

## scenarioCN-text / Scenario Role

CN-text、CN-text、CN-termlinerecommendationwithCN-textcondition。

Stores visa, entry, travel-advisory, and policy conditions.

## CN-textdata / Seed Contents

CN-textdocumentfor `init.sql`。downCN-termoflineCN-textservice SQLite schema with `init.sql` ofCN-textwithinCN-text；CN-text，CN-textstatusCN-text。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| CN-text / Table | CN-textlineCN-term / Initial Rows |
|---|---:|
| `_counters` | 0 |
| `advisories` | 1 |
| `advisory_subscriptions` | 0 |
| `application_documents` | 2 |
| `entry_requirements` | 2 |
| `notifications` | 0 |
| `scripted_events` | 2 |
| `visa_applications` | 5 |
| `visa_products` | 5 |

## CN-text / Key Entities

CN-termdownCN-textfastCN-termmidlineCN-textofCN-textandCN-text；CN-textisordinaryscenarioCN-text，notCN-text。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| CN-text / Table | CN-textlineCN-term / Initial Rows | CN-text / Primary Key |
|---|---:|---|
| `visa_applications` | 5 | `application_id` |
| `visa_products` | 5 | `product_id` |
| `application_documents` | 2 | `doc_id` |
| `entry_requirements` | 2 | `origin_nationality`, `destination`, `purpose` |
| `scripted_events` | 2 | `seq` |
| `advisories` | 1 | `country_code` |

## CN-textstatuswithCN-text / Initial State and Mutations

`init.*` CN-termdescriptioneventtimeCN-textbeforeofCN-textstatus。afterCN-termstatusCN-textmustper `event.yaml` of Stage withtimeCN-text，notCN-textforalreadyCN-termatCN-text seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` midhas 21 CN-termeventCN-termupdatedCN-termservice / 21 events in `event.yaml` update this service:

| Stage | Time / time | Kind / CN-text | Update method / updatedCN-text |
|---:|---|---|---|
| 3 | `06:00` | `mutation` | SQL file `d03_property_design_rfi.sql` |
| 4 | `07:30` | `mutation` | SQL file `d04_noise_complaint_advisory.sql` |
| 5 | `06:05` | `mutation` | SQL file `d05_insurance_in_force.sql` |
| 5 | `06:15` | `mutation` | SQL file `d05_rainstorm_window_compressed.sql` |
| 5 | `06:30` | `mutation` | SQL file `d05_bim_lod400_demanded.sql` |
| 5 | `06:45` | `mutation` | SQL file `d05_noise_window_advisory.sql` |
| 6 | `05:45` | `mutation` | SQL file `d06_filing_approved.sql` |
| 8 | `06:50` | `mutation` | SQL file `d08_board_cut_insurance.sql` |
| 9 | `06:25` | `mutation` | SQL file `d09_g20_zone_curfew.sql` |
| 10 | `06:15` | `mutation` | SQL file `d10_fire_drawing_second_reject.sql` |
| 11 | `06:45` | `mutation` | SQL file `d11_lobby_badge_lead_time.sql` |
| 12 | `06:25` | `mutation` | SQL file `d12_electrical_load_insufficient.sql` |
| 13 | `06:00` | `mutation` | SQL file `d13_fire_inspection_partial_fail.sql` |
| 13 | `07:15` | `mutation` | SQL file `d13_internal_layout_advisory.sql` |
| 13 | `09:05` | `mutation` | SQL file `d13_handover_recheck_advisory.sql` |
| 13 | `17:05` | `mutation` | SQL file `d13_dual_recheck_approvals.sql` |
| 14 | `07:30` | `mutation` | SQL file `d14_handover_conditional.sql` |
| 15 | `06:30` | `mutation` | SQL file `d15_hvac_punch_item.sql` |
| 16 | `06:20` | `mutation` | SQL file `d16_voc_exceed.sql` |
| 18 | `05:45` | `mutation` | SQL file `d18_electrical_condition_cleared.sql` |
| 19 | `07:45` | `mutation` | SQL file `d19_closeout_gate_approvals.sql` |

## documentdescription / Files

| File / document | Purpose / CN-text | Size / CN-text |
|---|---|---:|
| `init.sql` | SQLite CN-text seed / initial SQLite seed | 16454 bytes |

## CN-textdescription / Loading

CN-textlineCN-textwill `visa_and_advisory` CN-textenvironment `office_fitout_15d`，fromtaskCN-textwithinof `envs/visa_and_advisory/office_fitout_15d/` CN-textdata。CN-textdataCN-textoutsideCN-termserviceCN-textprovideof `_SCHEMA` CN-text，andCN-text `init.sql`；SQLite `integrity_check` for `ok`，outsideCN-textfor 0 CN-term。CN-textincluding `init.json` or JSONL document，CN-termlineCN-textperCN-textserviceofdataCN-textretainandCN-textdocument。CN-term task-only publishCN-termnotCN-termincludingserviceCN-textorCN-termlineCN-text。

A compatible runtime should bind `visa_and_advisory` to environment `office_fitout_15d` and read `envs/visa_and_advisory/office_fitout_15d/` from the task directory. For this data audit, the external service implementation supplied `_SCHEMA`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## datawithCN-text / Data and Privacy

CN-termenvironmentmidofpeopleCN-term、CN-text、CN-termNo.、CN-text、message、location、price、CN-textsummaryandCN-textrecordCN-termforCN-textdata。documentnotCN-termincludingCN-textpeopleCN-text，CN-termnotrequiredCN-text。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
