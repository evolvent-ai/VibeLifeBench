-- Calendar seed for galapagos_no_us_transit.
--
-- STAGE-0 WORLD ONLY. This is Lin Qiao's ordinary working diary as it stood on
-- 2026-07-24, plus the two immovable commitments that bracket the trip and the
-- workshop sessions she put in when she accepted the invitation back in June.
--
-- Nothing here is a future reveal: no hold expiry, no flight, no hotel, no
-- transfer, no registration ETA. Those only exist once the agent creates them
-- or a later stage injects them.

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_linqiao_primary', 'linqiao', 'Lin Qiao', '#4285F4', 'Asia/Shanghai', 1, '2019-09-01T00:00:00Z'),
  ('cal_linqiao_teaching', 'linqiao', 'Teaching and supervision', '#0B8043', 'Asia/Shanghai', 0, '2021-09-01T00:00:00Z'),
  ('cal_linqiao_personal', 'linqiao', 'Personal', '#8E24AA', 'Asia/Shanghai', 0, '2019-09-01T00:00:00Z');

-- ---------------------------------------------------------------------------
-- The two boundaries that constrain the whole trip.
-- ---------------------------------------------------------------------------

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('ev_group_meeting_0814','cal_linqiao_primary','Group meeting (I chair)',
   'Monthly lab group meeting. Wang Rong confirmed this one cannot move.','Online',
   '2026-08-14T16:30:00+08:00','2026-08-14T17:30:00+08:00',0,'confirmed',
   '2026-07-10T17:25:00+08:00','2026-07-10T17:25:00+08:00',NULL,NULL),
  ('ev_faculty_meeting_0825','cal_linqiao_primary','Faculty meeting - funding line on agenda',
   'In person. Wang Rong: cannot move, my funding line is on the agenda.','Building A, room 402',
   '2026-08-25T14:00:00+08:00','2026-08-25T16:00:00+08:00',0,'confirmed',
   '2026-07-10T17:26:00+08:00','2026-07-10T17:26:00+08:00',NULL,NULL);

-- ---------------------------------------------------------------------------
-- Workshop sessions, entered from the invitation in June. Local island time.
-- ---------------------------------------------------------------------------

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('ev_workshop_open_0818','cal_linqiao_primary','Workshop opening session',
   'Galapagos Ecology Data Workshop 2026, day one: instrumentation and station metadata.',
   'Puerto Ayora Marine Data Lab, Avenida Charles Darwin 102',
   '2026-08-18T09:00:00-06:00','2026-08-18T17:00:00-06:00',0,'confirmed',
   '2026-06-16T09:00:00-06:00','2026-07-03T15:20:00-06:00',NULL,NULL),
  ('ev_workshop_day2_0819','cal_linqiao_primary','Workshop day two - shore transect',
   'Outdoor session, walked from the beach. Depends on marine conditions.',
   'Puerto Ayora Marine Data Lab',
   '2026-08-19T08:30:00-06:00','2026-08-19T17:00:00-06:00',0,'confirmed',
   '2026-07-03T15:20:00-06:00','2026-07-03T15:20:00-06:00',NULL,NULL),
  ('ev_workshop_day3_0820','cal_linqiao_primary','Workshop day three - reserve dataset',
   'Tortoise reserve dataset session.','Puerto Ayora Marine Data Lab',
   '2026-08-20T09:00:00-06:00','2026-08-20T17:00:00-06:00',0,'confirmed',
   '2026-07-03T15:20:00-06:00','2026-07-03T15:20:00-06:00',NULL,NULL),
  ('ev_workshop_day4_0821','cal_linqiao_primary','Workshop day four - joint analysis',
   'Joint analysis session.','Puerto Ayora Marine Data Lab',
   '2026-08-21T09:00:00-06:00','2026-08-21T17:00:00-06:00',0,'confirmed',
   '2026-07-03T15:20:00-06:00','2026-07-03T15:20:00-06:00',NULL,NULL),
  ('ev_workshop_close_0822','cal_linqiao_primary','Workshop closing session',
   'Closing session ends at midday, followed by the closing reception.',
   'Puerto Ayora Marine Data Lab',
   '2026-08-22T09:00:00-06:00','2026-08-22T12:00:00-06:00',0,'confirmed',
   '2026-06-16T09:00:00-06:00','2026-06-16T09:00:00-06:00',NULL,NULL),
  ('ev_workshop_optional_0823','cal_linqiao_primary','Optional excursion (boat) - probably skipping',
   'Optional Sunday boat excursion. Not programme content. Xu Wen will not be going.',
   'Puerto Ayora',
   '2026-08-23T08:00:00-06:00','2026-08-23T13:00:00-06:00',0,'tentative',
   '2026-07-06T11:10:00-06:00','2026-07-06T11:10:00-06:00',NULL,NULL);

