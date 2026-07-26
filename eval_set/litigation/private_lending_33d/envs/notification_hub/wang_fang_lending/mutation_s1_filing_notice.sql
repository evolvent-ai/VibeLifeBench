BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s1_filing', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000001',
   '西湖法院网上立案服务指引更新',
   '西湖区人民法院发布网上立案服务指引：民事起诉可在线提交起诉状、主体材料和证据，立案审核及缴费通知通过诉讼服务渠道送达。',
   '{"account_id":"oa_hz_court","event":"filing_guidance","court":"杭州市西湖区人民法院"}',
   '2026-05-21T08:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
