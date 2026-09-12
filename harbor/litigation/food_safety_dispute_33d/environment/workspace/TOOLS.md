 # MCP Tool Quick Reference

## legal_search (Legal Research Database: Case Law + Statutes + Citations)
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?)` — Search case law;
This case_type is primarily a **contract dispute** (online shopping contract dispute), with a small amount of tort liability (platform joint and several liability).
- `get_case(case_id)` — Full judgment (parties/cause of action/facts/reasoning of the judgment/holding/operative part of the judgment/result/keywords)
- `get_similar_cases(case_id, limit?)` — Similar cases (ranked by keyword overlap)
- `get_case_citations(case_id)` — Statutes cited (`statutes_cited`) and cases cited (`cases_cited`) in the case
- `search_statutes(keyword?, limit?)` / `get_statute(statute_id)` — Laws and regulations (including status: currently effective/revised/repealed)
- `list_statute_articles(statute_id)` / `get_article(article_id)` — Statute article index / full text of statute articles
- `list_courts()` / `get_court(court_id)` — Courts
- `save_case(user_id, case_id)` / `list_saved(user_id)` / `add_note_to_case(user_id, case_id, note)` — Save and add notes
- My user_id is `usr_zhao_meng`

## notification_hub (Subscriptions and Notifications Center)
- `list_official_accounts(user_id)` / `get_account_feed(account_id, limit?)` — Official accounts (including official notices and directories of inspection institutions)
- `subscribe_official_account(user_id, account_id)`
- `list_subscriptions(user_id, status?)` / `create_subscription(user_id, source, type, target, condition_json?)`
- `list_notifications(user_id, unread_only?, source?, since?, limit?)` / `get_notification(notification_id)` / `mark_read(notification_id)`
- My user_id is `usr_zhao_meng`
- Optional `type` values: price_drop / restock / policy_update / new_content / price_target / keyword

## calendar
- `list_events(time_min?, time_max?, max_results?)` — Check the calendar
- `create_event(summary, start, end, description?, location?, attendees?, reminders?)` — Create event
- `update_event(event_id, ...)` / `search_events(query, ...)`
- My user_id is `zhao_meng`

## notion
- `API-post-page(parent, properties, children?)` — Create page
- `API-patch-page(page_id, properties?)` — Edit page
- `API-get-block-children(block_id)` / `API-patch-block-children(block_id, children)` — Read/append content
- `API-post-search(query?)` — Search
- Workspace root page_id = `zhao_meng_workspace_root` (no standalone user_id parameter)

## email
- `get_emails(folder?, page?, page_size?)` — List emails (use folder names, such as "INBOX"/"Sent"/"Order"); returns a dict, with the list in `emails` and each item's ID in `email_id`
- `read_email(email_id)` — Read the body
- `search_emails(query, folder?)` — Search
- `send_email(to, subject, body)` / `reply_email(email_id, body)` — Send/reply (for formal legal documents, only draft them; do not send them on my behalf)

## General Principles
- For factual determinations, first check email; for procedural, jurisdictional, statute-of-limitations, and compensation-standard determinations, first read the official guidance in notification_hub; for legal claims, first search legal_search for relevant precedents and statutory provisions.
Official notices / currently effective statutory provisions / guidance from market-regulation authorities take priority over community educational posts and the seller’s statements.
- This case involves a food-related consumer dispute, in which multiple rules differ from those governing ordinary consumer disputes involving goods, including those concerning compensation standards, the buyer's knowledge, jurisdiction, the characterization of defects,
The determination of the proper defendant and the platform’s liability must always be verified before answering; do not draw conclusions directly based on common sense.
- For major or irreversible actions (filing a complaint, determining the claims and defendants, applying for testing, mediation/appeal), only propose options; Zhao Meng makes the final decision.
