BEGIN;
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s13_inspector_pause', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '拟委托检验机构资质状态发生变化',
   '上海法律服务平台收到资质状态更新：沪正检测技术有限公司（JY-006）的食品检验CMA资质暂停，尚未出具的本案报告不能按原安排交付。',
   '{"event":"inspection_provider_paused","provider_id":"JY-006","report_status":"not_issued"}',
   '2026-06-10T09:00:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
