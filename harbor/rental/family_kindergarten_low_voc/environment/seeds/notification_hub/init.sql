PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "official_account_subscriptions";
DELETE FROM "official_account_posts";
DELETE FROM "notifications";
DELETE FROM "subscriptions";
DELETE FROM "price_alerts";
DELETE FROM "official_accounts";
INSERT INTO "subscriptions" ("subscription_id","user_id","source","type","target","condition_json","status","created_at","updated_at") VALUES ('sub_rental','usr_family_038','rental_updates','policy_update','lin.lan@example.invalid','{"channel":"webhook"}','active','2026-07-18T09:00:00+08:00','2026-07-18T09:00:00+08:00');
INSERT INTO "notifications" ("notification_id","user_id","source","type","subscription_id","title","body","payload_json","created_at","read") VALUES ('nt_20260712_7KmQ','usr_family_038','river_property','policy_update',NULL,'Riverside Garden elevator maintenance completed','Elevator 2 has resumed service; the walls need to be checked on site during the rainy season.','{"community":"Riverside Garden"}','2026-07-12T10:10:00+08:00',1);
INSERT INTO "notifications" ("notification_id","user_id","source","type","subscription_id","title","body","payload_json","created_at","read") VALUES ('nt_20260714_P4xR','usr_family_038','maple_property','policy_update',NULL,'Maple Lane quiet hours','Continuous drilling is prohibited during weekday midday hours.','{"quiet_hours":"12:00-14:00"}','2026-07-14T15:25:00+08:00',1);
INSERT INTO "notifications" ("notification_id","user_id","source","type","subscription_id","title","body","payload_json","created_at","read") VALUES ('nt_20260717_M9vT','usr_family_038','greenfield_property','policy_update',NULL,'Greenfield Phase II shuttle schedule adjustment','The early morning service will be reduced during the summer holiday.','{"route":"commute"}','2026-07-17T11:05:00+08:00',0);
COMMIT;
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
INSERT INTO subscriptions(subscription_id,user_id,source,type,target,condition_json,status,created_at,updated_at) VALUES
('sub_family_library','usr_family_038','city_library','new_content','lin.lan@example.invalid','{"topic":"children_books"}','active','2026-01-05T09:00:00+08:00','2026-06-30T09:00:00+08:00'),
('sub_family_clinic','usr_family_038','child_clinic','policy_update','lin.lan@example.invalid','{"department":"pediatrics"}','active','2026-01-08T12:00:00+08:00','2026-01-08T12:00:00+08:00'),
('sub_family_grocery','usr_family_038','weekly_grocery','restock','lin.lan@example.invalid','{"category":"fresh_food"}','paused','2026-02-02T18:10:00+08:00','2026-06-11T08:30:00+08:00'),
('sub_family_daycare','usr_family_038','old_daycare','new_content','lin.lan@example.invalid','{"class":"orange"}','active','2026-02-06T17:45:00+08:00','2026-07-05T18:55:00+08:00'),
('sub_family_weather','usr_family_038','city_weather','keyword','lin.lan@example.invalid','{"keywords":["heavy rain","high temperature"]}','active','2026-03-01T07:20:00+08:00','2026-07-16T17:30:00+08:00'),
('sub_family_broadband','usr_family_038','home_broadband','policy_update','lin.lan@example.invalid','{"account":"HZ-LAN-77"}','active','2026-03-03T15:30:00+08:00','2026-03-03T15:30:00+08:00'),
('sub_family_pool','usr_family_038','community_pool','new_content','lin.lan@example.invalid','{"course":"parent_child"}','deleted','2026-04-29T10:05:00+08:00','2026-05-17T09:40:00+08:00'),
('sub_family_rail','usr_family_038','rail_trip','policy_update','lin.lan@example.invalid','{"passenger":"grandma"}','deleted','2026-05-18T08:25:00+08:00','2026-05-25T19:00:00+08:00'),
('sub_family_appliance','usr_family_038','appliance_service','policy_update','lin.lan@example.invalid','{"ticket":"washer-drain"}','deleted','2026-05-27T08:00:00+08:00','2026-05-29T15:10:00+08:00'),
('sub_family_photos','usr_family_038','photo_studio','new_content','lin.lan@example.invalid','{"order":"family-id"}','deleted','2026-06-09T16:22:00+08:00','2026-06-13T11:10:00+08:00'),
('sub_family_bike','usr_family_038','bike_service','policy_update','lin.lan@example.invalid','{"vehicle":"family-bike"}','deleted','2026-06-25T11:35:00+08:00','2026-06-27T17:25:00+08:00'),
('sub_family_parcel','usr_family_038','parcel_locker','new_content','lin.lan@example.invalid','{"locker":"old-home-east"}','active','2026-03-19T20:00:00+08:00','2026-07-15T12:20:00+08:00');
INSERT INTO notifications(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read) VALUES
('nt_family_library_card','usr_family_038','city_library','new_content','sub_family_library','Library card renewal complete','Valid through January 2027.','{"card":"child"}','2026-01-17T16:20:00+08:00',1),
('nt_family_clinic_queue','usr_family_038','child_clinic','policy_update','sub_family_clinic','Child health clinic waiting area relocated','The child health outpatient clinic has moved to the east side of the second floor.','{"floor":2,"wing":"east"}','2026-02-01T08:35:00+08:00',1),
('nt_family_grocery_orange','usr_family_038','weekly_grocery','restock','sub_family_grocery','Gannan navel oranges back in stock','This week''s size is the 5-pound family pack.','{"weight_kg":2.5}','2026-02-12T09:14:00+08:00',1),
('nt_family_daycare_trip','usr_family_038','old_daycare','new_content','sub_family_daycare','Spring outing album now available','The botanical garden album contains 26 photos.','{"album":"botanical"}','2026-04-28T17:55:00+08:00',1),
('nt_family_weather_hail','usr_family_038','city_weather','keyword','sub_family_weather','Short-term hail warning for Binjiang','The thunderstorm cloud cluster is expected to move east in half an hour.','{"level":"orange"}','2026-03-22T15:48:00+08:00',1),
('nt_family_broadband_closed','usr_family_038','home_broadband','policy_update','sub_family_broadband','Broadband service ticket closed','The study''s network port tested at 936 Mbps.','{"ticket":"HZ-LAN-77"}','2026-03-03T16:05:00+08:00',1),
('nt_family_pool_trial','usr_family_038','community_pool','new_content','sub_family_pool','Parent-child trial class booking successful','Entry is at 3:00 p.m. on May 16.','{"lane":"kids-2"}','2026-05-11T18:18:00+08:00',1),
('nt_family_rail_gate','usr_family_038','rail_trip','policy_update','sub_family_rail','Train boarding gate announced','Train G7532 boards through gate 12B.','{"train":"G7532"}','2026-05-23T13:25:00+08:00',1),
('nt_family_washer_arrival','usr_family_038','appliance_service','policy_update','sub_family_appliance','Repair technician has arrived at the complex','The service ticket shows that the engineer registered at the east gate.','{"ticket":"washer-drain"}','2026-05-29T13:27:00+08:00',1),
('nt_family_photo_ready','usr_family_038','photo_studio','new_content','sub_family_photos','Digital ID photos ready for download','The download code expires in 30 days.','{"order":"family-id"}','2026-06-13T11:07:00+08:00',1),
('nt_family_bike_done','usr_family_038','bike_service','policy_update','sub_family_bike','Bicycle maintenance complete','The rear brake cable and seat screws have been replaced.','{"vehicle":"family-bike"}','2026-06-27T17:18:00+08:00',1),
('nt_family_parcel_books','usr_family_038','parcel_locker','new_content','sub_family_parcel','Picture-book parcel placed in locker','Compartment E17; the pickup code has been hidden.','{"locker":"E17"}','2026-03-19T20:38:00+08:00',1),
('nt_family_parcel_shoes','usr_family_038','parcel_locker','new_content','sub_family_parcel','Children''s indoor shoes placed in locker','Compartment B06; parcel weight is 0.6 kilograms.','{"locker":"B06"}','2026-07-15T12:18:00+08:00',0),
('nt_family_weather_rain','usr_family_038','city_weather','keyword','sub_family_weather','Blue heavy-rain warning for Hangzhou','Temporary flooding has appeared on low-lying roads along the river.','{"level":"blue"}','2026-06-19T05:32:00+08:00',1),
('nt_family_weather_heat','usr_family_038','city_weather','keyword','sub_family_weather','Yellow high-temperature warning for Hangzhou','The next day''s high is expected to reach 38 degrees.','{"level":"yellow"}','2026-07-16T17:31:00+08:00',0),
('nt_family_library_due','usr_family_038','city_library','new_content','sub_family_library','Three picture books due soon','The return date is July 10.','{"count":3}','2026-07-03T07:02:00+08:00',1),
('nt_family_daycare_bedding','usr_family_038','old_daycare','new_content','sub_family_daycare','Summer bedding packed','The blue storage bag is by the classroom door.','{"bag":"blue"}','2026-07-05T19:00:00+08:00',0),
('nt_family_grocery_slot','usr_family_038','weekly_grocery','policy_update',NULL,'Saturday delivery window updated','Fresh-food orders have been moved to 4:00 p.m. to 6:00 p.m.','{"window":"16:00-18:00"}','2026-07-09T13:40:00+08:00',1),
('nt_family_clinic_system','usr_family_038','child_clinic','policy_update','sub_family_clinic','Child health system maintenance','Online report lookup will be suspended overnight on June 26.','{"maintenance":"2026-06-26"}','2026-06-24T10:12:00+08:00',1),
('nt_family_library_event','usr_family_038','city_library','new_content','sub_family_library','Weekend picture-book reading session','The theme is summer insects; all spots are filled.','{"topic":"summer insects"}','2026-06-30T09:02:00+08:00',0);
INSERT INTO price_alerts(alert_id,user_id,item_ref,target_price_minor,currency,status,created_at) VALUES
('alert_family_picture_books','usr_family_038','book_bundle_picture',6800,'CNY','triggered','2026-01-06T11:20:00+08:00'),
('alert_family_raincoat','usr_family_038','kids_raincoat_yellow',9900,'CNY','cancelled','2026-02-18T13:05:00+08:00'),
('alert_family_router','usr_family_038','mesh_router_pair',69900,'CNY','active','2026-03-04T09:42:00+08:00'),
('alert_family_swim_goggles','usr_family_038','child_swim_goggles',7600,'CNY','triggered','2026-05-10T20:18:00+08:00'),
('alert_family_storage_box','usr_family_038','folding_storage_box',4500,'CNY','cancelled','2026-05-26T18:50:00+08:00'),
('alert_family_bike_helmet','usr_family_038','child_bike_helmet',15900,'CNY','active','2026-06-05T08:22:00+08:00'),
('alert_family_school_shoes','usr_family_038','indoor_shoes_size27',8900,'CNY','triggered','2026-06-28T21:10:00+08:00'),
('alert_family_air_filter','usr_family_038','air_purifier_filter_oldhome',23900,'CNY','active','2026-07-02T12:36:00+08:00');
COMMIT;
