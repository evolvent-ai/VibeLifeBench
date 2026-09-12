# MCP CJK_5DE5_CJK_5177_CJK_901F_CJK_67E5_CJK_8868_

## legal_search（case-law and statute search：precedent + statute article + CJK_63F4_CJK_5F15_）
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?)` — CJK_641C_precedent；
  case_type ∈ CJK_52B3_CJK_52A8_CJK_4E89_CJK_8BAE_/CJK_5408_CJK_540C_CJK_7EA0_CJK_7EB7_/CJK_4FB5_CJK_6743_CJK_8D23_CJK_4EFB_/CJK_5A5A_CJK_59FB_CJK_5BB6_CJK_5EAD_/CJK_52B3_CJK_52A8_CJK_4EF2_CJK_88C1_/CJK_5176_CJK_4ED6_（private lendingCJK_5C5E_"CJK_5408_CJK_540C_CJK_7EA0_CJK_7EB7_"）
- `get_case(case_id)` — judgmentCJK_5168_CJK_6587_（CJK_5F53_CJK_4E8B_CJK_4EBA_/CJK_6848_CJK_7531_/CJK_4E8B_CJK_5B9E_/CJK_88C1_CJK_5224_CJK_7406_CJK_7531_/CJK_88C1_CJK_5224_CJK_8981_CJK_65E8_/judgmentCJK_4E3B_CJK_6587_/CJK_7ED3_CJK_679C_/CJK_5173_CJK_952E_CJK_8BCD_）
- `get_similar_cases(case_id, limit?)` — CJK_540C_CJK_7C7B_precedent（underCJK_5173_CJK_952E_CJK_8BCD_CJK_91CD_CJK_5408_CJK_5EA6_CJK_6392_CJK_5E8F_）
- `get_case_citations(case_id)` — CJK_8BE5_CJK_6848_CJK_63F4_CJK_5F15_ofstatute article(statutes_cited)andCJK_6848_CJK_4F8B_(cases_cited)
- `search_statutes(keyword?, limit?)` / `get_statute(statute_id)` — CJK_6CD5_CJK_5F8B_CJK_6CD5_CJK_89C4_（CJK_542B_ status：currently effective/alreadyCJK_4FEE_CJK_8BA2_/alreadyCJK_5E9F_CJK_6B62_）
- `list_statute_articles(statute_id)` / `get_article(article_id)` — statute articleCJK_76EE_CJK_5F55_ / statute articleCJK_5168_CJK_6587_
- `list_courts()` / `get_court(court_id)` — court
- `save_case(user_id, case_id)` / `list_saved(user_id)` / `add_note_to_case(user_id, case_id, note)` — savedandCJK_5907_CJK_6CE8_
- CJK_6211_of user_id is `usr_wang_fang`

## notification_hub（CJK_8BA2_CJK_9605_andnoticeinCJK_5FC3_）
- `list_official_accounts(user_id)` / `get_account_feed(account_id, limit?)` — official account（CJK_542B_CJK_5B98_CJK_65B9_CJK_987B_CJK_77E5_ + lawyerCJK_540D_CJK_5F55_）
- `subscribe_official_account(user_id, account_id)`
- `list_subscriptions(user_id, status?)` / `create_subscription(user_id, source, type, target, condition_json?)`
- `list_notifications(user_id, unread_only?, source?, since?, limit?)` / `get_notification(notification_id)` / `mark_read(notification_id)`
- CJK_6211_of user_id is `usr_wang_fang`
- type canCJK_9009_: price_drop / restock / policy_update / new_content / price_target / keyword

## calendar
- `list_events(time_min?, time_max?, max_results?)` — CJK_67E5_dayCJK_7A0B_
- `create_event(summary, start, end, description?, location?, attendees?, reminders?)` — CJK_5EFA_CJK_4E8B_CJK_4EF6_
- `update_event(event_id, ...)` / `search_events(query, ...)`
- CJK_6211_of user_id is `wang_fang`

## notion
- `API-post-page(parent, properties, children?)` — CJK_5EFA_CJK_9875_CJK_9762_
- `API-patch-page(page_id, properties?)` — CJK_6539_CJK_9875_CJK_9762_
- `API-get-block-children(block_id)` / `API-patch-block-children(block_id, children)` — CJK_8BFB_/CJK_8FFD_CJK_52A0_content
- `API-post-search(query?)` — CJK_641C_CJK_7D22_
- CJK_5DE5_CJK_4F5C_CJK_533A_ root page_id = `wang_fang_workspace_root`（noneCJK_72EC_CJK_7ACB_ user_id CJK_53C2_CJK_6570_）

## email
- `get_emails(folder?, page?, page_size?)` — CJK_5217_CJK_90AE_CJK_4EF6_（folder CJK_7528_CJK_540D_CJK_5B57_，CJK_5982_ "INBOX"/"Sent"/"Lending"）；CJK_8FD4_CJK_56DE_ dict，CJK_5217_CJK_8868_at `emails`，CJK_9879_ id is `email_id`
- `read_email(email_id)` — CJK_8BFB_CJK_6B63_CJK_6587_
- `search_emails(query, folder?)` — CJK_641C_
- `send_email(to, subject, body)` / `reply_email(email_id, body)` — CJK_53D1_/CJK_56DE_（formalCJK_6CD5_CJK_5F8B_CJK_6587_CJK_4E66_CJK_53EA_CJK_8D77_CJK_8349_CJK_8349_CJK_7A3F_，CJK_4E0D_CJK_66FF_CJK_6211_CJK_53D1_CJK_9001_）

## CJK_901A_CJK_7528_CJK_539F_CJK_5219_
- CJK_505A_procedure/CJK_7BA1_CJK_8F96_/hourCJK_6548_/CJK_5229_CJK_7387_/securityCJK_5224_CJK_65AD_CJK_524D_，CJK_5148_CJK_67E5_CJK_5B98_CJK_65B9_CJK_987B_CJK_77E5_ + currently effectivestatute article + CJK_540C_CJK_7C7B_precedent，CJK_9010_CJK_9879_verifyCJK_518D_CJK_4E0B_CJK_7ED3_CJK_8BBA_
- CJK_5F15_CJK_7528_precedentCJK_951A_CJK_5B9A_ case_id、CJK_5F15_CJK_7528_statute articleCJK_951A_CJK_5B9A_ article_no/CJK_6761_No.，CJK_91D1_CJK_989D_CJK_8BA1_CJK_7B97_CJK_5199_CJK_6E05_"IOUCJK_91D1_CJK_989D_ vs actually received"
- CJK_5BF9_evidenceCJK_8584_CJK_5F31_CJK_5904_（noneCJK_51ED_CJK_8BC1_cashCJK_4EA4_CJK_4ED8_）CJK_5982_CJK_5B9E_CJK_63D0_CJK_793A_CJK_98CE_CJK_9669_；CJK_4E0D_canCJK_9006_CJK_52A8_CJK_4F5C_CJK_53EA_CJK_63D0_CJK_65B9_CJK_6848_，CJK_7531_Wang FangCJK_51B3_CJK_5B9A_
