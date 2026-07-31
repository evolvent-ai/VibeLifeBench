BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_lending_s9_evidence', 'usr_wang_fang', 'gov_policy', 'policy_update', 'sub_000002',
   '举证通知与保全进展送达',
   '本案举证期限为收到通知之日起15日；法院同时告知财产保全裁定已进入查封或冻结办理环节。请核对证据清单、程序意见和保全材料。',
   '{"case_no":"（2026）浙0106民初08812号","event":"evidence_and_preservation","evidence_days":15}',
   '2026-06-02T09:20:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
