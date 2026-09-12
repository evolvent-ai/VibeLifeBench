# weather env

## Scenario Usage

This env provides mock backend facts for `constructor_exam_site_project_safety`, covering constructor exam prep, project site milestones, safety material boundaries, textbook logistics, travel, and reimbursement. The time range is 2026-07-03 to 2026-09-16, primary time zone Asia/Shanghai.

## Key Objects and Status Conventions

- User: `user_lu_jing`, email `lu.jing@example.invalid`.
- Key facts exist only as business status in the mock backend; the agent needs to query, filter, and cross-verify through tools.
- Amounts use RMB fen or the server's existing amount fields; dates use ISO 8601 or YYYY-MM-DD.
- Around the key unique solution, keep interfering items such as nearby dates, nearby locations, old and new statuses, same-named examination sites, same routes with different policies, or prohibited materials.

## Table-Level Row Count Audit

| Table name | Whether core | Initial row count | Dependency capability axis/check | Interference strategy | Whether compliant |
|---|---|---:|---|---|---|
| `daily_weather` | Yes | 240 | weather / project safety / exam-day recheck | Multi-day weather, rainfall, and high-temperature disruptions in Hangzhou and Ningbo | Yes |
| `hourly_weather` | Yes | 240 | warning period refinement | Hourly weather disruptions | Yes |
| `alerts` | No | 2 | stage mutation safety warning | Single-object warning status carrier | Yes |

## Rework Audit Supplement

This round did not modify the SQL data volume or key facts. Weather-safety checks still need to bind location/date/alert status and the project calendar or safety hold; the repair only fixes low-score protection and no-op boundary enforcement, and does not treat weather alert text as an independent scoring basis. The newly added `s13_weather_alert_calendar_unique` requires the stage 13 active alert, calendar safety review hold, and risk ledger to all be present, to distinguish verbal reminders from real cross-service handling.

## Data Sources and Copyright

All data is synthetic data and is only for local benchmark tasks; it does not contain real individuals, companies, examination bodies, or project materials.
