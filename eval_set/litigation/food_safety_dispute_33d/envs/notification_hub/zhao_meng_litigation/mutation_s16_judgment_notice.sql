BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s16_judgment', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '一审判决书已送达',
   '浦东法院已送达一审判决书，判决认定涉案两项食品不符合食品安全标准，并对退款、惩罚性赔偿、就医损失和诉讼费用作出处理。',
   '{"case_no":"（2026）沪0115民初18426号","event":"judgment_delivered","delivered_at":"2026-06-16T09:50:00+08:00"}',
   '2026-06-16T09:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
