INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_linche_main_003', 'user_lin_che', 'Lin CheEnglish textdayEnglish text', '#1f77b4', 'Asia/Shanghai', 1, '2026-09-01T08:00:00+08:00');
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('cal_sg_flight_0917', 'cal_linche_main_003', '上海到新加坡项目航班', '长途出差日，晚间只适合轻量复盘。', 'PVG-SIN', '2026-09-17T09:30:00+08:00', '2026-09-17T15:00:00+08:00', 0, 'confirmed', '2026-09-01T08:00:00+08:00', '2026-09-01T08:00:00+08:00', NULL, NULL);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('cal_london_call_0924', 'cal_linche_main_003', '伦敦客户夜间电话', '跨时区会议，第二天早晨不排高强度模考。', 'Zoom', '2026-09-24T22:30:00+08:00', '2026-09-25T00:30:00+08:00', 0, 'confirmed', '2026-09-01T08:00:00+08:00', '2026-09-01T08:00:00+08:00', NULL, NULL);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('cal_client_workshop_hk_0929', 'cal_linche_main_003', '香港客户工作坊', '香港线下客户会议，不可取消。', 'Hong Kong', '2026-09-29T10:00:00+08:00', '2026-09-29T18:00:00+08:00', 0, 'confirmed', '2026-09-01T08:00:00+08:00', '2026-09-01T08:00:00+08:00', NULL, NULL);
INSERT INTO _counters (key, value) VALUES ('event_seq', 9000);

-- Handbook v1.14 remediation: replace generic calendar distractors with distinct consulting,
-- travel, study, and application commitments.  The paired topic/constraint facts create a
-- realistic retrieval space while preserving every original row.
WITH facts AS (
  SELECT rowid AS rid,
    CASE rowid % 17
      WHEN 0 THEN 'clientEnglish text' WHEN 1 THEN 'countEnglish text' WHEN 2 THEN 'programEnglish text'
      WHEN 3 THEN 'crosstime zoneEnglish text' WHEN 4 THEN 'English textsessionEnglish text' WHEN 5 THEN 'English textreminder'
      WHEN 6 THEN 'English textincorrect questionsEnglish text' WHEN 7 THEN 'English text' WHEN 8 THEN 'countEnglish textchartsEnglish text'
      WHEN 9 THEN 'MBA programdescriptionEnglish text' WHEN 10 THEN 'English text' WHEN 11 THEN 'scorescore sendingpolicyEnglish text'
      WHEN 12 THEN 'clientEnglish textschedule' WHEN 13 THEN 'English textandidentificationEnglish textcheck' WHEN 14 THEN 'English text'
      WHEN 15 THEN 'English text' ELSE 'English textpleaseEnglish textorganize' END AS topic,
    CASE rowid % 19
      WHEN 0 THEN 'notcanEnglish text，English textexamEnglish text' WHEN 1 THEN 'canaroundEnglish text' WHEN 2 THEN 'English textatclientEnglish textafterEnglish text'
      WHEN 3 THEN 'English textcanEnglish text' WHEN 4 THEN 'English textafterEnglish textgiveprogramEnglish text' WHEN 5 THEN 'andHong Kongtime zoneEnglish text'
      WHEN 6 THEN 'andSingaporebusiness travelEnglish text' WHEN 7 THEN 'needretainEnglish text' WHEN 8 THEN 'English textflightEnglish text'
      WHEN 9 THEN 'onlydoEnglish text，notEnglish textschedulemock exam' WHEN 10 THEN 'English textfirstEnglish textofficialEnglish text' WHEN 11 THEN 'notEnglish textclientworkshop'
      WHEN 12 THEN 'English textandEnglish text' WHEN 13 THEN 'English textnotEnglish textplease' WHEN 14 THEN 'English textafterEnglish textscheduleEnglish text'
      WHEN 15 THEN 'English textworkEnglish text' WHEN 16 THEN 'useemailconfirmedtimeas authority' WHEN 17 THEN 'English textretaincancelledEnglish text'
      ELSE 'English texttotalstudyEnglish textnotEnglish text' END AS constraint_text
  FROM events WHERE event_id LIKE 'cal_noise_examprep_%'
)
UPDATE events
SET summary = (SELECT topic FROM facts WHERE facts.rid = events.rowid),
    description = CASE events.rowid % 7
      WHEN 0 THEN (SELECT topic || 'alreadyconfirmed；' || constraint_text || '。' FROM facts WHERE facts.rid=events.rowid)
      WHEN 1 THEN (SELECT 'English textschedulechange，' || topic || 'English textretain；' || constraint_text || '。' FROM facts WHERE facts.rid=events.rowid)
      WHEN 2 THEN (SELECT constraint_text || '；English texton' || topic || '，English textafterrecordEnglish text。' FROM facts WHERE facts.rid=events.rowid)
      WHEN 3 THEN (SELECT topic || 'andEnglish textdayEnglish textplanEnglish textatEnglish text，English textas：' || constraint_text || '。' FROM facts WHERE facts.rid=events.rowid)
      WHEN 4 THEN (SELECT 'dayEnglish text：' || topic || '。English textis' || constraint_text || '。' FROM facts WHERE facts.rid=events.rowid)
      WHEN 5 THEN (SELECT 'retainEnglish text' || topic || '；English text，' || constraint_text || '。' FROM facts WHERE facts.rid=events.rowid)
      ELSE (SELECT topic || 'English textonEnglish texthasEnglish textschedule，statusalreadyconfirmed；' || constraint_text || '。' FROM facts WHERE facts.rid=events.rowid)
    END,
    event_id = replace(event_id, 'cal_noise_examprep_', 'cal_commitment_archive_')
WHERE event_id LIKE 'cal_noise_examprep_%';
