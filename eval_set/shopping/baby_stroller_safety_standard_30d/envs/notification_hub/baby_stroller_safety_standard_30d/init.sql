-- Generated notification_hub seed for baby_stroller_safety_standard_30d
BEGIN;
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_strr_customs', '海关跨境提醒', 'logistics', '跨境寄递、个人物品申报与限额政策提示');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_yan_ting', 'oa_strr_customs', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_strr_brand', '推车品牌官方服务', 'shopping_service', '官方保修/资质与海外售后说明');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_yan_ting', 'oa_strr_brand', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_strr_card', '招行信用卡', 'finance', '账单、外币交易与用卡安全提醒');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_yan_ting', 'oa_strr_card', '2026-06-06T00:00:00Z');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_strr_1', 'oa_strr_customs', '个人寄递锂电池运输与申报须知', '含锂电池物品航空运输受额定能量(Wh)限制，超规格不可航空运输；申报需如实填写品名与价值。', 'https://customs.example/li-battery-notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_strr_2', 'oa_strr_brand', '官方保修/资质与海外售后说明', '婴儿推车须符合制动/安全带安全标准；部分批次因制动不合格被召回。可凭生产批次核验召回与标准，并提供召回换新/加固配件/退货三种处理。', 'https://brand.example/notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_strr_3', 'oa_strr_card', '境外及外币交易用卡安全提示', '外币交易入账可能有汇率与时间差；如发现重复扣费或陌生商户，及时核对并可发起争议。', 'https://card.example/fx-safety', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_strr_4', 'oa_strr_brand', '处理三方案对比', '召回换新费用为 ¥0，预计约 2 周；制动配件加固费用为 ¥120，可自行安装；退货按原支付路径退款，后续需另行购置。', 'https://brand.example/options', '2026-06-08');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_strr_log', 'usr_yan_ting', 'delivery_logistics', 'keyword', 'ZTOSTRR5520002CN', '{"keywords": ["转运", "出运", "申报", "合规"], "order_id": "ord_strr_0002"}', 'active', '2026-06-14T00:30:00Z', '2026-06-14T00:30:00Z');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_strr_card', 'usr_yan_ting', 'credit_card', 'keyword', 'card_strr_01', '{"keywords": ["外币", "重复扣费", "争议"]}', 'active', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z');
INSERT INTO price_alerts (alert_id, user_id, item_ref, target_price_minor, currency, status, created_at) VALUES ('alr_strr_1', 'usr_yan_ting', 'prod_strr_main', 242910, 'CNY', 'active', '2026-06-15T00:00:00Z');
INSERT INTO _counters (key,value) VALUES ('subscription_seq',2),('alert_seq',1);
COMMIT;
