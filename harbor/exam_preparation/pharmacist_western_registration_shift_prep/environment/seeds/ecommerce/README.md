# `ecommerce/pharmacist_western_registration_shift_prep`

## translated business textdescription

thistranslated business texttask `exam_preparation/pharmacist_western_registration_shift_prep`（licensed pharmacistWestern medicineregistrationtranslated business text、legitimate coursetranslated business textandtranslated business textexam preparation）translated business text task-local `ecommerce` environment。translated business textstoresscenario startavailabletranslated business textofflinesynthetictranslated business textstatus，environmenttranslated business textis `pharmacist_western_registration_shift_prep`。scenariowindowis `2026-08-01` translated business text `2026-10-11`，timezoneis `Asia/Shanghai`。

## English Summary

This is the task-local `ecommerce` environment for `exam_preparation/pharmacist_western_registration_shift_prep` (Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation). It contains the offline synthetic business state available at scenario start. The environment name is `pharmacist_western_registration_shift_prep`, the scenario window is `2026-08-01` through `2026-10-11`, and the timezone is `Asia/Shanghai`.

## translated business texttask / Associated Task

- **Task / task:** `exam_preparation/pharmacist_western_registration_shift_prep`
- **translated business text / Chinese title:** licensed pharmacistWestern medicineregistrationtranslated business text、legitimate coursetranslated business textandtranslated business textexam preparation
- **English title / translated business text:** Licensed Pharmacist Registration, Course Purchase, and Shift-Based Preparation
- **Service / service:** `ecommerce`
- **Environment / environmenttranslated business text:** `pharmacist_western_registration_shift_prep`
- **Scenario window / scenariowindow:** `2026-08-01` → `2026-10-11`
- **Timezone / timezone:** `Asia/Shanghai`

## scenariotranslated business text / Scenario Role

storestranslated business text、translated business text、translated business text、translated business text、refundandtranslated business textstatus。

Stores products, carts, orders, promotions, refunds, and after-sales state.

## initialdata / Seed Contents

initialfileis `init.sql`。translated business textservice SQLite schema and `init.sql` translated business textload；translated business text，withtranslated business textinitial stateboundary。

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| translated business text / Table | initialtranslated business text / Initial Rows |
|---|---:|
| `_counters` | 3 |
| `addresses` | 1 |
| `applied_coupons` | 0 |
| `cart_items` | 0 |
| `carts` | 1 |
| `coupons` | 0 |
| `order_items` | 0 |
| `order_status_history` | 0 |
| `orders` | 0 |
| `products` | 220 |
| `refunds` | 0 |
| `skus` | 220 |
| `stocks` | 220 |

## translated business text / Key Entities

withtranslated business textinitialtranslated business textandtranslated business textfield；translated business textordinaryscenarioentities，does not implypreset outcome。

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| translated business text / Table | initialtranslated business text / Initial Rows | translated business textfield / Primary Key |
|---|---:|---|
| `products` | 220 | `product_id` |
| `skus` | 220 | `sku_id` |
| `stocks` | 220 | `sku_id` |
| `addresses` | 1 | `address_id` |
| `carts` | 1 | `user_id` |

## initial stateanddynamic changes / Initial State and Mutations

`init.*` translated business textdescriptiontranslated business textunitstranslated business textinitial state。later state changestranslated business text `event.yaml` translated business text Stage andtranslated business text，translated business textisalreadytranslated business textattranslated business textinitial seed。

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

`event.yaml` translated business texthas 4 itemstranslated business textunitstranslated business textservice / 4 events in `event.yaml` update this service:

| Stage | Time / translated business text | Kind / translated business text | Update method / translated business text |
|---:|---|---|---|
| 5 | `2026-08-12T19:59:00+08:00` | `mutation` | SQL file `stage_5_course_catalog.sql` |
| 10 | `2026-08-24T10:20:00+08:00` | `mutation` | inline `update` on `products` |
| 11 | `2026-08-25T07:30:00+08:00` | `mutation` | SQL file `stage_11_law_sku_title.sql` |
| 22 | `2026-09-24T09:30:00+08:00` | `mutation` | SQL file `stage_22_law_patch.sql` |

## filedescription / Files

| File / file | Purpose / purpose | Size / translated business text |
|---|---|---:|
| `init.sql` | SQLite initial seed / initial SQLite seed | 101859 bytes |

## loaddescription / Loading

translated business textwill `ecommerce` translated business textenvironment `pharmacist_western_registration_shift_prep`，translated business texttaskdirectorytranslated business text `envs/ecommerce/pharmacist_western_registration_shift_prep/` readdata。thistranslated business textdatatranslated business textservicetranslated business textnowtranslated business text `SCHEMA_SQL` translated business text，andload `init.sql`；SQLite `integrity_check` is `ok`，translated business textis 0 translated business text。translated business textdirectorytranslated business text `init.json` or JSONL file，translated business textservicetranslated business textdataloadtranslated business textretainandreadthistranslated business textfile。translated business text task-only translated business textcontains noservicetranslated business textnowortranslated business text。

A compatible runtime should bind `ecommerce` to environment `pharmacist_western_registration_shift_prep` and read `envs/ecommerce/pharmacist_western_registration_shift_prep/` from the task directory. For this data audit, the external service implementation supplied `SCHEMA_SQL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## dataandprivacystatement / Data and Privacy

thisenvironmenttranslated business textpeopletranslated business text、translated business text、translated business text、translated business text、translated business text、location、price、policytranslated business textrecordtranslated business textisofflinesyntheticdata。filecontains nogenuineitemspeopleprivacy，translated business textrequires internet access。

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
