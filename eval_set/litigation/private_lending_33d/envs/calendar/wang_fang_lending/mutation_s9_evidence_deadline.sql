BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_lending_sys_evidence_due', 'cal_wang_fang', '法院送达：举证期限节点',
   '按2026年6月2日收到举证通知起算15日暂记；应结合电子送达时间核对最终截止时点。', NULL,
   '2026-06-17T17:00:00+08:00', '2026-06-17T17:30:00+08:00', 0, 'tentative',
   '2026-06-02T09:21:00+08:00', '2026-06-02T09:21:00+08:00', NULL, NULL),
  ('evt_lending_sys_preservation_followup', 'cal_wang_fang', '法院送达待办：核对财产保全进展',
   '法院已开始办理查封或冻结手续；该事件为送达同步，后续跟进和补充材料需本人确认。', NULL,
   '2026-06-05T10:00:00+08:00', '2026-06-05T10:30:00+08:00', 0, 'tentative',
   '2026-06-02T09:21:00+08:00', '2026-06-02T09:21:00+08:00', NULL, NULL);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='event_seq';
COMMIT;
