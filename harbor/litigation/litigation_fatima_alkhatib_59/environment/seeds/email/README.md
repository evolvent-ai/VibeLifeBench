# email env for litigation_fatima_alkhatib_59

purpose：providesrecord、counsel letter、QC original/summary、recordmanufacturer supplemental note。time range is 2026-07 to 2026-08，time zone Asia/Shanghai。

record、record、counsel letter、QC original、QC supplemental testing、recordrecallrecordupdate。record、ordinaryrecord、other product returnrecord，messages record 200 rows。record。

## core business-table audit

| table | core | initial row count | dependent capability axis/check | decoy strategy | meets target |
|---|---|---:|---|---|---|
| `messages` | yes | 230 | record、counsel letter、QC、record、recallrecord / `s4_legal_letter_indexed`、`s5_after_sales_thread_indexed`、`s8_qc_original_indexed`、`s15_privacy_request_logged`、`s19_recall_scope_expansion_detected`、`s21_qc_addendum_logged` | record、ordinaryrecord、other product return、record | yes |
| `folders` | no | 4 | INBOX/Sent/Drafts record | record/record；core-table exemption reason：record，sent/draft recordstatusrecord | yes |
| `attachments` | no | 3 | QC original/summaryrecord / `s8_qc_original_not_forwarded` | record；core-table exemption reason：recordyes messages，record | yes |
| `account_config` | no | 1 | recordnumberrecord | recordnumberrecord；core-table exemption reason：record | yes |
