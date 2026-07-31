BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s13_lawyer', 'usr_wang_fang', 'content_platform', 'keyword', 'sub_000003',
   '代理律师因利益冲突退出',
   '浙江法律服务平台通知：周敏律师（LD-006）所在求是律师事务所与陈强常年顾问所在律所合并，形成利益冲突，周敏需退出本案代理。6月12日开庭安排未变，请尽快办理交接。',
   '{"event":"lawyer_withdraw","lawyer_id":"LD-006","reason":"律所合并后利益冲突","hearing_at":"2026-06-12T09:30:00+08:00"}',
   '2026-06-10T09:00:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
