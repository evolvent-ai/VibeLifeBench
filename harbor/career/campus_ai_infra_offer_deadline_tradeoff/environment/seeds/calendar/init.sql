-- Curated Stage-0 seed for campus_ai_infra_offer_deadline_tradeoff / calendar.

BEGIN;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
  ('cal_lin_primary', 'usr_lin_che', 'Study and job hunting', '#4285F4', 'Asia/Shanghai', 1, '2025-09-01T00:00:00Z');

INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('cal_thesis_001', 'cal_lin_primary', 'Paper experimental result review', 'Review the throughput and latency charts, and supplement the experimental conditions and error explanation.', 'Laboratory', '2026-05-15T09:00:00+08:00', '2026-05-15T18:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_group_meeting_001', 'cal_lin_primary', 'Mentor group meeting', 'Report on graduation thesis progress, and classmates in the group discuss experiment issues one by one.', 'College building 402', '2026-05-19T15:00:00+08:00', '2026-05-19T17:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_lab_sync_001', 'cal_lin_primary', 'Inference systems research group weekly meeting', 'Discuss KV cache experiments and next week’s replication experiment schedule.', 'Laboratory meeting room', '2026-05-13T10:00:00+08:00', '2026-05-13T11:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_library_renewal_001', 'cal_lin_primary', 'Book return', 'Return the borrowed GPU programming and distributed systems textbook.', 'School library', '2026-05-14T12:10:00+08:00', '2026-05-14T12:40:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_alumni_talk_001', 'cal_lin_primary', 'System direction alumni online sharing', 'The alumnus will introduce the daily division of labor of the basic software team and last year''s campus recruitment process.', 'Online meeting', '2026-05-14T19:30:00+08:00', '2026-05-14T20:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_gpu_booking_001', 'cal_lin_primary', 'A800 node experiment reservation', 'Run vLLM benchmarks with different batch sizes and save the raw logs.', 'GPU cluster', '2026-05-16T09:00:00+08:00', '2026-05-16T12:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_roommate_dinner_001', 'cal_lin_primary', 'Roommate graduation dinner', 'A table for four has already been reserved, and the meetup time is 18:30.', 'Wudaokou', '2026-05-16T18:30:00+08:00', '2026-05-16T20:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_resume_review_001', 'cal_lin_primary', 'College resume clinic', 'The career counseling teacher will return a public version of the resume with annotations on site.', 'Career center', '2026-05-17T10:00:00+08:00', '2026-05-17T10:45:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_run_001', 'cal_lin_primary', 'Jogging on the playground', 'Recovery training; leave half an hour after finishing for washing up.', 'East playground', '2026-05-17T17:00:00+08:00', '2026-05-17T18:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_paper_edit_002', 'cal_lin_primary', 'Revision of Chapter 2 of the paper', 'This revision covers terminology consistency, citation verification, and two flowcharts.', 'Dormitory', '2026-05-18T13:00:00+08:00', '2026-05-18T17:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_department_photo_001', 'cal_lin_primary', 'Graduation photo gathering', 'The college notified everyone to arrive fifteen minutes early and wear academic regalia.', 'In front of the main building', '2026-05-20T08:30:00+08:00', '2026-05-20T10:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_mock_interview_001', 'cal_lin_primary', 'Classmate mock system interview', 'Practice performance bottleneck diagnosis and system design, without involving real company confidential questions.', 'Online meeting', '2026-05-20T19:00:00+08:00', '2026-05-20T20:00:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_advisor_office_001', 'cal_lin_primary', 'Mentor office hour', 'Reserved for paper Q&A; if there are no questions, it may be canceled early.', 'College building 518', '2026-05-21T14:00:00+08:00', '2026-05-21T15:00:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_family_call_001', 'cal_lin_primary', 'Video call with parents', 'The call topic is the graduation ceremony date, return ticket, and luggage shipping.', 'Dormitory', '2026-05-22T20:00:00+08:00', '2026-05-22T20:40:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_thesis_format_001', 'cal_lin_primary', 'Paper format self-check', 'Check chart numbers, references, and the college template requirements.', 'Library', '2026-05-23T09:30:00+08:00', '2026-05-23T11:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_badminton_001', 'cal_lin_primary', 'Laboratory badminton', 'Two courts have been reserved in the gymnasium, and six students have currently signed up.', 'Gymnasium', '2026-05-23T16:00:00+08:00', '2026-05-23T18:00:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_career_office_001', 'cal_lin_primary', 'Consultation open hours for the three-party process', 'On that day, the career center provides the materials checklist, the location of the stamping window, and system entry instructions.', 'Career center', '2026-05-25T14:00:00+08:00', '2026-05-25T15:00:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_lab_cleanup_001', 'cal_lin_primary', 'Laboratory workstation cleanup', 'Back up personal experimental data and return shared equipment.', 'Laboratory', '2026-05-26T17:00:00+08:00', '2026-05-26T18:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_english_practice_001', 'cal_lin_primary', 'English technical expression practice', 'Practice explaining PagedAttention, continuous batching, and performance trade-offs.', 'Online meeting', '2026-05-27T20:00:00+08:00', '2026-05-27T21:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_health_check_001', 'cal_lin_primary', 'Campus hospital report pickup', 'Collect the paper report of the annual physical examination; keep it in your own custody only.', 'Campus hospital', '2026-05-28T11:00:00+08:00', '2026-05-28T11:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_graduation_form_001', 'cal_lin_primary', 'Verification of graduation destination information', 'The college system has currently saved the student ID, major, and expected graduation date, and the organization field is still empty.', 'College system', '2026-05-29T09:00:00+08:00', '2026-05-29T09:40:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_project_handoff_001', 'cal_lin_primary', 'Project code handover', 'Organize reproducible experiment scripts that can be publicly shared, excluding laboratory internal data.', 'Laboratory', '2026-05-29T15:00:00+08:00', '2026-05-29T17:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_weekly_review_001', 'cal_lin_primary', 'Weekly job search review', 'The calendar block comes from personal habits; last week the actual duration was twenty-five minutes.', 'Dormitory', '2026-05-17T21:00:00+08:00', '2026-05-17T21:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_weekly_review_002', 'cal_lin_primary', 'Second job search retrospective', 'This week''s record will be saved separately from the personal notes dated May 17.', 'Dormitory', '2026-05-24T21:00:00+08:00', '2026-05-24T21:40:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_systems_seminar_001', 'cal_lin_primary', 'System direction academic talk', 'The topic is memory management and scheduling for large-model services.', 'College lecture hall', '2026-05-26T10:00:00+08:00', '2026-05-26T11:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_cuda_reading_001', 'cal_lin_primary', 'CUDA document reading', 'Review streams, memory hierarchy, and synchronization semantics.', 'Library', '2026-05-18T20:00:00+08:00', '2026-05-18T21:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_storage_reading_001', 'cal_lin_primary', 'Distributed storage reading group', 'Discuss consistency and fault recovery, which belongs to an adjacent systems direction.', 'Online meeting', '2026-05-22T14:00:00+08:00', '2026-05-22T15:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_train_ticket_001', 'cal_lin_primary', 'Graduation trip waitlist check', '12306 currently shows waitlisted, and the order has not yet been charged.', 'Mobile reminder', '2026-05-24T12:00:00+08:00', '2026-05-24T12:15:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_dorm_inspection_001', 'cal_lin_primary', 'Dormitory safety inspection', 'Keep the room occupied and tidy up the power strip.', 'Student dormitory', '2026-05-27T09:00:00+08:00', '2026-05-27T09:30:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_bank_card_001', 'cal_lin_primary', 'Bank card expiration reminder handling', 'The mobile banking app indicates the ID document will expire in June, and the online update entry is already open.', 'Bank App', '2026-05-30T10:00:00+08:00', '2026-05-30T10:20:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_backup_001', 'cal_lin_primary', 'Paper and resume backup', 'The public resume, thesis source files, and original experiment logs are located in three separate directories.', 'Personal computer', '2026-05-31T16:00:00+08:00', '2026-05-31T17:00:00+08:00', 0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_graduation_rehearsal_001', 'cal_lin_primary', 'Graduation ceremony rehearsal', 'The college announced the time in advance, and the final arrangement may be adjusted.', 'Gymnasium', '2026-06-06T09:00:00+08:00', '2026-06-06T11:00:00+08:00', 0, 'tentative', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL),
  ('cal_proposal_feedback_archive', 'cal_lin_primary', 'Proposal feedback archive', 'The three issues in the mentor''s annotations have been moved into the appendix of the thesis, and the old version of the presentation remains on the college network drive.', 'Library study room', '2026-01-12T14:10:00+08:00', '2026-01-12T15:05:00+08:00', 0, 'confirmed', '2026-01-08T03:25:00Z', '2026-01-12T07:20:00Z', NULL, NULL),
  ('cal_campus_card_reissue', 'cal_lin_primary', 'Campus card replacement pickup', 'The new card number ends in 4821, the old card balance has been migrated, and access control permissions were restored the same day.', 'Student service hall', '2026-01-24T10:20:00+08:00', '2026-01-24T10:45:00+08:00', 0, 'confirmed', '2026-01-21T01:18:00Z', '2026-01-24T03:05:00Z', NULL, NULL),
  ('cal_maintainer_roundtable', 'cal_lin_primary', 'Online communication with open-source maintainers', 'Discuss the compatibility issues of the stress test script in the ROCm environment; the meeting minutes were published by the community host.', 'Jitsi meeting room', '2026-02-06T20:00:00+08:00', '2026-02-06T21:15:00+08:00', 0, 'confirmed', '2026-01-30T09:42:00Z', '2026-02-06T13:30:00Z', NULL, NULL),
  ('cal_dorm_meter_reading', 'cal_lin_primary', 'Dormitory utilities meter reading', 'The floor manager recorded the water meter at 318.6 tons, the electricity meter at 7421.3 kWh, and all four people in the room were registered.', 'Building 7 of the student dormitory', '2026-02-18T17:40:00+08:00', '2026-02-18T18:00:00+08:00', 0, 'confirmed', '2026-02-15T06:12:00Z', '2026-02-18T10:18:00Z', NULL, NULL),
  ('cal_library_hold_pickup', 'cal_lin_primary', 'Reserved book pickup', 'Pick up the English edition of Designing Data-Intensive Applications; the reservation will be held until closing on that day.', 'Second floor of the school library', '2026-03-03T12:15:00+08:00', '2026-03-03T12:35:00+08:00', 0, 'confirmed', '2026-02-28T11:05:00Z', '2026-03-03T04:52:00Z', NULL, NULL),
  ('cal_family_birthday_call', 'cal_lin_primary', 'Grandma birthday video', 'Seven people are already in the family group, and uncle is responsible for connecting the living room TV.', 'Dormitory', '2026-03-16T19:45:00+08:00', '2026-03-16T20:25:00+08:00', 0, 'confirmed', '2026-03-10T02:30:00Z', '2026-03-16T12:40:00Z', NULL, NULL),
  ('cal_physio_followup', 'cal_lin_primary', 'Ankle rehabilitation follow-up test', 'Retesting showed the single-leg standing time recovered to forty-five seconds, and the physical therapist recorded mild soreness after light activity.', 'Campus hospital rehabilitation room', '2026-03-28T09:30:00+08:00', '2026-03-28T10:10:00+08:00', 0, 'confirmed', '2026-03-22T08:14:00Z', '2026-03-28T02:36:00Z', NULL, NULL),
  ('cal_cloud_invoice_review', 'cal_lin_primary', 'Personal cloud account bill verification', 'March expenses included 18.7 yuan for object storage and 46.2 yuan for temporary GPU instances, with 40 yuan offset by the education credit.', 'Personal computer', '2026-04-07T21:10:00+08:00', '2026-04-07T21:40:00+08:00', 0, 'confirmed', '2026-04-04T05:28:00Z', '2026-04-07T14:05:00Z', NULL, NULL),
  ('cal_transit_refund', 'cal_lin_primary', 'Campus bus card refund', 'The old card deposit and remaining 23.5 yuan have been refunded to Alipay, and the service window issued an electronic receipt.', 'Campus transportation service point', '2026-04-19T11:25:00+08:00', '2026-04-19T11:50:00+08:00', 0, 'confirmed', '2026-04-15T01:47:00Z', '2026-04-19T04:16:00Z', NULL, NULL),
  ('cal_network_seminar', 'cal_lin_primary', 'High-Performance Networking Academic Report', 'The report case studies cover RDMA congestion control and multi-tenant isolation, and the Q&A lasted twenty-five minutes.', 'College building 101', '2026-04-27T15:20:00+08:00', '2026-04-27T17:05:00+08:00', 0, 'confirmed', '2026-04-20T07:33:00Z', '2026-04-27T09:25:00Z', NULL, NULL),
  ('cal_parcel_pickup', 'cal_lin_primary', 'Graduation materials parcel pickup', 'The parcel at the pickup station contains a degree gown collection form and alumni card instructions; the last four digits of the signing code are 7316.', 'Cainiao Station at the East Gate', '2026-05-03T18:05:00+08:00', '2026-05-03T18:25:00+08:00', 0, 'confirmed', '2026-05-02T03:09:00Z', '2026-05-03T10:44:00Z', NULL, NULL),
  ('cal_camera_checkout', 'cal_lin_primary', 'College camera borrowing registration', 'The publicity team tentatively plans to hand over the camera and backup batteries on the morning of May 20; the registration status has not yet been confirmed.', 'Main building lobby', '2026-05-20T09:00:00+08:00', '2026-05-20T09:25:00+08:00', 0, 'tentative', '2026-05-09T06:50:00Z', '2026-05-09T07:12:00Z', NULL, NULL);

INSERT INTO attendees (event_id, email, name, response_status) VALUES
  ('cal_maintainer_roundtable', 'host@open-runtime.example.org', 'Luo Jin', 'accepted'),
  ('cal_family_birthday_call', 'uncle.chen@example.net', 'Chen Kai', 'accepted'),
  ('cal_network_seminar', 'seminar@cs.example.edu.cn', 'System Institute report group', 'accepted'),
  ('cal_roommate_dinner_001', 'roommate.zhou@example.com', 'Zhou Ning', 'tentative'),
  ('cal_group_meeting_001', 'advisor-prof-he@example.edu.cn', 'Professor He', 'accepted'),
  ('cal_camera_checkout', 'media.team@example.edu.cn', 'College publicity team', 'needsAction');

INSERT INTO reminders (event_id, method, minutes_before) VALUES
  ('cal_thesis_001', 'popup', 60),
  ('cal_group_meeting_001', 'popup', 30),
  ('cal_lab_sync_001', 'popup', 30),
  ('cal_library_renewal_001', 'popup', 60),
  ('cal_alumni_talk_001', 'popup', 30),
  ('cal_gpu_booking_001', 'popup', 30),
  ('cal_roommate_dinner_001', 'popup', 60),
  ('cal_resume_review_001', 'popup', 30),
  ('cal_run_001', 'popup', 30),
  ('cal_paper_edit_002', 'popup', 60),
  ('cal_department_photo_001', 'popup', 30),
  ('cal_mock_interview_001', 'popup', 30),
  ('cal_advisor_office_001', 'popup', 60),
  ('cal_family_call_001', 'popup', 30),
  ('cal_thesis_format_001', 'popup', 30),
  ('cal_badminton_001', 'popup', 60),
  ('cal_career_office_001', 'popup', 30),
  ('cal_lab_cleanup_001', 'popup', 30),
  ('cal_campus_card_reissue', 'email', 720),
  ('cal_maintainer_roundtable', 'popup', 20),
  ('cal_library_hold_pickup', 'popup', 90),
  ('cal_physio_followup', 'email', 1440),
  ('cal_network_seminar', 'popup', 45),
  ('cal_camera_checkout', 'popup', 15);

COMMIT;
