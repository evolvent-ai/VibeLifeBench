-- Generated notification_hub seed for highrise_handover_v5_30d
BEGIN;
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_hhigh_customs', '海关跨境提醒', 'logistics', '跨境寄递、个人物品申报与限额政策提示');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_chu_nuo', 'oa_hhigh_customs', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_hhigh_brand', '官方家装监理服务', 'shopping_service', '官方保修/资质与海外售后说明');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_chu_nuo', 'oa_hhigh_brand', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_hhigh_card', '招行信用卡', 'finance', '账单、外币交易与用卡安全提醒');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_chu_nuo', 'oa_hhigh_card', '2026-06-06T00:00:00Z');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_hhigh_1', 'oa_hhigh_customs', '个人寄递锂电池运输与申报须知', '含锂电池物品航空运输受额定能量(Wh)限制，超规格不可航空运输；申报需如实填写品名与价值。', 'https://customs.example/li-battery-notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_hhigh_2', 'oa_hhigh_brand', '官方保修/资质与海外售后说明', '付款开工前请用商品/SKU 详情核验施工方资质、合同与合同校验码；阶段验收与隐蔽工程需完整留证与时限管理。', 'https://brand.example/notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_hhigh_3', 'oa_hhigh_card', '境外及外币交易用卡安全提示', '外币交易入账可能有汇率与时间差；如发现重复扣费或陌生商户，及时核对并可发起争议。', 'https://card.example/fx-safety', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('post_hhigh_4', 'oa_hhigh_brand', '处理三方案对比', '官方返工(补差¥780,最快)；第三方整改(补差¥450,折中)；解约退款(免补差但需举证且质检约¥600)。请按到手净额与把握权衡。', 'https://brand.example/options', '2026-06-08');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_hhigh_log', 'usr_chu_nuo', 'delivery_logistics', 'keyword', 'YTOHIGH5520002CN', '{"keywords": ["转运", "出运", "申报", "合规"], "order_id": "ord_hhigh_0002"}', 'active', '2026-06-15T09:00:00Z', '2026-06-15T09:00:00Z');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_hhigh_card', 'usr_chu_nuo', 'credit_card', 'keyword', 'card_hhigh_01', '{"keywords": ["外币", "重复扣费", "争议"]}', 'active', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z');
INSERT INTO price_alerts (alert_id, user_id, item_ref, target_price_minor, currency, status, created_at) VALUES ('alr_hhigh_1', 'usr_chu_nuo', 'prod_hhigh_main', 5310000, 'CNY', 'active', '2026-06-15T00:00:00Z');
INSERT INTO notifications (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES ('ntf_hhigh_seed1', 'usr_chu_nuo', 'delivery_logistics', 'policy_update', 'sub_hhigh_log', '验收提示：阶段验收请留证', '您的高层塔楼交付验收维权套餐阶段验收后请及时留底并保留工况凭证。', '{"order_id": "ord_hhigh_0002", "tracking_no": "YTOHIGH5520002CN"}', '2026-06-15T12:05:00Z', 0);
INSERT INTO notifications (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES ('ntf_hhigh_seed2', 'usr_chu_nuo', 'credit_card', 'policy_update', 'sub_hhigh_card', '外币交易入账提醒', '您的卡新增一笔外币交易，入账可能有汇率与时间差，请留意后续对账。', '{"card_id": "card_hhigh_01", "tx_id": "tx_hhigh_fx"}', '2026-06-15T11:35:00Z', 0);
INSERT INTO _counters (key,value) VALUES ('subscription_seq',2),('alert_seq',1);
COMMIT;
