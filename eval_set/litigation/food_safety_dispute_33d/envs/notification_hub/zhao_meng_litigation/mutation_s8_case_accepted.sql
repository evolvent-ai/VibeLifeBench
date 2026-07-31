BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s8_case_accepted', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '食品安全网购纠纷案件已受理',
   '浦东法院已受理赵萌诉环球优选等网络购物合同纠纷，案号为（2026）沪0115民初18426号；电子送达材料包含受理通知和举证说明。',
   '{"case_no":"（2026）沪0115民初18426号","event":"accepted","court":"上海市浦东新区人民法院"}',
   '2026-06-01T09:30:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
