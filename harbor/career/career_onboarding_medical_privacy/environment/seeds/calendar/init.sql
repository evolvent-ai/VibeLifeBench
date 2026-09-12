-- calendar_mock seed: career_onboarding_medical_privacy. Times Asia/Shanghai.
BEGIN;
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_privacy','usr_gao_kai','Mina Huo','#6A5ACD','Asia/Shanghai',1,'2019-04-12T00:00:00Z');
INSERT INTO _counters (key, value) VALUES ('event_seq',10),('attendee_seq',0),('reminder_seq',0);
-- Only facts that existed by event-000 (2026-06-08T11:00:00+08:00) belong in t=0.
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_gk_0001','cal_privacy','Private Follow-up','Private personal appointment; no diagnosis or examination details are exposed.','Puhe Occupational Health Center','2026-06-07T18:30:00+08:00','2026-06-07T19:30:00+08:00',0,'confirmed','2026-06-01T00:00:00Z','2026-06-01T00:00:00Z',NULL,NULL);
COMMIT;
