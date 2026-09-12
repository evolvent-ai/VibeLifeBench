-- calendar_mock japan_20d — init.sql
-- Personal + Work calendars for usr_li_wei as visible before 2026-04-17.

BEGIN;

-- Calendars.
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_000001', 'usr_li_wei', 'Personal', '#4285F4', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z'),
  ('cal_000002', 'usr_li_wei', 'Work',     '#0B8043', 'Asia/Shanghai', 0, '2024-01-01T00:00:00Z');

-- Counters (seed prefixes so newly-issued IDs don't collide with seed IDs).
INSERT INTO _counters (key, value) VALUES
  ('event_seq', 18),
  ('attendee_seq', 0),
  ('reminder_seq', 0);

-- ------------------------------------------------------------------
-- Family events (Personal calendar)
-- ------------------------------------------------------------------
-- Mom's birthday (5/8) — all-day-ish placeholder, evening dinner.
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000001', 'cal_000001', 'Momtranslated content (Mom''s Birthday Dinner)',
   'translated content。Calling mom in the morning.', 'Shanghai·translated content',
   '2026-05-08T18:30:00+08:00', '2026-05-08T21:00:00+08:00',
   0, 'confirmed', '2026-04-01T09:00:00Z', '2026-04-01T09:00:00Z', NULL, NULL);

-- Dad's doctor appointment (5/12 9am).
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000002', 'cal_000001', 'translated contentDadtranslated content (Dad - Cardiology Follow-up)',
   'translated content - translated content。Bring previous ECG report.', 'translated content translated content',
   '2026-05-12T09:00:00+08:00', '2026-05-12T11:00:00+08:00',
   0, 'confirmed', '2026-04-10T10:00:00Z', '2026-04-10T10:00:00Z', NULL, NULL);

-- Anniversary dinner with spouse (4/22).
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000003', 'cal_000001', 'translated content (Anniversary Dinner)',
   'translated content，translated content。', 'Shanghai·translated content',
   '2026-04-22T19:00:00+08:00', '2026-04-22T22:00:00+08:00',
   0, 'confirmed', '2026-03-15T08:00:00Z', '2026-03-15T08:00:00Z', NULL, NULL);

-- Parent-teacher meeting (4/18 Sat morning).
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000004', 'cal_000001', 'translated content (School Parent-Teacher Meeting)',
   'translated content，translated content。', 'Shanghaitranslated content',
   '2026-04-18T09:00:00+08:00', '2026-04-18T11:30:00+08:00',
   0, 'confirmed', '2026-04-05T12:00:00Z', '2026-04-05T12:00:00Z', NULL, NULL);

-- ------------------------------------------------------------------
-- Recurring weekly events (Personal calendar)
-- ------------------------------------------------------------------
-- Thursday 7pm yoga class (recurring weekly until 2026-12-31).
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000005', 'cal_000001', 'translated content (Yoga Class)',
   'Hatha yoga, intermediate. Towel + mat.', 'translated content Pure Yoga',
   '2026-04-02T19:00:00+08:00', '2026-04-02T20:00:00+08:00',
   0, 'confirmed', '2026-01-15T00:00:00Z', '2026-01-15T00:00:00Z',
   'FREQ=WEEKLY;BYDAY=TH;UNTIL=20261231', NULL);

-- Wednesday morning swim (recurring weekly until 2026-08-31).
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000006', 'cal_000001', 'translated content (Morning Swim)',
   '50 laps. Pack goggles + cap.', 'translated content',
   '2026-04-01T07:00:00+08:00', '2026-04-01T08:00:00+08:00',
   0, 'confirmed', '2026-01-15T00:00:00Z', '2026-01-15T00:00:00Z',
   'FREQ=WEEKLY;BYDAY=WE;UNTIL=20260831', NULL);

-- ------------------------------------------------------------------
-- Recurring weekly events (Work calendar)
-- ------------------------------------------------------------------
-- Monday 9am team sync.
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000007', 'cal_000002', 'Team Sync (Weekly)',
   'Standing weekly sync. Agenda in Notion.', 'Zoom - team room A',
   '2026-04-06T09:00:00+08:00', '2026-04-06T09:30:00+08:00',
   0, 'confirmed', '2026-01-15T00:00:00Z', '2026-01-15T00:00:00Z',
   'FREQ=WEEKLY;BYDAY=MO;UNTIL=20261231', NULL);

-- Friday 4pm 1:1 with manager.
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000008', 'cal_000002', '1:1 with Manager (Wang Jun)',
   'Bi-weekly career check-in.', 'Zoom',
   '2026-04-03T16:00:00+08:00', '2026-04-03T16:30:00+08:00',
   0, 'confirmed', '2026-01-15T00:00:00Z', '2026-01-15T00:00:00Z',
   'FREQ=WEEKLY;BYDAY=FR;UNTIL=20261231', NULL);

