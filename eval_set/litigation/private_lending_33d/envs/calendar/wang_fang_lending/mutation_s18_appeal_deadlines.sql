BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_lending_sys_appeal_packet_watch', 'cal_wang_fang', '二审送达待办：等待上诉状副本',
   '杭州市中级人民法院已受理陈强上诉；收到副本后需按正式通知核对答辩和举证期限。', NULL,
   '2026-06-20T09:00:00+08:00', '2026-06-20T09:30:00+08:00', 0, 'tentative',
   '2026-06-18T13:51:00+08:00', '2026-06-18T13:51:00+08:00', NULL, NULL);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='event_seq';
COMMIT;