-- ---------------------------------------------------------------------------
-- Ordinary July/August diary: a real calendar, not a stage script.
-- ---------------------------------------------------------------------------

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('ev_supervision_zhaomin_0727','cal_linqiao_teaching','Supervision: Zhao Min, chapter 3',
   'Go through the redone seasonal decomposition before I travel.','Office',
   '2026-07-27T14:00:00+08:00','2026-07-27T15:00:00+08:00',0,'confirmed',
   '2026-07-21T09:00:00+08:00','2026-07-21T09:00:00+08:00',NULL,NULL),
  ('ev_lab_meeting_0731','cal_linqiao_primary','Lab meeting',
   'Standing weekly lab meeting.','Building A, room 210',
   '2026-07-31T10:00:00+08:00','2026-07-31T11:30:00+08:00',0,'confirmed',
   '2026-01-05T09:00:00+08:00','2026-01-05T09:00:00+08:00','FREQ=WEEKLY;BYDAY=FR',NULL),
  ('ev_dentist_0805','cal_linqiao_personal','Dentist',
   'Six month check. Booked in February.','Clinic, Xuhui',
   '2026-08-05T18:30:00+08:00','2026-08-05T19:15:00+08:00',0,'confirmed',
   '2026-02-06T10:00:00+08:00','2026-02-06T10:00:00+08:00',NULL,NULL),
  ('ev_pharmacy_pickup_0726','cal_linqiao_personal','Collect pharmacy order 88231',
   'Motion sickness tablets, rehydration sachets, sun cream.','Pharmacy',
   '2026-07-26T11:00:00+08:00','2026-07-26T11:30:00+08:00',0,'confirmed',
   '2026-07-22T13:35:00+08:00','2026-07-22T13:35:00+08:00',NULL,NULL),
  ('ev_water_shutoff_0726','cal_linqiao_personal','Building water off',
   'Riser maintenance, block C.','Home',
   '2026-07-26T09:00:00+08:00','2026-07-26T15:00:00+08:00',0,'confirmed',
   '2026-07-22T18:05:00+08:00','2026-07-22T18:05:00+08:00',NULL,NULL),
  ('ev_grant_report_0810','cal_linqiao_primary','Interim grant report due',
   'Submit before I leave; the portal closes on the day.','Online',
   '2026-08-10T09:00:00+08:00','2026-08-10T10:00:00+08:00',0,'confirmed',
   '2026-05-14T09:00:00+08:00','2026-05-14T09:00:00+08:00',NULL,NULL),
  ('ev_xuwen_leave_start','cal_linqiao_personal','Xu Wen on leave',
   'Leave approved 14 to 25 August. Back at work on the 26th.','',
   '2026-08-14T00:00:00+08:00','2026-08-26T00:00:00+08:00',1,'confirmed',
   '2026-07-17T12:15:00+08:00','2026-07-17T12:15:00+08:00',NULL,NULL),
  ('ev_journal_review_declined','cal_linqiao_primary','(declined) Review MEE-2026-0417',
   'Declined: travelling for most of August.','',
   '2026-08-13T09:00:00+08:00','2026-08-13T09:30:00+08:00',0,'cancelled',
   '2026-07-16T19:05:00+02:00','2026-07-17T08:16:00+08:00',NULL,NULL),
  ('ev_teaching_prep_0901','cal_linqiao_teaching','Autumn module prep',
   'First lecture I actually give is week 3; cover handles weeks 1 and 2.','Office',
   '2026-09-01T14:00:00+08:00','2026-09-01T16:00:00+08:00',0,'tentative',
   '2026-06-01T10:05:00+08:00','2026-07-15T14:05:00+08:00',NULL,NULL);

