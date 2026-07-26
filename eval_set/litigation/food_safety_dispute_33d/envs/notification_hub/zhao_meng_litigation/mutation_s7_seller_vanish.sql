BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s7_seller_vanish', 'usr_zhao_meng', 'content_platform', 'new_content', 'sub_000001',
   '涉案店铺经营状态异常',
   '优鲜购风控记录显示“环球优选”店铺已暂停营业，在线客服和登记电话暂时无法接通；平台正在复核经营者联系资料。',
   '{"case_ref":"food_2026_zm","event":"seller_unreachable","store":"环球优选","platform_review":"pending"}',
   '2026-05-30T09:00:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
