BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s12_hearing', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '开庭传票已送达',
   '（2026）浙0106民初08812号定于2026年6月12日9:30在西湖区人民法院第五法庭开庭。请携带身份证、借条原件、银行回单和微信记录等证据原件。',
   '{"case_no":"（2026）浙0106民初08812号","event":"hearing","hearing_at":"2026-06-12T09:30:00+08:00","courtroom":"第五法庭"}',
   '2026-06-08T09:40:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
