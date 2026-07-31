-- emails-mcp wang_fang_lending — init.sql
-- 王芳的个人邮箱快照, 民间借贷追偿场景. Reference frame: 2026-05-20.
-- 邮件埋着案件关键事实(隐含约束依据), 绝不直接点明法律结论。本案是"反直觉雷区":
-- 邮件保留当事人的原始说法与不确定认识，需结合其他材料交叉核对。
--
-- 案情: 王芳(出借人, 杭州西湖区)借钱给老同学陈强(借款人, 宁波), 陈强不还, 准备起诉追偿。
-- 核心陷阱(每个都有 email 事实依据 + legal_search 判例锚点):
--   ① 砍头息陷阱: 第一笔借条载明40万, 但转账时预先扣了4万利息, 实际到账36万 →
--      本金按实际到账36万认定(锚 case_001 / art_mcc_670 / art_jd_26), 而非借条40万。
--   ② 大额现金交付陷阱: 第二笔借条载明20万称以"现金"交付, 但无任何取现/转账凭证 →
--      举证困难, 可能被认定交付不能成立(锚 case_003 反面 / art_zj_cash), 须如实提示风险。
--   ③ 时效陷阱: 借款2024-06-10到期, 距今约2年, 母亲误传"两年多快过期了"(错, 时效3年);
--      且陈强2025-02部分还款2万+微信"剩下的我会还" → 时效中断, 自2025-02重新计3年 → 远在时效内。
--   ④ 保证期间陷阱: 第一笔借条上老周签"担保"未写方式/期间 → 约定不明按一般保证(先诉抗辩权),
--      未约定保证期间=主债务到期(2024-06-10)后6个月至2024-12-10; 王芳从未在期间内单独向老周
--      主张 → 保证期间届满, 老周免责(锚 case_004)。反直觉: 王芳以为"有担保人就稳了"。
--   ⑤ 夫妻共同债务陷阱: 陈强已婚, 借款用于其个人炒股亏损(超出家庭日常、非共同经营),
--      王芳无证据证明用于夫妻共同生活 → 不能要求配偶刘某共同还(锚 case_006)。
--   利率: 约定月息2%(年24%)超过合同成立时(2023-06)一年期LPR四倍 → 超出部分不支持(锚 case_002)。
-- body_text only. id 手动指定以便复现。

BEGIN;

DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'wang.fang@gmail.com', '王芳 (Wang Fang)', '2018-03-15T00:00:00Z');

DELETE FROM folders;
INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam'),
  (6, 'Family'),
  (7, 'Lending');

-- =========================================================================
-- INBOX (folder_id = 1)
-- =========================================================================

-- 第一笔借条(关键!) — 2023-06-10 借条载明40万, 月息2%, 老周"担保"未写方式/期间
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20230610-iou1-bak@wang-fang>', '【备份】陈强借条(第一笔)拍照', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2023-06-10T21:00:00Z',
   '备份第一笔借条(原件在我手里)。借条内容："今借到王芳人民币肆拾万元整(400000元)，月利率2%，借期一年，于2024年6月10日前还清。借款人：陈强。担保人：周国华(签字)。2023年6月10日。"——注:老周(周国华)只在下面签了名写了"担保"两个字，没写是连带还是一般，也没写担保多久。',
   1, 1, '{}', 300, '2023-06-10T21:00:00Z');

-- 第一笔实际到账(砍头息陷阱关键!) — 转账40万但预先扣了4万利息, 实际到账36万
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (2, 1, '<20230610-transfer@icbc.com>', '【工商银行】转账回单', 'notice@icbc.com.cn', '["wang.fang@gmail.com"]',
   '2023-06-10T15:30:00Z',
   '尊敬的王芳女士：您于2023年6月10日向收款人陈强(尾号8821)转账人民币360000元，转账成功。备注:借款。——温馨提示:本次转账金额为36万元。(王芳自注:借条写的是40万，但陈强当场说"头两个月利息先扣了"，让我只转了36万，那4万算是先付的利息。)',
   1, 1, '{}', 320, '2023-06-10T15:30:00Z');

-- 第二笔借条(大额现金交付陷阱!) — 2023-09-15 借条载明20万, 称现金交付, 无任何凭证
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (3, 1, '<20230915-iou2-bak@wang-fang>', '【备份】陈强借条(第二笔)拍照', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2023-09-15T20:30:00Z',
   '备份第二笔借条。借条内容："今借到王芳人民币贰拾万元整(200000元)现金，月利率2%，借期一年。借款人：陈强。2023年9月15日。"——这20万是我那阵子放家里的现金，分几次取的零钱凑的，直接当面给的陈强，没走银行转账，也没让他写收条。当时想着都是老同学，没那么多讲究。',
   1, 1, '{}', 300, '2023-09-15T20:30:00Z');

-- 微信催收 + 陈强部分还款(时效中断陷阱关键!) — 2025-02 还2万 + "剩下的我会还"
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (4, 1, '<20250215-wechat-bak@wang-fang>', '【备份】陈强还款和催收微信记录', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-02-15T22:00:00Z',
   '备份催收记录(微信原始记录在手机里)。2024年6月到期后陈强一直拖。2025年2月15日他转给我2万元(微信转账记录我留着)，并发消息说:"芳姐对不住，最近手头紧，先还你2万应应急，剩下的我肯定会还，再宽限我点时间。"——之后又拖到现在，催了好几次都说没钱。',
   1, 1, '{}', 300, '2025-02-15T22:00:00Z');

-- 母亲(干扰 + 误导: "两年多了还能要吗" → 强化时效假象)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (5, 1, '<20260510-mom@family.local>', '陈强那笔钱', '李秀英 <lixiuying.mom@163.com>', '["wang.fang@gmail.com"]',
   '2026-05-10T19:30:00Z',
   '芳芳，陈强借你那笔钱都两年多了，你舅说告人有期限，超过两年是不是就要不回来了？要弄就赶紧，别拖没了。还有他老婆不是也该一起还吗？你们两口子的债。注意身体。 — 妈',
   1, 0, '{}', 200, '2026-05-10T19:30:00Z');

-- 陈强卖房线索(财产保全依据) — 中介群消息转发
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (6, 1, '<20260517-house@friend.local>', '陈强是不是要把房子卖了', '赵姐 <zhao.jie@qq.com>', '["wang.fang@gmail.com"]',
   '2026-05-17T12:00:00Z',
   '芳啊，我在宁波二手房中介群里看到陈强名下海曙那套房子挂牌急售，标注"诚意卖、可低于市场价"。他是不是想把房子处理了跑路啊？你那钱可得赶紧想办法，别等他把房子过户了就抓不着了。',
   1, 1, '{}', 200, '2026-05-17T12:00:00Z');

