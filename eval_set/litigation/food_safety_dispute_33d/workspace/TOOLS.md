# MCP 工具速查表

## legal_search（法律检索库：判例 + 法条 + 援引）
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?)` — 搜判例；
  本案 case_type 主要为 **合同纠纷**（网络购物合同纠纷），少量 侵权责任（平台连带）
- `get_case(case_id)` — 判决全文（当事人/案由/事实/裁判理由/裁判要旨/判决主文/结果/关键词）
- `get_similar_cases(case_id, limit?)` — 同类判例（按关键词重合度排序）
- `get_case_citations(case_id)` — 该案援引的法条(statutes_cited)与案例(cases_cited)
- `search_statutes(keyword?, limit?)` / `get_statute(statute_id)` — 法律法规（含 status：现行有效/已修订/已废止）
- `list_statute_articles(statute_id)` / `get_article(article_id)` — 法条目录 / 法条全文
- `list_courts()` / `get_court(court_id)` — 法院
- `save_case(user_id, case_id)` / `list_saved(user_id)` / `add_note_to_case(user_id, case_id, note)` — 收藏与备注
- 我的 user_id 是 `usr_zhao_meng`

## notification_hub（订阅与通知中心）
- `list_official_accounts(user_id)` / `get_account_feed(account_id, limit?)` — 公众号（含官方须知、检验机构名录）
- `subscribe_official_account(user_id, account_id)`
- `list_subscriptions(user_id, status?)` / `create_subscription(user_id, source, type, target, condition_json?)`
- `list_notifications(user_id, unread_only?, source?, since?, limit?)` / `get_notification(notification_id)` / `mark_read(notification_id)`
- 我的 user_id 是 `usr_zhao_meng`
- type 可选: price_drop / restock / policy_update / new_content / price_target / keyword

## calendar
- `list_events(time_min?, time_max?, max_results?)` — 查日程
- `create_event(summary, start, end, description?, location?, attendees?, reminders?)` — 建事件
- `update_event(event_id, ...)` / `search_events(query, ...)`
- 我的 user_id 是 `zhao_meng`

## notion
- `API-post-page(parent, properties, children?)` — 建页面
- `API-patch-page(page_id, properties?)` — 改页面
- `API-get-block-children(block_id)` / `API-patch-block-children(block_id, children)` — 读/追加内容
- `API-post-search(query?)` — 搜索
- 工作区 root page_id = `zhao_meng_workspace_root`（无独立 user_id 参数）

## email
- `get_emails(folder?, page?, page_size?)` — 列邮件（folder 用名字，如 "INBOX"/"Sent"/"Order"）；返回 dict，列表在 `emails`，项 id 为 `email_id`
- `read_email(email_id)` — 读正文
- `search_emails(query, folder?)` — 搜
- `send_email(to, subject, body)` / `reply_email(email_id, body)` — 发/回（正式法律文书只起草草稿，不替我发送）

## 通用原则
- 做事实判断先查 email、做程序/管辖/时效/赔偿标准判断先读 notification_hub 官方须知、做法律主张先查 legal_search 判例与法条；
  官方须知 / 现行有效法条 / 市监口径优先于社区科普贴与卖家说法。
- 本案为食品类消费纠纷，多处规则与普通商品消费纠纷不同，凡涉及赔偿标准、买受人知情、管辖、缺陷定性、
  被告主体与平台责任的判断，一律先查证再作答，不得凭常识直接下结论。
- 重大或不可逆动作（递交诉状、定诉求与被告、申请检验、调解/上诉）只提方案，由赵萌拍板。
