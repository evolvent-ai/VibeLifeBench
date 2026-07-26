-- Generated notification_hub seed for central_ac_install_30d
BEGIN;
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_iscac_customs', '家电送装规则', 'service', '大件家电配送、安装和上门验收规则');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_luo_wei', 'oa_iscac_customs', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_iscac_brand', '官方送装售后服务', 'shopping_service', '官方保修/资质与海外售后说明');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_luo_wei', 'oa_iscac_brand', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_iscac_card', '招行信用卡', 'finance', '账单、外币交易与用卡安全提醒');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_luo_wei', 'oa_iscac_card', '2026-06-06T00:00:00Z');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_iscac_1', 'oa_iscac_customs', '大件家电送装验收与改期规则', '恶劣天气或现场条件不满足时可改约上门；服务记录保留原工单编号与预约历史。', 'https://service.example/delivery-installation', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_iscac_2', 'oa_iscac_brand', '官方保修/资质与海外售后说明', '官方安装记录包含适配机型、服务人员资质、上门服务码和公示收费项目；施工验收记录可用于后续售后。', 'https://brand.example/notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_iscac_3', 'oa_iscac_card', '境外及外币交易用卡安全提示', '外币交易入账可能有汇率与时间差；如发现重复扣费或陌生商户，及时核对并可发起争议。', 'https://card.example/fx-safety', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_iscac_4', 'oa_iscac_brand', '处理三方案对比', '官方返工需补差 ¥780；改约第三方持证安装预计补差 ¥450；自行整改可申请报销，但材料预计约 ¥600 且需提交合格凭证。', 'https://brand.example/options', '2026-06-08');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_iscac_log', 'usr_luo_wei', 'delivery_logistics', 'keyword', 'YTOSCAC5520002CN', '{"keywords": ["送装", "上门", "安装", "验收"], "order_id": "ord_iscac_0002"}', 'active', '2026-06-14T00:30:00Z', '2026-06-14T00:30:00Z');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_iscac_card', 'usr_luo_wei', 'credit_card', 'keyword', 'card_iscac_01', '{"keywords": ["外币", "重复扣费", "争议"]}', 'active', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z');
INSERT INTO price_alerts (alert_id, user_id, item_ref, target_price_minor, currency, status, created_at) VALUES ('alr_iscac_1', 'usr_luo_wei', 'prod_iscac_main', 1709910, 'CNY', 'active', '2026-06-15T00:00:00Z');
INSERT INTO _counters (key,value) VALUES ('subscription_seq',2),('alert_seq',1);
COMMIT;
