BEGIN;
INSERT OR REPLACE INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('cal_school_extra_test_20261014', 'cal_linyu_broadcast', '文化课周测', '学校临时加测，个人训练需要避开。', '学校教室', '2026-10-14T19:00:00+08:00', '2026-10-14T21:00:00+08:00', 0, 'confirmed', '2026-10-12T16:00:00+08:00', '2026-10-12T16:00:00+08:00', NULL, NULL);
COMMIT;
