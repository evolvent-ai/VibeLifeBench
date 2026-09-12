-- calendar_mock zhao_meng_litigation — init.sql
-- Zhao Meng's personal calendar, May–June 2026. Food safety online-shopping consumer who purchased substandard imported food and is preparing a lawsuit for a refund plus tenfold compensation.
-- Existing events: scheduled consultation with a consumer-rights lawyer, follow-up visit to a community hospital (sought medical care after drinking the problematic tea, implying actual losses), credit card payment due date (distractor).
-- Subsequent case milestones shall be updated by the user or collaborator according to the actual service of process.
-- All times Asia/Shanghai (+08:00). Reference frame: 2026-05-20. user_id = zhao_meng.

BEGIN;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
 ('cal_zhao_meng', 'zhao_meng', 'Zhao Meng Personal', '#4285F4', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');

-- Scheduled in-person consultation with a consumer-rights protection lawyer (background: Zhao Meng has already consulted a lawyer, but mainly relies on her own research of case law)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_lawyer_0522', 'cal_zhao_meng', 'In-Person Consultation with a Consumer Rights Lawyer', 'Bring a screenshot of the order, proof of payment, an unboxing video, the food involved in the case, and medical invoices', 'A certain law firm at People''s Square',
  '2026-05-22T15:00:00+08:00', '2026-05-22T16:00:00+08:00',
  0, 'confirmed', '2026-05-15T00:00:00Z', '2026-05-15T00:00:00Z', NULL, NULL);

-- Follow-up visit to a community hospital (sought medical care after drinking the problematic tea, suggesting actual losses/medical expenses)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_clinic_0527', 'cal_zhao_meng', 'Follow-up visit at the community hospital', 'Follow-up examination after experiencing heart palpitations from drinking wellness tea', 'Pudong Community Hospital',
  '2026-05-27T10:00:00+08:00', '2026-05-27T11:00:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

-- Credit card payment due date (distractor)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_card_repay', 'cal_zhao_meng', 'Credit card repayment', '¥2,400 due on the account ending in 7788', NULL,
  '2026-06-05T00:00:00+08:00', '2026-06-05T23:59:00+08:00',
  1, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);


INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_001', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-03T09:15:00+08:00', '2026-05-03T10:15:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_002', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-05T10:30:00+08:00', '2026-05-05T11:45:00+08:00',
  0, 'confirmed', '2026-04-23T00:00:00Z', '2026-04-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_003', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-07T11:45:00+08:00', '2026-05-07T12:30:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_004', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-09T12:00:00+08:00', '2026-05-09T13:00:00+08:00',
  0, 'confirmed', '2026-04-25T00:00:00Z', '2026-04-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_005', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-12T14:15:00+08:00', '2026-05-12T15:30:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_006', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-14T16:30:00+08:00', '2026-05-14T17:15:00+08:00',
  0, 'confirmed', '2026-05-03T00:00:00Z', '2026-05-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_007', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-16T18:45:00+08:00', '2026-05-16T19:45:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_008', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-18T19:00:00+08:00', '2026-05-18T20:15:00+08:00',
  0, 'confirmed', '2026-05-05T00:00:00Z', '2026-05-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_009', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-20T08:15:00+08:00', '2026-05-20T09:00:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_010', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-23T09:30:00+08:00', '2026-05-23T10:30:00+08:00',
  0, 'confirmed', '2026-05-13T00:00:00Z', '2026-05-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_011', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-25T00:00:00+08:00', '2026-05-25T23:59:00+08:00',
  1, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_012', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-27T11:00:00+08:00', '2026-05-27T11:45:00+08:00',
  0, 'confirmed', '2026-05-15T00:00:00Z', '2026-05-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_013', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-29T12:15:00+08:00', '2026-05-29T13:15:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_014', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-31T14:30:00+08:00', '2026-05-31T15:45:00+08:00',
  0, 'confirmed', '2026-05-17T00:00:00Z', '2026-05-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_015', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-03T16:45:00+08:00', '2026-06-03T17:30:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_016', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-05T18:00:00+08:00', '2026-06-05T19:00:00+08:00',
  0, 'confirmed', '2026-05-25T00:00:00Z', '2026-05-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_017', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-07T19:15:00+08:00', '2026-06-07T20:30:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_018', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-09T08:30:00+08:00', '2026-06-09T09:15:00+08:00',
  0, 'confirmed', '2026-05-27T00:00:00Z', '2026-05-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_019', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-11T09:45:00+08:00', '2026-06-11T10:45:00+08:00',
  0, 'confirmed', '2026-05-28T00:00:00Z', '2026-05-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_020', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-14T10:00:00+08:00', '2026-06-14T11:15:00+08:00',
  0, 'confirmed', '2026-06-04T00:00:00Z', '2026-06-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_021', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-16T11:15:00+08:00', '2026-06-16T12:00:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_022', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-18T00:00:00+08:00', '2026-06-18T23:59:00+08:00',
  1, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_023', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-20T14:45:00+08:00', '2026-06-20T16:00:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_024', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-22T16:00:00+08:00', '2026-06-22T16:45:00+08:00',
  0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_025', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-25T18:15:00+08:00', '2026-06-25T19:15:00+08:00',
  0, 'confirmed', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_026', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-27T19:30:00+08:00', '2026-06-27T20:45:00+08:00',
  0, 'confirmed', '2026-06-16T00:00:00Z', '2026-06-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_027', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-06-29T08:45:00+08:00', '2026-06-29T09:30:00+08:00',
  0, 'confirmed', '2026-06-17T00:00:00Z', '2026-06-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_028', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-01T09:00:00+08:00', '2026-05-01T10:00:00+08:00',
  0, 'confirmed', '2026-04-18T00:00:00Z', '2026-04-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_029', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-03T10:15:00+08:00', '2026-05-03T11:30:00+08:00',
  0, 'confirmed', '2026-04-19T00:00:00Z', '2026-04-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_030', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-06T11:30:00+08:00', '2026-05-06T12:15:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_031', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-08T12:45:00+08:00', '2026-05-08T13:45:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_032', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-10T14:00:00+08:00', '2026-05-10T15:15:00+08:00',
  0, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_033', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-12T00:00:00+08:00', '2026-05-12T23:59:00+08:00',
  1, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_034', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-14T18:30:00+08:00', '2026-05-14T19:30:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_035', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-17T19:45:00+08:00', '2026-05-17T21:00:00+08:00',
  0, 'confirmed', '2026-05-07T00:00:00Z', '2026-05-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_036', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-19T08:00:00+08:00', '2026-05-19T08:45:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_037', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-21T09:15:00+08:00', '2026-05-21T10:15:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_038', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-23T10:30:00+08:00', '2026-05-23T11:45:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_039', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-25T11:45:00+08:00', '2026-05-25T12:30:00+08:00',
  0, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_040', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-28T12:00:00+08:00', '2026-05-28T13:00:00+08:00',
  0, 'confirmed', '2026-05-18T00:00:00Z', '2026-05-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_041', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-30T14:15:00+08:00', '2026-05-30T15:30:00+08:00',
  0, 'confirmed', '2026-05-19T00:00:00Z', '2026-05-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_042', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-06-01T16:30:00+08:00', '2026-06-01T17:15:00+08:00',
  0, 'confirmed', '2026-05-20T00:00:00Z', '2026-05-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_043', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-03T18:45:00+08:00', '2026-06-03T19:45:00+08:00',
  0, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_044', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-05T00:00:00+08:00', '2026-06-05T23:59:00+08:00',
  1, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_045', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-08T08:15:00+08:00', '2026-06-08T09:00:00+08:00',
  0, 'confirmed', '2026-05-29T00:00:00Z', '2026-05-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_046', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-10T09:30:00+08:00', '2026-06-10T10:30:00+08:00',
  0, 'confirmed', '2026-05-30T00:00:00Z', '2026-05-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_047', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-12T10:45:00+08:00', '2026-06-12T12:00:00+08:00',
  0, 'confirmed', '2026-05-31T00:00:00Z', '2026-05-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_048', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-14T11:00:00+08:00', '2026-06-14T11:45:00+08:00',
  0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_049', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-16T12:15:00+08:00', '2026-06-16T13:15:00+08:00',
  0, 'confirmed', '2026-06-02T00:00:00Z', '2026-06-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_050', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-19T14:30:00+08:00', '2026-06-19T15:45:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_051', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-21T16:45:00+08:00', '2026-06-21T17:30:00+08:00',
  0, 'confirmed', '2026-06-10T00:00:00Z', '2026-06-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_052', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-23T18:00:00+08:00', '2026-06-23T19:00:00+08:00',
  0, 'confirmed', '2026-06-11T00:00:00Z', '2026-06-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_053', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-25T19:15:00+08:00', '2026-06-25T20:30:00+08:00',
  0, 'confirmed', '2026-06-12T00:00:00Z', '2026-06-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_054', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-27T08:30:00+08:00', '2026-06-27T09:15:00+08:00',
  0, 'confirmed', '2026-06-13T00:00:00Z', '2026-06-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_055', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-06-30T00:00:00+08:00', '2026-06-30T23:59:00+08:00',
  1, 'confirmed', '2026-06-20T00:00:00Z', '2026-06-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_056', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-02T10:00:00+08:00', '2026-05-02T11:15:00+08:00',
  0, 'confirmed', '2026-04-21T00:00:00Z', '2026-04-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_057', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-04T11:15:00+08:00', '2026-05-04T12:00:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_058', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-06T12:30:00+08:00', '2026-05-06T13:30:00+08:00',
  0, 'confirmed', '2026-04-23T00:00:00Z', '2026-04-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_059', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-08T14:45:00+08:00', '2026-05-08T16:00:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_060', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-11T16:00:00+08:00', '2026-05-11T16:45:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_061', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-13T18:15:00+08:00', '2026-05-13T19:15:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_062', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-15T19:30:00+08:00', '2026-05-15T20:45:00+08:00',
  0, 'confirmed', '2026-05-03T00:00:00Z', '2026-05-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_063', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-17T08:45:00+08:00', '2026-05-17T09:30:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_064', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-19T09:00:00+08:00', '2026-05-19T10:00:00+08:00',
  0, 'confirmed', '2026-05-05T00:00:00Z', '2026-05-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_065', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-22T10:15:00+08:00', '2026-05-22T11:30:00+08:00',
  0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_066', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-24T00:00:00+08:00', '2026-05-24T23:59:00+08:00',
  1, 'confirmed', '2026-05-13T00:00:00Z', '2026-05-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_067', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-26T12:45:00+08:00', '2026-05-26T13:45:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_068', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-28T14:00:00+08:00', '2026-05-28T15:15:00+08:00',
  0, 'confirmed', '2026-05-15T00:00:00Z', '2026-05-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_069', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-30T16:15:00+08:00', '2026-05-30T17:00:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_070', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-06-02T18:30:00+08:00', '2026-06-02T19:30:00+08:00',
  0, 'confirmed', '2026-05-23T00:00:00Z', '2026-05-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_071', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-04T19:45:00+08:00', '2026-06-04T21:00:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_072', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-06T08:00:00+08:00', '2026-06-06T08:45:00+08:00',
  0, 'confirmed', '2026-05-25T00:00:00Z', '2026-05-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_073', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-08T09:15:00+08:00', '2026-06-08T10:15:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_074', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-10T10:30:00+08:00', '2026-06-10T11:45:00+08:00',
  0, 'confirmed', '2026-05-27T00:00:00Z', '2026-05-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_075', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-13T11:45:00+08:00', '2026-06-13T12:30:00+08:00',
  0, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_076', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-15T12:00:00+08:00', '2026-06-15T13:00:00+08:00',
  0, 'confirmed', '2026-06-04T00:00:00Z', '2026-06-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_077', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-17T00:00:00+08:00', '2026-06-17T23:59:00+08:00',
  1, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_078', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-19T16:30:00+08:00', '2026-06-19T17:15:00+08:00',
  0, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_079', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-21T18:45:00+08:00', '2026-06-21T19:45:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_080', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-24T19:00:00+08:00', '2026-06-24T20:15:00+08:00',
  0, 'confirmed', '2026-06-14T00:00:00Z', '2026-06-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_081', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-26T08:15:00+08:00', '2026-06-26T09:00:00+08:00',
  0, 'confirmed', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_082', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-28T09:30:00+08:00', '2026-06-28T10:30:00+08:00',
  0, 'confirmed', '2026-06-16T00:00:00Z', '2026-06-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_083', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-06-30T10:45:00+08:00', '2026-06-30T12:00:00+08:00',
  0, 'confirmed', '2026-06-17T00:00:00Z', '2026-06-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_084', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-02T11:00:00+08:00', '2026-05-02T11:45:00+08:00',
  0, 'confirmed', '2026-04-18T00:00:00Z', '2026-04-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_085', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-05T12:15:00+08:00', '2026-05-05T13:15:00+08:00',
  0, 'confirmed', '2026-04-25T00:00:00Z', '2026-04-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_086', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-07T14:30:00+08:00', '2026-05-07T15:45:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_087', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-09T16:45:00+08:00', '2026-05-09T17:30:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_088', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-11T00:00:00+08:00', '2026-05-11T23:59:00+08:00',
  1, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_089', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-13T19:15:00+08:00', '2026-05-13T20:30:00+08:00',
  0, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_090', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-16T08:30:00+08:00', '2026-05-16T09:15:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_091', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-18T09:45:00+08:00', '2026-05-18T10:45:00+08:00',
  0, 'confirmed', '2026-05-07T00:00:00Z', '2026-05-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_092', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-20T10:00:00+08:00', '2026-05-20T11:15:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_093', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-22T11:15:00+08:00', '2026-05-22T12:00:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_094', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-24T12:30:00+08:00', '2026-05-24T13:30:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_095', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-27T14:45:00+08:00', '2026-05-27T16:00:00+08:00',
  0, 'confirmed', '2026-05-17T00:00:00Z', '2026-05-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_096', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-29T16:00:00+08:00', '2026-05-29T16:45:00+08:00',
  0, 'confirmed', '2026-05-18T00:00:00Z', '2026-05-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_097', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-31T18:15:00+08:00', '2026-05-31T19:15:00+08:00',
  0, 'confirmed', '2026-05-19T00:00:00Z', '2026-05-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_098', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-06-02T19:30:00+08:00', '2026-06-02T20:45:00+08:00',
  0, 'confirmed', '2026-05-20T00:00:00Z', '2026-05-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_099', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-04T00:00:00+08:00', '2026-06-04T23:59:00+08:00',
  1, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_100', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-07T09:00:00+08:00', '2026-06-07T10:00:00+08:00',
  0, 'confirmed', '2026-05-28T00:00:00Z', '2026-05-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_101', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-09T10:15:00+08:00', '2026-06-09T11:30:00+08:00',
  0, 'confirmed', '2026-05-29T00:00:00Z', '2026-05-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_102', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-11T11:30:00+08:00', '2026-06-11T12:15:00+08:00',
  0, 'confirmed', '2026-05-30T00:00:00Z', '2026-05-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_103', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-13T12:45:00+08:00', '2026-06-13T13:45:00+08:00',
  0, 'confirmed', '2026-05-31T00:00:00Z', '2026-05-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_104', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-15T14:00:00+08:00', '2026-06-15T15:15:00+08:00',
  0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_105', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-18T16:15:00+08:00', '2026-06-18T17:00:00+08:00',
  0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_106', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-20T18:30:00+08:00', '2026-06-20T19:30:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_107', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-22T19:45:00+08:00', '2026-06-22T21:00:00+08:00',
  0, 'confirmed', '2026-06-10T00:00:00Z', '2026-06-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_108', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-24T08:00:00+08:00', '2026-06-24T08:45:00+08:00',
  0, 'confirmed', '2026-06-11T00:00:00Z', '2026-06-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_109', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-26T09:15:00+08:00', '2026-06-26T10:15:00+08:00',
  0, 'confirmed', '2026-06-12T00:00:00Z', '2026-06-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_110', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-29T00:00:00+08:00', '2026-06-29T23:59:00+08:00',
  1, 'confirmed', '2026-06-19T00:00:00Z', '2026-06-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_111', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-01T11:45:00+08:00', '2026-05-01T12:30:00+08:00',
  0, 'confirmed', '2026-04-20T00:00:00Z', '2026-04-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_112', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-03T12:00:00+08:00', '2026-05-03T13:00:00+08:00',
  0, 'confirmed', '2026-04-21T00:00:00Z', '2026-04-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_113', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-05T14:15:00+08:00', '2026-05-05T15:30:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_114', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-07T16:30:00+08:00', '2026-05-07T17:15:00+08:00',
  0, 'confirmed', '2026-04-23T00:00:00Z', '2026-04-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_115', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-10T18:45:00+08:00', '2026-05-10T19:45:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_116', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-12T19:00:00+08:00', '2026-05-12T20:15:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_117', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-14T08:15:00+08:00', '2026-05-14T09:00:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_118', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-16T09:30:00+08:00', '2026-05-16T10:30:00+08:00',
  0, 'confirmed', '2026-05-03T00:00:00Z', '2026-05-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_119', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-18T10:45:00+08:00', '2026-05-18T12:00:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_120', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-21T11:00:00+08:00', '2026-05-21T11:45:00+08:00',
  0, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_121', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-23T00:00:00+08:00', '2026-05-23T23:59:00+08:00',
  1, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_122', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-25T14:30:00+08:00', '2026-05-25T15:45:00+08:00',
  0, 'confirmed', '2026-05-13T00:00:00Z', '2026-05-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_123', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-27T16:45:00+08:00', '2026-05-27T17:30:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_124', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-29T18:00:00+08:00', '2026-05-29T19:00:00+08:00',
  0, 'confirmed', '2026-05-15T00:00:00Z', '2026-05-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_125', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-06-01T19:15:00+08:00', '2026-06-01T20:30:00+08:00',
  0, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_126', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-06-03T08:30:00+08:00', '2026-06-03T09:15:00+08:00',
  0, 'confirmed', '2026-05-23T00:00:00Z', '2026-05-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_127', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-05T09:45:00+08:00', '2026-06-05T10:45:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_128', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-07T10:00:00+08:00', '2026-06-07T11:15:00+08:00',
  0, 'confirmed', '2026-05-25T00:00:00Z', '2026-05-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_129', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-09T11:15:00+08:00', '2026-06-09T12:00:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_130', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-12T12:30:00+08:00', '2026-06-12T13:30:00+08:00',
  0, 'confirmed', '2026-06-02T00:00:00Z', '2026-06-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_131', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-14T14:45:00+08:00', '2026-06-14T16:00:00+08:00',
  0, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_132', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-16T00:00:00+08:00', '2026-06-16T23:59:00+08:00',
  1, 'confirmed', '2026-06-04T00:00:00Z', '2026-06-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_133', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-18T18:15:00+08:00', '2026-06-18T19:15:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_134', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-20T19:30:00+08:00', '2026-06-20T20:45:00+08:00',
  0, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_135', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-23T08:45:00+08:00', '2026-06-23T09:30:00+08:00',
  0, 'confirmed', '2026-06-13T00:00:00Z', '2026-06-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_136', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-25T09:00:00+08:00', '2026-06-25T10:00:00+08:00',
  0, 'confirmed', '2026-06-14T00:00:00Z', '2026-06-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_137', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-27T10:15:00+08:00', '2026-06-27T11:30:00+08:00',
  0, 'confirmed', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_138', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-29T11:30:00+08:00', '2026-06-29T12:15:00+08:00',
  0, 'confirmed', '2026-06-16T00:00:00Z', '2026-06-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_139', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-01T12:45:00+08:00', '2026-05-01T13:45:00+08:00',
  0, 'confirmed', '2026-04-17T00:00:00Z', '2026-04-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_140', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-04T14:00:00+08:00', '2026-05-04T15:15:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_141', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-06T16:15:00+08:00', '2026-05-06T17:00:00+08:00',
  0, 'confirmed', '2026-04-25T00:00:00Z', '2026-04-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_142', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-08T18:30:00+08:00', '2026-05-08T19:30:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_143', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-10T00:00:00+08:00', '2026-05-10T23:59:00+08:00',
  1, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_144', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-12T08:00:00+08:00', '2026-05-12T08:45:00+08:00',
  0, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_145', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-15T09:15:00+08:00', '2026-05-15T10:15:00+08:00',
  0, 'confirmed', '2026-05-05T00:00:00Z', '2026-05-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_146', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-17T10:30:00+08:00', '2026-05-17T11:45:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_147', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-19T11:45:00+08:00', '2026-05-19T12:30:00+08:00',
  0, 'confirmed', '2026-05-07T00:00:00Z', '2026-05-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_148', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-21T12:00:00+08:00', '2026-05-21T13:00:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_149', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-23T14:15:00+08:00', '2026-05-23T15:30:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_150', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-26T16:30:00+08:00', '2026-05-26T17:15:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_151', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-28T18:45:00+08:00', '2026-05-28T19:45:00+08:00',
  0, 'confirmed', '2026-05-17T00:00:00Z', '2026-05-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_152', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-30T19:00:00+08:00', '2026-05-30T20:15:00+08:00',
  0, 'confirmed', '2026-05-18T00:00:00Z', '2026-05-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_153', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-06-01T08:15:00+08:00', '2026-06-01T09:00:00+08:00',
  0, 'confirmed', '2026-05-19T00:00:00Z', '2026-05-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_154', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-06-03T00:00:00+08:00', '2026-06-03T23:59:00+08:00',
  1, 'confirmed', '2026-05-20T00:00:00Z', '2026-05-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_155', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-06T10:45:00+08:00', '2026-06-06T12:00:00+08:00',
  0, 'confirmed', '2026-05-27T00:00:00Z', '2026-05-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_156', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-08T11:00:00+08:00', '2026-06-08T11:45:00+08:00',
  0, 'confirmed', '2026-05-28T00:00:00Z', '2026-05-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_157', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-10T12:15:00+08:00', '2026-06-10T13:15:00+08:00',
  0, 'confirmed', '2026-05-29T00:00:00Z', '2026-05-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_158', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-12T14:30:00+08:00', '2026-06-12T15:45:00+08:00',
  0, 'confirmed', '2026-05-30T00:00:00Z', '2026-05-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_159', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-14T16:45:00+08:00', '2026-06-14T17:30:00+08:00',
  0, 'confirmed', '2026-05-31T00:00:00Z', '2026-05-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_160', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-17T18:00:00+08:00', '2026-06-17T19:00:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_161', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-19T19:15:00+08:00', '2026-06-19T20:30:00+08:00',
  0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_162', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-21T08:30:00+08:00', '2026-06-21T09:15:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_163', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-23T09:45:00+08:00', '2026-06-23T10:45:00+08:00',
  0, 'confirmed', '2026-06-10T00:00:00Z', '2026-06-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_164', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-25T10:00:00+08:00', '2026-06-25T11:15:00+08:00',
  0, 'confirmed', '2026-06-11T00:00:00Z', '2026-06-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_165', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-28T00:00:00+08:00', '2026-06-28T23:59:00+08:00',
  1, 'confirmed', '2026-06-18T00:00:00Z', '2026-06-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_166', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-30T12:30:00+08:00', '2026-06-30T13:30:00+08:00',
  0, 'confirmed', '2026-06-19T00:00:00Z', '2026-06-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_167', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-02T14:45:00+08:00', '2026-05-02T16:00:00+08:00',
  0, 'confirmed', '2026-04-20T00:00:00Z', '2026-04-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_168', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-04T16:00:00+08:00', '2026-05-04T16:45:00+08:00',
  0, 'confirmed', '2026-04-21T00:00:00Z', '2026-04-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_169', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-06T18:15:00+08:00', '2026-05-06T19:15:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_170', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-09T19:30:00+08:00', '2026-05-09T20:45:00+08:00',
  0, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_171', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-11T08:45:00+08:00', '2026-05-11T09:30:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_172', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-13T09:00:00+08:00', '2026-05-13T10:00:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_173', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-15T10:15:00+08:00', '2026-05-15T11:30:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_174', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-17T11:30:00+08:00', '2026-05-17T12:15:00+08:00',
  0, 'confirmed', '2026-05-03T00:00:00Z', '2026-05-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_175', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-05-20T12:45:00+08:00', '2026-05-20T13:45:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_176', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-05-22T00:00:00+08:00', '2026-05-22T23:59:00+08:00',
  1, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_177', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-05-24T16:15:00+08:00', '2026-05-24T17:00:00+08:00',
  0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_178', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-05-26T18:30:00+08:00', '2026-05-26T19:30:00+08:00',
  0, 'confirmed', '2026-05-13T00:00:00Z', '2026-05-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_179', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-05-28T19:45:00+08:00', '2026-05-28T21:00:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_180', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-05-31T08:00:00+08:00', '2026-05-31T08:45:00+08:00',
  0, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_181', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-06-02T09:15:00+08:00', '2026-06-02T10:15:00+08:00',
  0, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_182', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-06-04T10:30:00+08:00', '2026-06-04T11:45:00+08:00',
  0, 'confirmed', '2026-05-23T00:00:00Z', '2026-05-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_183', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-06-06T11:45:00+08:00', '2026-06-06T12:30:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_184', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-06-08T12:00:00+08:00', '2026-06-08T13:00:00+08:00',
  0, 'confirmed', '2026-05-25T00:00:00Z', '2026-05-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_185', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-06-11T14:15:00+08:00', '2026-06-11T15:30:00+08:00',
  0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_186', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-06-13T16:30:00+08:00', '2026-06-13T17:15:00+08:00',
  0, 'confirmed', '2026-06-02T00:00:00Z', '2026-06-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_187', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-06-15T00:00:00+08:00', '2026-06-15T23:59:00+08:00',
  1, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_188', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-06-17T19:00:00+08:00', '2026-06-17T20:15:00+08:00',
  0, 'confirmed', '2026-06-04T00:00:00Z', '2026-06-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_189', 'cal_zhao_meng', 'A meal with friends', 'Have a meal and chat with university classmates. If any adjustments are needed, update the calendar in advance.', 'Lujiazui Restaurant',
  '2026-06-19T08:15:00+08:00', '2026-06-19T09:00:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_190', 'cal_zhao_meng', 'Book Club', 'Discuss the nonfiction works we’ve been reading recently. If any adjustments are needed, please update the calendar in advance.', 'Community library',
  '2026-06-22T09:30:00+08:00', '2026-06-22T10:30:00+08:00',
  0, 'confirmed', '2026-06-12T00:00:00Z', '2026-06-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_191', 'cal_zhao_meng', 'Dental follow-up', 'Routine teeth cleaning and oral examination. If any changes are needed, please update the calendar in advance.', 'Shiji Avenue Dental Clinic',
  '2026-06-24T10:45:00+08:00', '2026-06-24T12:00:00+08:00',
  0, 'confirmed', '2026-06-13T00:00:00Z', '2026-06-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_192', 'cal_zhao_meng', 'Project Retrospective', 'Organize the administrative project review and budget explanation. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room B',
  '2026-06-26T11:00:00+08:00', '2026-06-26T11:45:00+08:00',
  0, 'confirmed', '2026-06-14T00:00:00Z', '2026-06-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_193', 'cal_zhao_meng', 'Weekend chores', 'Organize the wardrobe, clean the house, and change the bedding. If adjustments are needed, update the calendar in advance.', 'Home',
  '2026-06-28T12:15:00+08:00', '2026-06-28T13:15:00+08:00',
  0, 'confirmed', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_194', 'cal_zhao_meng', 'Package receipt reminder', 'Note the delivery arrival time to avoid missing the delivery. If you need to make changes, please update the calendar in advance.', NULL,
  '2026-06-30T14:30:00+08:00', '2026-06-30T15:45:00+08:00',
  0, 'confirmed', '2026-06-16T00:00:00Z', '2026-06-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_195', 'cal_zhao_meng', 'Team-Building Coordination', 'Confirm the team-building attendee list, transportation, and catering. If you need to make changes, please update the calendar in advance.', 'Video conference',
  '2026-05-03T16:45:00+08:00', '2026-05-03T17:30:00+08:00',
  0, 'confirmed', '2026-04-23T00:00:00Z', '2026-04-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_196', 'cal_zhao_meng', 'Reminder to renew identification documents', 'Check document expiration dates and renewal materials. If adjustments are needed, update the calendar in advance', NULL,
  '2026-05-05T18:00:00+08:00', '2026-05-05T19:00:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_197', 'cal_zhao_meng', 'Administrative regular meeting', 'Follow up on administrative procurement, reimbursement, and supplier progress. If adjustments are needed, update the calendar in advance.', 'Company Meeting Room A',
  '2026-05-07T19:15:00+08:00', '2026-05-07T20:30:00+08:00',
  0, 'confirmed', '2026-04-25T00:00:00Z', '2026-04-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_198', 'cal_zhao_meng', 'Team Morning Meeting', 'Confirm this week’s to-dos and cross-department collaboration items. If any changes are needed, please update the calendar in advance.', 'Video conference',
  '2026-05-09T00:00:00+08:00', '2026-05-09T23:59:00+08:00',
  1, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_199', 'cal_zhao_meng', 'Fitness Class', 'After work, attend a group fitness class to relieve shoulder and neck discomfort. If any adjustments are needed, please update the calendar in advance.', 'Pudong Fitness Center',
  '2026-05-11T09:45:00+08:00', '2026-05-11T10:45:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_200', 'cal_zhao_meng', 'Household Purchasing', 'Replenish daily necessities and ingredients for the refrigerator. If adjustments are needed, please update the calendar in advance.', 'Lianhua Supermarket',
  '2026-05-14T10:00:00+08:00', '2026-05-14T11:15:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_201', 'cal_zhao_meng', 'Accompany Mom to a follow-up appointment', 'Take Mom to her follow-up appointment and pick up her medication. If any changes are needed, please update the calendar in advance.', 'Pudong New Area People’s Hospital',
  '2026-05-16T11:15:00+08:00', '2026-05-16T12:00:00+08:00',
  0, 'confirmed', '2026-05-05T00:00:00Z', '2026-05-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_202', 'cal_zhao_meng', 'Property Fee Payment Reminder', 'Check the property management fees, utility bills, and parking fees. If any adjustments are needed, update the calendar in advance.', 'Neighborhood Property Management Center',
  '2026-05-18T12:30:00+08:00', '2026-05-18T13:30:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO _counters (key, value) VALUES
 ('event_seq', 500),
 ('attendee_seq', 0),
 ('reminder_seq', 0);


-- evt_bg_* denotes personal arrangements established before the reference date; only creation metadata is corrected, without changing the timing of the arrangements themselves.
UPDATE events
SET created_at = '2026-05-19T08:00:00Z',
    updated_at = CASE WHEN updated_at > '2026-05-20T23:59:59' THEN '2026-05-19T08:00:00Z' ELSE updated_at END
WHERE event_id LIKE 'evt_bg_%' AND created_at > '2026-05-20T23:59:59';

COMMIT;
