-- emails-mcp zhao_meng_litigation — init.sql
-- 赵萌的个人邮箱快照, 食品安全网络购物合同纠纷(消费者诉卖家退一赔十)维权场景. Reference frame: 2026-05-20.
-- 邮件埋着案件关键事实(隐含约束依据), 绝不直接点明法律结论。本案是"反直觉雷区":
-- 邮件保留当事人的原始说法与不确定认识，需结合其他材料交叉核对。
--
-- 核心陷阱(每个都有 email 事实依据 + legal_search 判例锚点):
--   ① 赔偿倍数陷阱: 赵萌以为食品也是"退一赔三"; 正确是食品安全法"退一赔十"、保底一千(art_fsl_148/case_f01)。
--   ② 知假买假陷阱: 赵萌担心自己看了差评仍下单算"知假买假"不能赔; 食品领域不影响索赔(art_interp_03/case_f04)。
--   ③ 管辖陷阱: 卖家在杭州, 赵萌以为要去杭州告; 网购收货地(上海)即合同履行地、可在收货地起诉(case_f10)。
--   ④ 标签瑕疵 vs 实质不符合: 无中文标签/过期/非法添加=实质不符合可赔十倍; 仅不影响安全的小瑕疵不赔(art_interp_15/case_f07)。
--   ⑤ 被告主体: 生产者/销售者择一、平台不能提供卖家信息可先行赔付(art_fsl_148/art_cpl_c_44/case_f05/f08)。
--   购买 2026-04-18 / 收货 2026-04-22 / 价款进口奶粉一罐¥680 + 进口代用茶¥1200 / 无中文标签 + 一款检出非法添加 /
--   卖家"环球优选"住所地浙江杭州 / 电商平台"优鲜购"。3年普通时效, 远在时效内。
-- body_text only. id 手动指定以便复现。

BEGIN;

DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'zhao.meng@gmail.com', '赵萌 (Zhao Meng)', '2026-01-01T00:00:00Z');

DELETE FROM folders;
INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam'),
  (6, 'Family'),
  (7, 'Order');

-- =========================================================================
-- INBOX (folder_id = 1)
-- =========================================================================

-- 电商平台: 订单确认(关键!) — 商品/价款/卖家名称/平台/收货地
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20260418-order@youxiangou.com>', '【优鲜购】订单确认 NO.YX20260418', '优鲜购商城 <order@youxiangou.com>', '["zhao.meng@gmail.com"]',
   '2026-04-18T20:20:00Z',
   '赵萌您好，您在优鲜购商城"环球优选"店铺的订单已确认：①进口婴幼儿配方奶粉1罐 ¥680；②进口代用茶(养生茶)1盒 ¥1200。合计¥1880。卖家：环球优选(经营者：杭州环球优选食品有限公司，住所地浙江省杭州市余杭区)。收货地址：上海市浦东新区XX路XX号(赵萌)。平台：优鲜购商城。',
   1, 1, '{}', 320, '2026-04-18T20:20:00Z');

-- 支付凭证
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (2, 1, '<20260418-pay@youxiangou.com>', '【优鲜购】支付成功', 'pay@youxiangou.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T20:25:00Z',
   '您的订单 YX20260418 已支付成功，实付¥1880(微信支付)。感谢惠顾。',
   1, 0, '{}', 160, '2026-04-18T20:25:00Z');

-- 收货 + 发现问题(关键! 无中文标签 + 怀疑非法添加) — 不符合食品安全标准线索
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (3, 1, '<20260422-recv@zhao-meng>', '【备份】收货后发现的问题', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-22T19:00:00Z',
   '4月22日收到货。问题记录(开箱视频和照片都留了)：①那罐进口奶粉整罐只有外文(德文)、完全没有中文标签和中文说明书，看不懂成分、保质期和境内代理商信息；②那盒"养生代用茶"页面宣称能"降血压降血糖、改善睡眠"，但只是普通食品、没有保健食品批号，我喝了两天心慌、查了下怀疑加了不该加的东西。两样我都原样封存没继续用了。',
   1, 1, '{}', 320, '2026-04-22T19:00:00Z');

-- 卖家客服(干扰 + 误导: "最多给你退货退款" + "你看了差评还买就是知假买假赔不了")
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (4, 1, '<20260425-seller@huanqiu.com>', '回复：关于您的退货申请', '环球优选客服 <kefu@huanqiu-youxuan.com>', '["zhao.meng@gmail.com"]',
   '2026-04-25T11:00:00Z',
   '赵女士您好，您反映的问题我们最多给您退货退款，赔偿是不可能的。而且我们看到您下单前就在评论区看过别人说"没有中文标签"的差评、您是知道情况还买的，这属于知假买假、职业打假，法律不会支持您索赔的。建议您接受退款，别折腾了。',
   1, 1, '{}', 240, '2026-04-25T11:00:00Z');

-- 母亲(干扰 + 误导: "退一赔三" + "为一千多块钱犯不上打官司")
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (5, 1, '<20260510-mom@family.local>', '为这点钱别太较真', '赵母 <zhao.mom@163.com>', '["zhao.meng@gmail.com"]',
   '2026-05-10T19:30:00Z',
   '萌萌，不就一千多块钱的东西嘛，我听人说买到假货顶多"退一赔三"，你这一千多就算赔三倍也没多少，犯得上为这个跟人打官司、耗这么大精力？要不让他退了钱就算了。 — 妈',
   1, 0, '{}', 180, '2026-05-10T19:30:00Z');

