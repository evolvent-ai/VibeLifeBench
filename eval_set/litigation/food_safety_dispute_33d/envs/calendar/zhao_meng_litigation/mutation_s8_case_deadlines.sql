BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_food_sys_inspection_apply', 'cal_zhao_meng', '法院送达待办：核对食品检验申请安排',
   '受理材料提示本案涉及食品安全专门问题；此项由电子送达同步到日历，具体申请内容和是否提交仍需本人确认。', NULL,
   '2026-06-05T17:00:00+08:00', '2026-06-05T17:30:00+08:00', 0, 'tentative',
   '2026-06-01T09:31:00+08:00', '2026-06-01T09:31:00+08:00', NULL, NULL),
  ('evt_food_sys_evidence_due', 'cal_zhao_meng', '法院送达：举证期限节点',
   '根据受理材料暂记的举证节点；应结合正式举证通知核对截止时间并自行设置提前提醒。', NULL,
   '2026-06-16T17:00:00+08:00', '2026-06-16T17:30:00+08:00', 0, 'tentative',
   '2026-06-01T09:31:00+08:00', '2026-06-01T09:31:00+08:00', NULL, NULL);
INSERT OR IGNORE INTO reminders (id, event_id, method, minutes_before) VALUES
  (9101, 'evt_food_sys_inspection_apply', 'popup', 1440),
  (9102, 'evt_food_sys_evidence_due', 'popup', 2880);
UPDATE _counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key IN ('event_seq','reminder_seq');
COMMIT;