-- ------------------------------------------------------------------
-- One-off work events
-- ------------------------------------------------------------------
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000009', 'cal_000002', 'Q2 Planning Review',
   'Review Q2 OKRs with leadership. Slides due Mon EOD.', 'Office HQ - Room 4F-302',
   '2026-04-21T14:00:00+08:00', '2026-04-21T16:00:00+08:00',
   0, 'confirmed', '2026-04-01T00:00:00Z', '2026-04-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000010', 'cal_000002', 'Customer Interview - Acme Co',
   'Discovery call with Acme product team.', 'Zoom',
   '2026-04-29T10:00:00+08:00', '2026-04-29T11:00:00+08:00',
   0, 'confirmed', '2026-04-15T00:00:00Z', '2026-04-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000011', 'cal_000002', 'Internal All-Hands',
   'Quarterly all-hands. CEO Q&A.', 'Office HQ - Auditorium',
   '2026-05-06T15:00:00+08:00', '2026-05-06T16:30:00+08:00',
   0, 'confirmed', '2026-04-16T00:00:00Z', '2026-04-16T00:00:00Z', NULL, NULL);

-- ------------------------------------------------------------------
-- Ordinary future commitments.  The Japan trip itself is deliberately
-- absent: Stage 0 asks the agent to create the first durable trip hold.
-- ------------------------------------------------------------------
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000012', 'cal_000001', 'Family video call with Aunt Liu',
   'Monthly family check-in; confirm whether the time still works.',
   'WeChat video',
   '2026-05-15T19:30:00+08:00', '2026-05-15T20:15:00+08:00',
   0, 'tentative', '2026-03-01T00:00:00Z', '2026-04-15T00:00:00Z', NULL, NULL);

-- A work deadline that creates natural calendar search context.
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000013', 'cal_000002', 'Q2 release handoff review',
   'Confirm owner, escalation contact, and unresolved customer tickets.', 'Office HQ - Room 3F-208',
   '2026-04-30T16:00:00+08:00', '2026-04-30T17:00:00+08:00',
   0, 'confirmed', '2026-03-05T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

-- A non-travel personal commitment near the planning window.
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000014', 'cal_000001', 'Community first-aid refresher',
   'Bring the prior course card; registration is tentative until payment.', 'translated content',
   '2026-04-26T14:00:00+08:00', '2026-04-26T16:00:00+08:00',
   0, 'tentative', '2026-04-12T00:00:00Z', '2026-04-12T00:00:00Z', NULL, NULL);

-- ------------------------------------------------------------------
-- A couple of past events (April) for "what happened last week" queries.
-- ------------------------------------------------------------------
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
  ('evt_00000015', 'cal_000001', 'translated content (Annual Physical)',
   'translated content。translated content。', 'translated content',
   '2026-04-10T08:00:00+08:00', '2026-04-10T10:30:00+08:00',
   0, 'confirmed', '2026-03-20T00:00:00Z', '2026-04-10T11:00:00Z', NULL, NULL);

-- Events created after event-000 are released with their source event rather
-- than being visible in the initial calendar snapshot.

-- ------------------------------------------------------------------
-- Attendees / reminders for a few flagship events.
-- ------------------------------------------------------------------
INSERT INTO attendees (event_id, email, name, response_status) VALUES
  ('evt_00000001', 'zhangfang@example.com', 'Mom Zhang Fang',     'accepted'),
  ('evt_00000001', 'libo@example.com',     'Dad translated content',      'accepted'),
  ('evt_00000001', 'spouse@example.com',   'translated content',           'accepted'),
  ('evt_00000002', 'libo@example.com',     'Dad translated content',      'accepted'),
  ('evt_00000007', 'chenwei@example.com',  'Chen Wei',       'accepted'),
  ('evt_00000007', 'wangjun@example.com',  'Wang Jun',       'accepted'),
  ('evt_00000007', 'liyan@example.com',    'Li Yan',         'needsAction'),
  ('evt_00000008', 'wangjun@example.com',  'Wang Jun',       'accepted'),
  ('evt_00000009', 'wangjun@example.com',  'Wang Jun',       'accepted'),
  ('evt_00000009', 'cfo@example.com',      'CFO',            'accepted'),
  ('evt_00000010', 'acme.pm@example.com',  'Acme PM',        'accepted'),
  ('evt_00000011', 'allhands@example.com', 'All-Hands List', 'accepted');

INSERT INTO reminders (event_id, method, minutes_before) VALUES
  ('evt_00000001', 'popup', 60),
  ('evt_00000001', 'email', 1440),
  ('evt_00000002', 'popup', 30),
  ('evt_00000007', 'popup', 10),
  ('evt_00000008', 'popup', 10),
  ('evt_00000009', 'popup', 60),
  ('evt_00000010', 'popup', 15),
  ('evt_00000012', 'email', 4320),
  ('evt_00000014', 'popup', 120);

COMMIT;
