PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DELETE FROM "transit_schedule";
DELETE FROM "transit_events";
DELETE FROM "road_events";
DELETE FROM "place_reviews";
DELETE FROM "transit_stops";
DELETE FROM "transit_lines";
DELETE FROM "roads";
DELETE FROM "places";
DELETE FROM "notifications";
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_01','rental record','residential',32.1127,118.7284,'China','Nanjing',4.1,2,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental record189numberattachrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_02','Qiaobei Waterfront','residential',32.1189,118.7236,'China','Nanjing',4.0,2,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordQiaobei Waterfrontrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_03','rental record','residential',32.1264,118.7191,'China','Nanjing',3.9,2,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental record28numberattachrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_04','Qiaolin New Estate','residential',32.1321,118.7108,'China','Nanjing',4.2,2,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_05','Top-of-the-Hill Street Xinyuan','residential',32.1298,118.6995,'China','Nanjing',3.8,1,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordattachrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_06','Tianrun City Block 10','residential',32.1396,118.7179,'China','Nanjing',4.4,3,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordTianrun City Block 10');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_07','Hongyang Plaza Apartments','residential',32.1452,118.7217,'China','Nanjing',4.0,3,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_08','Mingfa Riverside New City','residential',32.1511,118.7164,'China','Nanjing',4.5,3,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordMingfa Riverside New Cityrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_09','Riverside Homes','residential',32.1478,118.7072,'China','Nanjing',3.7,2,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordRiverside Homes');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_10','Pujiang Yayan','residential',32.1563,118.7119,'China','Nanjing',4.1,2,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordPujiang Yayanrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_11','Xuri Shangcheng','residential',32.1608,118.7205,'China','Nanjing',4.6,3,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordXuri Shangchengrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_12','Venice Water City','residential',32.1662,118.7126,'China','Nanjing',4.2,3,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordVenice Water Cityrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_corr_13','rental record','residential',32.1715,118.7041,'China','Nanjing',4.4,3,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_company','Software Avenue','office',32.1742,118.7168,'China','Nanjing',4.5,2,NULL,NULL,NULL,'rental recordNanjingrental recordJiangbei New AreaSoftware Avenuerental recordsendrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_company_alias','Jiangbei New AreaSoftware Avenue','office',32.1737,118.7175,'China','Nanjing',4.4,2,NULL,NULL,NULL,'rental recordNanjingrental recordJiangbei New AreaSoftware Avenuerental recorditemrental recordArental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_nanjing_south','Nanjingrental record Station','train_station',31.9702,118.7914,'China','Nanjing',4.5,2,NULL,NULL,NULL,'rental recordNanjingrental recordNanjingrental record Station');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_hankou_station','rental record Station','train_station',30.618,114.255,'China','Wuhan',4.4,2,NULL,NULL,NULL,'rental recordWuhanrental record Station');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_jiangbei_hotel','rental recorditemrental recordpersonrental record','lodging',32.1688,118.7182,'China','Nanjing',4.2,3,NULL,NULL,NULL,'rental recordNanjingrental recordJiangbei New AreaSoftware Avenueattachrental record');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_pukou_service_center','Pukourental recordinrental record','government',32.0648,118.6275,'China','Nanjing',4.3,1,NULL,NULL,NULL,'rental recordNanjingrental recordPukou Districtrental recordinrental record');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('rd_jiangbei_avenue','rental record','Nanjing','[[32.1127,118.7284],[32.1396,118.7179],[32.1511,118.7164],[32.1742,118.7168]]');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('rd_puzhu_north','rental record','Nanjing','[[32.120,118.700],[32.150,118.715]]');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('rd_pubin','rental record','Nanjing','[[32.130,118.705],[32.165,118.720]]');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('rd_hengjiang','rental record','Nanjing','[[32.140,118.700],[32.170,118.730]]');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('rd_software','Software Avenue','Nanjing','[[32.165,118.710],[32.172,118.720]]');
INSERT INTO "transit_lines" ("line_id","name","mode","operator","segment_minutes_json") VALUES ('ln_njr_s8','NanjingMetroS8 Line(rental recorddaysrental record)','subway','NanjingMetro','[4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4]');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('nkg_stop_LZD7K','rental record',32.113,118.728,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_QBS_4mP','Qiaobei Waterfront',32.1192,118.7231,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('nkg-poi-DQBL-A8x','rental record',32.126,118.7187,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop-QLXY-73q','Qiaolin New Estate',32.1325,118.7103,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('nkg_stop_DSJ_9Vt','Top-of-the-Hill Street Xinyuan',32.1301,118.699,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('s8_TRC10J6p','Tianrun City Block 10',32.1399,118.7174,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('poi_HYGC_5qN','Hongyang Plaza Apartments',32.1456,118.7212,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('nkgstop_MFBJ_8Kr','Mingfa Riverside New City',32.1515,118.716,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_JPRJ_C3v','Riverside Homes',32.1481,118.7067,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('s8_PJYY_6mQ','Pujiang Yayan',32.1567,118.7114,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('nkg_stop_XRSC_2Wx','Xuri Shangcheng',32.1612,118.72,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('poi_VNSC_7Lp','Venice Water City',32.1666,118.7121,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_JSH_4tM','rental record',32.1719,118.7036,'Nanjing');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('nkg_metro_RJDD_9Qk','Software Avenue',32.1745,118.7163,'Nanjing');
INSERT INTO "place_reviews" ("id","place_id","author","rating","text","time") VALUES (6,'pl_corr_08','commuteliverental recordA',4,'morning peaktransferaboutrental recordminutes，rental recorddaysrental recordwillrental recordtorental record。','2026-05-18T09:00:00Z');
INSERT INTO "place_reviews" ("id","place_id","author","rating","text","time") VALUES (7,'pl_corr_11','rentrental recordB',4,'communityrental record，rental record。','2026-04-23T18:30:00Z');
INSERT INTO "place_reviews" ("id","place_id","author","rating","text","time") VALUES (8,'pl_corr_12','liverental recordC',3,'communityrental record，rental recordtoMetrorental recordofsteprental recordveryrental record。','2026-05-06T12:10:00Z');
INSERT INTO "place_reviews" ("id","place_id","author","rating","text","time") VALUES (9,'pl_company','rental recordD',5,'rental record 9:00 beforerental record，9:20 afterrental recordpersonrental record。','2026-06-12T08:45:00Z');
INSERT INTO "place_reviews" ("id","place_id","author","rating","text","time") VALUES (10,'pl_nanjing_south','rental recordE',4,'rental recorditemrental recordtransferMetroneedleaverental recordelevatortime。','2026-03-15T14:20:00Z');
INSERT INTO "road_events" ("event_id","road_id","start_dt","end_dt","kind","magnitude","note","active") VALUES ('re_jiangbei_peak','rd_jiangbei_avenue','2026-06-28T07:00:00Z','2026-06-28T20:00:00Z','heavy_traffic',0.6,'workdayrental record。',1);
INSERT INTO "road_events" ("event_id","road_id","start_dt","end_dt","kind","magnitude","note","active") VALUES ('re_puzhu_works','rd_puzhu_north','2026-06-27T08:00:00Z','2026-07-10T18:00:00Z','closure',1.0,'rental record，rental record Stationrental recordhourrental record。',1);
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (1,'ln_njr_s8','nkg_stop_LZD7K','outbound',1,'06:00');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (2,'ln_njr_s8','stop_QBS_4mP','outbound',2,'06:04');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (3,'ln_njr_s8','nkg-poi-DQBL-A8x','outbound',3,'06:07');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (4,'ln_njr_s8','stop-QLXY-73q','outbound',4,'06:11');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (5,'ln_njr_s8','nkg_stop_DSJ_9Vt','outbound',5,'06:14');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (6,'ln_njr_s8','s8_TRC10J6p','outbound',6,'06:18');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (7,'ln_njr_s8','poi_HYGC_5qN','outbound',7,'06:21');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (8,'ln_njr_s8','nkgstop_MFBJ_8Kr','outbound',8,'06:25');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (9,'ln_njr_s8','stop_JPRJ_C3v','outbound',9,'06:28');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (10,'ln_njr_s8','s8_PJYY_6mQ','outbound',10,'06:32');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (11,'ln_njr_s8','nkg_stop_XRSC_2Wx','outbound',11,'06:35');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (12,'ln_njr_s8','poi_VNSC_7Lp','outbound',12,'06:39');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (13,'ln_njr_s8','stop_JSH_4tM','outbound',13,'06:42');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (14,'ln_njr_s8','nkg_metro_RJDD_9Qk','outbound',14,'06:46');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (15,'ln_njr_s8','nkg_stop_LZD7K','outbound',1,'06:30');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (16,'ln_njr_s8','stop_QBS_4mP','outbound',2,'06:34');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (17,'ln_njr_s8','nkg-poi-DQBL-A8x','outbound',3,'06:37');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (18,'ln_njr_s8','stop-QLXY-73q','outbound',4,'06:41');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (19,'ln_njr_s8','nkg_stop_DSJ_9Vt','outbound',5,'06:44');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (20,'ln_njr_s8','s8_TRC10J6p','outbound',6,'06:48');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (21,'ln_njr_s8','poi_HYGC_5qN','outbound',7,'06:51');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (22,'ln_njr_s8','nkgstop_MFBJ_8Kr','outbound',8,'06:55');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (23,'ln_njr_s8','stop_JPRJ_C3v','outbound',9,'06:58');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (24,'ln_njr_s8','s8_PJYY_6mQ','outbound',10,'07:02');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (25,'ln_njr_s8','nkg_stop_XRSC_2Wx','outbound',11,'07:05');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (26,'ln_njr_s8','poi_VNSC_7Lp','outbound',12,'07:09');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (27,'ln_njr_s8','stop_JSH_4tM','outbound',13,'07:12');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (28,'ln_njr_s8','nkg_metro_RJDD_9Qk','outbound',14,'07:16');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (29,'ln_njr_s8','nkg_stop_LZD7K','outbound',1,'07:00');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (30,'ln_njr_s8','stop_QBS_4mP','outbound',2,'07:04');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (31,'ln_njr_s8','nkg-poi-DQBL-A8x','outbound',3,'07:07');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (32,'ln_njr_s8','stop-QLXY-73q','outbound',4,'07:11');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (33,'ln_njr_s8','nkg_stop_DSJ_9Vt','outbound',5,'07:14');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (34,'ln_njr_s8','s8_TRC10J6p','outbound',6,'07:18');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (35,'ln_njr_s8','poi_HYGC_5qN','outbound',7,'07:21');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (36,'ln_njr_s8','nkgstop_MFBJ_8Kr','outbound',8,'07:25');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (37,'ln_njr_s8','stop_JPRJ_C3v','outbound',9,'07:28');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (38,'ln_njr_s8','s8_PJYY_6mQ','outbound',10,'07:32');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (39,'ln_njr_s8','nkg_stop_XRSC_2Wx','outbound',11,'07:35');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (40,'ln_njr_s8','poi_VNSC_7Lp','outbound',12,'07:39');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (41,'ln_njr_s8','stop_JSH_4tM','outbound',13,'07:42');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (42,'ln_njr_s8','nkg_metro_RJDD_9Qk','outbound',14,'07:46');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (43,'ln_njr_s8','nkg_stop_LZD7K','outbound',1,'07:30');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (44,'ln_njr_s8','stop_QBS_4mP','outbound',2,'07:34');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (45,'ln_njr_s8','nkg-poi-DQBL-A8x','outbound',3,'07:37');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (46,'ln_njr_s8','stop-QLXY-73q','outbound',4,'07:41');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (47,'ln_njr_s8','nkg_stop_DSJ_9Vt','outbound',5,'07:44');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (48,'ln_njr_s8','s8_TRC10J6p','outbound',6,'07:48');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (49,'ln_njr_s8','poi_HYGC_5qN','outbound',7,'07:51');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (50,'ln_njr_s8','nkgstop_MFBJ_8Kr','outbound',8,'07:55');
COMMIT;
DELETE FROM road_events WHERE start_dt > '2026-06-28T01:00:00Z';
-- Road incidents beginning after t=0 must not be active in the seed world.
DELETE FROM road_events
WHERE start_dt > '2026-06-28T01:00:00Z';
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
INSERT INTO transit_schedule(schedule_id,line_id,stop_id,direction,stop_seq,time) VALUES
(101,'ln_njr_s8','nkg_metro_RJDD_9Qk','inbound',1,'06:08'),
(102,'ln_njr_s8','nkgstop_MFBJ_8Kr','outbound',8,'08:05'),
(103,'ln_njr_s8','stop_JSH_4tM','inbound',2,'06:12'),
(104,'ln_njr_s8','nkg_stop_LZD7K','outbound',1,'08:10'),
(105,'ln_njr_s8','poi_VNSC_7Lp','inbound',3,'06:15'),
(106,'ln_njr_s8','s8_PJYY_6mQ','outbound',10,'08:12'),
(107,'ln_njr_s8','nkg_stop_XRSC_2Wx','inbound',4,'06:19'),
(108,'ln_njr_s8','nkg-poi-DQBL-A8x','outbound',3,'08:17'),
(109,'ln_njr_s8','s8_PJYY_6mQ','inbound',5,'06:22'),
(110,'ln_njr_s8','poi_VNSC_7Lp','outbound',12,'08:19'),
(111,'ln_njr_s8','stop_JPRJ_C3v','inbound',6,'06:26'),
(112,'ln_njr_s8','nkg_stop_DSJ_9Vt','outbound',5,'08:24'),
(113,'ln_njr_s8','nkgstop_MFBJ_8Kr','inbound',7,'06:29'),
(114,'ln_njr_s8','nkg_metro_RJDD_9Qk','outbound',14,'08:26'),
(115,'ln_njr_s8','poi_HYGC_5qN','inbound',8,'06:33'),
(116,'ln_njr_s8','poi_HYGC_5qN','outbound',7,'08:31'),
(117,'ln_njr_s8','s8_TRC10J6p','inbound',9,'06:36'),
(118,'ln_njr_s8','stop_JPRJ_C3v','outbound',9,'08:34'),
(119,'ln_njr_s8','nkg_stop_DSJ_9Vt','inbound',10,'06:40'),
(120,'ln_njr_s8','stop_QBS_4mP','outbound',2,'08:38');
COMMIT;

BEGIN TRANSACTION;
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
('pl_njr_pukou_service_hall','Pukourental recordinrental recordnotrental record','government',32.0598,118.6274,'CN','Nanjing',4.2,1,'{"weekday":"09:00-17:30"}','025-58115672',NULL,'Nanjingrental recordPukou Districtrental record4numberBrental record'),
('pl_njr_jiangbei_cowork','rental recordofficeinrental record','coworking',32.1526,118.6921,'CN','Nanjing',4.4,3,'{"weekday":"08:00-22:00","weekend":"09:00-18:00"}','025-58890631',NULL,'Nanjingrental recordJiangbei New Arearental record99number'),
('pl_njr_taishan_police','rental recordnewrental record room','police',32.1189,118.7186,'CN','Nanjing',4.0,1,'{"weekday":"09:00-17:30"}','025-58850743',NULL,'Nanjingrental recordPukou Districtrental record58number'),
('pl_njr_qiaobei_hospital','Nanjingrental recordPukourental record','hospital',32.1237,118.7215,'CN','Nanjing',4.1,2,'{"daily":"08:00-20:00"}','025-58881120',NULL,'Nanjingrental recordJiangbei New Arearental record68number'),
('pl_njr_mingfa_courier','Mingfarental record Station','parcel_service',32.1409,118.7168,'CN','Nanjing',4.3,1,'{"daily":"08:00-21:00"}','025-58530218',NULL,'Nanjingrental recordPukou DistrictMingfa Riverside New Cityrental record'),
('pl_njr_tianruncheng_market','daysrental record','supermarket',32.1318,118.7097,'CN','Nanjing',4.0,2,'{"daily":"07:00-22:00"}','025-58491366',NULL,'Nanjingrental recordPukou Districtrental record12number'),
('pl_njr_longhua_bank','rental recordbankrental record','bank',32.0675,118.6279,'CN','Nanjing',4.2,1,'{"weekday":"09:00-17:00"}','025-58882340',NULL,'Nanjingrental recordPukou Districtrental record18number'),
('pl_njr_jiangbei_library','Jiangbei New Arearental record','library',32.1692,118.6896,'CN','Nanjing',4.7,1,'{"tue_sun":"09:00-20:00"}','025-58801032',NULL,'Nanjingrental recordJiangbei New Arearental record1number');
INSERT INTO place_reviews(place_id,author,rating,text,time) VALUES
('pl_njr_pukou_service_hall','rental record',4,'rentrental recordunderrental recordafterrental record，rental recordidentity cardrental record。','2026-05-14T15:22:00Z'),
('pl_njr_jiangbei_cowork','remoterental recordsendrental record',5,'rental recordmessagebetweenrental recordcan，fixedrental recordmonthrental recordcontainsrental recordbetweenaccess control。','2026-06-09T11:48:00Z'),
('pl_njr_taishan_police','newrental recordliverental record',4,'rental recordliverental recordnumberafterwillrental recordrentrental recordsame addressandlandlordcontactrental recordmessage。','2026-04-26T09:36:00Z'),
('pl_njr_mingfa_courier','communityliverental record',3,'rental recorditemcannotrental recordcanrental record，rental recordafterrental recorditempersonrental record。','2026-06-17T19:14:00Z'),
('pl_njr_jiangbei_library','readrental record',5,'rental recordhaverental record，weekrental recorddayrental record。','2026-05-31T16:08:00Z');
INSERT INTO roads(road_id,name,city,geom_json) VALUES
('rd_njr_taifeng_registry','rental record roomexcerpt','Nanjing','[[32.1157,118.7152],[32.1214,118.7210]]'),
('rd_njr_tuanjie_cowork','rental recordexcerpt','Nanjing','[[32.1491,118.6877],[32.1560,118.6965]]'),
('rd_njr_bairun_market','rental recordexcerpt','Nanjing','[[32.1282,118.7054],[32.1351,118.7136]]'),
('rd_njr_shifo_library','rental recordexcerpt','Nanjing','[[32.1654,118.6848],[32.1727,118.6941]]');
INSERT INTO road_events(event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
('re_njr_taifeng_signal_apr','rd_njr_taifeng_registry','2026-04-12T22:00:00Z','2026-04-13T05:30:00Z','heavy_traffic',0.3,'rental recordnumberrental recordbetweenrental recordbetweenonlyrental record。',0),
('re_njr_tuanjie_drain_may','rd_njr_tuanjie_cowork','2026-05-19T07:30:00Z','2026-05-21T18:00:00Z','closure',0.5,'rental record，rental recordfromrental record。',0),
('re_njr_bairun_market_jun','rd_njr_bairun_market','2026-06-11T05:00:00Z','2026-06-11T12:00:00Z','heavy_traffic',0.7,'rental recordhourrental record。',0),
('re_njr_shifo_event_jun','rd_njr_shifo_library','2026-06-22T08:00:00Z','2026-06-22T17:30:00Z','closure',0.6,'rental recordreadrental recorddaysrental recordpersoncommunicaterental record。',0);
INSERT INTO notifications(created_at,channel,payload_json) VALUES ('2026-06-18T10:26:00Z','map_update','{"place_id":"pl_njr_mingfa_courier","change":"rental recordtimerental recordto21:00"}');
COMMIT;
DELETE FROM road_events WHERE start_dt > '2026-06-28T01:00:00Z';
