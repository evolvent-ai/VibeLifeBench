# notification_hub env

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
| `notifications` | Yes | 230 | official notices / proactive discovery / scheduled recheck | Mixed official, advertising, project, and travel sources, with close timing | Yes |
| `subscriptions` | No | 3 | monitoring intent | Single-user subscription status carrier | Yes |

## Rework Audit Supplement

This round did not modify the SQL data volume or key facts. The subscription and official-notice check still need to bind user_id, source/type/target/status or notification source; the basic low-weight item only removes a fixed-ledger single-point failure and does not allow any arbitrary notification existence to earn points.

## Data Sources and Copyright

All data is synthetic data and is only for local benchmark tasks; it does not contain real individuals, companies, examination bodies, or project materials.
