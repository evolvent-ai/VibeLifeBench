BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s19_response', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '二审上诉状副本及答辩期限送达',
   '杭州市中级人民法院送达上诉状副本：王芳应在收到之日起15日内提交答辩状，并按举证通知提交证据；二审围绕上诉请求范围审理。',
   '{"event":"appeal_response_notice","received_at":"2026-06-20","response_days":15,"court":"杭州市中级人民法院"}',
   '2026-06-20T08:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
