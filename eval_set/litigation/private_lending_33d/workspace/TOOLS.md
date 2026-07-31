# MCP 工具速查表

## legal_search（法律检索库：判例 + 法条 + 援引）
- `search_cases(keyword?, court?, case_type?, date_from?, date_to?, limit?)` — 搜判例；
  case_type ∈ 劳动争议/合同纠纷/侵权责任/婚姻家庭/劳动仲裁/其他（民间借贷属"合同纠纷"）
- `get_case(case_id)` — 判决全文（当事人/案由/事实/裁判理由/裁判要旨/判决主文/结果/关键词）
- `get_similar_cases(case_id, limit?)` — 同类判例（按关键词重合度排序）
- `get_case_citations(case_id)` — 该案援引的法条(statutes_cited)与案例(cases_cited)
- `search_statutes(keyword?, limit?)` / `get_statute(statute_id)` — 法律法规（含 status：现行有效/已修订/已废止）
- `list_statute_articles(statute_id)` / `get_article(article_id)` — 法条目录 / 法条全文
- `list_courts()` / `get_court(court_id)` — 法院
- `save_case(user_id, case_id)` / `list_saved(user_id)` / `add_note_to_case(user_id, case_id, note)` — 收藏与备注
- 我的 user_id 是 `usr_wang_fang`

## notification_hub（订阅与通知中心）
- `list_official_accounts(user_id)` / `get_account_feed(account_id, limit?)` — 公众号（含官方须知 + 律师名录）
- `subscribe_official_account(user_id, account_id)`
- `list_subscriptions(user_id, status?)` / `create_subscription(user_id, source, type, target, condition_json?)`
- `list_notifications(user_id, unread_only?, source?, since?, limit?)` / `get_notification(notification_id)` / `mark_read(notification_id)`
- 我的 user_id 是 `usr_wang_fang`
- type 可选: price_drop / restock / policy_update / new_content / price_target / keyword

## calendar
- `list_events(time_min?, time_max?, max_results?)` — 查日程
- `create_event(summary, start, end, description?, location?, attendees?, reminders?)` — 建事件
- `update_event(event_id, ...)` / `search_events(query, ...)`
- 我的 user_id 是 `wang_fang`

## notion
- `API-post-page(parent, properties, children?)` — 建页面
- `API-patch-page(page_id, properties?)` — 改页面
- `API-get-block-children(block_id)` / `API-patch-block-children(block_id, children)` — 读/追加内容
- `API-post-search(query?)` — 搜索
- 工作区 root page_id = `wang_fang_workspace_root`（无独立 user_id 参数）

## email
- `get_emails(folder?, page?, page_size?)` — 列邮件（folder 用名字，如 "INBOX"/"Sent"/"Lending"）；返回 dict，列表在 `emails`，项 id 为 `email_id`
- `read_email(email_id)` — 读正文
- `search_emails(query, folder?)` — 搜
- `send_email(to, subject, body)` / `reply_email(email_id, body)` — 发/回（正式法律文书只起草草稿，不替我发送）

## 通用原则
- 做程序/管辖/时效/利率/担保判断前，先查官方须知 + 现行有效法条 + 同类判例，逐项核对再下结论
- 引用判例锚定 case_id、引用法条锚定 article_no/条号，金额计算写清"借条金额 vs 实际到账"
- 对证据薄弱处（无凭证现金交付）如实提示风险；不可逆动作只提方案，由王芳决定
