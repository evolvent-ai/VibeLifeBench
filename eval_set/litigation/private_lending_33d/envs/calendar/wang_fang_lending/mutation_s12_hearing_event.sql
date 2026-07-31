BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_lending_sys_hearing', 'cal_wang_fang', '法院传票：王芳诉陈强民间借贷纠纷开庭',
   '案号（2026）浙0106民初08812号。法院要求携带身份证、借条原件、银行转账回单、微信记录及其他证据原件。',
   '杭州市西湖区人民法院第五法庭',
   '2026-06-12T09:30:00+08:00', '2026-06-12T12:00:00+08:00', 0, 'confirmed',
   '2026-06-08T09:41:00+08:00', '2026-06-08T09:41:00+08:00', NULL, NULL);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='event_seq';
COMMIT;