-- 赵萌自己列的"想一起追的账"草稿(诉求筛选矩阵的事实依据)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (6, 1, '<20260519-claims-bak@zhao-meng>', '【备份】我想跟卖家要的几笔账', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-19T22:00:00Z',
   '这次维权把能要的都要回来：①先把1880块货款退给我；②那罐没中文标签的进口奶粉和那盒怀疑非法添加的茶，要退一赔十；③我喝了茶心慌去医院看了急诊花了300多，挂号和检查费想一起要；④我还想让卖家额外赔我精神损失费2万出口气；⑤要是卖家跑了找不到，能不能让优鲜购平台赔？⑥我下单前确实看过差评，这会不会让我赔不了？先问问助理这些怎么弄、能不能要、该告谁。',
   1, 0, '{}', 360, '2026-05-19T22:00:00Z');

-- 赵萌自己的"找检验机构预算"备忘(检验机构选聘的硬约束依据)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (7, 1, '<20260516-budget-bak@zhao-meng>', '【备份】找食品检验机构的预算和要求', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-16T22:00:00Z',
   '律师说那盒茶到底有没有非法添加、奶粉标签合不合规，最好找正规食品检验机构出个检验报告，法院才认。我的几个底线：①检验费我最多出3000块(¥3000)，再多掏不起，我只需要测标签符合性和非法添加这一两项、不需要做全项套餐；②必须有食品检验 CMA 资质(最好还有 CNAS)、报告能在上海法院被采信；③要独立客观、跟卖家那家公司没有任何关联或利益往来；④别找那种"保证给你检出不合格、按结果收费"的，这种报告法院不认。先去法律服务平台那个检验机构名录里帮我筛筛靠谱又付得起的。',
   1, 0, '{}', 360, '2026-05-16T22:00:00Z');

-- 急诊小票(实际损失线索: 就医费用)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (8, 1, '<20260424-clinic@zhao-meng>', '【备份】喝茶后就医的费用', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-24T21:00:00Z',
   '记一下：4月23日喝了那个养生茶后心慌、手抖，去社区医院急诊看了，挂号+心电图+检查一共花了320元，发票和病历都留着。医生说像是摄入了某种刺激性成分引起的。',
   1, 0, '{}', 180, '2026-04-24T21:00:00Z');

-- 知情线索(下单前看过差评 — 知假买假抗辩的事实依据, 但食品领域不影响)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (9, 1, '<20260418-review@zhao-meng>', '【备份】下单前看到的差评', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T19:00:00Z',
   '存个证：我下单那款进口奶粉前，评论区确实有人说"整罐没有中文标签、看不懂"。我当时想着便宜、抱着试试看也想留证维权就买了。卖家后来拿这个说我"知假买假"。截图我留了。',
   1, 0, '{}', 180, '2026-04-18T19:00:00Z');

-- =========================================================================
-- Sent (folder_id = 2)
-- =========================================================================
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (20, 2, '<20260428-sent-seller@zhao-meng>', '关于退款及食品安全赔偿的函', 'zhao.meng@gmail.com', '["kefu@huanqiu-youxuan.com"]',
   '2026-04-28T09:00:00Z',
   '环球优选：本人于2026-04-18在贵店购买进口奶粉及代用茶共计1880元，收货后发现进口奶粉无中文标签、代用茶涉嫌非法添加且违法宣称功效，均不符合食品安全标准。现要求退还货款并依《食品安全法》第一百四十八条支付价款十倍赔偿。请于收函后十日内处理，否则本人将通过诉讼维权。 — 赵萌',
   1, 0, '{}', 300, '2026-04-28T09:00:00Z');

-- =========================================================================
-- Order folder (folder_id = 7) — 卖家/平台信息 + 商品页面存档
-- =========================================================================
-- 卖家与平台信息(住所地/收货地, 用于网购管辖 + 平台责任判断)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (30, 7, '<20260418-sellerinfo@zhao-meng>', '卖家与平台信息(备查)', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T20:40:00Z',
   '备查：卖家"环球优选"，经营者杭州环球优选食品有限公司，住所地浙江省杭州市余杭区。销售平台：优鲜购商城(平台经营者：上海优鲜购网络科技有限公司)。我的收货地：上海市浦东新区。',
   1, 0, '{}', 180, '2026-04-18T20:40:00Z');

-- 商品页面存档(代用茶违法宣称功效 + 无保健食品批号)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (31, 7, '<20260418-page@zhao-meng>', '【备份】商品页面截图说明', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T21:00:00Z',
   '存档：那盒"养生代用茶"商品详情页写着"专治高血压、降血糖、根治失眠"，但它只是普通食品(配料表写的是茶叶和草本)，没有保健食品批号(没有"蓝帽子"标志)。普通食品这样宣称疾病治疗功效本身就违规。截图都留了。',
   1, 0, '{}', 200, '2026-04-18T21:00:00Z');



INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1000, 1, '<inbox-bg-001@mail.local>', '行政系统提醒 #001', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-03T09:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 181, '2026-01-03T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1001, 1, '<inbox-bg-002@mail.local>', '物业账单提醒 #002', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-04T10:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 182, '2026-01-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1002, 1, '<inbox-bg-003@mail.local>', '平台促销资讯 #003', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-05T11:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 183, '2026-01-05T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1003, 1, '<inbox-bg-004@mail.local>', '快递到件通知 #004', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-06T12:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 184, '2026-01-06T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1004, 1, '<inbox-bg-005@mail.local>', '同事会议纪要 #005', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-07T13:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 185, '2026-01-07T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1005, 1, '<inbox-bg-006@mail.local>', '体检中心提醒 #006', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-08T14:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 186, '2026-01-08T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1006, 1, '<inbox-bg-007@mail.local>', '银行对账提醒 #007', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-09T15:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 187, '2026-01-09T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1007, 1, '<inbox-bg-008@mail.local>', '社区活动通知 #008', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-10T16:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 188, '2026-01-10T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1008, 1, '<inbox-bg-009@mail.local>', '行政系统提醒 #009', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-11T08:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 189, '2026-01-11T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1009, 1, '<inbox-bg-010@mail.local>', '物业账单提醒 #010', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-12T09:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 190, '2026-01-12T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1010, 1, '<inbox-bg-011@mail.local>', '平台促销资讯 #011', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-13T10:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 191, '2026-01-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1011, 1, '<inbox-bg-012@mail.local>', '快递到件通知 #012', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-14T11:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 192, '2026-01-14T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1012, 1, '<inbox-bg-013@mail.local>', '同事会议纪要 #013', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-15T12:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 193, '2026-01-15T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1013, 1, '<inbox-bg-014@mail.local>', '体检中心提醒 #014', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-16T13:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 194, '2026-01-16T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1014, 1, '<inbox-bg-015@mail.local>', '银行对账提醒 #015', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-17T14:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 195, '2026-01-17T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1015, 1, '<inbox-bg-016@mail.local>', '社区活动通知 #016', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-18T15:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 196, '2026-01-18T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1016, 1, '<inbox-bg-017@mail.local>', '行政系统提醒 #017', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-19T16:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 1, '{}', 197, '2026-01-19T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1017, 1, '<inbox-bg-018@mail.local>', '物业账单提醒 #018', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-20T08:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 198, '2026-01-20T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1018, 1, '<inbox-bg-019@mail.local>', '平台促销资讯 #019', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-21T09:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 199, '2026-01-21T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1019, 1, '<inbox-bg-020@mail.local>', '快递到件通知 #020', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-22T10:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 200, '2026-01-22T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1020, 1, '<inbox-bg-021@mail.local>', '同事会议纪要 #021', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-23T11:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 201, '2026-01-23T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1021, 1, '<inbox-bg-022@mail.local>', '体检中心提醒 #022', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-24T12:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 202, '2026-01-24T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1022, 1, '<inbox-bg-023@mail.local>', '银行对账提醒 #023', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-25T13:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 203, '2026-01-25T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1023, 1, '<inbox-bg-024@mail.local>', '社区活动通知 #024', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-26T14:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 204, '2026-01-26T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1024, 1, '<inbox-bg-025@mail.local>', '行政系统提醒 #025', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-27T15:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 205, '2026-01-27T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1025, 1, '<inbox-bg-026@mail.local>', '物业账单提醒 #026', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-28T16:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 206, '2026-01-28T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1026, 1, '<inbox-bg-027@mail.local>', '平台促销资讯 #027', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-29T08:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 207, '2026-01-29T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1027, 1, '<inbox-bg-028@mail.local>', '快递到件通知 #028', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-30T09:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 208, '2026-01-30T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1028, 1, '<inbox-bg-029@mail.local>', '同事会议纪要 #029', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-31T10:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 209, '2026-01-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1029, 1, '<inbox-bg-030@mail.local>', '体检中心提醒 #030', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-01T11:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 210, '2026-02-01T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1030, 1, '<inbox-bg-031@mail.local>', '银行对账提醒 #031', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-02T12:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 211, '2026-02-02T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1031, 1, '<inbox-bg-032@mail.local>', '社区活动通知 #032', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-03T13:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 212, '2026-02-03T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1032, 1, '<inbox-bg-033@mail.local>', '行政系统提醒 #033', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-04T14:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 213, '2026-02-04T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1033, 1, '<inbox-bg-034@mail.local>', '物业账单提醒 #034', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-05T15:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 1, '{}', 214, '2026-02-05T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1034, 1, '<inbox-bg-035@mail.local>', '平台促销资讯 #035', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-06T16:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 215, '2026-02-06T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1035, 1, '<inbox-bg-036@mail.local>', '快递到件通知 #036', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-07T08:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 216, '2026-02-07T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1036, 1, '<inbox-bg-037@mail.local>', '同事会议纪要 #037', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-08T09:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 217, '2026-02-08T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1037, 1, '<inbox-bg-038@mail.local>', '体检中心提醒 #038', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-09T10:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 218, '2026-02-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1038, 1, '<inbox-bg-039@mail.local>', '银行对账提醒 #039', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-10T11:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 219, '2026-02-10T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1039, 1, '<inbox-bg-040@mail.local>', '社区活动通知 #040', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-11T12:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 220, '2026-02-11T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1040, 1, '<inbox-bg-041@mail.local>', '行政系统提醒 #041', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-12T13:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 221, '2026-02-12T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1041, 1, '<inbox-bg-042@mail.local>', '物业账单提醒 #042', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-13T14:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 222, '2026-02-13T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1042, 1, '<inbox-bg-043@mail.local>', '平台促销资讯 #043', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-14T15:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 223, '2026-02-14T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1043, 1, '<inbox-bg-044@mail.local>', '快递到件通知 #044', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-15T16:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 224, '2026-02-15T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1044, 1, '<inbox-bg-045@mail.local>', '同事会议纪要 #045', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-16T08:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 225, '2026-02-16T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1045, 1, '<inbox-bg-046@mail.local>', '体检中心提醒 #046', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-17T09:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 226, '2026-02-17T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1046, 1, '<inbox-bg-047@mail.local>', '银行对账提醒 #047', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-18T10:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 227, '2026-02-18T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1047, 1, '<inbox-bg-048@mail.local>', '社区活动通知 #048', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-19T11:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 228, '2026-02-19T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1048, 1, '<inbox-bg-049@mail.local>', '行政系统提醒 #049', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-20T12:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 229, '2026-02-20T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1049, 1, '<inbox-bg-050@mail.local>', '物业账单提醒 #050', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-21T13:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 230, '2026-02-21T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1050, 1, '<inbox-bg-051@mail.local>', '平台促销资讯 #051', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-22T14:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 1, '{}', 231, '2026-02-22T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1051, 1, '<inbox-bg-052@mail.local>', '快递到件通知 #052', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-23T15:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 232, '2026-02-23T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1052, 1, '<inbox-bg-053@mail.local>', '同事会议纪要 #053', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-24T16:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 233, '2026-02-24T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1053, 1, '<inbox-bg-054@mail.local>', '体检中心提醒 #054', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-25T08:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 234, '2026-02-25T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1054, 1, '<inbox-bg-055@mail.local>', '银行对账提醒 #055', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-26T09:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 235, '2026-02-26T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1055, 1, '<inbox-bg-056@mail.local>', '社区活动通知 #056', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-27T10:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 236, '2026-02-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1056, 1, '<inbox-bg-057@mail.local>', '行政系统提醒 #057', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-28T11:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 237, '2026-02-28T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1057, 1, '<inbox-bg-058@mail.local>', '物业账单提醒 #058', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-01T12:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 238, '2026-03-01T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1058, 1, '<inbox-bg-059@mail.local>', '平台促销资讯 #059', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-02T13:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 239, '2026-03-02T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1059, 1, '<inbox-bg-060@mail.local>', '快递到件通知 #060', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-03T14:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 240, '2026-03-03T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1060, 1, '<inbox-bg-061@mail.local>', '同事会议纪要 #061', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-04T15:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 241, '2026-03-04T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1061, 1, '<inbox-bg-062@mail.local>', '体检中心提醒 #062', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-05T16:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 242, '2026-03-05T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1062, 1, '<inbox-bg-063@mail.local>', '银行对账提醒 #063', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-06T08:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 243, '2026-03-06T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1063, 1, '<inbox-bg-064@mail.local>', '社区活动通知 #064', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-07T09:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 244, '2026-03-07T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1064, 1, '<inbox-bg-065@mail.local>', '行政系统提醒 #065', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-08T10:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 245, '2026-03-08T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1065, 1, '<inbox-bg-066@mail.local>', '物业账单提醒 #066', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-09T11:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 246, '2026-03-09T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1066, 1, '<inbox-bg-067@mail.local>', '平台促销资讯 #067', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-10T12:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 247, '2026-03-10T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1067, 1, '<inbox-bg-068@mail.local>', '快递到件通知 #068', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-11T13:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 1, '{}', 248, '2026-03-11T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1068, 1, '<inbox-bg-069@mail.local>', '同事会议纪要 #069', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-12T14:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 249, '2026-03-12T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1069, 1, '<inbox-bg-070@mail.local>', '体检中心提醒 #070', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-13T15:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 180, '2026-03-13T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1070, 1, '<inbox-bg-071@mail.local>', '银行对账提醒 #071', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-14T16:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 181, '2026-03-14T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1071, 1, '<inbox-bg-072@mail.local>', '社区活动通知 #072', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-15T08:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 182, '2026-03-15T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1072, 1, '<inbox-bg-073@mail.local>', '行政系统提醒 #073', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-16T09:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 183, '2026-03-16T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1073, 1, '<inbox-bg-074@mail.local>', '物业账单提醒 #074', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-17T10:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 184, '2026-03-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1074, 1, '<inbox-bg-075@mail.local>', '平台促销资讯 #075', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-18T11:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 185, '2026-03-18T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1075, 1, '<inbox-bg-076@mail.local>', '快递到件通知 #076', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-19T12:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 186, '2026-03-19T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1076, 1, '<inbox-bg-077@mail.local>', '同事会议纪要 #077', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-20T13:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 187, '2026-03-20T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1077, 1, '<inbox-bg-078@mail.local>', '体检中心提醒 #078', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-21T14:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 188, '2026-03-21T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1078, 1, '<inbox-bg-079@mail.local>', '银行对账提醒 #079', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-22T15:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 189, '2026-03-22T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1079, 1, '<inbox-bg-080@mail.local>', '社区活动通知 #080', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-23T16:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 190, '2026-03-23T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1080, 1, '<inbox-bg-081@mail.local>', '行政系统提醒 #081', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-24T08:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 191, '2026-03-24T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1081, 1, '<inbox-bg-082@mail.local>', '物业账单提醒 #082', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-25T09:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 192, '2026-03-25T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1082, 1, '<inbox-bg-083@mail.local>', '平台促销资讯 #083', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-26T10:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 193, '2026-03-26T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1083, 1, '<inbox-bg-084@mail.local>', '快递到件通知 #084', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-27T11:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 194, '2026-03-27T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1084, 1, '<inbox-bg-085@mail.local>', '同事会议纪要 #085', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-28T12:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 1, '{}', 195, '2026-03-28T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1085, 1, '<inbox-bg-086@mail.local>', '体检中心提醒 #086', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-29T13:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 196, '2026-03-29T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1086, 1, '<inbox-bg-087@mail.local>', '银行对账提醒 #087', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-30T14:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 197, '2026-03-30T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1087, 1, '<inbox-bg-088@mail.local>', '社区活动通知 #088', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-31T15:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 198, '2026-03-31T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1088, 1, '<inbox-bg-089@mail.local>', '行政系统提醒 #089', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-01T16:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 199, '2026-04-01T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1089, 1, '<inbox-bg-090@mail.local>', '物业账单提醒 #090', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-02T08:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 200, '2026-04-02T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1090, 1, '<inbox-bg-091@mail.local>', '平台促销资讯 #091', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-03T09:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 201, '2026-04-03T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1091, 1, '<inbox-bg-092@mail.local>', '快递到件通知 #092', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-04T10:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 202, '2026-04-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1092, 1, '<inbox-bg-093@mail.local>', '同事会议纪要 #093', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-05T11:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 203, '2026-04-05T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1093, 1, '<inbox-bg-094@mail.local>', '体检中心提醒 #094', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-06T12:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 204, '2026-04-06T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1094, 1, '<inbox-bg-095@mail.local>', '银行对账提醒 #095', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-07T13:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 205, '2026-04-07T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1095, 1, '<inbox-bg-096@mail.local>', '社区活动通知 #096', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-08T14:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 206, '2026-04-08T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1096, 1, '<inbox-bg-097@mail.local>', '行政系统提醒 #097', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-09T15:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 207, '2026-04-09T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1097, 1, '<inbox-bg-098@mail.local>', '物业账单提醒 #098', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-10T16:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 208, '2026-04-10T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1098, 1, '<inbox-bg-099@mail.local>', '平台促销资讯 #099', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-11T08:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 209, '2026-04-11T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1099, 1, '<inbox-bg-100@mail.local>', '快递到件通知 #100', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-12T09:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 210, '2026-04-12T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1100, 1, '<inbox-bg-101@mail.local>', '同事会议纪要 #101', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-13T10:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 211, '2026-04-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1101, 1, '<inbox-bg-102@mail.local>', '体检中心提醒 #102', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-14T11:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 1, '{}', 212, '2026-04-14T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1102, 1, '<inbox-bg-103@mail.local>', '银行对账提醒 #103', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-15T12:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 213, '2026-04-15T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1103, 1, '<inbox-bg-104@mail.local>', '社区活动通知 #104', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-16T13:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 214, '2026-04-16T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1104, 1, '<inbox-bg-105@mail.local>', '行政系统提醒 #105', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-17T14:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 215, '2026-04-17T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1105, 1, '<inbox-bg-106@mail.local>', '物业账单提醒 #106', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-18T15:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 216, '2026-04-18T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1106, 1, '<inbox-bg-107@mail.local>', '平台促销资讯 #107', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-19T16:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 217, '2026-04-19T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1107, 1, '<inbox-bg-108@mail.local>', '快递到件通知 #108', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-20T08:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 218, '2026-04-20T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1108, 1, '<inbox-bg-109@mail.local>', '同事会议纪要 #109', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-21T09:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 219, '2026-04-21T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1109, 1, '<inbox-bg-110@mail.local>', '体检中心提醒 #110', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-22T10:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 220, '2026-04-22T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1110, 1, '<inbox-bg-111@mail.local>', '银行对账提醒 #111', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-23T11:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 221, '2026-04-23T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1111, 1, '<inbox-bg-112@mail.local>', '社区活动通知 #112', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-24T12:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 222, '2026-04-24T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1112, 1, '<inbox-bg-113@mail.local>', '行政系统提醒 #113', '行政服务台 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-25T13:00:00Z', '本周行政事项待确认，包括报销、办公用品和会议室调整。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 223, '2026-04-25T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1113, 1, '<inbox-bg-114@mail.local>', '物业账单提醒 #114', '浦东物业中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-26T14:00:00Z', '本月物业和停车费用账单已出，请在月底前完成核对。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 224, '2026-04-26T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1114, 1, '<inbox-bg-115@mail.local>', '平台促销资讯 #115', '优鲜购商城 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-27T15:00:00Z', '平台例行促销信息，包含粮油零食、清洁用品和母婴用品折扣。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 225, '2026-04-27T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1115, 1, '<inbox-bg-116@mail.local>', '快递到件通知 #116', '顺联速运 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-28T16:00:00Z', '您有包裹即将派送，请保持电话畅通并留意签收时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 226, '2026-04-28T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1116, 1, '<inbox-bg-117@mail.local>', '同事会议纪要 #117', '行政部同事 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-29T08:00:00Z', '附上部门例会纪要，涉及会议室改造、办公耗材与供应商安排。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 227, '2026-04-29T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1117, 1, '<inbox-bg-118@mail.local>', '体检中心提醒 #118', '浦东体检中心 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-30T09:00:00Z', '年度体检预约窗口已开放，请在系统内确认时间。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 0, '{}', 228, '2026-04-30T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1118, 1, '<inbox-bg-119@mail.local>', '银行对账提醒 #119', '浦发银行 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-05-01T10:00:00Z', '您的信用卡账单已生成，请核对最近一周期消费明细。 请按邮件主题核对相关事项，需要时再跟进处理。',
   1, 1, '{}', 229, '2026-05-01T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1119, 1, '<inbox-bg-120@mail.local>', '社区活动通知 #120', '小区居委会 <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-05-02T11:00:00Z', '周末有居民活动与旧物回收安排，欢迎按需参加。 请按邮件主题核对相关事项，需要时再跟进处理。',
   0, 0, '{}', 230, '2026-05-02T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1120, 6, '<family-bg-001@family.local>', '周末吃饭吗', '赵母 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-04T19:00:00Z', '周末回家吃饭，顺便带点水果回来。（Family 001）', 1, 0, '{}', 151, '2026-02-04T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1121, 6, '<family-bg-002@family.local>', '家族群照片', '表姐 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-07T19:00:00Z', '把上次聚会照片发你留念，有空挑几张给家里。（Family 002）', 1, 0, '{}', 152, '2026-02-07T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1122, 6, '<family-bg-003@family.local>', '爸爸体检单', '赵父 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-10T19:00:00Z', '体检单放在抽屉里，记得提醒我复查时间。（Family 003）', 1, 0, '{}', 153, '2026-02-10T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1123, 6, '<family-bg-004@family.local>', '暑假出游想法', '小姨 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-13T19:00:00Z', '大家想暑假找个近一点的地方散散心。（Family 004）', 1, 0, '{}', 154, '2026-02-13T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1124, 6, '<family-bg-005@family.local>', '周末吃饭吗', '赵母 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-16T19:00:00Z', '周末回家吃饭，顺便带点水果回来。（Family 005）', 1, 0, '{}', 155, '2026-02-16T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1125, 6, '<family-bg-006@family.local>', '家族群照片', '表姐 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-19T19:00:00Z', '把上次聚会照片发你留念，有空挑几张给家里。（Family 006）', 1, 0, '{}', 156, '2026-02-19T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1126, 6, '<family-bg-007@family.local>', '爸爸体检单', '赵父 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-22T19:00:00Z', '体检单放在抽屉里，记得提醒我复查时间。（Family 007）', 1, 0, '{}', 157, '2026-02-22T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1127, 6, '<family-bg-008@family.local>', '暑假出游想法', '小姨 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-25T19:00:00Z', '大家想暑假找个近一点的地方散散心。（Family 008）', 1, 0, '{}', 158, '2026-02-25T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1128, 6, '<family-bg-009@family.local>', '周末吃饭吗', '赵母 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-28T19:00:00Z', '周末回家吃饭，顺便带点水果回来。（Family 009）', 1, 0, '{}', 159, '2026-02-28T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1129, 6, '<family-bg-010@family.local>', '家族群照片', '表姐 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-03T19:00:00Z', '把上次聚会照片发你留念，有空挑几张给家里。（Family 010）', 1, 0, '{}', 160, '2026-03-03T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1130, 6, '<family-bg-011@family.local>', '爸爸体检单', '赵父 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-06T19:00:00Z', '体检单放在抽屉里，记得提醒我复查时间。（Family 011）', 1, 0, '{}', 161, '2026-03-06T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1131, 6, '<family-bg-012@family.local>', '暑假出游想法', '小姨 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-09T19:00:00Z', '大家想暑假找个近一点的地方散散心。（Family 012）', 1, 0, '{}', 162, '2026-03-09T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1132, 6, '<family-bg-013@family.local>', '周末吃饭吗', '赵母 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-12T19:00:00Z', '周末回家吃饭，顺便带点水果回来。（Family 013）', 1, 0, '{}', 163, '2026-03-12T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1133, 6, '<family-bg-014@family.local>', '家族群照片', '表姐 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-15T19:00:00Z', '把上次聚会照片发你留念，有空挑几张给家里。（Family 014）', 1, 0, '{}', 164, '2026-03-15T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1134, 6, '<family-bg-015@family.local>', '爸爸体检单', '赵父 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-18T19:00:00Z', '体检单放在抽屉里，记得提醒我复查时间。（Family 015）', 1, 0, '{}', 165, '2026-03-18T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1135, 6, '<family-bg-016@family.local>', '暑假出游想法', '小姨 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-21T19:00:00Z', '大家想暑假找个近一点的地方散散心。（Family 016）', 1, 0, '{}', 166, '2026-03-21T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1136, 6, '<family-bg-017@family.local>', '周末吃饭吗', '赵母 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-24T19:00:00Z', '周末回家吃饭，顺便带点水果回来。（Family 017）', 1, 0, '{}', 167, '2026-03-24T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1137, 6, '<family-bg-018@family.local>', '家族群照片', '表姐 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-27T19:00:00Z', '把上次聚会照片发你留念，有空挑几张给家里。（Family 018）', 1, 0, '{}', 168, '2026-03-27T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1138, 6, '<family-bg-019@family.local>', '爸爸体检单', '赵父 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-30T19:00:00Z', '体检单放在抽屉里，记得提醒我复查时间。（Family 019）', 1, 0, '{}', 169, '2026-03-30T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1139, 6, '<family-bg-020@family.local>', '暑假出游想法', '小姨 <family@local>', '["zhao.meng@gmail.com"]',
   '2026-04-02T19:00:00Z', '大家想暑假找个近一点的地方散散心。（Family 020）', 1, 0, '{}', 170, '2026-04-02T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1140, 7, '<order-bg-001@orders.local>', '【订单】日用品已发货 #001', '生活馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-07T10:00:00Z', '您购买的纸巾、洗衣液等日用品已发货。（Order 001）', 1, 0, '{}', 171, '2026-01-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1141, 7, '<order-bg-002@orders.local>', '【订单】办公用品确认 #002', '办公集采 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-09T10:00:00Z', '订购的文件夹、标签纸和笔记本已确认。（Order 002）', 1, 0, '{}', 172, '2026-01-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1142, 7, '<order-bg-003@orders.local>', '【售后】退款进度提醒 #003', '商城售后 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-11T10:00:00Z', '您提交的售后申请正在处理中，请留意后续通知。（Order 003）', 1, 0, '{}', 173, '2026-01-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1143, 7, '<order-bg-004@orders.local>', '【订单】牛奶和麦片配送 #004', '社区到家 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-13T10:00:00Z', '早餐用品将于今晚送达，请注意查收。（Order 004）', 1, 0, '{}', 174, '2026-01-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1144, 7, '<order-bg-005@orders.local>', '【订单】小家电下单成功 #005', '家电馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-15T10:00:00Z', '小家电订单已确认，预计两日内派送。（Order 005）', 1, 0, '{}', 175, '2026-01-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1145, 7, '<order-bg-006@orders.local>', '【订单】日用品已发货 #006', '生活馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-17T10:00:00Z', '您购买的纸巾、洗衣液等日用品已发货。（Order 006）', 1, 0, '{}', 176, '2026-01-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1146, 7, '<order-bg-007@orders.local>', '【订单】办公用品确认 #007', '办公集采 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-19T10:00:00Z', '订购的文件夹、标签纸和笔记本已确认。（Order 007）', 1, 0, '{}', 177, '2026-01-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1147, 7, '<order-bg-008@orders.local>', '【售后】退款进度提醒 #008', '商城售后 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-21T10:00:00Z', '您提交的售后申请正在处理中，请留意后续通知。（Order 008）', 1, 0, '{}', 178, '2026-01-21T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1148, 7, '<order-bg-009@orders.local>', '【订单】牛奶和麦片配送 #009', '社区到家 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-23T10:00:00Z', '早餐用品将于今晚送达，请注意查收。（Order 009）', 1, 0, '{}', 179, '2026-01-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1149, 7, '<order-bg-010@orders.local>', '【订单】小家电下单成功 #010', '家电馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-25T10:00:00Z', '小家电订单已确认，预计两日内派送。（Order 010）', 1, 0, '{}', 180, '2026-01-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1150, 7, '<order-bg-011@orders.local>', '【订单】日用品已发货 #011', '生活馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-27T10:00:00Z', '您购买的纸巾、洗衣液等日用品已发货。（Order 011）', 1, 0, '{}', 181, '2026-01-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1151, 7, '<order-bg-012@orders.local>', '【订单】办公用品确认 #012', '办公集采 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-29T10:00:00Z', '订购的文件夹、标签纸和笔记本已确认。（Order 012）', 1, 0, '{}', 182, '2026-01-29T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1152, 7, '<order-bg-013@orders.local>', '【售后】退款进度提醒 #013', '商城售后 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-31T10:00:00Z', '您提交的售后申请正在处理中，请留意后续通知。（Order 013）', 1, 1, '{}', 183, '2026-01-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1153, 7, '<order-bg-014@orders.local>', '【订单】牛奶和麦片配送 #014', '社区到家 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-02T10:00:00Z', '早餐用品将于今晚送达，请注意查收。（Order 014）', 1, 0, '{}', 184, '2026-02-02T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1154, 7, '<order-bg-015@orders.local>', '【订单】小家电下单成功 #015', '家电馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-04T10:00:00Z', '小家电订单已确认，预计两日内派送。（Order 015）', 1, 0, '{}', 185, '2026-02-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1155, 7, '<order-bg-016@orders.local>', '【订单】日用品已发货 #016', '生活馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-06T10:00:00Z', '您购买的纸巾、洗衣液等日用品已发货。（Order 016）', 1, 0, '{}', 186, '2026-02-06T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1156, 7, '<order-bg-017@orders.local>', '【订单】办公用品确认 #017', '办公集采 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-08T10:00:00Z', '订购的文件夹、标签纸和笔记本已确认。（Order 017）', 1, 0, '{}', 187, '2026-02-08T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1157, 7, '<order-bg-018@orders.local>', '【售后】退款进度提醒 #018', '商城售后 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-10T10:00:00Z', '您提交的售后申请正在处理中，请留意后续通知。（Order 018）', 1, 0, '{}', 188, '2026-02-10T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1158, 7, '<order-bg-019@orders.local>', '【订单】牛奶和麦片配送 #019', '社区到家 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-12T10:00:00Z', '早餐用品将于今晚送达，请注意查收。（Order 019）', 1, 0, '{}', 189, '2026-02-12T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1159, 7, '<order-bg-020@orders.local>', '【订单】小家电下单成功 #020', '家电馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-14T10:00:00Z', '小家电订单已确认，预计两日内派送。（Order 020）', 1, 0, '{}', 190, '2026-02-14T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1160, 7, '<order-bg-021@orders.local>', '【订单】日用品已发货 #021', '生活馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-16T10:00:00Z', '您购买的纸巾、洗衣液等日用品已发货。（Order 021）', 1, 0, '{}', 191, '2026-02-16T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1161, 7, '<order-bg-022@orders.local>', '【订单】办公用品确认 #022', '办公集采 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-18T10:00:00Z', '订购的文件夹、标签纸和笔记本已确认。（Order 022）', 1, 0, '{}', 192, '2026-02-18T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1162, 7, '<order-bg-023@orders.local>', '【售后】退款进度提醒 #023', '商城售后 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-20T10:00:00Z', '您提交的售后申请正在处理中，请留意后续通知。（Order 023）', 1, 0, '{}', 193, '2026-02-20T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1163, 7, '<order-bg-024@orders.local>', '【订单】牛奶和麦片配送 #024', '社区到家 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-22T10:00:00Z', '早餐用品将于今晚送达，请注意查收。（Order 024）', 1, 0, '{}', 194, '2026-02-22T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1164, 7, '<order-bg-025@orders.local>', '【订单】小家电下单成功 #025', '家电馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-24T10:00:00Z', '小家电订单已确认，预计两日内派送。（Order 025）', 1, 0, '{}', 195, '2026-02-24T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1165, 7, '<order-bg-026@orders.local>', '【订单】日用品已发货 #026', '生活馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-26T10:00:00Z', '您购买的纸巾、洗衣液等日用品已发货。（Order 026）', 1, 1, '{}', 196, '2026-02-26T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1166, 7, '<order-bg-027@orders.local>', '【订单】办公用品确认 #027', '办公集采 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-28T10:00:00Z', '订购的文件夹、标签纸和笔记本已确认。（Order 027）', 1, 0, '{}', 197, '2026-02-28T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1167, 7, '<order-bg-028@orders.local>', '【售后】退款进度提醒 #028', '商城售后 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-03-02T10:00:00Z', '您提交的售后申请正在处理中，请留意后续通知。（Order 028）', 1, 0, '{}', 198, '2026-03-02T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1168, 7, '<order-bg-029@orders.local>', '【订单】牛奶和麦片配送 #029', '社区到家 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-03-04T10:00:00Z', '早餐用品将于今晚送达，请注意查收。（Order 029）', 1, 0, '{}', 199, '2026-03-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1169, 7, '<order-bg-030@orders.local>', '【订单】小家电下单成功 #030', '家电馆 <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-03-06T10:00:00Z', '小家电订单已确认，预计两日内派送。（Order 030）', 1, 0, '{}', 200, '2026-03-06T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1170, 2, '<sent-bg-001@zhao-meng>', '会议确认 #001', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-03-05T09:30:00Z', '已收到，你们先按这个版本安排，我下午再补充。（Sent 001）', 1, 0, '{}', 141, '2026-03-05T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1171, 2, '<sent-bg-002@zhao-meng>', '资料回传 #002', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-03-09T09:30:00Z', '附件已收到，晚些时候我会统一核对。（Sent 002）', 1, 0, '{}', 142, '2026-03-09T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1172, 2, '<sent-bg-003@zhao-meng>', '家庭回复 #003', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-03-13T09:30:00Z', '周末我回去，顺便给你带药。（Sent 003）', 1, 0, '{}', 143, '2026-03-13T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1173, 2, '<sent-bg-004@zhao-meng>', '会议确认 #004', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-03-17T09:30:00Z', '已收到，你们先按这个版本安排，我下午再补充。（Sent 004）', 1, 0, '{}', 144, '2026-03-17T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1174, 2, '<sent-bg-005@zhao-meng>', '资料回传 #005', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-03-21T09:30:00Z', '附件已收到，晚些时候我会统一核对。（Sent 005）', 1, 0, '{}', 145, '2026-03-21T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1175, 2, '<sent-bg-006@zhao-meng>', '家庭回复 #006', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-03-25T09:30:00Z', '周末我回去，顺便给你带药。（Sent 006）', 1, 0, '{}', 146, '2026-03-25T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1176, 2, '<sent-bg-007@zhao-meng>', '会议确认 #007', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-03-29T09:30:00Z', '已收到，你们先按这个版本安排，我下午再补充。（Sent 007）', 1, 0, '{}', 147, '2026-03-29T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1177, 2, '<sent-bg-008@zhao-meng>', '资料回传 #008', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-04-02T09:30:00Z', '附件已收到，晚些时候我会统一核对。（Sent 008）', 1, 0, '{}', 148, '2026-04-02T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1178, 2, '<sent-bg-009@zhao-meng>', '家庭回复 #009', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-04-06T09:30:00Z', '周末我回去，顺便给你带药。（Sent 009）', 1, 0, '{}', 149, '2026-04-06T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1179, 2, '<sent-bg-010@zhao-meng>', '会议确认 #010', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-04-10T09:30:00Z', '已收到，你们先按这个版本安排，我下午再补充。（Sent 010）', 1, 0, '{}', 150, '2026-04-10T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1180, 2, '<sent-bg-011@zhao-meng>', '资料回传 #011', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-04-14T09:30:00Z', '附件已收到，晚些时候我会统一核对。（Sent 011）', 1, 0, '{}', 151, '2026-04-14T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1181, 2, '<sent-bg-012@zhao-meng>', '家庭回复 #012', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-04-18T09:30:00Z', '周末我回去，顺便给你带药。（Sent 012）', 1, 0, '{}', 152, '2026-04-18T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1182, 2, '<sent-bg-013@zhao-meng>', '会议确认 #013', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-04-22T09:30:00Z', '已收到，你们先按这个版本安排，我下午再补充。（Sent 013）', 1, 0, '{}', 153, '2026-04-22T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1183, 2, '<sent-bg-014@zhao-meng>', '资料回传 #014', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-04-26T09:30:00Z', '附件已收到，晚些时候我会统一核对。（Sent 014）', 1, 0, '{}', 154, '2026-04-26T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1184, 2, '<sent-bg-015@zhao-meng>', '家庭回复 #015', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-04-30T09:30:00Z', '周末我回去，顺便给你带药。（Sent 015）', 1, 0, '{}', 155, '2026-04-30T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1185, 3, '<draft-bg-001@zhao-meng>', '草稿：待处理事项 1', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-02T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-02T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1186, 3, '<draft-bg-002@zhao-meng>', '草稿：待处理事项 2', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-03T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-03T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1187, 3, '<draft-bg-003@zhao-meng>', '草稿：待处理事项 3', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-04T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-04T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1188, 3, '<draft-bg-004@zhao-meng>', '草稿：待处理事项 4', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-05T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-05T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1189, 3, '<draft-bg-005@zhao-meng>', '草稿：待处理事项 5', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-06T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-06T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1190, 3, '<draft-bg-006@zhao-meng>', '草稿：待处理事项 6', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-07T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-07T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1191, 3, '<draft-bg-007@zhao-meng>', '草稿：待处理事项 7', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-08T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-08T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1192, 3, '<draft-bg-008@zhao-meng>', '草稿：待处理事项 8', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-09T22:00:00Z', '这是未发送的个人草稿，用于形成真实邮箱结构。', 0, 0, '{}', 120, '2026-05-09T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1193, 5, '<spam-bg-001@spam.local>', '限时优惠/异常登录提醒 1', '陌生发件人 <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-02-26T06:00:00Z', '典型垃圾邮件样本，用于丰富邮箱噪声。', 0, 0, '{}', 110, '2026-02-26T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1194, 5, '<spam-bg-002@spam.local>', '限时优惠/异常登录提醒 2', '陌生发件人 <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-03-09T06:00:00Z', '典型垃圾邮件样本，用于丰富邮箱噪声。', 0, 0, '{}', 110, '2026-03-09T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1195, 5, '<spam-bg-003@spam.local>', '限时优惠/异常登录提醒 3', '陌生发件人 <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-03-20T06:00:00Z', '典型垃圾邮件样本，用于丰富邮箱噪声。', 0, 0, '{}', 110, '2026-03-20T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1196, 5, '<spam-bg-004@spam.local>', '限时优惠/异常登录提醒 4', '陌生发件人 <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-03-31T06:00:00Z', '典型垃圾邮件样本，用于丰富邮箱噪声。', 0, 0, '{}', 110, '2026-03-31T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1197, 5, '<spam-bg-005@spam.local>', '限时优惠/异常登录提醒 5', '陌生发件人 <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-04-11T06:00:00Z', '典型垃圾邮件样本，用于丰富邮箱噪声。', 0, 0, '{}', 110, '2026-04-11T06:00:00Z');

-- Refresh denormalised folder counts.

UPDATE folders SET
  message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
  unread_count  = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND messages.is_read = 0);

INSERT INTO _counters (key, value) VALUES
  ('msg_seq', 500);

COMMIT;
