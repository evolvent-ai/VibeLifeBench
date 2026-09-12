# MCP case record

## legal_search（case record：case record + case record + case record）
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?)` — case record；
  case_type ∈ case record/contractcase record/case record/case record/case record/case recordhe（case record**contractcase record**）
- `get_case(case_id)` — judgmentcase record（case record/case record/case record/case record/case record/judgmentcase record/result/case record）
- `get_similar_cases(case_id, limit?)` — case record（percase record）
- `get_case_citations(case_id)` — case recordofcase record(statutes_cited)andcase record(cases_cited)
- `search_statutes(keyword?, limit?)` / `get_statute(statute_id)` — case record（case record status：case recordhascase record/alreadycase record/alreadycase record）
- `list_statute_articles(statute_id)` / `get_article(article_id)` — case record / case record
- `list_courts()` / `get_court(court_id)` — court
- `save_case(user_id, case_id)` / `list_saved(user_id)` / `add_note_to_case(user_id, case_id, note)` — case recordandcase record
- Iof user_id is `usr_chen_yue`

## notification_hub（case recordandnotificationincase record）
- `list_official_accounts(user_id)` / `get_account_feed(account_id, limit?)` — case recordNo.（case recordcourtofficialmustcase record、forensic appraisal institutiondirectory）
- `subscribe_official_account(user_id, account_id)`
- `list_subscriptions(user_id, status?)` / `create_subscription(user_id, source, type, target, condition_json?)`
- `list_notifications(user_id, unread_only?, source?, since?, limit?)` / `get_notification(notification_id)` / `mark_read(notification_id)`
- Iof user_id is `usr_chen_yue`
- type cancase record: price_drop / restock / policy_update / new_content / price_target / keyword
- **appraisalinstitutiondirectoryatcase recordNo. `oa_judicial_appraisal`（Shanghai Forensic Appraisal Service Platform）of feed case record**

## calendar
- `list_events(time_min?, time_max?, max_results?)` — case recorddaycase record
- `create_event(summary, start, end, description?, location?, attendees?, reminders?)` — case record
- `update_event(event_id, ...)` / `search_events(query, ...)`
- Iof user_id is `chen_yue`

## notion
- `API-post-page(parent, properties, children?)` — case recordpage
- `API-patch-page(page_id, properties?)` — case recordpage
- `API-get-block-children(block_id)` / `API-patch-block-children(block_id, children)` — case record/case recordcontent
- `API-post-search(query?)` — case record
- workcase record root page_id = `chen_yue_workspace_root`（nonecase record user_id case record）

## email
- `get_emails(folder?, page?, page_size?)` — case record（folder case record，if "INBOX"/"Sent"/"Lease"）；case record dict，case recordat `emails`，case record id case record `email_id`
- `read_email(email_id)` — case recordbody
- `search_emails(query, folder?)` — case record
- `send_email(to, subject, body)` / `reply_email(email_id, body)` — case record/case record（case record，notcase recordIsend）

## case record
- procedurecase recordusingcourtofficialmustcase record（case recordNo. `oa_minhang_court`）case record，communitycase record。
- case recordappraisalinstitutionrequiredcase record `oa_judicial_appraisal` directory，case recordIofcase recordverify。
- case recordbeforeconfirm status=case recordhascase record；case record/notcancase record、case recordrecommendation，case recordIdecision。
