BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s7_jurisdiction', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '被告提出管辖权异议',
   '西湖区人民法院送达程序材料：陈强以其住所地在宁波市海曙区为由，请求将本案移送宁波法院。法院要求王芳就管辖事项提交书面意见。',
   '{"case_no":"（2026）浙0106民初08812号","event":"jurisdiction_objection","respondent_claim":"被告住所地宁波"}',
   '2026-05-30T09:00:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
