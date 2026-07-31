BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_food_sys_appeal_response_due', 'cal_zhao_meng', '二审送达待办：核对答辩期限',
   '二审案件（2026）沪01民终09651号已登记。此节点来自电子送达，应按实际收到上诉状副本之日核对并更新答辩截止时间。', NULL,
   '2026-07-03T17:00:00+08:00', '2026-07-03T17:30:00+08:00', 0, 'tentative',
   '2026-06-18T13:51:00+08:00', '2026-06-18T13:51:00+08:00', NULL, NULL);
INSERT OR IGNORE INTO reminders (id, event_id, method, minutes_before) VALUES
  (9181, 'evt_food_sys_appeal_response_due', 'popup', 4320);
UPDATE _counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key IN ('event_seq','reminder_seq');
COMMIT;
