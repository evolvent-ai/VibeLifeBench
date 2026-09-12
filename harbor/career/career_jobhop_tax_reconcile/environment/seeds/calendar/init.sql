-- calendar_mock seed: career_jobhop_tax_reconcile. Times Asia/Shanghai.
BEGIN;
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_gk_0001','usr_gao_kai','record','#4285F4','Asia/Shanghai',1,'2018-08-01T00:00:00Z');
INSERT INTO _counters (key, value) VALUES ('event_seq',10),('attendee_seq',0),('reminder_seq',0);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_gk_0001','cal_gk_0001','record','record，record','record','2026-06-08T09:00:00+08:00','2026-06-08T10:30:00+08:00',0,'confirmed','2026-06-01T00:00:00Z','2026-06-01T00:00:00Z',NULL,NULL),
  ('evt_gk_0002','cal_gk_0001','2025 record','record、record，record','record','2026-06-08T06:30:00+08:00','2026-06-08T07:30:00+08:00',0,'confirmed','2026-06-07T00:00:00Z','2026-06-07T00:00:00Z',NULL,NULL),
  ('evt_gk_0003','cal_gk_0001','record','record、record','record','2026-06-08T07:30:00+08:00','2026-06-08T08:30:00+08:00',0,'tentative','2026-06-07T00:00:00Z','2026-06-07T00:00:00Z',NULL,NULL),
  ('evt_payroll_archive','cal_gk_0001','record','record、record','record','2026-05-24T09:30:00+08:00','2026-05-24T11:00:00+08:00',0,'confirmed','2026-05-18T08:12:00Z','2026-05-24T03:08:00Z',NULL,NULL),
  ('evt_family_school','cal_gk_0001','record','record，record','record','2026-06-08T09:00:00+08:00','2026-06-08T10:30:00+08:00',0,'confirmed','2026-06-06T11:02:00Z','2026-06-06T11:02:00Z',NULL,NULL),
  ('evt_observability_forum','cal_gk_0001','record','record，record','record','2026-06-08T10:45:00+08:00','2026-06-08T11:00:00+08:00',0,'confirmed','2026-05-21T12:18:00Z','2026-06-02T09:05:00Z',NULL,NULL),
  ('evt_dental_june','cal_gk_0001','record','record，record','record','2026-06-08T08:00:00+08:00','2026-06-08T08:50:00+08:00',0,'confirmed','2026-05-30T03:49:00Z','2026-05-30T03:49:00Z',NULL,NULL),
  ('evt_resume_review','cal_gk_0001','record','record、record，record','record','2026-06-08T07:00:00+08:00','2026-06-08T07:50:00+08:00',0,'tentative','2026-06-04T10:26:00Z','2026-06-07T13:44:00Z',NULL,NULL),
  ('evt_mortgage_budget','cal_gk_0001','record','record、record，record','record','2026-06-08T06:00:00+08:00','2026-06-08T06:45:00+08:00',0,'confirmed','2026-06-03T12:33:00Z','2026-06-05T07:18:00Z',NULL,NULL),
  ('evt_bank_export_check','cal_gk_0001','record','record','record','2026-06-08T10:00:00+08:00','2026-06-08T10:45:00+08:00',0,'confirmed','2026-06-08T01:02:00Z','2026-06-08T01:02:00Z',NULL,NULL),
  ('evt_drill_retrospective','cal_gk_0001','record','record，record','record','2026-06-08T08:00:00+08:00','2026-06-08T08:40:00+08:00',0,'tentative','2026-06-02T05:14:00Z','2026-06-06T02:31:00Z',NULL,NULL),
  ('evt_midyear_leave','cal_gk_0001','record','record，record','record','2026-06-08T05:00:00+08:00','2026-06-08T05:30:00+08:00',0,'tentative','2026-05-12T06:25:00Z','2026-06-01T04:38:00Z',NULL,NULL),
  ('evt_document_backup','cal_gk_0001','record','record、record；record','record','2026-06-08T09:00:00+08:00','2026-06-08T09:50:00+08:00',0,'confirmed','2026-06-05T15:22:00Z','2026-06-05T15:22:00Z',NULL,NULL);
COMMIT;
