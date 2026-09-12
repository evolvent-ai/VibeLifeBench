PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "official_account_subscriptions";
DELETE FROM "official_account_posts";
DELETE FROM "notifications";
DELETE FROM "subscriptions";
DELETE FROM "price_alerts";
DELETE FROM "official_accounts";
INSERT INTO "official_accounts" ("account_id","name","category","description") VALUES ('acct_property_hj','Hongqiao Jiayuanproperty management','property','property managementtranslated source textnotice');
INSERT INTO "official_accounts" ("account_id","name","category","description") VALUES ('acct_safeair_lab','translated source textair-quality testing','inspection','air-quality testingtranslated source textnotice');
INSERT INTO "notifications" ("notification_id","user_id","source","type","subscription_id","title","body","payload_json","created_at","read") VALUES ('ntf_elevator_maintenance_done','usr_zhanglan','property_office','policy_update',NULL,'translated source textcompleted','2translated source textalreadytranslated source text，translated source textstilltranslated source textpleasetranslated source text。','{"building":"6translated source text"}','2026-06-12T09:25:00+08:00',1);
INSERT INTO "notifications" ("notification_id","user_id","source","type","subscription_id","title","body","payload_json","created_at","read") VALUES ('ntf_water_outage_resolved','usr_zhanglan','property_office','policy_update',NULL,'translated source text','translated source text monthtranslated source textalreadytranslated source text，translated source textfoundwater seepagestillshouldtranslated source text。','{"status":"resolved"}','2026-06-20T18:10:00+08:00',1);
COMMIT;
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO official_accounts(account_id,name,category,description) VALUES
('acct_hj_utilities','Shanghaitranslated source text','utility','Shanghaitranslated source text'),
('acct_hj_fire','Minhangtranslated source text','public_service','translated source textrecord'),
('acct_hj_tax','Shanghaitranslated source text','government','translated source text'),
('acct_hj_insurance','translated source text','insurance','translated source text'),
('acct_hj_elevator','translated source text','maintenance','Hongqiao Jiayuantranslated source textandtranslated source textrecord'),
('acct_hj_recycling','Minhangtranslated source text','recycling','translated source textappliancestranslated source text'),
('acct_hj_weather','Shanghaitranslated source text','weather','Shanghaitranslated source textandtranslated source text'),
('acct_hj_homefiles','translated source text','archive','Zhang Lantranslated source text'),
('acct_hj_broadband','Shanghaitranslated source text','telecom','translated source text'),
('acct_hj_storage','Minhangtranslated source text','storage','translated source textand monthtranslated source textrecord');
INSERT INTO official_account_subscriptions(user_id,account_id,subscribed_at) VALUES
('usr_zhanglan','acct_hj_utilities','2026-01-02T09:00:00+08:00'),
('usr_zhanglan','acct_hj_fire','2026-01-10T09:20:00+08:00'),
('usr_zhanglan','acct_hj_tax','2026-01-15T10:30:00+08:00'),
('usr_zhanglan','acct_hj_insurance','2026-02-01T08:40:00+08:00'),
('usr_zhanglan','acct_hj_elevator','2026-02-12T13:15:00+08:00'),
('usr_zhanglan','acct_hj_recycling','2026-03-03T11:05:00+08:00'),
('usr_zhanglan','acct_hj_weather','2026-03-15T07:20:00+08:00'),
('usr_zhanglan','acct_hj_homefiles','2026-04-01T09:10:00+08:00'),
('usr_zhanglan','acct_hj_broadband','2026-04-20T12:30:00+08:00'),
('usr_zhanglan','acct_hj_storage','2026-05-01T15:40:00+08:00');
INSERT INTO official_account_posts(post_id,account_id,title,summary,url,published_at) VALUES
('post_hj_water_winter','acct_hj_utilities','translated source text','Unit 603, Hongqiao Jiayuantranslated source text monthtranslated source text。','https://utility.example/posts/water-winter','2026-01-08T07:25:00+08:00'),
('post_hj_power_curve','acct_hj_utilities','translated source text monthtranslated source text','translated source text。','https://utility.example/posts/power-jan','2026-01-12T08:15:00+08:00'),
('post_hj_extinguisher','acct_hj_fire','translated source textcompleted','translated source text。','https://fire.example/posts/extinguisher','2026-02-18T16:08:00+08:00'),
('post_hj_firedoor','acct_hj_fire','translated source text','translated source textalreadytranslated source text。','https://fire.example/posts/firedoor','2026-06-04T10:20:00+08:00'),
('post_hj_tax_receipt','acct_hj_tax','translated source text','translated source text CNY。','https://tax.example/posts/receipt','2026-03-18T10:18:00+08:00'),
('post_hj_policy_active','acct_hj_insurance','translated source text','translated source textandtranslated source text。','https://insurance.example/posts/policy','2026-03-05T10:30:00+08:00'),
('post_hj_elevator_plan','acct_hj_elevator','translated source text','translated source text daytranslated source text monthtranslated source text day。','https://elevator.example/posts/plan','2026-05-26T15:15:00+08:00'),
('post_hj_elevator_done','acct_hj_elevator','translated source textcompleted','translated source textandtranslated source textpassedtranslated source text。','https://elevator.example/posts/done','2026-06-12T11:45:00+08:00'),
('post_hj_fridge_recycle','acct_hj_recycling','translated source text','translated source text CNY。','https://recycle.example/posts/fridge','2026-06-28T08:26:00+08:00'),
('post_hj_furniture_reuse','acct_hj_recycling','translated source text','translated source text。','https://recycle.example/posts/bookcase','2026-04-13T14:22:00+08:00'),
('post_hj_rain_apr','acct_hj_weather','translated source text monthtranslated source text','Minhangtranslated source text monthtranslated source text daytranslated source textm。','https://weather.example/posts/apr-rain','2026-04-19T07:30:00+08:00'),
('post_hj_humidity_jun','acct_hj_weather','translated source text','translated source text monthtranslated source text daytranslated source text。','https://weather.example/posts/jun-humidity','2026-06-29T06:40:00+08:00'),
('post_hj_docs_property','acct_hj_homefiles','translated source text','translated source text。','https://homefiles.example/posts/property','2026-01-06T09:15:00+08:00'),
('post_hj_docs_meter','acct_hj_homefiles','translated source text','translated source textandtranslated source textalreadytranslated source text。','https://homefiles.example/posts/meters','2026-05-30T20:38:00+08:00'),
('post_hj_broadband_bill','acct_hj_broadband','translated source text monthtranslated source text','translated source text monthtranslated source text CNY。','https://telecom.example/posts/june-bill','2026-06-03T09:18:00+08:00'),
('post_hj_router_health','acct_hj_broadband','translated source text','translated source text。','https://telecom.example/posts/router','2026-06-17T13:44:00+08:00'),
('post_hj_storage_in','acct_hj_storage','translated source text','translated source textandtranslated source text。','https://storage.example/posts/inbound','2026-04-12T10:40:00+08:00'),
('post_hj_storage_humidity','acct_hj_storage','translated source text monthtranslated source text',' monthtranslated source text。','https://storage.example/posts/humidity','2026-05-31T18:20:00+08:00'),
('post_hj_storage_access','acct_hj_storage','translated source textrecord','Zhang Lantranslated source text monthtranslated source text daytranslated source text。','https://storage.example/posts/access','2026-06-15T16:35:00+08:00'),
('post_hj_insurance_reminder','acct_hj_insurance','translated source text monthtranslated source text','currenttranslated source text monthtranslated source text day。','https://insurance.example/posts/expiry','2026-06-21T11:32:00+08:00');
INSERT INTO notifications(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read) VALUES
('ntf_hj_lock_done','usr_zhanglan','lock_service','policy_update',NULL,'translated source text','C translated source text。','{"keys":2}','2026-02-16T17:08:00+08:00',1),
('ntf_hj_fire_pressure','usr_zhanglan','fire_service','policy_update',NULL,'translated source textnormal','translated source text。','{"count":2}','2026-02-18T16:10:00+08:00',1),
('ntf_hj_tax_paid','usr_zhanglan','tax_service','policy_update',NULL,'translated source text','translated source textalreadytranslated source text。','{"amount_minor":108000}','2026-03-18T10:20:00+08:00',1),
('ntf_hj_tenant_keys','usr_zhanglan','rental_archive','new_content',NULL,'translated source texttenanttranslated source text','translated source text，translated source text。','{"door_keys":3,"mailbox_keys":1}','2026-04-02T15:38:00+08:00',1),
('ntf_hj_balcony_flow','usr_zhanglan','property_office','policy_update',NULL,'translated source textcompleted','translated source textnottranslated source text。','{"minutes":10}','2026-04-18T11:48:00+08:00',1),
('ntf_hj_window_hinge','usr_zhanglan','window_service','policy_update',NULL,'translated source text','translated source textandtranslated source textnormal。','{"room":"secondary_bedroom"}','2026-04-27T16:38:00+08:00',1),
('ntf_hj_ac_clean','usr_zhanglan','aircon_service','policy_update',NULL,'translated source textcompleted','translated source textandtranslated source textalreadytranslated source text。','{"units":2}','2026-05-15T18:22:00+08:00',1),
('ntf_hj_elevator_plan','usr_zhanglan','elevator_service','policy_update',NULL,'translated source text daytranslated source text','translated source text monthtranslated source text daymorning。','{"date":"2026-06-12"}','2026-05-26T15:18:00+08:00',1),
('ntf_hj_smoke_alarm','usr_zhanglan','fire_service','policy_update',NULL,'translated source text','translated source textandtranslated source textnormal。','{"room":"living_room"}','2026-06-08T14:45:00+08:00',1),
('ntf_hj_lamps_delivered','usr_zhanglan','parcel_service','new_content',NULL,'translated source textalreadytranslated source text','translated source text。','{"packages":1}','2026-06-20T15:25:00+08:00',1),
('ntf_hj_tools_delivered','usr_zhanglan','parcel_service','new_content',NULL,'translated source textalreadytranslated source text','translated source textandtranslated source text603translated source text。','{"items":2}','2026-06-26T11:45:00+08:00',1);
COMMIT;
