PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "reminders";
DELETE FROM "attendees";
DELETE FROM "events";
DELETE FROM "calendars";
INSERT INTO "calendars" ("calendar_id","user_id","name","color","timezone","is_primary","created_at") VALUES ('cal_njr_primary','usr_gufeng','Gu Feng personal calendar','#3b82f6','Asia/Shanghai',1,'2026-06-28T08:00:00Z');
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_offer_hr_call','cal_njr_primary','Nanjingnew companyonboardingmaterialsconfirm','HR rental recordreportingidentity document、access controlandentryrental recordthisrental recordprocess。','online','2026-06-29T16:00:00Z','2026-06-29T16:30:00Z',0,'confirmed','2026-06-27T08:10:00Z','2026-06-27T08:10:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_video_viewing_hold','cal_njr_primary','remoteviewingrental recordleave','Gu Fengrental recordunitbetweenphotoandvideorental recordleaverental recordofrental recordpersontime。','online','2026-07-05T10:00:00Z','2026-07-05T11:00:00Z',0,'tentative','2026-06-27T09:20:00Z','2026-06-27T09:20:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_wuhan_pack','cal_njr_primary','Wuhanoldrental record','rental record、rental recordandrental recordrespectivelyrental record。','Wuhan','2026-07-11T09:00:00Z','2026-07-11T12:00:00Z',0,'confirmed','2026-06-26T18:00:00Z','2026-06-26T18:00:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_bank_counter','cal_njr_primary','bankrental recordconfirm','Gu Fengatrental recorddaytransferrental recordandrental record。','Wuhan','2026-07-13T14:00:00Z','2026-07-13T15:00:00Z',0,'confirmed','2026-06-27T11:30:00Z','2026-06-27T11:30:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_final_remote_check','cal_njr_primary','lease signingbeforeremotematerialsrental record','Gu Fengorganizeproperty deedcopy、contractversionandplatformpagescreenshot。','online','2026-07-15T19:00:00Z','2026-07-15T20:00:00Z',0,'tentative','2026-06-27T12:00:00Z','2026-06-27T12:00:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_train_to_nanjing','cal_njr_primary','Wuhanbeforerental recordNanjing','rental recordtimenot yetrental record，rental recordonerental recordandrental record。','Wuhan Station—Nanjingrental record Station','2026-07-19T13:00:00Z','2026-07-19T17:30:00Z',0,'tentative','2026-06-25T14:00:00Z','2026-06-25T14:00:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_first_day','cal_njr_primary','Nanjingnew companyfirstdayreport to work','9:30 beforetoJiangbei New AreaSoftware Avenueoffice room。','Jiangbei New AreaSoftware Avenue','2026-07-20T01:30:00Z','2026-07-20T10:00:00Z',0,'confirmed','2026-06-20T10:00:00Z','2026-06-20T10:00:00Z',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_family_call','cal_njr_primary','family video call','andrental recordWuhanoldrental recordrentandrental recordNanjingafterofliverental record。','online','2026-07-12T12:00:00Z','2026-07-12T12:30:00Z',0,'confirmed','2026-06-27T13:00:00Z','2026-06-27T13:00:00Z',NULL,NULL);
COMMIT;
DELETE FROM events WHERE start_dt > '2026-06-28T01:00:00Z';
UPDATE calendars SET created_at = '2026-06-27T23:00:00Z' WHERE calendar_id = 'cal_njr_primary';
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO calendars(calendar_id,user_id,name,color,timezone,is_primary,created_at) VALUES ('cal_4Kq9mT7vP','usr_gufeng','Gu Feng history and work','#64748b','Asia/Shanghai',0,'2026-01-03T09:00:00Z');
INSERT INTO events(event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id) VALUES
('evt_njr_interview_one','cal_4Kq9mT7vP','Nanjingrental record','rental recordpersonrental recordanditemrental recordweekrental record。','online','2026-03-18T11:00:00Z','2026-03-18T12:00:00Z',0,'confirmed','2026-03-14T08:20:00Z','2026-03-18T12:05:00Z',NULL,NULL),
('evt_njr_interview_two','cal_4Kq9mT7vP','Nanjingrental record','rental recordsendrental recordremoterental record。','online','2026-03-25T07:30:00Z','2026-03-25T08:20:00Z',0,'confirmed','2026-03-21T10:15:00Z','2026-03-25T08:25:00Z',NULL,NULL),
('evt_njr_offer_review','cal_4Kq9mT7vP','rental recordconditionsrental recordcommunicate','rental record、rental recordandreportingrental recordwritewillrental recordneed。','online','2026-04-07T06:00:00Z','2026-04-07T06:40:00Z',0,'confirmed','2026-04-03T11:35:00Z','2026-04-07T06:45:00Z',NULL,NULL),
('evt_njr_health_transfer','cal_njr_primary','rental recordonlinerental record','rental recordplatformrental recordplease。','online','2026-04-17T09:00:00Z','2026-04-17T09:30:00Z',0,'confirmed','2026-04-15T13:20:00Z','2026-04-17T09:32:00Z',NULL,NULL),
('evt_njr_training_intro','cal_4Kq9mT7vP','onboardingrental record','rental recordplatformrental record。','online','2026-05-01T02:00:00Z','2026-05-01T02:45:00Z',0,'confirmed','2026-04-29T12:10:00Z','2026-05-01T02:50:00Z',NULL,NULL),
('evt_njr_storage_visit','cal_njr_primary','rental recordyourental record','viewrental recordandaccess controlroute。','Wuhanrental record','2026-05-11T08:30:00Z','2026-05-11T09:20:00Z',0,'confirmed','2026-05-08T16:20:00Z','2026-05-11T09:25:00Z',NULL,NULL),
('evt_njr_oldhome_inventory','cal_njr_primary','oldrental record','landlord、Gu Fengrental recordrecordrental record。','Wuhanoldrental record','2026-05-13T13:00:00Z','2026-05-13T14:00:00Z',0,'confirmed','2026-05-10T09:45:00Z','2026-05-13T14:05:00Z',NULL,NULL),
('evt_njr_train_reschedule','cal_njr_primary','Nanjingrental record','rental recordhourrental recordtime。','online','2026-05-19T10:00:00Z','2026-05-19T10:20:00Z',0,'confirmed','2026-05-19T08:50:00Z','2026-05-19T10:25:00Z',NULL,NULL),
('evt_njr_mover_video','cal_njr_primary','rental recordvideorental record','rental recordunitbetweenvideorental record。','online','2026-05-24T08:00:00Z','2026-05-24T08:35:00Z',0,'confirmed','2026-05-21T12:10:00Z','2026-05-24T08:40:00Z',NULL,NULL),
('evt_njr_gym_freeze','cal_njr_primary','rental recordwillrental record','rental recordinrental recordmonthrental record。','Wuhanrental record','2026-05-30T13:30:00Z','2026-05-30T14:10:00Z',0,'confirmed','2026-05-27T18:15:00Z','2026-05-30T14:15:00Z',NULL,NULL),
('evt_njr_cert_exam','cal_4Kq9mT7vP','rental recordverifiedrental record','onlinerental recordhourrental recordminutes。','online','2026-06-08T06:30:00Z','2026-06-08T08:00:00Z',0,'confirmed','2026-05-22T12:15:00Z','2026-06-08T08:05:00Z',NULL,NULL),
('evt_njr_clinic_visit','cal_njr_primary','Wuhaninrental record','completerental recordandrental record。','Wuhanrental recordinrental record','2026-06-09T06:00:00Z','2026-06-09T07:10:00Z',0,'confirmed','2026-06-05T09:05:00Z','2026-06-09T07:15:00Z',NULL,NULL),
('evt_njr_oldhome_precheck','cal_njr_primary','Wuhanoldrental recordrentrental record','landlordrecordrental recordandkitchenrental recordstatus。','Wuhanoldrental record','2026-06-12T06:00:00Z','2026-06-12T06:45:00Z',0,'confirmed','2026-06-08T14:30:00Z','2026-06-12T06:50:00Z',NULL,NULL),
('evt_njr_box_delivery','cal_njr_primary','rental record','rental recordinnumberrental recordatoldrental recordliving room。','Wuhanoldrental record','2026-06-16T04:00:00Z','2026-06-16T04:30:00Z',0,'confirmed','2026-06-14T10:20:00Z','2026-06-16T04:35:00Z',NULL,NULL),
('evt_njr_storage_move','cal_njr_primary','rental record','rental recordandkitchenrental recordyourental record。','Wuhanrental record','2026-06-18T03:30:00Z','2026-06-18T05:00:00Z',0,'confirmed','2026-06-15T12:05:00Z','2026-06-18T05:10:00Z',NULL,NULL),
('evt_njr_laptop_service','cal_njr_primary','entryrental recordthisrental record','rental recordandcompleterental record。','Wuhanrental record','2026-06-19T08:00:00Z','2026-06-19T09:30:00Z',0,'confirmed','2026-06-17T11:45:00Z','2026-06-19T09:35:00Z',NULL,NULL),
('evt_njr_team_intro','cal_4Kq9mT7vP','Nanjingrental recordonlinerental record','rental recordnamerental recordandrental recordcommunicatechannel。','online','2026-06-22T12:00:00Z','2026-06-22T12:45:00Z',0,'confirmed','2026-06-20T07:30:00Z','2026-06-22T12:50:00Z',NULL,NULL),
('evt_njr_cancelled_picnic','cal_njr_primary','rental record','rental recordafterrental recordcancelled。','Wuhanrental record','2026-06-26T10:00:00Z','2026-06-26T13:00:00Z',0,'cancelled','2026-06-20T09:40:00Z','2026-06-25T13:20:00Z',NULL,NULL);
INSERT INTO attendees(event_id,email,name,response_status) VALUES
('evt_njr_interview_one','techlead@nanjing-tech.example.cn','rental recordperson','accepted'),
('evt_njr_interview_two','director@nanjing-tech.example.cn','rental recordsendrental record','accepted'),
('evt_njr_offer_review','hr@nanjing-tech.example.cn','rental record','accepted'),
('evt_njr_health_transfer','gufeng@vmail.example.cn','Gu Feng','accepted'),
('evt_njr_training_intro','learning@nanjing-tech.example.cn','rental record','accepted'),
('evt_njr_storage_visit','service@hankou-storage.example.cn','rental record','accepted'),
('evt_njr_oldhome_inventory','landlord.wuhan@example.cn','Wuhanoldlandlord','accepted'),
('evt_njr_train_reschedule','gufeng@vmail.example.cn','Gu Feng','accepted'),
('evt_njr_mover_video','survey@wuhan-move.example.cn','rental record','accepted'),
('evt_njr_gym_freeze','service@optics-gym.example.cn','willrental record','accepted'),
('evt_njr_cert_exam','gufeng@vmail.example.cn','Gu Feng','accepted'),
('evt_njr_clinic_visit','gufeng@vmail.example.cn','Gu Feng','accepted'),
('evt_njr_oldhome_precheck','landlord.wuhan@example.cn','Wuhanoldlandlord','accepted'),
('evt_njr_box_delivery','courier@packing.example.cn','rental record','accepted'),
('evt_njr_storage_move','gufeng@vmail.example.cn','Gu Feng','accepted'),
('evt_njr_laptop_service','service@computer.example.cn','rental record','accepted'),
('evt_njr_team_intro','manager@nanjing-tech.example.cn','Nanjingrental record','accepted'),
('evt_njr_cancelled_picnic','colleague@wuhan-oldjob.example.cn','rental record','declined');
INSERT INTO reminders(event_id,method,minutes_before) VALUES
('evt_njr_interview_one','email',1440),
('evt_njr_interview_two','popup',60),
('evt_njr_offer_review','email',720),
('evt_njr_health_transfer','popup',30),
('evt_njr_training_intro','email',360),
('evt_njr_storage_visit','popup',45),
('evt_njr_oldhome_inventory','email',1440),
('evt_njr_train_reschedule','popup',15),
('evt_njr_mover_video','email',120),
('evt_njr_gym_freeze','popup',40),
('evt_njr_cert_exam','email',2880),
('evt_njr_clinic_visit','popup',90),
('evt_njr_oldhome_precheck','email',720),
('evt_njr_box_delivery','popup',20),
('evt_njr_storage_move','email',360),
('evt_njr_laptop_service','popup',30),
('evt_njr_team_intro','email',1440),
('evt_njr_cancelled_picnic','popup',180);
COMMIT;
