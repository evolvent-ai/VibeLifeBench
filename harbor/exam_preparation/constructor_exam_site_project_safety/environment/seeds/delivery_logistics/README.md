# delivery_logistics env

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
| `shipments` | Yes | 220 | textbook logistics / misdelivery recovery / proactive recheck | Mixed similar tracking numbers, different carriers, and old/new statuses | Yes |
| `shipment_events` | Yes | 440 | logistics status timeline | Two status events per shipment, with similar interference for the target package | Yes |

## Rework Audit Supplement

This round did not modify the SQL data volume or key facts. The logistics recovery check still depends on tracking_no, shipment status, and issue/subscription backend status; the rework only prevents a fixed ledger single-point-not-written failure from causing a total loss of points in the health track, and does not weaken structured verification of wrong shipment / anomaly recovery.

## Data Sources and Copyright

All data is synthetic data and is only for local benchmark tasks; it does not contain real individuals, companies, examination bodies, or project materials.
