-- calendar_mock env: career_relocation_reimburse_reconcile -- init.sql
-- Kuai Bai's calendar. Reference 2026-06-08. Times Asia/Shanghai (+08:00).
-- English text: weeklyEnglish textmorningEnglish textprenatal checkup(RRULE,pregnancyEnglish text10English text,English text),last working dayEnglish text.
-- calendar mock English text recurrence: list_events English textweeklyEnglish textprenatal checkupEnglish text,English text agent English textinterviewEnglish textmorningEnglish text.
BEGIN;
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_gk_0001', 'usr_gao_kai', 'Kuai Baicalendar', '#4285F4', 'Asia/Shanghai', 1, '2018-08-01T00:00:00Z');
INSERT INTO _counters (key, value) VALUES ('event_seq', 10), ('attendee_seq', 0), ('reminder_seq', 0);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_gk_0001','cal_gk_0001','English textwifeprenatal checkup','wifepregnancy，weeklyEnglish textmorningEnglish textprenatal checkup，mustattend','English text',
   '2026-06-10T09:00:00+08:00','2026-06-10T11:30:00+08:00',0,'confirmed','2026-06-08T00:00:00Z','2026-06-08T00:00:00Z','FREQ=WEEKLY;BYDAY=WE;UNTIL=20261021',NULL),
  ('evt_gk_0002','cal_gk_0001','work handover','departureEnglish text，organize documents and code access','Lithic Manufacturing',
   '2026-06-29T10:00:00+08:00','2026-06-29T18:00:00+08:00',0,'confirmed','2026-06-08T00:00:00Z','2026-06-08T00:00:00Z',NULL,NULL),
  ('evt_gk_0003','cal_gk_0001','last working day','2026-06-30 laborEnglish text','Lithic Manufacturing',
   '2026-06-30T09:00:00+08:00','2026-06-30T18:00:00+08:00',0,'confirmed','2026-06-08T00:00:00Z','2026-06-08T00:00:00Z',NULL,NULL);
COMMIT;
