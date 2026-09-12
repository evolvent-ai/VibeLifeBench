-- Generated calendar seed for camera_resale_30d
BEGIN;
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_rscam_main', 'usr_zhan_peng', 'Personal', '#4285F4', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_rscam_task', 'usr_zhan_peng', 'Sonar A7M3 camera record', '#0B8043', 'Asia/Shanghai', 0, '2026-05-01T00:00:00Z');
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('evt_rscam_c1', 'cal_rscam_task', 'camera record', 'camera record，camera record、camera record、camera record、camera record。', '', '2026-07-15T10:30:00+08:00', '2026-07-15T13:00:00+08:00', 0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('evt_rscam_c2', 'cal_rscam_main', 'camera record', 'camera record 7 camera record 10 camera record；camera record。', '', '2026-07-10T09:00:00+08:00', '2026-07-10T09:30:00+08:00', 0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('evt_rscam_c3', 'cal_rscam_task', 'camera record(camera record)', 'camera record，camera record。', 'camera record(camera record)', '2026-07-02T18:00:00+08:00', '2026-07-02T18:30:00+08:00', 0, 'tentative', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);
INSERT INTO reminders (event_id,method,minutes_before) VALUES ('evt_rscam_c1','popup',2880),('evt_rscam_c2','popup',1440),('evt_rscam_c3','popup',1440);
INSERT INTO _counters (key,value) VALUES ('event_seq',3);
COMMIT;

-- Curated shoot, maintenance and household commitments known before Stage 0.
BEGIN;
INSERT INTO events (event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at,recurrence_rule,parent_event_id) VALUES
('evt_camera_gallery_proof','cal_rscam_main','camera record','camera record、camera record。','camera record','2026-06-04T15:00:00+08:00','2026-06-04T16:10:00+08:00',0,'confirmed','2026-06-03T17:35:00+08:00','2026-06-03T17:35:00+08:00',NULL,NULL),
('evt_camera_lens_pickup','cal_rscam_main','camera record','camera record、camera record。','camera record','2026-05-29T11:20:00+08:00','2026-05-29T11:50:00+08:00',0,'confirmed','2026-05-28T15:50:00+08:00','2026-05-28T15:50:00+08:00',NULL,NULL),
('evt_camera_food_shoot','cal_rscam_main','camera record','camera record，camera record。','camera record','2026-06-13T14:30:00+08:00','2026-06-13T18:20:00+08:00',0,'confirmed','2026-06-10T12:40:00+08:00','2026-06-11T09:15:00+08:00',NULL,NULL),
('evt_camera_print_compare','cal_rscam_main','camera record','camera record、camera record。','camera record','2026-06-07T10:00:00+08:00','2026-06-07T11:00:00+08:00',0,'confirmed','2026-06-01T14:55:00+08:00','2026-06-01T14:55:00+08:00',NULL,NULL),
('evt_camera_water_outage','cal_rscam_main','camera record','camera record。','camera record','2026-06-09T13:30:00+08:00','2026-06-09T16:30:00+08:00',0,'confirmed','2026-06-04T16:25:00+08:00','2026-06-04T16:25:00+08:00',NULL,NULL),
('evt_camera_backup_audit','cal_rscam_main','camera record','camera record，camera record。','camera record','2026-06-10T19:10:00+08:00','2026-06-10T20:25:00+08:00',0,'confirmed','2026-06-08T20:45:00+08:00','2026-06-08T20:45:00+08:00',NULL,NULL),
('evt_camera_bike_followup','cal_rscam_main','camera record','camera record 50 camera record。','camera record','2026-06-08T18:40:00+08:00','2026-06-08T19:05:00+08:00',0,'tentative','2026-05-26T18:25:00+08:00','2026-05-26T18:25:00+08:00',NULL,NULL),
('evt_camera_policy_inventory','cal_rscam_main','camera record','camera record，camera record。','camera record','2026-06-06T20:00:00+08:00','2026-06-06T20:45:00+08:00',0,'confirmed','2026-05-23T13:55:00+08:00','2026-05-23T13:55:00+08:00',NULL,NULL),
('evt_camera_retouch_workshop','cal_rscam_main','camera record','camera record，camera record。','camera record','2026-06-14T14:00:00+08:00','2026-06-14T17:30:00+08:00',0,'confirmed','2026-06-09T17:18:00+08:00','2026-06-09T17:18:00+08:00',NULL,NULL),
('evt_camera_router_visit','cal_rscam_main','camera record','camera record，camera record。','camera record','2026-06-14T09:00:00+08:00','2026-06-14T10:30:00+08:00',0,'confirmed','2026-06-13T10:55:00+08:00','2026-06-13T10:55:00+08:00',NULL,NULL);
INSERT INTO attendees (id,event_id,email,name,response_status) VALUES
(101,'evt_camera_gallery_proof','proof@studio.example','camera record','accepted'),(102,'evt_camera_gallery_proof','curator@southgallery.example','camera record','accepted'),(103,'evt_camera_gallery_proof','designer@studio.example','camera record','tentative'),
(104,'evt_camera_lens_pickup','service@repair.example','camera record','accepted'),(105,'evt_camera_lens_pickup','frontdesk@repair.example','camera record','accepted'),(106,'evt_camera_lens_pickup','assistant.photo@example.com','camera record','declined'),
(107,'evt_camera_food_shoot','project@brand.example','camera record','accepted'),(108,'evt_camera_food_shoot','chef@brand.example','camera record','accepted'),(109,'evt_camera_food_shoot','stylist@brand.example','camera record','accepted'),
(110,'evt_camera_print_compare','orders@lab.example','camera record','accepted'),(111,'evt_camera_print_compare','colorist@lab.example','camera record','accepted'),(112,'evt_camera_print_compare','gallery.peer@example.com','camera record','tentative'),
(113,'evt_camera_water_outage','notice@home.example','camera record','accepted'),(114,'evt_camera_water_outage','neighbor.chen@example.com','camera record','needsAction'),(115,'evt_camera_water_outage','maintenance@home.example','camera record','accepted'),
(116,'evt_camera_backup_audit','audit@workflow.example','camera record','accepted'),(117,'evt_camera_backup_audit','assistant.archive@example.com','camera record','accepted'),(118,'evt_camera_backup_audit','client.archive@example.com','camera record','declined'),
(119,'evt_camera_bike_followup','service@mobility.example','camera record','tentative'),(120,'evt_camera_bike_followup','ride.friend@example.com','camera record','accepted'),(121,'evt_camera_bike_followup','club.mechanic@example.com','camera record','needsAction'),
(122,'evt_camera_policy_inventory','policy@insurance.example','camera record','accepted'),(123,'evt_camera_policy_inventory','accounting@studio.example','camera record','accepted'),(124,'evt_camera_policy_inventory','gear.assistant@example.com','camera record','accepted'),
(125,'evt_camera_retouch_workshop','events@photo.example','camera record','accepted'),(126,'evt_camera_retouch_workshop','retoucher.liu@example.com','camera record','accepted'),(127,'evt_camera_retouch_workshop','venue@photo.example','camera record','accepted'),
(128,'evt_camera_router_visit','service@telecom.example','camera record','accepted'),(129,'evt_camera_router_visit','property.net@example.com','camera record','tentative'),(130,'evt_camera_router_visit','home.contact@example.com','camera record','needsAction');
INSERT INTO reminders (id,event_id,method,minutes_before) VALUES
(101,'evt_camera_gallery_proof','email',1440),(102,'evt_camera_gallery_proof','popup',180),(103,'evt_camera_gallery_proof','email',75),(104,'evt_camera_gallery_proof','popup',20),
(105,'evt_camera_lens_pickup','email',960),(106,'evt_camera_lens_pickup','popup',150),(107,'evt_camera_lens_pickup','email',60),(108,'evt_camera_lens_pickup','popup',15),
(109,'evt_camera_food_shoot','email',2880),(110,'evt_camera_food_shoot','popup',240),(111,'evt_camera_food_shoot','email',90),(112,'evt_camera_food_shoot','popup',25),
(113,'evt_camera_print_compare','email',1320),(114,'evt_camera_print_compare','popup',165),(115,'evt_camera_print_compare','email',55),(116,'evt_camera_print_compare','popup',12),
(117,'evt_camera_water_outage','email',2160),(118,'evt_camera_water_outage','popup',210),(119,'evt_camera_water_outage','email',80),(120,'evt_camera_water_outage','popup',18),
(121,'evt_camera_backup_audit','email',1080),(122,'evt_camera_backup_audit','popup',135),(123,'evt_camera_backup_audit','email',45),(124,'evt_camera_backup_audit','popup',10),
(125,'evt_camera_bike_followup','email',4320),(126,'evt_camera_bike_followup','popup',195),(127,'evt_camera_bike_followup','email',65),(128,'evt_camera_bike_followup','popup',22),
(129,'evt_camera_policy_inventory','email',2520),(130,'evt_camera_policy_inventory','popup',225),(131,'evt_camera_policy_inventory','email',85),(132,'evt_camera_policy_inventory','popup',16),
(133,'evt_camera_retouch_workshop','email',3240),(134,'evt_camera_retouch_workshop','popup',270),(135,'evt_camera_retouch_workshop','email',105),(136,'evt_camera_retouch_workshop','popup',28),
(137,'evt_camera_router_visit','email',720),(138,'evt_camera_router_visit','popup',120),(139,'evt_camera_router_visit','email',40),(140,'evt_camera_router_visit','popup',8);
UPDATE _counters SET value=13 WHERE key='event_seq';
COMMIT;
