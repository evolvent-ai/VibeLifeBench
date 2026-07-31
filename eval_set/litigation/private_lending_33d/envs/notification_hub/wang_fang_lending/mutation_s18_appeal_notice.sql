BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s18_appeal', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '陈强提起上诉，二审已受理',
   '杭州市中级人民法院告知：陈强不服一审判决并提起上诉，王芳为被上诉人；上诉状副本、答辩和举证期限将另行送达。',
   '{"event":"appeal_accepted","court":"杭州市中级人民法院","appellant":"陈强","respondent":"王芳"}',
   '2026-06-18T13:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
