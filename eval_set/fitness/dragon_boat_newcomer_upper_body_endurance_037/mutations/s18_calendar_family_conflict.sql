BEGIN;
INSERT OR REPLACE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id)
VALUES
  ('cal_family_birthday_0802', 'cal_chen_shan_main', '妈妈生日家庭聚餐',
   '既有家庭责任；若与个人训练冲突，应保留聚餐并把训练改到上午短恢复或另择时段。',
   'home', '2026-08-02T18:00:00+08:00', '2026-08-02T21:00:00+08:00',
   0, 'confirmed', '2026-07-29T08:00:00+08:00', '2026-07-29T08:00:00+08:00', NULL, NULL);
COMMIT;
