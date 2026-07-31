BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_lending_sys_appeal_response_due', 'cal_wang_fang', '法院送达：二审答辩期限节点',
   '按2026年6月20日收到上诉状副本起算15日暂记；应结合送达回证核对最终截止时点。', NULL,
   '2026-07-05T17:00:00+08:00', '2026-07-05T17:30:00+08:00', 0, 'tentative',
   '2026-06-20T08:51:00+08:00', '2026-06-20T08:51:00+08:00', NULL, NULL),
  ('evt_lending_sys_second_evidence_review', 'cal_wang_fang', '二审送达待办：证据目录复核',
   '按二审举证通知整理证据目录并区分一审已提交材料与补充材料；正式提交须本人确认。', NULL,
   '2026-06-26T16:00:00+08:00', '2026-06-26T16:30:00+08:00', 0, 'tentative',
   '2026-06-20T08:51:00+08:00', '2026-06-20T08:51:00+08:00', NULL, NULL);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='event_seq';
COMMIT;
