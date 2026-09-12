# delivery_logistics_mock env

recorddeliveryrecord 230 recorddeliveryrecord。recordplatformrecordeventrecordevent。

## core business table audit

| record | record | initial row count | capability axis/check | noise strategy | meets target |
|---|---|---:|---|---|---|
| `shipments` | record | 231 | order object identification、delivery baseline、record；s3_delivery_trace_loaded、s13_delivery_refresh_after_mutation、s22_backend_review_reconciled | 230 record、record、merchantrecorddeliveryrecord，record ID record seed record | record，single table >=200 |
| `shipment_events` | record | 235 | trackingeventrecord、platformrecordmanual handoffrecord；s7_platform_time_indexed、s14_time_versions_preserved、cross_time_conflicts_preserved | recordtimerecordpickup、detour、record、recordeventrecord，recordorderrecordsourcerecord | record，single table >=200 |
| `address_book` | record | 2 | recordfield | recordmerchantrecord，recordresearchrecord | not applicable，record |
