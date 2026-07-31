BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s8_accepted', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '民间借贷纠纷案件已受理',
   '西湖区人民法院已受理王芳诉陈强民间借贷纠纷，案号（2026）浙0106民初08812号；请关注后续举证、程序意见和开庭送达。',
   '{"case_no":"（2026）浙0106民初08812号","event":"accepted","court":"杭州市西湖区人民法院"}',
   '2026-06-01T09:30:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
