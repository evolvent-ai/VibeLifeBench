BEGIN;
INSERT OR REPLACE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id)
VALUES
  ('cal_work_demo_prep_0714', 'cal_chen_shan_main', '客户演示准备会',
   '临时工作会议；如与个人训练冲突，应保留工作安排并重排个人训练。',
   'office', '2026-07-14T19:00:00+08:00', '2026-07-14T21:00:00+08:00',
   0, 'confirmed', '2026-07-11T09:00:00+08:00', '2026-07-11T09:00:00+08:00', NULL, NULL);
COMMIT;
