BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s16_judgment', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '一审判决书已送达',
   '西湖区人民法院判决陈强返还实际出借本金36万元并按一年期LPR四倍支付利息、扣除已还2万元；未支持第二笔20万元现金借款及其他共同清偿、精神损失和误工请求。',
   '{"case_no":"（2026）浙0106民初08812号","event":"judgment","delivered_at":"2026-06-16"}',
   '2026-06-16T09:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
