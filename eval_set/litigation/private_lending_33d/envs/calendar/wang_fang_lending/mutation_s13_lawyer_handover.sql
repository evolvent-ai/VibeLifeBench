BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_lending_sys_lawyer_handover', 'cal_wang_fang', '代理变更：材料交接时间窗',
   '周敏律师因利益冲突退出，平台同步的紧急交接时间窗；新代理选择和正式授权仍需王芳确认。',
   '线上/律所待确认',
   '2026-06-10T15:00:00+08:00', '2026-06-10T16:00:00+08:00', 0, 'tentative',
   '2026-06-10T09:01:00+08:00', '2026-06-10T09:01:00+08:00', NULL, NULL);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='event_seq';
COMMIT;
