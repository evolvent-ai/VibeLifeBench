PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
('cal_zhangming_primary', 'zhang_ming', 'Zhang Ming Work', '#3367D6', 'Asia/Shanghai', 1, '2024-01-05T09:00:00+08:00');

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
('evt_q2_pipeline_review', 'cal_zhangming_primary', 'Q2 pipeline review', 'Review closed opportunities and unresolved account risks.', 'Shanghai office 18F', '2026-06-25T14:00:00+08:00', '2026-06-25T16:00:00+08:00', 0, 'confirmed', '2026-05-20T11:12:00+08:00', '2026-06-24T09:08:00+08:00', NULL, NULL),
('evt_osaka_receipt_closeout', 'cal_zhangming_primary', 'Osaka receipt closeout', 'Historical expense review for the May Osaka client visit.', 'Finance room 3', '2026-06-26T10:30:00+08:00', '2026-06-26T11:15:00+08:00', 0, 'confirmed', '2026-06-18T15:24:00+08:00', '2026-06-25T17:41:00+08:00', NULL, NULL),
('evt_regional_forecast', 'cal_zhangming_primary', 'Regional sales forecast', 'APAC forecast assumptions and conversion pipeline.', 'Company Meet — Forecast channel', '2026-07-02T10:00:00+08:00', '2026-07-02T11:00:00+08:00', 0, 'confirmed', '2026-06-10T09:07:00+08:00', '2026-06-28T13:32:00+08:00', NULL, NULL),
('evt_product_launch_sync', 'cal_zhangming_primary', 'Product launch messaging sync', 'Confirm translation ownership for the August release.', 'Shanghai office 12F', '2026-07-03T15:30:00+08:00', '2026-07-03T16:20:00+08:00', 0, 'confirmed', '2026-06-21T14:22:00+08:00', '2026-06-29T10:04:00+08:00', NULL, NULL),
('evt_passport_photo_appointment', 'cal_zhangming_primary', 'Passport photo appointment', 'Photo update appointment with no document number stored in calendar.', 'Pudong photo studio', '2026-07-06T08:30:00+08:00', '2026-07-06T09:00:00+08:00', 0, 'confirmed', '2026-06-27T18:05:00+08:00', '2026-06-27T18:05:00+08:00', NULL, NULL),
('evt_travel_policy_briefing', 'cal_zhangming_primary', 'International travel policy briefing', 'Finance and travel operations explain reversible-booking and evidence rules.', 'Video conference', '2026-07-07T16:00:00+08:00', '2026-07-07T16:45:00+08:00', 0, 'confirmed', '2026-06-30T09:18:00+08:00', '2026-06-30T09:18:00+08:00', NULL, NULL),
('evt_japan_entry_document_review', 'cal_zhangming_primary', 'Japan entry document review', 'Review official instructions and identify missing supporting documents.', 'Shanghai office 9F', '2026-07-08T11:00:00+08:00', '2026-07-08T11:40:00+08:00', 0, 'tentative', '2026-06-30T13:44:00+08:00', '2026-06-30T13:44:00+08:00', NULL, NULL),
('evt_client_alpha_handoff', 'cal_zhangming_primary', 'Alpha account handoff', 'Transfer open client issues before international travel.', 'Shanghai office 18F', '2026-07-13T14:00:00+08:00', '2026-07-13T14:50:00+08:00', 0, 'confirmed', '2026-06-28T10:13:00+08:00', '2026-06-30T16:27:00+08:00', NULL, NULL),
('evt_family_call_before_departure', 'cal_zhangming_primary', 'Family call before travel', 'Confirm home arrangements and emergency contact availability.', 'Personal call', '2026-07-13T20:30:00+08:00', '2026-07-13T21:00:00+08:00', 0, 'confirmed', '2026-06-29T19:06:00+08:00', '2026-06-29T19:06:00+08:00', NULL, NULL),
('evt_team_handoff_final', 'cal_zhangming_primary', 'Final client handoff review', 'Verify account owners and escalation contacts.', 'Shanghai office 18F', '2026-07-14T15:00:00+08:00', '2026-07-14T16:00:00+08:00', 0, 'confirmed', '2026-06-28T10:19:00+08:00', '2026-06-30T16:31:00+08:00', NULL, NULL),
('evt_expired_seoul_trip_hold', 'cal_zhangming_primary', 'Seoul partner visit hold', 'Earlier travel option that did not proceed.', 'Seoul', '2026-07-15T00:00:00+09:00', '2026-07-17T00:00:00+09:00', 1, 'cancelled', '2026-04-08T13:28:00+08:00', '2026-05-02T09:46:00+08:00', NULL, NULL),
('evt_apac_leadership_call', 'cal_zhangming_primary', 'APAC leadership call', 'Weekly regional update where attendance may be delegated while traveling.', 'Video conference', '2026-07-16T09:00:00+08:00', '2026-07-16T09:45:00+08:00', 0, 'tentative', '2026-06-17T17:23:00+08:00', '2026-06-30T11:56:00+08:00', NULL, NULL),
('evt_invoice_followup', 'cal_zhangming_primary', 'Hangzhou invoice follow-up', 'Check corrected VAT invoice from the June workshop.', 'Video conference', '2026-07-17T10:30:00+08:00', '2026-07-17T11:00:00+08:00', 0, 'confirmed', '2026-06-20T12:09:00+08:00', '2026-06-29T14:16:00+08:00', NULL, NULL),
('evt_marketing_metrics_review', 'cal_zhangming_primary', 'Marketing metrics review', 'Internal review of campaign attribution data.', 'Video conference', '2026-07-20T11:00:00+08:00', '2026-07-20T12:00:00+08:00', 0, 'confirmed', '2026-06-22T08:52:00+08:00', '2026-06-30T10:21:00+08:00', NULL, NULL),
('evt_sales_ops_daily', 'cal_zhangming_primary', 'Sales operations daily sync', 'Short status meeting that can be delegated if a time-zone conflict occurs.', 'Video conference', '2026-07-21T09:30:00+08:00', '2026-07-21T09:50:00+08:00', 0, 'tentative', '2026-06-23T09:26:00+08:00', '2026-06-30T10:25:00+08:00', NULL, NULL),
('evt_board_pack_review', 'cal_zhangming_primary', 'Board pack review', 'Draft regional notes before the Monday executive meeting.', 'Shanghai office 20F', '2026-07-22T16:00:00+08:00', '2026-07-22T17:00:00+08:00', 0, 'tentative', '2026-06-24T16:48:00+08:00', '2026-06-30T10:31:00+08:00', NULL, NULL),
('evt_post_trip_debrief_hold', 'cal_zhangming_primary', 'Post-travel debrief hold', 'Provisional internal review after return with timing that can move with transport.', 'Shanghai office 18F', '2026-07-23T15:00:00+08:00', '2026-07-23T16:00:00+08:00', 0, 'tentative', '2026-06-28T10:36:00+08:00', '2026-06-30T16:38:00+08:00', NULL, NULL),
('evt_finance_cutoff', 'cal_zhangming_primary', 'July expense evidence cutoff', 'Submit complete evidence or record open gaps for the next cycle.', 'Finance room 3', '2026-07-24T17:00:00+08:00', '2026-07-24T17:30:00+08:00', 0, 'confirmed', '2026-06-11T14:04:00+08:00', '2026-06-27T09:53:00+08:00', NULL, NULL),
('evt_insurance_claim_clinic', 'cal_zhangming_primary', 'Travel-claim document clinic', 'Optional office hour for claim evidence questions.', 'Video conference', '2026-07-27T13:30:00+08:00', '2026-07-27T14:15:00+08:00', 0, 'confirmed', '2026-06-26T11:43:00+08:00', '2026-06-29T15:02:00+08:00', NULL, NULL),
('evt_august_campaign_kickoff', 'cal_zhangming_primary', 'August campaign kickoff', 'Confirm creative review dates and local-market owners.', 'Shanghai office 12F', '2026-07-29T10:00:00+08:00', '2026-07-29T11:30:00+08:00', 0, 'confirmed', '2026-06-19T10:34:00+08:00', '2026-06-30T11:02:00+08:00', NULL, NULL),
('evt_dentist_checkup', 'cal_zhangming_primary', 'Dental check-up', 'Routine personal appointment.', 'Pudong dental clinic', '2026-08-03T18:30:00+08:00', '2026-08-03T19:15:00+08:00', 0, 'confirmed', '2026-06-15T12:27:00+08:00', '2026-06-15T12:27:00+08:00', NULL, NULL),
('evt_cancelled_vendor_demo', 'cal_zhangming_primary', 'Vendor analytics demo', 'Vendor postponed the session to August.', 'Video conference', '2026-06-30T16:00:00+08:00', '2026-06-30T17:00:00+08:00', 0, 'cancelled', '2026-06-16T10:17:00+08:00', '2026-06-29T08:42:00+08:00', NULL, NULL);

INSERT INTO reminders (event_id, method, minutes_before) VALUES
('evt_passport_photo_appointment', 'popup', 720),
('evt_travel_policy_briefing', 'email', 1440),
('evt_japan_entry_document_review', 'popup', 120),
('evt_client_alpha_handoff', 'email', 1440),
('evt_family_call_before_departure', 'popup', 60),
('evt_team_handoff_final', 'popup', 180),
('evt_post_trip_debrief_hold', 'email', 2880),
('evt_finance_cutoff', 'popup', 1440),
('evt_insurance_claim_clinic', 'email', 1440),
('evt_august_campaign_kickoff', 'popup', 30);

INSERT INTO _counters (key, value) VALUES ('event_seq', 9000);
COMMIT;
