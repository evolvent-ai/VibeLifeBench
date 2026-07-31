BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_lending_sys_acceptance_review', 'cal_wang_fang', '法院送达待办：核对立案信息',
   '（2026）浙0106民初08812号受理材料同步事项；核对当事人信息、送达方式和后续通知。', NULL,
   '2026-06-02T18:00:00+08:00', '2026-06-02T18:30:00+08:00', 0, 'tentative',
   '2026-06-01T09:31:00+08:00', '2026-06-01T09:31:00+08:00', NULL, NULL),
  ('evt_lending_sys_procedure_response', 'cal_wang_fang', '法院送达待办：程序意见准备',
   '受理材料提示被告已提出程序事项；具体书面意见内容和提交动作仍需王芳确认。', NULL,
   '2026-06-04T17:00:00+08:00', '2026-06-04T17:30:00+08:00', 0, 'tentative',
   '2026-06-01T09:31:00+08:00', '2026-06-01T09:31:00+08:00', NULL, NULL);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='event_seq';
COMMIT;
