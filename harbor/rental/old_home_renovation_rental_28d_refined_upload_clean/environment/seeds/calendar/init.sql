PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "reminders";
DELETE FROM "attendees";
DELETE FROM "events";
DELETE FROM "calendars";
INSERT INTO "calendars" ("calendar_id","user_id","name","color","timezone","is_primary","created_at") VALUES ('cal_zl_rental_reno','usr_zhanglan','translated source textrefurbishmentrental','#3366cc','Asia/Shanghai',1,'2026-07-01T08:00:00+08:00');
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_budget_review_0709','cal_zl_rental_reno','refurbishmenttranslated source text','translated source text、alreadytranslated source textandtranslated source text。','translated source text','2026-07-09T09:00:00+08:00','2026-07-09T09:30:00+08:00',0,'tentative','2026-07-01T08:00:00+08:00','2026-07-01T08:00:00+08:00',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_air_test_hold_0717','cal_zl_rental_reno','air-quality testingtranslated source text','testingtranslated source textnottranslated source text，translated source text。','Unit 603, Hongqiao Jiayuan','2026-07-17T10:00:00+08:00','2026-07-17T11:00:00+08:00',0,'tentative','2026-07-01T08:00:00+08:00','2026-07-01T08:00:00+08:00',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_meter_read_0708','cal_zl_rental_reno','translated source text','recordtranslated source text、translated source textandtranslated source text daytranslated source text。','Unit 603, Hongqiao Jiayuan','2026-07-08T08:30:00+08:00','2026-07-08T09:00:00+08:00',0,'confirmed','2026-06-30T09:00:00+08:00','2026-06-30T09:00:00+08:00',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_bank_visit_0712','cal_zl_rental_reno','translated source text','Zhang Lantranslated source textandtranslated source text。','translated source text','2026-07-12T14:00:00+08:00','2026-07-12T15:00:00+08:00',0,'confirmed','2026-06-29T10:00:00+08:00','2026-06-29T10:00:00+08:00',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_family_visit_0714','cal_zl_rental_reno','translated source text','Zhang Lantranslated source textChangningtranslated source text，translated source text。','Shanghai','2026-07-14T18:30:00+08:00','2026-07-14T20:30:00+08:00',0,'confirmed','2026-06-28T12:00:00+08:00','2026-06-28T12:00:00+08:00',NULL,NULL);
INSERT INTO "events" ("event_id","calendar_id","summary","description","location","start_dt","end_dt","all_day","status","created_at","updated_at","recurrence_rule","parent_event_id") VALUES ('evt_20260726_R7mK4Q','cal_zl_rental_reno','rentaltranslated source text','translated source text、translated source textandtranslated source text。','translated source text','2026-07-26T09:30:00+08:00','2026-07-26T11:00:00+08:00',0,'tentative','2026-06-30T15:00:00+08:00','2026-06-30T15:00:00+08:00',NULL,NULL);
COMMIT;
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO events(event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id) VALUES
('evt_hjtranslated source text','cal_zl_rental_reno','translated source text','translated source text。','translated source text','2026-01-06T09:00:00+08:00','2026-01-06T09:40:00+08:00',0,'confirmed','2026-01-04T18:20:00+08:00','2026-01-06T09:45:00+08:00',NULL,NULL),
('evt_hj_lock_service','cal_zl_rental_reno','translated source text','translated source text C translated source text。','Unit 603, Hongqiao Jiayuan','2026-02-16T16:00:00+08:00','2026-02-16T17:00:00+08:00',0,'confirmed','2026-02-13T11:15:00+08:00','2026-02-16T17:05:00+08:00',NULL,NULL),
('evt_hj_fire_service','cal_zl_rental_reno','translated source text','translated source textcompletedtranslated source textandtranslated source text。','Unit 603, Hongqiao Jiayuan','2026-02-18T15:00:00+08:00','2026-02-18T16:00:00+08:00',0,'confirmed','2026-02-14T08:40:00+08:00','2026-02-18T16:05:00+08:00',NULL,NULL),
('evt_hj_drain_clean','cal_zl_rental_reno','translated source text','translated source text。','Unit 603, Hongqiao Jiayuan','2026-02-22T13:00:00+08:00','2026-02-22T14:00:00+08:00',0,'confirmed','2026-02-20T19:20:00+08:00','2026-02-22T14:10:00+08:00',NULL,NULL),
('evt_hj_policy_review','cal_zl_rental_reno','translated source text','translated source textandtranslated source text。','translated source text','2026-03-05T10:00:00+08:00','2026-03-05T10:30:00+08:00',0,'confirmed','2026-03-02T09:10:00+08:00','2026-03-05T10:35:00+08:00',NULL,NULL),
('evt_hj_tax_filing','cal_zl_rental_reno','translated source text','translated source text。','translated source text','2026-03-18T09:30:00+08:00','2026-03-18T10:20:00+08:00',0,'confirmed','2026-03-12T15:25:00+08:00','2026-03-18T10:25:00+08:00',NULL,NULL),
('evt_hj_tenant_exit','cal_zl_rental_reno','translated source texttenanttranslated source text','translated source text、translated source textandtranslated source text。','Unit 603, Hongqiao Jiayuan','2026-04-02T14:00:00+08:00','2026-04-02T15:30:00+08:00',0,'confirmed','2026-03-25T10:05:00+08:00','2026-04-02T15:35:00+08:00',NULL,NULL),
('evt_hj_spring_clean','cal_zl_rental_reno','translated source text','translated source texttreatmenttranslated source text、translated source textandtranslated source text。','Unit 603, Hongqiao Jiayuan','2026-04-09T14:00:00+08:00','2026-04-09T17:30:00+08:00',0,'confirmed','2026-04-05T12:10:00+08:00','2026-04-09T17:45:00+08:00',NULL,NULL),
('evt_hj_storage_pickup','cal_zl_rental_reno','translated source text','translated source textandtranslated source text。','Unit 603, Hongqiao Jiayuan','2026-04-12T09:00:00+08:00','2026-04-12T10:30:00+08:00',0,'confirmed','2026-04-08T18:40:00+08:00','2026-04-12T10:35:00+08:00',NULL,NULL),
('evt_hj_balcony_test','cal_zl_rental_reno','translated source text','translated source text，translated source text。','Unit 603, Hongqiao Jiayuan','2026-04-18T11:00:00+08:00','2026-04-18T11:40:00+08:00',0,'confirmed','2026-04-16T09:30:00+08:00','2026-04-18T11:45:00+08:00',NULL,NULL),
('evt_hj_window_hinge','cal_zl_rental_reno','translated source text','translated source text。','Unit 603, Hongqiao Jiayuan','2026-04-27T15:30:00+08:00','2026-04-27T16:30:00+08:00',0,'confirmed','2026-04-23T13:15:00+08:00','2026-04-27T16:35:00+08:00',NULL,NULL),
('evt_hj_pipe_check','cal_zl_rental_reno','translated source text','translated source textandtranslated source textcompletedtranslated source text。','Unit 603, Hongqiao Jiayuan','2026-05-12T08:30:00+08:00','2026-05-12T09:30:00+08:00',0,'confirmed','2026-05-09T17:05:00+08:00','2026-05-12T09:35:00+08:00',NULL,NULL),
('evt_hj_ac_clean','cal_zl_rental_reno','translated source text','translated source textandtranslated source textcompletedtranslated source text。','Unit 603, Hongqiao Jiayuan','2026-05-15T16:00:00+08:00','2026-05-15T18:00:00+08:00',0,'confirmed','2026-05-10T10:50:00+08:00','2026-05-15T18:20:00+08:00',NULL,NULL),
('evt_hj_elevator_check','cal_zl_rental_reno','translated source text','translated source textcompletedtranslated source textandtranslated source text。','Hongqiao Jiayuan6translated source text','2026-06-12T08:00:00+08:00','2026-06-12T11:30:00+08:00',0,'confirmed','2026-05-26T15:20:00+08:00','2026-06-12T11:40:00+08:00',NULL,NULL),
('evt_hj_lamps_arrival','cal_zl_rental_reno','translated source textarrival','translated source textandtranslated source text。','Hongqiao Jiayuantranslated source text','2026-06-20T15:00:00+08:00','2026-06-20T15:30:00+08:00',0,'confirmed','2026-06-18T10:10:00+08:00','2026-06-20T15:35:00+08:00',NULL,NULL),
('evt_hj_tools_arrival','cal_zl_rental_reno','translated source text','translated source textandtranslated source text603translated source text。','Unit 603, Hongqiao Jiayuan','2026-06-26T11:20:00+08:00','2026-06-26T12:00:00+08:00',0,'confirmed','2026-06-24T13:40:00+08:00','2026-06-26T12:05:00+08:00',NULL,NULL);
INSERT INTO attendees(event_id,email,name,response_status) VALUES
('evt_hjtranslated source text','zhanglan@example.com','Zhang Lan','accepted'),
('evt_hj_lock_service','service@minhang-lock.example','translated source text','accepted'),
('evt_hj_fire_service','service@mh-fire.example','translated source text','accepted'),
('evt_hj_drain_clean','service@qibao-pipe.example','translated source text','accepted'),
('evt_hj_policy_review','advisor@cpic.example','translated source text','accepted'),
('evt_hj_tax_filing','zhanglan@example.com','Zhang Lan','accepted'),
('evt_hj_tenant_exit','archive@rental-agent.example','translated source textleasetranslated source text','accepted'),
('evt_hj_spring_clean','service@hongjie-clean.example','translated source text','accepted'),
('evt_hj_storage_pickup','service@minhang-storage.example','translated source text','accepted'),
('evt_hj_balcony_test','property@hongqiao-estate.example','property managementtranslated source text','tentative'),
('evt_hj_window_hinge','service@windowcare.example','translated source text','accepted'),
('evt_hj_pipe_check','service@qibao-pipe.example','translated source text','accepted'),
('evt_hj_ac_clean','service@coolair.example','translated source text','accepted'),
('evt_hj_elevator_check','property@hongqiao-estate.example','property managementtranslated source text','accepted'),
('evt_hj_lamps_arrival','courier@sf.example','SF Expresstranslated source text','accepted'),
('evt_hj_tools_arrival','courier@jd-logistics.example','translated source textdeliverytranslated source text','accepted');
INSERT INTO reminders(event_id,method,minutes_before) VALUES
('evt_hjtranslated source text','popup',30),
('evt_hj_lock_service','email',720),
('evt_hj_fire_service','popup',60),
('evt_hj_drain_clean','email',1440),
('evt_hj_policy_review','popup',20),
('evt_hj_tax_filing','email',2880),
('evt_hj_tenant_exit','popup',90),
('evt_hj_spring_clean','email',720),
('evt_hj_storage_pickup','popup',45),
('evt_hj_balcony_test','email',360),
('evt_hj_window_hinge','popup',40),
('evt_hj_pipe_check','email',720),
('evt_hj_ac_clean','popup',60),
('evt_hj_elevator_check','email',1440),
('evt_hj_lamps_arrival','popup',20),
('evt_hj_tools_arrival','email',360);
COMMIT;
