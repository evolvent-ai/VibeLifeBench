-- Stage 0 calendar state for  translated text  on 2026-06-15; review and settlement results are event-gated.
BEGIN;
INSERT INTO calendars (calendar_id,user_id,name,color,timezone,is_primary,created_at) VALUES
('cal_awch_main','usr_mo_fan','Personal calendar','#4285F4','Asia/Shanghai',1,'2024-01-01T00:00:00Z'),
('cal_awch_task','usr_mo_fan','Apple Watch trade-in','#0B8043','Asia/Shanghai',0,'2026-05-22T00:00:00Z'),
('cal_awch_work','usr_mo_fan','Fitness studio schedule','#8E24AA','Asia/Shanghai',0,'2025-10-01T00:00:00Z');
INSERT INTO events (event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id) VALUES
('0d7a4c92-b561-48ef-93a2-6c18e5b7d4fa','cal_awch_task',' translated text table translated text review','verifymodel、serial number、batch、inspection reference translated text battery healthrecord。','online','2026-06-16T19:30:00+08:00','2026-06-16T20:20:00+08:00',0,'confirmed','2026-06-09T00:00:00Z','2026-06-09T00:00:00Z',NULL,NULL),
('83e1b6d5-2c94-47a0-bf38-5d7a21e96c4f','cal_awch_task','recycler translated text ',' translated text appraisalreview translated text formalstatus translated text 。','online','2026-06-20T12:00:00+08:00','2026-06-20T12:20:00+08:00',0,'tentative','2026-06-14T00:00:00Z','2026-06-14T00:00:00Z',NULL,NULL),
('f4a29c81-6d35-42be-8c71-1b9e50d64af3','cal_awch_task',' translated text ',' translated text battery health translated text 、appearancephotos、 translated text video、 translated text record。','Home translated text ','2026-06-24T20:00:00+08:00','2026-06-24T21:00:00+08:00',0,'confirmed','2026-06-12T00:00:00Z','2026-06-12T00:00:00Z',NULL,NULL),
('2b97d5e3-c816-49a4-a1f3-7e52c08d64bf','cal_awch_task',' translated text ledgerreview',' translated text table translated text 、 translated text discount translated text 、dispute translated text credited。','online','2026-06-30T09:00:00+08:00','2026-06-30T09:30:00+08:00',0,'confirmed','2026-06-12T00:00:00Z','2026-06-12T00:00:00Z',NULL,NULL),
('d61c4a09-3e58-43fb-97d2-8a20b5e16c7f','cal_awch_task','platform reviewevidence submission translated text ',' translated text  7  translated text  9  translated text ；confirm translated text 。','online','2026-07-09T18:00:00+08:00','2026-07-09T18:30:00+08:00',0,'confirmed','2026-06-11T00:00:00Z','2026-06-11T00:00:00Z',NULL,NULL),
('75e8b3d2-f104-46ac-9b71-2c5d80a63ef4','cal_awch_main',' translated text payment due date','normalamount due translated text disputeamountrespectivelyverify。',' translated text ','2026-07-10T09:00:00+08:00','2026-07-10T09:20:00+08:00',0,'confirmed','2026-06-06T00:00:00Z','2026-06-06T00:00:00Z',NULL,NULL),
('a3d52f86-7c19-45e0-b4a8-9f20d76c315e','cal_awch_task','closing deadline',' translated text tableverify、appraisalreview、top-up payment translated text archive。','online','2026-07-15T10:30:00+08:00','2026-07-15T11:30:00+08:00',0,'confirmed','2026-06-01T00:00:00Z','2026-06-01T00:00:00Z',NULL,NULL),
('6c18e5b4-92d3-4fa7-81c0-5e26b9d74a3f','cal_awch_work',' translated text ','verify translated text 、 translated text rules translated text 。',' translated text  2F','2026-06-18T15:00:00+08:00','2026-06-18T16:00:00+08:00',0,'confirmed','2026-06-05T00:00:00Z','2026-06-05T00:00:00Z',NULL,NULL),
('e802b7a1-4d73-48cf-a519-6b9e25d63f0c','cal_awch_main',' translated text ',' translated text 。',' translated text ','2026-06-28T10:00:00+08:00','2026-06-28T11:00:00+08:00',0,'confirmed','2026-06-10T00:00:00Z','2026-06-10T00:00:00Z',NULL,NULL),
('5f63a8d9-b210-46e4-97c5-1d8a42b73e6f','cal_awch_main','Home translated text ',' translated text ，retain translated text 。','ShanghaiXuhui translated text ','2026-06-14T09:00:00+08:00','2026-06-14T11:00:00+08:00',0,'cancelled','2026-06-11T00:00:00Z','2026-06-13T00:00:00Z',NULL,NULL),
('b4d91c36-2a75-49ef-83b0-7c86e15d4a2f','cal_awch_work',' translated text ',' translated text 。','online translated text ','2026-07-03T16:00:00+08:00','2026-07-03T17:00:00+08:00',0,'confirmed','2026-06-08T00:00:00Z','2026-06-08T00:00:00Z',NULL,NULL),
('38a7e5c4-d961-43b8-a2f0-6e25c97d14ba','cal_awch_main',' translated text ',' translated text ， translated text 。',' translated text ','2026-05-31T13:30:00+08:00','2026-05-31T17:10:00+08:00',0,'confirmed','2026-05-16T08:20:00Z','2026-05-31T09:25:00Z',NULL,NULL),
('c7f42b93-8e15-46ad-90d3-2a6b51e78cf4','cal_awch_main',' translated text item',' translated text ， translated text 。',' translated text ','2026-06-12T18:20:00+08:00','2026-06-12T18:45:00+08:00',0,'confirmed','2026-06-09T05:10:00Z','2026-06-12T11:05:00Z',NULL,NULL),
('90d3a7f8-2c65-4be1-b940-5e37d82a6c1f','cal_awch_main',' translated text ',' translated text photos，active translated text  86  translated text 。',' translated text ','2026-06-06T18:10:00+08:00','2026-06-06T21:30:00+08:00',0,'confirmed','2026-05-28T09:35:00Z','2026-06-06T14:15:00Z',NULL,NULL),
('4a82e1d7-f356-40bc-8d59-3c70a96e25bf','cal_awch_main',' translated text ',' translated text table translated text ， translated text item translated text 。',' translated text ','2026-06-09T14:00:00+08:00','2026-06-09T16:05:00+08:00',0,'confirmed','2026-06-01T06:50:00Z','2026-06-09T08:20:00Z',NULL,NULL);
INSERT INTO attendees (event_id,email,name,response_status) VALUES
('6c18e5b4-92d3-4fa7-81c0-5e26b9d74a3f','ops-review@studio.example',' translated text group','accepted'),
('e802b7a1-4d73-48cf-a519-6b9e25d63f0c','booking@jingan-sports.example',' translated text ','accepted'),
('b4d91c36-2a75-49ef-83b0-7c86e15d4a2f','coaches@studio.example',' translated text ','accepted');
INSERT INTO reminders (event_id,method,minutes_before) VALUES
('0d7a4c92-b561-48ef-93a2-6c18e5b7d4fa','popup',120),('83e1b6d5-2c94-47a0-bf38-5d7a21e96c4f','email',1440),('f4a29c81-6d35-42be-8c71-1b9e50d64af3','popup',180),('2b97d5e3-c816-49a4-a1f3-7e52c08d64bf','popup',60),
('d61c4a09-3e58-43fb-97d2-8a20b5e16c7f','email',2880),('d61c4a09-3e58-43fb-97d2-8a20b5e16c7f','popup',360),('75e8b3d2-f104-46ac-9b71-2c5d80a63ef4','popup',1440),('a3d52f86-7c19-45e0-b4a8-9f20d76c315e','email',2880),
('6c18e5b4-92d3-4fa7-81c0-5e26b9d74a3f','popup',30),('e802b7a1-4d73-48cf-a519-6b9e25d63f0c','popup',1440),('b4d91c36-2a75-49ef-83b0-7c86e15d4a2f','popup',60),
('38a7e5c4-d961-43b8-a2f0-6e25c97d14ba','popup',45),('c7f42b93-8e15-46ad-90d3-2a6b51e78cf4','email',360),
('90d3a7f8-2c65-4be1-b940-5e37d82a6c1f','popup',90),('4a82e1d7-f356-40bc-8d59-3c70a96e25bf','email',720);
INSERT INTO _counters (key,value) VALUES ('event_seq',15);
COMMIT;
