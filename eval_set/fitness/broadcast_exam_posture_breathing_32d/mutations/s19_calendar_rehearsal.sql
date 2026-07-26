BEGIN;
INSERT OR REPLACE INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('cal_rehearsal_20261029', 'cal_linyu_broadcast', '模拟流程彩排', '播音主持模拟面试流程彩排，需穿正式鞋并提前到场。', '校内演播厅', '2026-10-29T16:30:00+08:00', '2026-10-29T19:30:00+08:00', 0, 'confirmed', '2026-10-25T15:30:00+08:00', '2026-10-25T15:30:00+08:00', NULL, NULL);
COMMIT;
