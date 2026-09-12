# maps env

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
| `places` | Yes | 230 | examination site unique resolution / interference from places with the same name / route verification | Mixed training centers, stations, hotels, and background locations with the same name | Yes |
| `transit_schedule` | Yes | 240 | examination site transit routes | Same line with different stops and time disruptions | Yes |

## Rework Audit Supplement

This round did not modify the SQL data volume or key facts. The unique exam site solution is still derived by cross-referencing the official notice with the maps location category/city/name; the rework did not write the correct place_id into workspace/event, nor did it allow passing by matching only the text "Ningbo". To fix checker false negatives, the rubric backend probe no longer passes the mock-tool-unaccepted `category=exam_site` parameter to `search_places`; instead it searches for "construction" and structurally verifies that `place_nb_exam_haishu` and `place_nb_training_same` are visible at the same time, supporting `s15_exam_site_official_map_crosscheck`.

## Data Sources and Copyright

All data is synthetic data and is only for local benchmark tasks; it does not contain real individuals, companies, examination bodies, or project materials.
