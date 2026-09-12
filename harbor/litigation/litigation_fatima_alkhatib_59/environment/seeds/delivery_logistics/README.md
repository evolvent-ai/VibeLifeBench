# delivery_logistics env for litigation_fatima_alkhatib_59

purpose：providesrecord、record、recallrecordordinaryrecord。time range is 2026-06 to 2026-08，time zone Asia/Shanghai。

record、recordrecallrecord。mutation recordrecallrecordissuerecord。record、record tracking、ordinaryrecord。shipments record 200 rows。

## core business-table audit

| table | core | initial row count | dependent capability axis/check | decoy strategy | meets target |
|---|---|---:|---|---|---|
| `shipments` | yes | 220 | record、record、recallrecord / `s3_initial_delivery_logged`、`s10_return_shipment_tracked`、`s17_return_sample_damage_logged`、`s20_sample_issue_followed` | record tracking record、record tracking、ordinaryrecord、record | yes |
| `shipment_events` | yes | 330 | record mutation recordstatusrecord / `s17_return_sample_damage_logged`、`s20_sample_issue_followed` | record，recordordinaryrecord | yes |
| `address_book` | no | 1 | record | single-store address holder，not a search entry point；core-table exemption reason：record safety-critical record | yes |
