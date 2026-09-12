# calendar env

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
| `events` | Yes | 230 | project milestones / exam conflicts / study windows | Background meetings, inspections, study blocks, and nearby high-risk milestones | Yes |
| `calendars` | No | 1 | user primary calendar | Single-object status carrier | Yes |

## Rework Audit Supplement

This round did not modify the SQL data volume or key facts. The low-score fix only adjusts how the checker combines stage-local trace, back-end facts, and persistent evidence; the base layer still must have corresponding calendar tool calls and back-end event facts, and cannot be passed by event text, workspace template, or no-op behavior.

## Data Sources and Copyright

All data is synthetic data and is only for local benchmark tasks; it does not contain real individuals, companies, examination bodies, or project materials.
