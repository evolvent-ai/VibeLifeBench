# ecommerce env for litigation_fatima_alkhatib_59

purpose：provides Fatima record、SKU、record、same lotrecord、refundrecordlotrecallstatus。time range is 2026-06 to 2026-09，time zone Asia/Shanghai。

record：record、record SKU、order at issue、same lot B17 recordrecall mutation。record search/get/list record；workspace recordnumberrecordrecallrecord。record SKU、nearby lot、ordinaryrefundrecordotherrecord，record products/orders record 200 rows。

## core business-table audit

| table | core | initial row count | dependent capability axis/check | decoy strategy | meets target |
|---|---|---:|---|---|---|
| `products` | yes | 220 | record、usage instructions、recallstatus / `s2_product_sku_batch_identified`、`s5_product_instruction_logged`、`s13_recall_mutation_detected` | recordotherrecord、recordnoterecordstatus | yes |
| `skus` | yes | 222 | SKU recordlotrecord / `s2_product_sku_batch_identified`、`s13_recall_mutation_detected` | record、nearby lot、recordstatusrecordrecallrecord SKU record | yes |
| `stocks` | yes | 222 | recordrecall reviewrecord / `s13_recall_mutation_detected` | record SKU record SKU record | yes |
| `orders` | yes | 230 | order at issue、same lotrecord、recallrecord / `s2_claim_order_indexed`、`s9_same_batch_orders_counted`、`s19_recall_scope_expansion_detected` | same lot、nearby lot、other SKU、ordinaryrecord，record batch_id record | yes |
| `order_items` | yes | 230 | record SKU record / `s2_claim_order_indexed`、`s9_same_batch_orders_counted` | record，record SKU recordlot | yes |
| `order_status_history` | yes | 230 | recordstatusrecord/refundrecord / `s23_auth_audit_safe` | record、ordinaryrecordstatusrecordstatusrecordrecord | yes |
| `refunds` | no | 5 | recordrefundrecord / `no_cancelled_or_new_refund` helper | recordstatusrecord；core-table exemption reason：recordyesrecord，recordrefundrecord | yes |
| `addresses` | no | 1 | record | single-store address holder；core-table exemption reason：record | yes |
