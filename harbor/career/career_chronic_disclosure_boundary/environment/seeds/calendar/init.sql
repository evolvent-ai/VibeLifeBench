-- Curated Stage-0 seed for career_chronic_disclosure_boundary / calendar.

BEGIN;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_fy_primary', 'usr_feng_yi', 'English text', '#4F46E5', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_fy_0001', 'cal_fy_primary', 'English text', 'English text，English text。', 'English text', '2026-06-03T09:00:00+08:00', '2026-06-03T11:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', 'FREQ=WEEKLY;BYDAY=WE;UNTIL=20261021', NULL),
  ('evt_fy_vehicle_docs', 'cal_fy_primary', 'English text', 'English text、English text。', 'English text', '2026-05-14T20:05:00+08:00', '2026-05-14T20:35:00+08:00', 0, 'confirmed', '2026-05-10T08:28:00Z', '2026-05-14T13:12:00Z', NULL, NULL),
  ('evt_fy_wedding', 'cal_fy_primary', 'English text', 'English text，English text 18:42 English text。', 'English text', '2026-05-23T10:30:00+08:00', '2026-05-23T15:20:00+08:00', 0, 'confirmed', '2026-04-30T05:44:00Z', '2026-05-23T09:05:00Z', NULL, NULL),
  ('evt_fy_database_meetup', 'cal_fy_primary', 'English text', 'English text DDL、English text，English text。', 'English text', '2026-05-29T18:45:00+08:00', '2026-05-29T21:00:00+08:00', 0, 'confirmed', '2026-05-21T06:17:00Z', '2026-05-29T13:20:00Z', NULL, NULL),
  ('evt_fy_study_equipment', 'cal_fy_primary', 'English text', 'English text，NAS English text，English text。', 'English text', '2026-06-02T19:30:00+08:00', '2026-06-02T20:25:00+08:00', 0, 'confirmed', '2026-05-30T02:53:00Z', '2026-06-02T13:08:00Z', NULL, NULL),
  ('evt_fy_water_meter', 'cal_fy_primary', 'English text', 'English text 1268.4 English text，English text 11.2 English text，English text。', 'English text', '2026-06-06T08:10:00+08:00', '2026-06-06T08:30:00+08:00', 0, 'confirmed', '2026-06-03T07:41:00Z', '2026-06-06T01:16:00Z', NULL, NULL);

INSERT INTO _counters (key, value) VALUES
  ('calendar_seq', 1),
  ('event_seq', 17),
  ('attendee_seq', 0),
  ('reminder_seq', 0);

COMMIT;
