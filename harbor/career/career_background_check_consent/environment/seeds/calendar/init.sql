-- Curated Stage-0 seed for career_background_check_consent / calendar.

BEGIN;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_sw_primary', 'usr_sang_wu', 'Sang Wutranslated textprimary calendar', '#4F46E5', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_sw_prenatal_wed', 'cal_sw_primary', 'translated textspousetranslated text', 'Ling Botranslated text，translated text。', 'translated text', '2026-06-10T09:00:00+08:00', '2026-06-10T11:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', 'FREQ=WEEKLY;BYDAY=WE;UNTIL=20261021', NULL),
  ('evt_sw_handover_review', 'cal_sw_primary', 'transaction middlewaretranslated text', 'translated textcurrenttranslated textservice、translated textincompletetranslated text。', 'Yanmu Network', '2026-06-11T14:00:00+08:00', '2026-06-11T15:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_contract_archive', 'cal_sw_primary', 'translated text', 'hometranslated text、translated text。', 'home', '2026-06-13T10:00:00+08:00', '2026-06-13T11:00:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_access_handover', 'cal_sw_primary', 'translated text', 'translated textplatformresponsible fortranslated textmeeting，translated textgrouptranslated text。', 'Yanmu Network', '2026-06-18T15:00:00+08:00', '2026-06-18T16:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_cashflow_review', 'cal_sw_primary', 'mortgagetranslated texthouseholdtranslated textretrospective', 'translated textreconciletranslated text、translated textemergencytranslated text。', 'home', '2026-06-20T19:30:00+08:00', '2026-06-20T20:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_resume_review', 'cal_sw_primary', 'translated textresumetranslated text', 'translated textresumecurrenttranslated textsystemtranslated text，translated text。', 'online', '2026-06-21T20:00:00+08:00', '2026-06-21T21:00:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_docs_handover', 'cal_sw_primary', 'translated textconfirm', 'translated text，translated textemergencytranslated textdo nottranslated text。', 'Yanmu Network', '2026-06-25T10:00:00+08:00', '2026-06-25T11:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_device_return', 'cal_sw_primary', 'translated text', 'translated text、translated text，translated text。', 'Yanmu Network', '2026-06-29T16:00:00+08:00', '2026-06-29T17:00:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_last_workday', 'cal_sw_primary', 'last working day', 'HR systemtranslated textlast working daytranslated text 6 translated text 30 translated text，translated text 20:00。', 'Yanmu Network', '2026-06-30T09:00:00+08:00', '2026-06-30T18:00:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_job_search_evening', 'cal_sw_primary', 'Shanghaibackendroletranslated text', 'translated textShanghaitranslated textroletranslated text。', 'online', '2026-07-01T19:30:00+08:00', '2026-07-01T21:00:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_dev_meetup', 'cal_sw_primary', 'developmenttranslated textcommunitytranslated text', 'translated textsubjecttranslated textcasetranslated text，translated textconfirmemailtranslated text。', 'translated textdaytranslated text', '2026-07-04T14:00:00+08:00', '2026-07-04T16:30:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_family_weekly', 'cal_sw_primary', 'householdweektranslated text', 'translated textweekhouseholdtranslated text、weektranslated textweektranslated text。', 'home', '2026-07-05T20:00:00+08:00', '2026-07-05T20:45:00+08:00', 0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL),
  ('evt_sw_mortgage_reset', 'cal_sw_primary', 'mortgagetranslated textmaterialstranslated text', 'translated text App translated text 7 translated text 1 translated text，translated text。', 'home', '2026-05-16T19:10:00+08:00', '2026-05-16T19:50:00+08:00', 0, 'confirmed', '2026-05-11T07:25:00Z', '2026-05-16T12:08:00Z', NULL, NULL),
  ('evt_sw_recycling_pickup', 'cal_sw_primary', 'communitytranslated text', 'translated text，translated text。', 'translated text', '2026-05-22T08:20:00+08:00', '2026-05-22T08:50:00+08:00', 0, 'confirmed', '2026-05-18T03:14:00Z', '2026-05-22T01:02:00Z', NULL, NULL),
  ('evt_sw_java_meetup', 'cal_sw_primary', 'Java translated text', 'translated textsubjecttranslated textservicetranslated text，translated textsigntranslated text。', 'translated text', '2026-05-28T19:00:00+08:00', '2026-05-28T21:10:00+08:00', 0, 'confirmed', '2026-05-20T10:36:00Z', '2026-05-28T13:35:00Z', NULL, NULL),
  ('evt_sw_parent_router', 'cal_sw_primary', 'translated text', 'translated text，translated text。', 'translated text', '2026-06-01T14:30:00+08:00', '2026-06-01T16:20:00+08:00', 0, 'confirmed', '2026-05-29T05:45:00Z', '2026-06-01T09:02:00Z', NULL, NULL),
  ('evt_sw_glasses_pickup', 'cal_sw_primary', 'translated text', 'translated text 1.67 translated text，translated textrecordtranslated text。', 'translated text', '2026-06-05T18:25:00+08:00', '2026-06-05T19:05:00+08:00', 0, 'confirmed', '2026-06-02T02:22:00Z', '2026-06-05T11:48:00Z', NULL, NULL);

INSERT INTO _counters (key, value) VALUES
  ('calendar_seq', 1),
  ('event_seq', 17),
  ('attendee_seq', 0),
  ('reminder_seq', 0);

COMMIT;
