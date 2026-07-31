BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_food_sys_inspection_replan', 'cal_zhao_meng', '检验委托变更：确认样品和替代机构安排',
   'JY-006资质暂停且报告未出具；核对样品交接、可用机构、费用和法院举证衔接，最终委托仍由赵萌确认。', NULL,
   '2026-06-10T16:00:00+08:00', '2026-06-10T17:00:00+08:00', 0, 'confirmed',
   '2026-06-10T09:01:00+08:00', '2026-06-10T09:01:00+08:00', NULL, NULL);
INSERT OR IGNORE INTO reminders (id, event_id, method, minutes_before) VALUES
  (9131, 'evt_food_sys_inspection_replan', 'popup', 120);
UPDATE _counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key IN ('event_seq','reminder_seq');
COMMIT;