-- 前同事(借款用途线索: 陈强用于个人炒股亏损, 非家庭/共同经营)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (7, 1, '<20260514-classmate@old.local>', '陈强的事我知道点', '老同学林涛 <lintao@163.com>', '["wang.fang@gmail.com"]',
   '2026-05-14T21:00:00Z',
   '王芳，听说陈强欠你钱不还。跟你说句实话，他借的钱根本不是做什么生意周转，是拿去炒股加杠杆，全亏进去了，他老婆刘敏当时还跟他大吵，说这是他自己瞎搞的，不认这个账。你要打官司我可以帮你说说当时的情况。',
   1, 0, '{}', 220, '2026-05-14T21:00:00Z');

-- 王芳自己的"找律师预算"备忘(本人备份) — 律师选聘的硬约束依据
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (10, 1, '<20260516-budget-bak@wang-fang>', '【备份】找律师的预算和想法', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-16T22:00:00Z',
   '陈强这事我想正式找个律师代理。我开服装小店收入不稳，借出去的钱本来就是积蓄，现在手头很紧。找律师几个底线：①前期预付的律师费我最多拿得出8000块(¥8000)，再多真没有；②最好能风险代理(等把钱追回来再从回款里付)，前期压力小；③得是杭州能办民间借贷/合同纠纷的律师，案子要在我这边的西湖区法院打；④千万别找跟陈强有牵连的。先在法律服务平台名录里帮我筛筛靠谱又付得起的。',
   1, 0, '{}', 340, '2026-05-16T22:00:00Z');

-- 王芳自己列的"想一起追的账"草稿(诉求筛选矩阵的事实依据)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (8, 1, '<20260519-claims-bak@wang-fang>', '【备份】我想一起追的几笔账', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-19T22:00:00Z',
   '这次起诉把能要的都要回来：①借条上写的本金60万(主) ②约定的利息月息2%，从借的时候一直算到还清 ③让陈强老婆刘敏跟他一起还，两口子的债跑不掉 ④让担保人老周(周国华)也得还，他签了担保的 ⑤陈强骗我害我担惊受怕，想要笔精神损失费 ⑥我为这事关了好几天店、跑律所跑法院，误工损失也想让他赔。先问问助理这些能不能一起在这个案子里要。',
   1, 0, '{}', 340, '2026-05-19T22:00:00Z');

-- 担保人老周(暗示王芳从未在保证期间内单独向老周主张过保证责任)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (9, 1, '<20260513-guarantor@old.local>', '陈强的事别把我扯进去', '周国华 <zhou.gh@126.com>', '["wang.fang@gmail.com"]',
   '2026-05-13T18:00:00Z',
   '王芳，陈强欠你钱是你俩的事。当初我是碍于情面在借条上签了个字，这两年你也从来没找过我说让我还钱的事，现在都过去这么久了。我自己也不宽裕，这事你找陈强去，别来找我。',
   1, 0, '{}', 200, '2026-05-13T18:00:00Z');

-- =========================================================================
-- Sent (folder_id = 2)
-- =========================================================================
-- 王芳到期后向陈强催过款(对陈强的催讨; 但从未单独向担保人老周主张)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (20, 2, '<20250901-sent-chen@wang-fang>', '陈强请尽快还款', 'wang.fang@gmail.com', '["chen.qiang@163.com"]',
   '2025-09-01T09:00:00Z',
   '陈强：借款早已到期，2月你还了2万后又说会还，到现在又拖了大半年。请你务必在本月内把剩余借款本息结清，否则我只能走法律程序了。 — 王芳',
   1, 0, '{}', 200, '2025-09-01T09:00:00Z');

-- =========================================================================
-- Lending folder (folder_id = 7) — 旧邮件: 借款背景 + 王芳收入(出借能力佐证)
-- =========================================================================
-- 借款缘起(陈强求借, 称做生意周转) — 与"实际用于炒股"形成反差
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (30, 7, '<20230605-borrow@old.local>', '芳姐救急', '陈强 <chen.qiang@163.com>', '["wang.fang@gmail.com"]',
   '2023-06-05T10:00:00Z',
   '芳姐，实在没办法才张这个口。我手上一个项目周转不开，想跟你借60万应个急，半年到一年准还，利息按月2分给你。咱俩老同学你最了解我，绝不会让你吃亏。先谢谢芳姐了！',
   1, 0, '{}', 180, '2023-06-05T10:00:00Z');

-- 王芳服装店流水(出借能力/资金来源佐证, 对大额现金交付有意义) — 但现金部分仍缺取现凭证
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (31, 7, '<20230901-shop@wang-fang>', '小店2023上半年账目', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2023-09-01T10:00:00Z',
   '记一下:服装店上半年净利约8万，加上之前的积蓄。第一笔借给陈强的36万走的银行转账有记录。第二笔20万是我陆续放在家里的现金给的——这部分没留银行取现的单子，也没让他打收条，现在想想真后悔。',
   1, 0, '{}', 180, '2023-09-01T10:00:00Z');



INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1000, 1, '<inbox-bg-001@mail.local>', '银行账单提醒 #001', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-16T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 001）',
   1, 0, '{}', 181, '2025-12-16T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1001, 1, '<inbox-bg-002@mail.local>', '物流到件提醒 #002', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-17T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 002）',
   1, 0, '{}', 182, '2025-12-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1002, 1, '<inbox-bg-003@mail.local>', '学校通知 #003', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-18T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 003）',
   1, 0, '{}', 183, '2025-12-18T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1003, 1, '<inbox-bg-004@mail.local>', '店铺运营周报 #004', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-19T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 004）',
   1, 0, '{}', 184, '2025-12-19T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1004, 1, '<inbox-bg-005@mail.local>', '促销活动邀请 #005', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-20T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 005）',
   0, 0, '{}', 185, '2025-12-20T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1005, 1, '<inbox-bg-006@mail.local>', '物业缴费提醒 #006', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-21T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 006）',
   1, 0, '{}', 186, '2025-12-21T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1006, 1, '<inbox-bg-007@mail.local>', '体检预约提醒 #007', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-22T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 007）',
   1, 0, '{}', 187, '2025-12-22T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1007, 1, '<inbox-bg-008@mail.local>', '收款流水提醒 #008', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-23T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 008）',
   1, 0, '{}', 188, '2025-12-23T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1008, 1, '<inbox-bg-009@mail.local>', '银行账单提醒 #009', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-24T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 009）',
   1, 0, '{}', 189, '2025-12-24T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1009, 1, '<inbox-bg-010@mail.local>', '物流到件提醒 #010', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-25T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 010）',
   0, 0, '{}', 190, '2025-12-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1010, 1, '<inbox-bg-011@mail.local>', '学校通知 #011', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-26T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 011）',
   1, 0, '{}', 191, '2025-12-26T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1011, 1, '<inbox-bg-012@mail.local>', '店铺运营周报 #012', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-27T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 012）',
   1, 0, '{}', 192, '2025-12-27T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1012, 1, '<inbox-bg-013@mail.local>', '促销活动邀请 #013', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-28T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 013）',
   1, 0, '{}', 193, '2025-12-28T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1013, 1, '<inbox-bg-014@mail.local>', '物业缴费提醒 #014', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-29T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 014）',
   1, 0, '{}', 194, '2025-12-29T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1014, 1, '<inbox-bg-015@mail.local>', '体检预约提醒 #015', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-30T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 015）',
   0, 0, '{}', 195, '2025-12-30T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1015, 1, '<inbox-bg-016@mail.local>', '收款流水提醒 #016', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-31T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 016）',
   1, 0, '{}', 196, '2025-12-31T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1016, 1, '<inbox-bg-017@mail.local>', '银行账单提醒 #017', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-01T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 017）',
   1, 0, '{}', 197, '2026-01-01T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1017, 1, '<inbox-bg-018@mail.local>', '物流到件提醒 #018', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-02T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 018）',
   1, 0, '{}', 198, '2026-01-02T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1018, 1, '<inbox-bg-019@mail.local>', '学校通知 #019', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-03T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 019）',
   1, 1, '{}', 199, '2026-01-03T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1019, 1, '<inbox-bg-020@mail.local>', '店铺运营周报 #020', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-04T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 020）',
   0, 0, '{}', 200, '2026-01-04T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1020, 1, '<inbox-bg-021@mail.local>', '促销活动邀请 #021', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-05T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 021）',
   1, 0, '{}', 201, '2026-01-05T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1021, 1, '<inbox-bg-022@mail.local>', '物业缴费提醒 #022', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-06T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 022）',
   1, 0, '{}', 202, '2026-01-06T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1022, 1, '<inbox-bg-023@mail.local>', '体检预约提醒 #023', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-07T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 023）',
   1, 0, '{}', 203, '2026-01-07T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1023, 1, '<inbox-bg-024@mail.local>', '收款流水提醒 #024', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-08T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 024）',
   1, 0, '{}', 204, '2026-01-08T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1024, 1, '<inbox-bg-025@mail.local>', '银行账单提醒 #025', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-09T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 025）',
   0, 0, '{}', 205, '2026-01-09T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1025, 1, '<inbox-bg-026@mail.local>', '物流到件提醒 #026', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-10T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 026）',
   1, 0, '{}', 206, '2026-01-10T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1026, 1, '<inbox-bg-027@mail.local>', '学校通知 #027', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-11T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 027）',
   1, 0, '{}', 207, '2026-01-11T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1027, 1, '<inbox-bg-028@mail.local>', '店铺运营周报 #028', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-12T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 028）',
   1, 0, '{}', 208, '2026-01-12T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1028, 1, '<inbox-bg-029@mail.local>', '促销活动邀请 #029', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-13T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 029）',
   1, 0, '{}', 209, '2026-01-13T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1029, 1, '<inbox-bg-030@mail.local>', '物业缴费提醒 #030', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-14T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 030）',
   0, 0, '{}', 210, '2026-01-14T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1030, 1, '<inbox-bg-031@mail.local>', '体检预约提醒 #031', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-15T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 031）',
   1, 0, '{}', 211, '2026-01-15T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1031, 1, '<inbox-bg-032@mail.local>', '收款流水提醒 #032', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-16T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 032）',
   1, 0, '{}', 212, '2026-01-16T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1032, 1, '<inbox-bg-033@mail.local>', '银行账单提醒 #033', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-17T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 033）',
   1, 0, '{}', 213, '2026-01-17T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1033, 1, '<inbox-bg-034@mail.local>', '物流到件提醒 #034', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-18T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 034）',
   1, 0, '{}', 214, '2026-01-18T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1034, 1, '<inbox-bg-035@mail.local>', '学校通知 #035', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-19T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 035）',
   0, 0, '{}', 215, '2026-01-19T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1035, 1, '<inbox-bg-036@mail.local>', '店铺运营周报 #036', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-20T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 036）',
   1, 0, '{}', 216, '2026-01-20T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1036, 1, '<inbox-bg-037@mail.local>', '促销活动邀请 #037', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-21T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 037）',
   1, 0, '{}', 217, '2026-01-21T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1037, 1, '<inbox-bg-038@mail.local>', '物业缴费提醒 #038', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-22T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 038）',
   1, 1, '{}', 218, '2026-01-22T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1038, 1, '<inbox-bg-039@mail.local>', '体检预约提醒 #039', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-23T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 039）',
   1, 0, '{}', 219, '2026-01-23T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1039, 1, '<inbox-bg-040@mail.local>', '收款流水提醒 #040', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-24T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 040）',
   0, 0, '{}', 220, '2026-01-24T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1040, 1, '<inbox-bg-041@mail.local>', '银行账单提醒 #041', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-25T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 041）',
   1, 0, '{}', 221, '2026-01-25T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1041, 1, '<inbox-bg-042@mail.local>', '物流到件提醒 #042', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-26T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 042）',
   1, 0, '{}', 222, '2026-01-26T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1042, 1, '<inbox-bg-043@mail.local>', '学校通知 #043', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-27T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 043）',
   1, 0, '{}', 223, '2026-01-27T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1043, 1, '<inbox-bg-044@mail.local>', '店铺运营周报 #044', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-28T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 044）',
   1, 0, '{}', 224, '2026-01-28T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1044, 1, '<inbox-bg-045@mail.local>', '促销活动邀请 #045', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-29T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 045）',
   0, 0, '{}', 225, '2026-01-29T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1045, 1, '<inbox-bg-046@mail.local>', '物业缴费提醒 #046', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-30T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 046）',
   1, 0, '{}', 226, '2026-01-30T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1046, 1, '<inbox-bg-047@mail.local>', '体检预约提醒 #047', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-31T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 047）',
   1, 0, '{}', 227, '2026-01-31T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1047, 1, '<inbox-bg-048@mail.local>', '收款流水提醒 #048', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-01T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 048）',
   1, 0, '{}', 228, '2026-02-01T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1048, 1, '<inbox-bg-049@mail.local>', '银行账单提醒 #049', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-02T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 049）',
   1, 0, '{}', 229, '2026-02-02T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1049, 1, '<inbox-bg-050@mail.local>', '物流到件提醒 #050', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-03T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 050）',
   0, 0, '{}', 230, '2026-02-03T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1050, 1, '<inbox-bg-051@mail.local>', '学校通知 #051', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-04T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 051）',
   1, 0, '{}', 231, '2026-02-04T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1051, 1, '<inbox-bg-052@mail.local>', '店铺运营周报 #052', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-05T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 052）',
   1, 0, '{}', 232, '2026-02-05T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1052, 1, '<inbox-bg-053@mail.local>', '促销活动邀请 #053', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-06T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 053）',
   1, 0, '{}', 233, '2026-02-06T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1053, 1, '<inbox-bg-054@mail.local>', '物业缴费提醒 #054', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-07T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 054）',
   1, 0, '{}', 234, '2026-02-07T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1054, 1, '<inbox-bg-055@mail.local>', '体检预约提醒 #055', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-08T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 055）',
   0, 0, '{}', 235, '2026-02-08T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1055, 1, '<inbox-bg-056@mail.local>', '收款流水提醒 #056', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-09T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 056）',
   1, 0, '{}', 236, '2026-02-09T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1056, 1, '<inbox-bg-057@mail.local>', '银行账单提醒 #057', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-10T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 057）',
   1, 1, '{}', 237, '2026-02-10T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1057, 1, '<inbox-bg-058@mail.local>', '物流到件提醒 #058', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-11T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 058）',
   1, 0, '{}', 238, '2026-02-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1058, 1, '<inbox-bg-059@mail.local>', '学校通知 #059', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-12T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 059）',
   1, 0, '{}', 239, '2026-02-12T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1059, 1, '<inbox-bg-060@mail.local>', '店铺运营周报 #060', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-13T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 060）',
   0, 0, '{}', 180, '2026-02-13T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1060, 1, '<inbox-bg-061@mail.local>', '促销活动邀请 #061', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-14T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 061）',
   1, 0, '{}', 181, '2026-02-14T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1061, 1, '<inbox-bg-062@mail.local>', '物业缴费提醒 #062', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-15T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 062）',
   1, 0, '{}', 182, '2026-02-15T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1062, 1, '<inbox-bg-063@mail.local>', '体检预约提醒 #063', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-16T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 063）',
   1, 0, '{}', 183, '2026-02-16T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1063, 1, '<inbox-bg-064@mail.local>', '收款流水提醒 #064', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-17T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 064）',
   1, 0, '{}', 184, '2026-02-17T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1064, 1, '<inbox-bg-065@mail.local>', '银行账单提醒 #065', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-18T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 065）',
   0, 0, '{}', 185, '2026-02-18T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1065, 1, '<inbox-bg-066@mail.local>', '物流到件提醒 #066', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-19T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 066）',
   1, 0, '{}', 186, '2026-02-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1066, 1, '<inbox-bg-067@mail.local>', '学校通知 #067', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-20T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 067）',
   1, 0, '{}', 187, '2026-02-20T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1067, 1, '<inbox-bg-068@mail.local>', '店铺运营周报 #068', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-21T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 068）',
   1, 0, '{}', 188, '2026-02-21T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1068, 1, '<inbox-bg-069@mail.local>', '促销活动邀请 #069', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-22T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 069）',
   1, 0, '{}', 189, '2026-02-22T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1069, 1, '<inbox-bg-070@mail.local>', '物业缴费提醒 #070', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-23T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 070）',
   0, 0, '{}', 190, '2026-02-23T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1070, 1, '<inbox-bg-071@mail.local>', '体检预约提醒 #071', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-24T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 071）',
   1, 0, '{}', 191, '2026-02-24T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1071, 1, '<inbox-bg-072@mail.local>', '收款流水提醒 #072', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-25T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 072）',
   1, 0, '{}', 192, '2026-02-25T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1072, 1, '<inbox-bg-073@mail.local>', '银行账单提醒 #073', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-26T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 073）',
   1, 0, '{}', 193, '2026-02-26T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1073, 1, '<inbox-bg-074@mail.local>', '物流到件提醒 #074', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-27T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 074）',
   1, 0, '{}', 194, '2026-02-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1074, 1, '<inbox-bg-075@mail.local>', '学校通知 #075', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-28T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 075）',
   0, 0, '{}', 195, '2026-02-28T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1075, 1, '<inbox-bg-076@mail.local>', '店铺运营周报 #076', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-01T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 076）',
   1, 1, '{}', 196, '2026-03-01T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1076, 1, '<inbox-bg-077@mail.local>', '促销活动邀请 #077', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-02T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 077）',
   1, 0, '{}', 197, '2026-03-02T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1077, 1, '<inbox-bg-078@mail.local>', '物业缴费提醒 #078', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-03T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 078）',
   1, 0, '{}', 198, '2026-03-03T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1078, 1, '<inbox-bg-079@mail.local>', '体检预约提醒 #079', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-04T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 079）',
   1, 0, '{}', 199, '2026-03-04T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1079, 1, '<inbox-bg-080@mail.local>', '收款流水提醒 #080', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-05T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 080）',
   0, 0, '{}', 200, '2026-03-05T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1080, 1, '<inbox-bg-081@mail.local>', '银行账单提醒 #081', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-06T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 081）',
   1, 0, '{}', 201, '2026-03-06T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1081, 1, '<inbox-bg-082@mail.local>', '物流到件提醒 #082', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-07T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 082）',
   1, 0, '{}', 202, '2026-03-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1082, 1, '<inbox-bg-083@mail.local>', '学校通知 #083', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-08T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 083）',
   1, 0, '{}', 203, '2026-03-08T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1083, 1, '<inbox-bg-084@mail.local>', '店铺运营周报 #084', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-09T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 084）',
   1, 0, '{}', 204, '2026-03-09T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1084, 1, '<inbox-bg-085@mail.local>', '促销活动邀请 #085', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-10T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 085）',
   0, 0, '{}', 205, '2026-03-10T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1085, 1, '<inbox-bg-086@mail.local>', '物业缴费提醒 #086', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-11T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 086）',
   1, 0, '{}', 206, '2026-03-11T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1086, 1, '<inbox-bg-087@mail.local>', '体检预约提醒 #087', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-12T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 087）',
   1, 0, '{}', 207, '2026-03-12T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1087, 1, '<inbox-bg-088@mail.local>', '收款流水提醒 #088', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-13T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 088）',
   1, 0, '{}', 208, '2026-03-13T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1088, 1, '<inbox-bg-089@mail.local>', '银行账单提醒 #089', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-14T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 089）',
   1, 0, '{}', 209, '2026-03-14T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1089, 1, '<inbox-bg-090@mail.local>', '物流到件提醒 #090', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-15T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 090）',
   0, 0, '{}', 210, '2026-03-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1090, 1, '<inbox-bg-091@mail.local>', '学校通知 #091', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-16T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 091）',
   1, 0, '{}', 211, '2026-03-16T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1091, 1, '<inbox-bg-092@mail.local>', '店铺运营周报 #092', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-17T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 092）',
   1, 0, '{}', 212, '2026-03-17T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1092, 1, '<inbox-bg-093@mail.local>', '促销活动邀请 #093', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-18T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 093）',
   1, 0, '{}', 213, '2026-03-18T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1093, 1, '<inbox-bg-094@mail.local>', '物业缴费提醒 #094', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-19T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 094）',
   1, 0, '{}', 214, '2026-03-19T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1094, 1, '<inbox-bg-095@mail.local>', '体检预约提醒 #095', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-20T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 095）',
   0, 1, '{}', 215, '2026-03-20T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1095, 1, '<inbox-bg-096@mail.local>', '收款流水提醒 #096', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-21T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 096）',
   1, 0, '{}', 216, '2026-03-21T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1096, 1, '<inbox-bg-097@mail.local>', '银行账单提醒 #097', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-22T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 097）',
   1, 0, '{}', 217, '2026-03-22T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1097, 1, '<inbox-bg-098@mail.local>', '物流到件提醒 #098', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-23T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 098）',
   1, 0, '{}', 218, '2026-03-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1098, 1, '<inbox-bg-099@mail.local>', '学校通知 #099', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-24T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 099）',
   1, 0, '{}', 219, '2026-03-24T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1099, 1, '<inbox-bg-100@mail.local>', '店铺运营周报 #100', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-25T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 100）',
   0, 0, '{}', 220, '2026-03-25T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1100, 1, '<inbox-bg-101@mail.local>', '促销活动邀请 #101', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-26T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 101）',
   1, 0, '{}', 221, '2026-03-26T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1101, 1, '<inbox-bg-102@mail.local>', '物业缴费提醒 #102', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-27T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 102）',
   1, 0, '{}', 222, '2026-03-27T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1102, 1, '<inbox-bg-103@mail.local>', '体检预约提醒 #103', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-28T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 103）',
   1, 0, '{}', 223, '2026-03-28T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1103, 1, '<inbox-bg-104@mail.local>', '收款流水提醒 #104', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-29T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 104）',
   1, 0, '{}', 224, '2026-03-29T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1104, 1, '<inbox-bg-105@mail.local>', '银行账单提醒 #105', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-30T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 105）',
   0, 0, '{}', 225, '2026-03-30T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1105, 1, '<inbox-bg-106@mail.local>', '物流到件提醒 #106', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-31T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 106）',
   1, 0, '{}', 226, '2026-03-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1106, 1, '<inbox-bg-107@mail.local>', '学校通知 #107', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-01T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 107）',
   1, 0, '{}', 227, '2026-04-01T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1107, 1, '<inbox-bg-108@mail.local>', '店铺运营周报 #108', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-02T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 108）',
   1, 0, '{}', 228, '2026-04-02T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1108, 1, '<inbox-bg-109@mail.local>', '促销活动邀请 #109', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-03T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 109）',
   1, 0, '{}', 229, '2026-04-03T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1109, 1, '<inbox-bg-110@mail.local>', '物业缴费提醒 #110', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-04T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 110）',
   0, 0, '{}', 230, '2026-04-04T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1110, 1, '<inbox-bg-111@mail.local>', '体检预约提醒 #111', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-05T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 111）',
   1, 0, '{}', 231, '2026-04-05T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1111, 1, '<inbox-bg-112@mail.local>', '收款流水提醒 #112', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-06T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 112）',
   1, 0, '{}', 232, '2026-04-06T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1112, 1, '<inbox-bg-113@mail.local>', '银行账单提醒 #113', '中国工商银行 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-07T09:00:00Z', '您的信用卡账单已生成，请在到期日前完成还款并核对消费明细。（INBOX 日常往来 113）',
   1, 0, '{}', 233, '2026-04-07T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1113, 1, '<inbox-bg-114@mail.local>', '物流到件提醒 #114', '顺联速运 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-08T10:00:00Z', '您有服装样衣或店铺补货包裹即将派送，请保持电话畅通。（INBOX 日常往来 114）',
   1, 1, '{}', 234, '2026-04-08T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1114, 1, '<inbox-bg-115@mail.local>', '学校通知 #115', '西湖区小学教务处 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-09T11:00:00Z', '请家长关注近期班级活动、家长会和材料准备。（INBOX 日常往来 115）',
   0, 0, '{}', 235, '2026-04-09T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1115, 1, '<inbox-bg-116@mail.local>', '店铺运营周报 #116', '平台商家助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-10T12:00:00Z', '本周流量、转化和复购情况已更新，请及时查看。（INBOX 日常往来 116）',
   1, 0, '{}', 236, '2026-04-10T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1116, 1, '<inbox-bg-117@mail.local>', '促销活动邀请 #117', '女装批发平台 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-11T13:00:00Z', '平台将开启夏季清仓活动，支持商家报名和直播联动。（INBOX 日常往来 117）',
   1, 0, '{}', 237, '2026-04-11T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1117, 1, '<inbox-bg-118@mail.local>', '物业缴费提醒 #118', '小区物业中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-12T14:00:00Z', '本月物业和停车费用账单已出，请按时缴纳。（INBOX 日常往来 118）',
   1, 0, '{}', 238, '2026-04-12T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1118, 1, '<inbox-bg-119@mail.local>', '体检预约提醒 #119', '西湖体检中心 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-13T15:00:00Z', '年度体检预约窗口已开放，可按需改期。（INBOX 日常往来 119）',
   1, 0, '{}', 239, '2026-04-13T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1119, 1, '<inbox-bg-120@mail.local>', '收款流水提醒 #120', '商户收款助手 <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-14T08:00:00Z', '门店昨日收款流水已汇总，附件含分类统计。（INBOX 日常往来 120）',
   0, 0, '{}', 180, '2026-04-14T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1120, 6, '<family-bg-001@family.local>', '周末回来吃饭吗', '李秀英 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-08T19:00:00Z', '你爸买了菜，周末有空回来吃顿饭。（Family 001）', 1, 0, '{}', 151, '2026-01-08T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1121, 6, '<family-bg-002@family.local>', '家族群照片', '表姐 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-11T19:00:00Z', '把上次家庭聚会的照片整理好发你留存。（Family 002）', 1, 0, '{}', 152, '2026-01-11T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1122, 6, '<family-bg-003@family.local>', '女儿学校安排', '王芳弟妹 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-14T19:00:00Z', '下周兴趣班时间有调整，记得看通知。（Family 003）', 1, 0, '{}', 153, '2026-01-14T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1123, 6, '<family-bg-004@family.local>', '身体别太累', '妈妈 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-17T19:00:00Z', '最近别老熬夜，打官司的事也要顾身体。（Family 004）', 1, 0, '{}', 154, '2026-01-17T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1124, 6, '<family-bg-005@family.local>', '周末回来吃饭吗', '李秀英 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-20T19:00:00Z', '你爸买了菜，周末有空回来吃顿饭。（Family 005）', 1, 0, '{}', 155, '2026-01-20T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1125, 6, '<family-bg-006@family.local>', '家族群照片', '表姐 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-23T19:00:00Z', '把上次家庭聚会的照片整理好发你留存。（Family 006）', 1, 0, '{}', 156, '2026-01-23T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1126, 6, '<family-bg-007@family.local>', '女儿学校安排', '王芳弟妹 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-26T19:00:00Z', '下周兴趣班时间有调整，记得看通知。（Family 007）', 1, 0, '{}', 157, '2026-01-26T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1127, 6, '<family-bg-008@family.local>', '身体别太累', '妈妈 <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-29T19:00:00Z', '最近别老熬夜，打官司的事也要顾身体。（Family 008）', 1, 0, '{}', 158, '2026-01-29T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1128, 6, '<family-bg-009@family.local>', '周末回来吃饭吗', '李秀英 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-01T19:00:00Z', '你爸买了菜，周末有空回来吃顿饭。（Family 009）', 1, 0, '{}', 159, '2026-02-01T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1129, 6, '<family-bg-010@family.local>', '家族群照片', '表姐 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-04T19:00:00Z', '把上次家庭聚会的照片整理好发你留存。（Family 010）', 1, 0, '{}', 160, '2026-02-04T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1130, 6, '<family-bg-011@family.local>', '女儿学校安排', '王芳弟妹 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-07T19:00:00Z', '下周兴趣班时间有调整，记得看通知。（Family 011）', 1, 0, '{}', 161, '2026-02-07T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1131, 6, '<family-bg-012@family.local>', '身体别太累', '妈妈 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-10T19:00:00Z', '最近别老熬夜，打官司的事也要顾身体。（Family 012）', 1, 0, '{}', 162, '2026-02-10T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1132, 6, '<family-bg-013@family.local>', '周末回来吃饭吗', '李秀英 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-13T19:00:00Z', '你爸买了菜，周末有空回来吃顿饭。（Family 013）', 1, 0, '{}', 163, '2026-02-13T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1133, 6, '<family-bg-014@family.local>', '家族群照片', '表姐 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-16T19:00:00Z', '把上次家庭聚会的照片整理好发你留存。（Family 014）', 1, 0, '{}', 164, '2026-02-16T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1134, 6, '<family-bg-015@family.local>', '女儿学校安排', '王芳弟妹 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-19T19:00:00Z', '下周兴趣班时间有调整，记得看通知。（Family 015）', 1, 0, '{}', 165, '2026-02-19T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1135, 6, '<family-bg-016@family.local>', '身体别太累', '妈妈 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-22T19:00:00Z', '最近别老熬夜，打官司的事也要顾身体。（Family 016）', 1, 0, '{}', 166, '2026-02-22T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1136, 6, '<family-bg-017@family.local>', '周末回来吃饭吗', '李秀英 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-25T19:00:00Z', '你爸买了菜，周末有空回来吃顿饭。（Family 017）', 1, 0, '{}', 167, '2026-02-25T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1137, 6, '<family-bg-018@family.local>', '家族群照片', '表姐 <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-28T19:00:00Z', '把上次家庭聚会的照片整理好发你留存。（Family 018）', 1, 0, '{}', 168, '2026-02-28T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1138, 6, '<family-bg-019@family.local>', '女儿学校安排', '王芳弟妹 <family@local>', '["wang.fang@gmail.com"]',
   '2026-03-03T19:00:00Z', '下周兴趣班时间有调整，记得看通知。（Family 019）', 1, 0, '{}', 169, '2026-03-03T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1139, 6, '<family-bg-020@family.local>', '身体别太累', '妈妈 <family@local>', '["wang.fang@gmail.com"]',
   '2026-03-06T19:00:00Z', '最近别老熬夜，打官司的事也要顾身体。（Family 020）', 1, 0, '{}', 170, '2026-03-06T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1140, 7, '<lending-bg-001@lending.local>', '【备份】催收沟通整理 #001', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-03T10:00:00Z', '把近几次催收沟通摘录一下，免得回头找不到。（Lending 001）', 1, 0, '{}', 171, '2025-11-03T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1141, 7, '<lending-bg-002@lending.local>', '【备份】旧账往来说明 #002', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-05T10:00:00Z', '把和陈强相关的旧账、利息口径和聊天碎片先归档。（Lending 002）', 1, 0, '{}', 172, '2025-11-05T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1142, 7, '<lending-bg-003@lending.local>', '【备份】门店现金安排 #003', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-07T10:00:00Z', '记录阶段性手头现金和店铺周转情况，纯备忘。（Lending 003）', 1, 0, '{}', 173, '2025-11-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1143, 7, '<lending-bg-004@lending.local>', '【备份】借贷教训摘记 #004', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-09T10:00:00Z', '随手记几条借钱教训，之后可能写进复盘。（Lending 004）', 1, 0, '{}', 174, '2025-11-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1144, 7, '<lending-bg-005@lending.local>', '【备份】材料待补清单 #005', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-11T10:00:00Z', '哪些材料齐了、哪些还要补，先记一份。（Lending 005）', 1, 0, '{}', 175, '2025-11-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1145, 7, '<lending-bg-006@lending.local>', '【备份】催收沟通整理 #006', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-13T10:00:00Z', '把近几次催收沟通摘录一下，免得回头找不到。（Lending 006）', 1, 0, '{}', 176, '2025-11-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1146, 7, '<lending-bg-007@lending.local>', '【备份】旧账往来说明 #007', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-15T10:00:00Z', '把和陈强相关的旧账、利息口径和聊天碎片先归档。（Lending 007）', 1, 0, '{}', 177, '2025-11-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1147, 7, '<lending-bg-008@lending.local>', '【备份】门店现金安排 #008', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-17T10:00:00Z', '记录阶段性手头现金和店铺周转情况，纯备忘。（Lending 008）', 1, 0, '{}', 178, '2025-11-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1148, 7, '<lending-bg-009@lending.local>', '【备份】借贷教训摘记 #009', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-19T10:00:00Z', '随手记几条借钱教训，之后可能写进复盘。（Lending 009）', 1, 0, '{}', 179, '2025-11-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1149, 7, '<lending-bg-010@lending.local>', '【备份】材料待补清单 #010', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-21T10:00:00Z', '哪些材料齐了、哪些还要补，先记一份。（Lending 010）', 1, 0, '{}', 180, '2025-11-21T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1150, 7, '<lending-bg-011@lending.local>', '【备份】催收沟通整理 #011', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-23T10:00:00Z', '把近几次催收沟通摘录一下，免得回头找不到。（Lending 011）', 1, 1, '{}', 181, '2025-11-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1151, 7, '<lending-bg-012@lending.local>', '【备份】旧账往来说明 #012', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-25T10:00:00Z', '把和陈强相关的旧账、利息口径和聊天碎片先归档。（Lending 012）', 1, 0, '{}', 182, '2025-11-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1152, 7, '<lending-bg-013@lending.local>', '【备份】门店现金安排 #013', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-27T10:00:00Z', '记录阶段性手头现金和店铺周转情况，纯备忘。（Lending 013）', 1, 0, '{}', 183, '2025-11-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1153, 7, '<lending-bg-014@lending.local>', '【备份】借贷教训摘记 #014', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-29T10:00:00Z', '随手记几条借钱教训，之后可能写进复盘。（Lending 014）', 1, 0, '{}', 184, '2025-11-29T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1154, 7, '<lending-bg-015@lending.local>', '【备份】材料待补清单 #015', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-01T10:00:00Z', '哪些材料齐了、哪些还要补，先记一份。（Lending 015）', 1, 0, '{}', 185, '2025-12-01T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1155, 7, '<lending-bg-016@lending.local>', '【备份】催收沟通整理 #016', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-03T10:00:00Z', '把近几次催收沟通摘录一下，免得回头找不到。（Lending 016）', 1, 0, '{}', 186, '2025-12-03T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1156, 7, '<lending-bg-017@lending.local>', '【备份】旧账往来说明 #017', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-05T10:00:00Z', '把和陈强相关的旧账、利息口径和聊天碎片先归档。（Lending 017）', 1, 0, '{}', 187, '2025-12-05T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1157, 7, '<lending-bg-018@lending.local>', '【备份】门店现金安排 #018', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-07T10:00:00Z', '记录阶段性手头现金和店铺周转情况，纯备忘。（Lending 018）', 1, 0, '{}', 188, '2025-12-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1158, 7, '<lending-bg-019@lending.local>', '【备份】借贷教训摘记 #019', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-09T10:00:00Z', '随手记几条借钱教训，之后可能写进复盘。（Lending 019）', 1, 0, '{}', 189, '2025-12-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1159, 7, '<lending-bg-020@lending.local>', '【备份】材料待补清单 #020', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-11T10:00:00Z', '哪些材料齐了、哪些还要补，先记一份。（Lending 020）', 1, 0, '{}', 190, '2025-12-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1160, 7, '<lending-bg-021@lending.local>', '【备份】催收沟通整理 #021', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-13T10:00:00Z', '把近几次催收沟通摘录一下，免得回头找不到。（Lending 021）', 1, 0, '{}', 191, '2025-12-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1161, 7, '<lending-bg-022@lending.local>', '【备份】旧账往来说明 #022', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-15T10:00:00Z', '把和陈强相关的旧账、利息口径和聊天碎片先归档。（Lending 022）', 1, 1, '{}', 192, '2025-12-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1162, 7, '<lending-bg-023@lending.local>', '【备份】门店现金安排 #023', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-17T10:00:00Z', '记录阶段性手头现金和店铺周转情况，纯备忘。（Lending 023）', 1, 0, '{}', 193, '2025-12-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1163, 7, '<lending-bg-024@lending.local>', '【备份】借贷教训摘记 #024', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-19T10:00:00Z', '随手记几条借钱教训，之后可能写进复盘。（Lending 024）', 1, 0, '{}', 194, '2025-12-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1164, 7, '<lending-bg-025@lending.local>', '【备份】材料待补清单 #025', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-21T10:00:00Z', '哪些材料齐了、哪些还要补，先记一份。（Lending 025）', 1, 0, '{}', 195, '2025-12-21T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1165, 7, '<lending-bg-026@lending.local>', '【备份】催收沟通整理 #026', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-23T10:00:00Z', '把近几次催收沟通摘录一下，免得回头找不到。（Lending 026）', 1, 0, '{}', 196, '2025-12-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1166, 7, '<lending-bg-027@lending.local>', '【备份】旧账往来说明 #027', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-25T10:00:00Z', '把和陈强相关的旧账、利息口径和聊天碎片先归档。（Lending 027）', 1, 0, '{}', 197, '2025-12-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1167, 7, '<lending-bg-028@lending.local>', '【备份】门店现金安排 #028', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-27T10:00:00Z', '记录阶段性手头现金和店铺周转情况，纯备忘。（Lending 028）', 1, 0, '{}', 198, '2025-12-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1168, 7, '<lending-bg-029@lending.local>', '【备份】借贷教训摘记 #029', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-29T10:00:00Z', '随手记几条借钱教训，之后可能写进复盘。（Lending 029）', 1, 0, '{}', 199, '2025-12-29T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1169, 7, '<lending-bg-030@lending.local>', '【备份】材料待补清单 #030', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-31T10:00:00Z', '哪些材料齐了、哪些还要补，先记一份。（Lending 030）', 1, 0, '{}', 200, '2025-12-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1170, 2, '<sent-bg-001@wang-fang>', '供应商回款确认 #001', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-02-05T09:30:00Z', '收到，你那边先按这个数量备货，我明天再确认。（Sent 001）', 1, 0, '{}', 141, '2026-02-05T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1171, 2, '<sent-bg-002@wang-fang>', '店员排班回复 #002', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-02-09T09:30:00Z', '这周先按新排班执行，有事提前说。（Sent 002）', 1, 0, '{}', 142, '2026-02-09T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1172, 2, '<sent-bg-003@wang-fang>', '家庭回复 #003', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-02-13T09:30:00Z', '周末我尽量回去，先把店里事情安排好。（Sent 003）', 1, 0, '{}', 143, '2026-02-13T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1173, 2, '<sent-bg-004@wang-fang>', '供应商回款确认 #004', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-02-17T09:30:00Z', '收到，你那边先按这个数量备货，我明天再确认。（Sent 004）', 1, 0, '{}', 144, '2026-02-17T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1174, 2, '<sent-bg-005@wang-fang>', '店员排班回复 #005', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-02-21T09:30:00Z', '这周先按新排班执行，有事提前说。（Sent 005）', 1, 0, '{}', 145, '2026-02-21T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1175, 2, '<sent-bg-006@wang-fang>', '家庭回复 #006', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-02-25T09:30:00Z', '周末我尽量回去，先把店里事情安排好。（Sent 006）', 1, 0, '{}', 146, '2026-02-25T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1176, 2, '<sent-bg-007@wang-fang>', '供应商回款确认 #007', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-03-01T09:30:00Z', '收到，你那边先按这个数量备货，我明天再确认。（Sent 007）', 1, 0, '{}', 147, '2026-03-01T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1177, 2, '<sent-bg-008@wang-fang>', '店员排班回复 #008', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-03-05T09:30:00Z', '这周先按新排班执行，有事提前说。（Sent 008）', 1, 0, '{}', 148, '2026-03-05T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1178, 2, '<sent-bg-009@wang-fang>', '家庭回复 #009', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-03-09T09:30:00Z', '周末我尽量回去，先把店里事情安排好。（Sent 009）', 1, 0, '{}', 149, '2026-03-09T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1179, 2, '<sent-bg-010@wang-fang>', '供应商回款确认 #010', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-03-13T09:30:00Z', '收到，你那边先按这个数量备货，我明天再确认。（Sent 010）', 1, 0, '{}', 150, '2026-03-13T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1180, 2, '<sent-bg-011@wang-fang>', '店员排班回复 #011', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-03-17T09:30:00Z', '这周先按新排班执行，有事提前说。（Sent 011）', 1, 0, '{}', 151, '2026-03-17T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1181, 2, '<sent-bg-012@wang-fang>', '家庭回复 #012', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-03-21T09:30:00Z', '周末我尽量回去，先把店里事情安排好。（Sent 012）', 1, 0, '{}', 152, '2026-03-21T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1182, 2, '<sent-bg-013@wang-fang>', '供应商回款确认 #013', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-03-25T09:30:00Z', '收到，你那边先按这个数量备货，我明天再确认。（Sent 013）', 1, 0, '{}', 153, '2026-03-25T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1183, 2, '<sent-bg-014@wang-fang>', '店员排班回复 #014', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-03-29T09:30:00Z', '这周先按新排班执行，有事提前说。（Sent 014）', 1, 0, '{}', 154, '2026-03-29T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1184, 2, '<sent-bg-015@wang-fang>', '家庭回复 #015', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-04-02T09:30:00Z', '周末我尽量回去，先把店里事情安排好。（Sent 015）', 1, 0, '{}', 155, '2026-04-02T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1185, 3, '<draft-bg-001@wang-fang>', '草稿：待办记录 1', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-02T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-02T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1186, 3, '<draft-bg-002@wang-fang>', '草稿：待办记录 2', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-03T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-03T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1187, 3, '<draft-bg-003@wang-fang>', '草稿：待办记录 3', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-04T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-04T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1188, 3, '<draft-bg-004@wang-fang>', '草稿：待办记录 4', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-05T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-05T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1189, 3, '<draft-bg-005@wang-fang>', '草稿：待办记录 5', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-06T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-06T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1190, 3, '<draft-bg-006@wang-fang>', '草稿：待办记录 6', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-07T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-07T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1191, 3, '<draft-bg-007@wang-fang>', '草稿：待办记录 7', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-08T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-08T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1192, 3, '<draft-bg-008@wang-fang>', '草稿：待办记录 8', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-09T22:00:00Z', '未发送的个人草稿，用来形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-09T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1193, 5, '<spam-bg-001@spam.local>', '异常登录提醒/限时优惠 1', '陌生发件人 <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-01-21T06:00:00Z', '可疑营销邮件，已识别为可疑营销内容。', 0, 0, '{}', 110, '2026-01-21T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1194, 5, '<spam-bg-002@spam.local>', '异常登录提醒/限时优惠 2', '陌生发件人 <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-02-01T06:00:00Z', '可疑营销邮件，已识别为可疑营销内容。', 0, 0, '{}', 110, '2026-02-01T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1195, 5, '<spam-bg-003@spam.local>', '异常登录提醒/限时优惠 3', '陌生发件人 <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-02-12T06:00:00Z', '可疑营销邮件，已识别为可疑营销内容。', 0, 0, '{}', 110, '2026-02-12T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1196, 5, '<spam-bg-004@spam.local>', '异常登录提醒/限时优惠 4', '陌生发件人 <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-02-23T06:00:00Z', '可疑营销邮件，已识别为可疑营销内容。', 0, 0, '{}', 110, '2026-02-23T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1197, 5, '<spam-bg-005@spam.local>', '异常登录提醒/限时优惠 5', '陌生发件人 <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-03-06T06:00:00Z', '可疑营销邮件，已识别为可疑营销内容。', 0, 0, '{}', 110, '2026-03-06T06:00:00Z');

-- Refresh denormalised folder counts.




UPDATE folders SET
  message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
  unread_count  = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND messages.is_read = 0);

INSERT INTO _counters (key, value) VALUES
  ('msg_seq', 500);

COMMIT;
