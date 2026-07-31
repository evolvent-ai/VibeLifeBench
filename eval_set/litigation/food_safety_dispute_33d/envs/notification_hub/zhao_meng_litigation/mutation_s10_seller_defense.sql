BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s10_defense', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '被告答辩材料已电子送达',
   '被告答辩涉及赔偿法律依据、购买前差评、中文标签性质和涉案食品安全性；法院要求原告在举证期限内提交质证意见。',
   '{"case_no":"（2026）沪0115民初18426号","event":"defense_served","attachment":"答辩状及证据目录"}',
   '2026-06-04T09:00:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
