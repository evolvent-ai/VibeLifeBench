BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s12_hearing', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '开庭通知已送达',
   '案件定于2026年6月12日9时30分在浦东新区人民法院第六法庭开庭，请按通知携带身份证明、证据原件和涉案食品材料。',
   '{"case_no":"（2026）沪0115民初18426号","event":"hearing_scheduled","hearing_at":"2026-06-12T09:30:00+08:00"}',
   '2026-06-08T09:40:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
