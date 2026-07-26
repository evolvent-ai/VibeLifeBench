BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s10_defense', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '被告答辩及证据意见已送达',
   '陈强主张第一笔借条虽载40万元但银行实际到账36万元，并否认第二笔20万元现金实际交付。法院已送达答辩状及附件，要求原告准备质证。',
   '{"case_no":"（2026）浙0106民初08812号","event":"defense","issues":["实际到账本金","现金交付"]}',
   '2026-06-04T09:00:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
