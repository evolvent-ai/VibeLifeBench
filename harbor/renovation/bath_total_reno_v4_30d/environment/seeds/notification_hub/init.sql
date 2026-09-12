-- Generated notification_hub seed for bath_total_reno_v4_30d
BEGIN;
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_qbath_customs', 'renovation project detail', 'logistics', 'renovation project detail、renovation project detail');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_geng_lu', 'oa_qbath_customs', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_qbath_brand', 'renovation project detail', 'shopping_service', 'renovation project detail/renovation project detail');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_geng_lu', 'oa_qbath_brand', '2026-06-06T00:00:00Z');
INSERT INTO official_accounts (account_id, name, category, description) VALUES ('oa_qbath_card', 'renovation project detail', 'finance', 'renovation project detail、renovation project detail');
INSERT INTO official_account_subscriptions (user_id, account_id, subscribed_at) VALUES ('usr_geng_lu', 'oa_qbath_card', '2026-06-06T00:00:00Z');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('PA-SHDEL-260608-M4Q7', 'oa_qbath_customs', 'renovation project detail', 'renovation project detail(Wh)renovation project detail，renovation project detail；renovation project detail。', 'https://customs.example/li-battery-notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('PA-SEAL-260608-V3K2', 'oa_qbath_brand', 'renovation project detail', 'renovation project detail v3 renovation project detail；renovation project detail、masonry work、renovation project detail，renovation project detail、renovation project detail。renovation project detail SKU renovation project detail。', 'https://brand.example/notice', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('PA-CMB-260608-FX9R', 'oa_qbath_card', 'renovation project detail', 'renovation project detail；renovation project detail，renovation project detail。', 'https://card.example/fx-safety', '2026-06-08');
INSERT INTO official_account_posts (post_id, account_id, title, summary, url, published_at) VALUES ('PA-SEAL-260608-OPT6', 'oa_qbath_brand', 'renovation project detail', 'renovation project detail、renovation project detail；renovation project detail 780 CNY、450 CNY，renovation project detail 600 renovation project detail，renovation project detail。', 'https://brand.example/options', '2026-06-08');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_qbath_log', 'usr_geng_lu', 'delivery_logistics', 'keyword', 'YTOBATH5520002CN', '{"keywords": ["renovation project detail", "renovation project detail", "renovation project detail", "renovation project detail"], "order_id": "ord_qbath_0002"}', 'active', '2026-06-15T09:00:00Z', '2026-06-15T09:00:00Z');
INSERT INTO subscriptions (subscription_id, user_id, source, type, target, condition_json, status, created_at, updated_at) VALUES ('sub_qbath_card', 'usr_geng_lu', 'credit_card', 'keyword', 'card_qbath_01', '{"keywords": ["renovation project detail", "duplicate charge", "dispute"]}', 'active', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z');
INSERT INTO price_alerts (alert_id, user_id, item_ref, target_price_minor, currency, status, created_at) VALUES ('alr_qbath_1', 'usr_geng_lu', 'prod_qbath_main', 3420000, 'CNY', 'active', '2026-06-15T00:00:00Z');
INSERT INTO notifications (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES ('DLV-260615-Q7M4-1205', 'usr_geng_lu', 'delivery_logistics', 'policy_update', 'sub_qbath_log', 'renovation project detail', 'renovation project detail、renovation project detail，renovation project detail。', '{"order_id": "ord_qbath_0002", "tracking_no": "YTOBATH5520002CN"}', '2026-06-15T12:05:00Z', 0);
INSERT INTO notifications (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES ('CMB-7H3K-2606151135', 'usr_geng_lu', 'credit_card', 'policy_update', 'sub_qbath_card', 'renovation project detail', 'renovation project detail，renovation project detail，renovation project detail。', '{"card_id": "card_qbath_01", "tx_id": "tx_qbath_fx"}', '2026-06-15T11:35:00Z', 0);
INSERT INTO _counters (key,value) VALUES ('subscription_seq',2),('alert_seq',1);

-- HANDBOOK_REMEDIATION_V113_notification_hub
INSERT OR IGNORE INTO official_account_posts VALUES
 ('PA-SEAL-260610-EVD8','oa_qbath_brand','renovation project detail','renovation project detail、renovation project detail、renovation project detail。','https://brand.example/qbath/evidence','2026-06-10'),
 ('PA-SEAL-260611-CTR5','oa_qbath_brand','renovation project detail','renovation project detail、renovation project detail、renovation project detail。','https://brand.example/qbath/contract','2026-06-11'),
 ('PA-CMB-260612-LED4','oa_qbath_card','renovation project detail','refund、renovation project detail。','https://card.example/qbath/refund','2026-06-12'),
 ('PA-SHDEL-260613-LQD7','oa_qbath_customs','renovation project detail','renovation project detail、renovation project detail。','https://logistics.example/qbath/liquid','2026-06-13');
INSERT OR IGNORE INTO notifications VALUES
 ('CAL-4Q8N-0614-0800','usr_geng_lu','calendar','policy_update',NULL,'renovation project detail','renovation project detail、renovation project detail。','{"event_id":"CAL-260621-JOINT-R4D9"}','2026-06-14T08:00:00+08:00',0),
 ('MAIL-260614-8D5M','usr_geng_lu','email','new_content',NULL,'renovation project detail','renovation project detail。','{"message_id":"<verify-4251g-260611-r7q4@brand.example>"}','2026-06-14T08:10:00+08:00',0),
 ('DLV-A6N3-2606140820','usr_geng_lu','delivery_logistics','policy_update','sub_qbath_log','renovation project detail','renovation project detail。','{"tracking_no":"QB26061403"}','2026-06-14T08:20:00+08:00',0),
 ('EC-260614-T9K2','usr_geng_lu','ecommerce','price_drop',NULL,'renovation project detail','renovation project detail 3%，renovation project detail。','{"sku_id":"sku_qbath_membrane"}','2026-06-14T08:30:00+08:00',1),
 ('CAL-7V2P-0614-0840','usr_geng_lu','calendar','policy_update',NULL,'renovation project detail','6 month 25 renovation project detail。','{"event_id":"CAL-260625-INSPECT-H6W2"}','2026-06-14T08:40:00+08:00',0),
 ('CMB-260614-R3W7','usr_geng_lu','credit_card','policy_update','sub_qbath_card','renovation project detail','renovation project detail。','{"card_id":"card_qbath_01"}','2026-06-14T08:50:00+08:00',1),
 ('LST-260614-5C9H','usr_geng_lu','listing_platform','new_content',NULL,'renovation project detail','renovation project detail。','{"listing_id":"LS-SH-WP-260614-B5R8"}','2026-06-14T09:00:00+08:00',0),
 ('MAIL-K2M8-2606140910','usr_geng_lu','email','new_content',NULL,'renovation project detail','renovation project detail 5% renovation project detail。','{"message_id":"<retention-5pct-260614-f3w8@sealpro.example>"}','2026-06-14T09:10:00+08:00',0),
 ('DLV-Z7P4-2606140920','usr_geng_lu','delivery_logistics','policy_update','sub_qbath_log','renovation project detail','renovation project detail。','{"tracking_no":"QB26061404"}','2026-06-14T09:20:00+08:00',0),
 ('CAL-9N6X-0614-0930','usr_geng_lu','calendar','policy_update',NULL,'renovation project detail','7 month 14 renovation project detail。','{"event_id":"CAL-260714-ARCHIVE-M9K1"}','2026-06-14T09:30:00+08:00',1);

COMMIT;

-- Stage-0 temporal fence: post-kickoff notifications are released later.
BEGIN;
DELETE FROM notifications WHERE notification_id IN ('DLV-260615-Q7M4-1205','CMB-7H3K-2606151135');
COMMIT;

-- REMEDIATION_20260730_RENOVATION_NOTIFICATION_CONTEXT
BEGIN;
UPDATE subscriptions
SET condition_json='{"keywords":["renovation project detail","renovation project detail","renovation project detail","renovation project detail"],"order_id":"ord_qbath_0002"}'
WHERE subscription_id='sub_qbath_log';
UPDATE subscriptions
SET condition_json='{"keywords":["project payment","duplicate charge","dispute","renovation project detail"]}'
WHERE subscription_id='sub_qbath_card';
UPDATE notifications
SET title='renovation project detail', body='renovation project detail，renovation project detail、renovation project detail。', payload_json='{"card_id":"card_qbath_01","tx_id":"tx_qbath_fx"}'
WHERE notification_id='CMB-7H3K-2606151135';
UPDATE official_accounts SET name='renovation project detail', category='logistics', description='renovation project detail、renovation project detail、renovation project detail' WHERE account_id='oa_qbath_customs';
UPDATE official_accounts SET description='renovation project detail、renovation project detail、renovation project detail' WHERE account_id='oa_qbath_brand';
UPDATE official_accounts SET description='renovation project detail、duplicate charge、renovation project detail' WHERE account_id='oa_qbath_card';
UPDATE official_account_posts SET title='renovation project detail', summary='renovation project detail、renovation project detail；renovation project detail、renovation project detail、renovation project detail。' WHERE post_id='PA-SHDEL-260608-M4Q7';
UPDATE official_account_posts SET title='renovation project detail', summary='renovation project detail v3 renovation project detail；renovation project detail、masonry work、renovation project detail，renovation project detail SKU renovation project detail。' WHERE post_id='PA-SEAL-260608-V3K2';
UPDATE official_account_posts SET title='renovation project detail', summary='project payment、renovation project detail、renovation project detail；renovation project detail。' WHERE post_id='PA-CMB-260608-FX9R';
COMMIT;

-- Final English official-account facts consumed by the English oracle and rubric.
BEGIN;
UPDATE official_accounts SET name='Official renovation supervision service', category='shopping_service', description='Contract validation, credentials, regional service, and warranty guidance' WHERE account_id='oa_qbath_brand';
UPDATE official_account_posts SET title='Shanghai regional standard contract and base scope', summary='Contract validation for Shanghai regional standard contract v3 covers the registered contract parties and credentials. Scope includes waterproofing, masonry work, electrical work, and supervision; change order items are separate.' WHERE post_id='PA-SEAL-260608-V3K2';
UPDATE official_account_posts SET title='Contract validation and change-order confirmation', summary='Contract parties, credentials, scope, and each change order must remain traceable.' WHERE post_id='PA-SEAL-260611-CTR5';
COMMIT;
