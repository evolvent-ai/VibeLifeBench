BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS calendars (
    calendar_id TEXT PRIMARY KEY,
    user_id TEXT,
    name TEXT,
    color TEXT,
    timezone TEXT DEFAULT 'UTC',
    is_primary INTEGER DEFAULT 0,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    calendar_id TEXT,
    summary TEXT,
    description TEXT,
    location TEXT,
    start_dt TEXT,
    end_dt TEXT,
    all_day INTEGER DEFAULT 0,
    status TEXT DEFAULT 'confirmed',
    created_at TEXT,
    updated_at TEXT,
    recurrence_rule TEXT,
    FOREIGN KEY (calendar_id) REFERENCES calendars(calendar_id)
);

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
('cal_personal', 'usr_chen_yu', 'Personal', '#4285F4', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z'),
('cal_work', 'usr_chen_yu', 'Work', '#0B8043', 'Asia/Shanghai', 0, '2024-01-01T00:00:00Z');

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule) VALUES
('evt_anniversary_2026', 'cal_personal', 'Anniversary Dinner', 'Our 3rd wedding anniversary celebration', 'The Chairman Restaurant, Shanghai', '2026-05-30T19:00:00+08:00', '2026-05-30T22:00:00+08:00', 0, 'confirmed', '2026-05-01T10:00:00Z', '2026-05-01T10:00:00Z', NULL),
('evt_prenatal_jun3', 'cal_personal', 'Prenatal Checkup', 'Ultrasound examination with Dr. Wang', 'Shanghai Maternity Hospital', '2026-06-03T10:00:00+08:00', '2026-06-03T11:30:00+08:00', 0, 'confirmed', '2026-05-22T10:00:00Z', '2026-05-22T10:00:00Z', NULL),
('evt_bali_trip', 'cal_personal', 'Annual Leave Request (Draft)', 'Tentative leave window submitted to HR; travel bookings and segment dates are not confirmed.', 'Out of office', '2026-06-10', '2026-07-01', 1, 'tentative', '2026-05-15T08:00:00Z', '2026-05-15T08:00:00Z', NULL),
('evt_mother_arrival', 'cal_personal', 'Call Mom about passport renewal', 'Check whether the renewal appointment and document pickup date are confirmed; no flight has been purchased.', 'Phone', '2026-06-01T19:30:00+08:00', '2026-06-01T20:00:00+08:00', 0, 'tentative', '2026-05-20T08:15:00Z', '2026-05-20T08:15:00Z', NULL),
('evt_yoga_recurring', 'cal_personal', 'Prenatal Yoga Class', 'Weekly prenatal yoga with Meilin', 'YogaLife Studio, Shanghai', '2026-05-22T19:00:00+08:00', '2026-05-22T20:30:00+08:00', 0, 'confirmed', '2026-04-01T10:00:00Z', '2026-04-01T10:00:00Z', 'FREQ=WEEKLY;BYDAY=TH;UNTIL=20260609T235959Z'),
('evt_standup_recurring', 'cal_work', 'Daily Standup', 'Team daily standup meeting', 'Conference Room A / Zoom', '2026-05-19T10:00:00+08:00', '2026-05-19T10:30:00+08:00', 0, 'confirmed', '2026-01-01T10:00:00Z', '2026-01-01T10:00:00Z', 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;UNTIL=20260807T235959Z'),
('evt_sprint_review_recurring', 'cal_work', 'Sprint Review', 'Bi-weekly sprint review and retrospective', 'Conference Room B', '2026-05-23T15:00:00+08:00', '2026-05-23T17:00:00+08:00', 0, 'confirmed', '2026-01-01T10:00:00Z', '2026-01-01T10:00:00Z', 'FREQ=WEEKLY;BYDAY=FR;INTERVAL=2;UNTIL=20260807T235959Z'),
('evt_game_launch', 'cal_work', 'Game Launch Deadline', 'Final deadline for game launch', '', '2026-06-08', '2026-06-08', 1, 'confirmed', '2026-04-15T10:00:00Z', '2026-04-15T10:00:00Z', NULL),
('evt_sprint_planning', 'cal_work', 'Sprint Planning - Week 22', 'Planning for final sprint before launch', 'Conference Room A', '2026-06-02T14:00:00+08:00', '2026-06-02T16:00:00+08:00', 0, 'confirmed', '2026-05-18T09:00:00Z', '2026-05-18T09:00:00Z', NULL),
('evt_code_freeze', 'cal_work', 'Code Freeze', 'No new features - bug fixes only', '', '2026-06-07', '2026-06-07', 1, 'confirmed', '2026-05-01T10:00:00Z', '2026-05-01T10:00:00Z', NULL),
('evt_team_building', 'cal_work', 'Team Building Activity', 'Company team building at Riverside Park', 'Riverside Park, Shanghai', '2026-06-05T14:00:00+08:00', '2026-06-05T18:00:00+08:00', 0, 'confirmed', '2026-04-28T13:00:00Z', '2026-04-28T13:00:00Z', NULL),
('evt_gamedev_meetup', 'cal_personal', 'Shanghai Game Developers Meetup', 'AI in Game Development discussion', 'TechHub Shanghai', '2026-05-30T19:00:00+08:00', '2026-05-30T21:00:00+08:00', 0, 'confirmed', '2026-05-10T09:00:00Z', '2026-05-10T09:00:00Z', NULL),
('evt_qa_final', 'cal_work', 'Final QA Testing', 'Final quality assurance testing phase', '', '2026-06-03', '2026-06-06', 1, 'confirmed', '2026-05-01T10:00:00Z', '2026-05-01T10:00:00Z', NULL),
('evt_features_complete', 'cal_work', 'All Features Complete Deadline', 'All features must be complete', '', '2026-06-01', '2026-06-01', 1, 'confirmed', '2026-05-01T10:00:00Z', '2026-05-01T10:00:00Z', NULL);


-- Historical and ordinary commitments visible before the scenario began.
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule) VALUES
('evt_dental_cleaning_2025', 'cal_personal', 'Dental Cleaning', 'Routine scaling completed; the clinic recorded no follow-up treatment.', 'Huashan Dental Clinic', '2025-10-18T09:20:00+08:00', '2025-10-18T10:10:00+08:00', 0, 'confirmed', '2025-09-30T03:12:00Z', '2025-10-18T03:00:00Z', NULL),
('evt_water_meter_2025', 'cal_personal', 'Water Meter Inspection', 'The property office cancelled this visit after receiving the meter photo.', 'Home', '2025-11-06T14:00:00+08:00', '2025-11-06T14:30:00+08:00', 0, 'cancelled', '2025-10-26T08:40:00Z', '2025-11-05T01:15:00Z', NULL),
('evt_family_dinner_2025', 'cal_personal', 'Winter Family Dinner', 'Six relatives met for an early year-end meal; Aunt Liu brought the old photo album.', 'Jade Garden, Xujiahui', '2025-12-20T18:15:00+08:00', '2025-12-20T21:10:00+08:00', 0, 'confirmed', '2025-11-18T06:05:00Z', '2025-12-14T09:22:00Z', NULL),
('evt_tax_packet_2026', 'cal_personal', 'Tax Document Handover', 'Delivered the 2025 income statement and deductible-expense folder to accountant Zhao.', 'Xuhui Service Center', '2026-01-17T11:00:00+08:00', '2026-01-17T11:35:00+08:00', 0, 'confirmed', '2026-01-08T04:25:00Z', '2026-01-17T04:10:00Z', NULL),
('evt_laptop_battery_2026', 'cal_work', 'Studio Laptop Battery Replacement', 'IT replaced the swollen battery and returned asset SH-GD-047 after a charging test.', 'IT Support Desk', '2026-02-03T16:10:00+08:00', '2026-02-03T16:55:00+08:00', 0, 'confirmed', '2026-01-28T02:18:00Z', '2026-02-03T09:20:00Z', NULL),
('evt_fire_drill_2026', 'cal_personal', 'Community Fire Drill', 'Residents practiced the east-stairwell route; assembly roll call ended at 10:42.', 'Residential Courtyard', '2026-03-14T09:30:00+08:00', '2026-03-14T10:50:00+08:00', 0, 'confirmed', '2026-03-02T07:46:00Z', '2026-03-14T03:05:00Z', NULL),
('evt_vehicle_service_2026', 'cal_personal', 'Vehicle Annual Service', 'Oil, brake fluid, and two worn wiper blades were replaced; odometer read 38,412 km.', 'Pudong Service Garage', '2026-03-29T08:40:00+08:00', '2026-03-29T11:25:00+08:00', 0, 'confirmed', '2026-03-12T05:33:00Z', '2026-03-29T04:02:00Z', NULL),
('evt_portfolio_review_2026', 'cal_work', 'Art Portfolio Review', 'The art director approved the lighting study and returned three character sheets for color revisions.', 'Studio Review Room', '2026-04-07T13:30:00+08:00', '2026-04-07T15:05:00+08:00', 0, 'confirmed', '2026-03-31T01:50:00Z', '2026-04-07T08:15:00Z', NULL),
('evt_insurance_call_2026', 'cal_personal', 'Insurance Billing Call', 'Customer service explained the outpatient invoice code and closed case BX-260418.', 'Phone', '2026-04-18T10:15:00+08:00', '2026-04-18T10:42:00+08:00', 0, 'confirmed', '2026-04-16T07:12:00Z', '2026-04-18T03:05:00Z', NULL),
('evt_nutrition_webinar_2026', 'cal_personal', 'Prenatal Nutrition Webinar', 'Dietitian Qiao covered iron-rich meals, food hygiene, and the clinic nutrition hotline.', 'Online', '2026-05-05T19:30:00+08:00', '2026-05-05T20:35:00+08:00', 0, 'confirmed', '2026-04-22T06:00:00Z', '2026-05-05T13:10:00Z', NULL),
('evt_delivery_cancelled_2026', 'cal_personal', 'Bookshelf Delivery', 'Order FS-882 was cancelled after the seller reported a damaged side panel.', 'Home', '2026-05-09T10:00:00+08:00', '2026-05-09T12:00:00+08:00', 0, 'cancelled', '2026-04-30T08:03:00Z', '2026-05-08T02:44:00Z', NULL),
('evt_audio_review_2026', 'cal_work', 'Localization Audio Review', 'Compared Mandarin voice takes for chapter four and marked two lines for pronunciation pickup.', 'Audio Suite 2', '2026-05-14T14:20:00+08:00', '2026-05-14T15:40:00+08:00', 0, 'confirmed', '2026-05-06T01:33:00Z', '2026-05-14T09:02:00Z', NULL);

INSERT INTO attendees (event_id, email, name, response_status) VALUES
('evt_family_dinner_2025', 'aunt.liu@example.com', 'Aunt Liu', 'accepted'),
('evt_tax_packet_2026', 'zhao.accounting@example.com', 'Zhao Ming', 'accepted'),
('evt_portfolio_review_2026', 'art.director@studio.example', 'Lin Wei', 'accepted'),
('evt_insurance_call_2026', 'chen.yu@example.com', 'Chen Yu', 'accepted'),
('evt_nutrition_webinar_2026', 'meilin.wang@example.com', 'Wang Meilin', 'accepted'),
('evt_audio_review_2026', 'audio.lead@studio.example', 'Guo Han', 'tentative');

INSERT INTO reminders (event_id, method, minutes_before) VALUES
('evt_dental_cleaning_2025', 'popup', 120),
('evt_family_dinner_2025', 'email', 1440),
('evt_tax_packet_2026', 'popup', 60),
('evt_fire_drill_2026', 'popup', 30),
('evt_vehicle_service_2026', 'email', 2880),
('evt_nutrition_webinar_2026', 'popup', 20),
('evt_audio_review_2026', 'popup', 15);

COMMIT;
