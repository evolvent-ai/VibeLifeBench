BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s18_appeal', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '被告上诉案件已登记',
   '上海市第一中级人民法院已登记环球优选针对一审判决提出的上诉，赵萌为被上诉人；上诉状副本和二审事项将电子送达。',
   '{"first_instance":"（2026）沪0115民初18426号","appeal_no":"（2026）沪01民终09651号","event":"appeal_accepted"}',
   '2026-06-18T13:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
