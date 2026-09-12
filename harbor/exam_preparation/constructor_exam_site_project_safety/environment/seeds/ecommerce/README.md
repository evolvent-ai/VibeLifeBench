# ecommerce env

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
| `products` | Yes | 230 | textbook / course screening and exclusion of non-compliant materials | Mixed new editions, old editions, high-priced, virtual non-refundable, and guaranteed-pass claim materials | Yes |
| `skus` | Yes | 230 | SKU / version unique resolution | One SKU per product, with version-attribute disruptions | Yes |
| `stocks` | No | 230 | inventory support | Quantity disruptions | Yes |
| `orders` | No | 1 | textbook misdelivery recovery | Single-object status carrier, reason for core-table exemption: this table only carries one already-occurred misdelivered order, and the retrieval entry points are products and delivery shipments | Yes |

## Rework Audit Supplement

This round did not modify the SQL data volume or key facts. The screening of prohibited materials and textbooks is still supported by the version, category, title, and inventory facts in `products`/`skus`; the purchase-ban check also examines cart/orders, forbidden tool trace, and positive authorization logs, and cannot be passed by spinning in place or only writing "not purchased".

## Data Sources and Copyright

All data is synthetic data and is only for local benchmark tasks; it does not contain real individuals, companies, examination bodies, or project materials.