INSERT INTO attendees (event_id, email, name, response_status) VALUES
  ('ev_group_meeting_0814','linqiao@example.com','Lin Qiao','accepted'),
  ('ev_group_meeting_0814','wang.rong@example.edu','Wang Rong','accepted'),
  ('ev_group_meeting_0814','zhao.min@example.edu','Zhao Min','needsAction'),
  ('ev_faculty_meeting_0825','linqiao@example.com','Lin Qiao','accepted'),
  ('ev_faculty_meeting_0825','wang.rong@example.edu','Wang Rong','accepted'),
  ('ev_workshop_open_0818','linqiao@example.com','Lin Qiao','accepted'),
  ('ev_workshop_open_0818','ops@galapagos-data.example','Galapagos Data Field Office','accepted'),
  ('ev_workshop_close_0822','linqiao@example.com','Lin Qiao','accepted'),
  ('ev_supervision_zhaomin_0727','zhao.min@example.edu','Zhao Min','accepted');

INSERT INTO reminders (event_id, method, minutes_before) VALUES
  ('ev_group_meeting_0814','popup',30),
  ('ev_faculty_meeting_0825','popup',120),
  ('ev_workshop_open_0818','popup',720),
  ('ev_grant_report_0810','email',1440),
  ('ev_pharmacy_pickup_0726','popup',60);

-- Additional reviewed pre-handover diary history: ten events, ten reminders and eleven attendees.
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<10)
INSERT INTO events(event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id)
SELECT printf('ev_history_reviewed_%02d',n),
       CASE n%3 WHEN 0 THEN 'cal_linqiao_primary' WHEN 1 THEN 'cal_linqiao_teaching' ELSE 'cal_linqiao_personal' END,
       CASE n WHEN 1 THEN 'Research data backup review' WHEN 2 THEN 'Student draft feedback' WHEN 3 THEN 'Department equipment inventory' WHEN 4 THEN 'Family dinner reservation' WHEN 5 THEN 'Insurance document check' WHEN 6 THEN 'Coastal dataset seminar' WHEN 7 THEN 'Passport storage review' WHEN 8 THEN 'Budget coding office hour' WHEN 9 THEN 'Field kit maintenance' ELSE 'Travel health consultation' END,
       CASE n WHEN 1 THEN 'Confirm the archive copy and checksum before closing the project folder.' WHEN 2 THEN 'Return comments on methods, figures and the reproducibility appendix.' WHEN 3 THEN 'Check borrowed sensors against the departmental asset register.' WHEN 4 THEN 'Meet family near home; no ticket or payment commitment is attached.' WHEN 5 THEN 'Review policy contact details and the claims-document checklist.' WHEN 6 THEN 'Present the shoreline time-series cleaning decisions to the lab.' WHEN 7 THEN 'Confirm physical document storage without copying identity numbers into notes.' WHEN 8 THEN 'Ask finance how shared costs should be separated in future claims.' WHEN 9 THEN 'Charge batteries, inspect seals and replace the first-aid consumables.' ELSE 'Discuss routine travel medication and motion-sickness planning with the clinic.' END,
       CASE n%5 WHEN 0 THEN 'Shanghai clinic' WHEN 1 THEN 'Online' WHEN 2 THEN 'Building A' WHEN 3 THEN 'Laboratory store' ELSE 'Near home' END,
       strftime('%Y-%m-%dT%H:00:00+08:00','2026-06-10 08:00:00','+'||((n-1)*3)||' days','+'||(n%8)||' hours'),
       strftime('%Y-%m-%dT%H:00:00+08:00','2026-06-10 09:00:00','+'||((n-1)*3)||' days','+'||(n%8)||' hours'),
       0,'confirmed','2026-06-01T09:00:00+08:00','2026-06-01T09:00:00+08:00',NULL,NULL
FROM seq;
INSERT INTO reminders(event_id,method,minutes_before)
SELECT event_id,CASE rowid%2 WHEN 0 THEN 'popup' ELSE 'email' END,CASE rowid%3 WHEN 0 THEN 30 WHEN 1 THEN 60 ELSE 180 END
FROM events WHERE event_id LIKE 'ev_history_reviewed_%';
INSERT INTO attendees(event_id,email,name,response_status)
SELECT event_id,'linqiao@example.com','Lin Qiao','accepted' FROM events WHERE event_id LIKE 'ev_history_reviewed_%';
INSERT INTO attendees(event_id,email,name,response_status)
VALUES ('ev_history_reviewed_06','wang.rong@example.edu','Wang Rong','accepted');
