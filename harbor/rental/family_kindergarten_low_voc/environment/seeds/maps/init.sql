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
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_kindergarten_xinghe','Xinghe Kindergarten Binjiang Campus','school',30.205,120.215,'CN','Hangzhou',4.7,2,'{}','','','Xinghe Kindergarten Binjiang Campus, Binjiang District, Hangzhou');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_cbd_qianjiang','Qianjiang New City CBD','business_district',30.249,120.22,'CN','Hangzhou',4.6,3,'{}','','','Shangcheng District, Hangzhou, Qianjiang New City CBD');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_river_garden','Riverside Garden','residential',30.207,120.211,'CN','Hangzhou',4.3,2,'{}','','','Binjiang District, Hangzhou, Riverside Garden');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_maple_lane','Maple Lane','residential',30.203,120.218,'CN','Hangzhou',4.5,2,'{}','','','Binjiang District, Hangzhou, Maple Lane');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_sunbay_loft','Chengwan Apartments','residential',30.21,120.222,'CN','Hangzhou',3.7,1,'{}','','','Binjiang District, Hangzhou, Chengwan Apartments');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_orangepark','Orange Garden','residential',30.198,120.213,'CN','Hangzhou',4.2,2,'{}','','','Binjiang District, Hangzhou, Orange Garden');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_greenfield','Greenfield Phase II','residential',30.195,120.23,'CN','Hangzhou',4.0,2,'{}','','','Binjiang District, Hangzhou, Greenfield Phase II');
INSERT INTO "places" ("place_id","name","category","lat","lng","country","city","rating","price_level","hours_json","phone","website","formatted") VALUES ('pl_lakeside','Riverside Garden','residential',30.206,120.209,'CN','Hangzhou',4.4,3,'{}','','','Riverside Garden, Binjiang District, Hangzhou');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('road_sunbay_work','Chengwan Apartments construction cycling segment','Hangzhou','[[30.210,120.222],[30.205,120.215]]');
INSERT INTO "roads" ("road_id","name","city","geom_json") VALUES ('road_maple_school','Maple Lane to Xinghe Kindergarten Binjiang Campus','Hangzhou','[[30.203,120.218],[30.205,120.215]]');
INSERT INTO "transit_lines" ("line_id","name","mode","operator","segment_minutes_json") VALUES ('line_006','Line 6','subway','Hangzhou Metro','[8,7,6]');
INSERT INTO "transit_lines" ("line_id","name","mode","operator","segment_minutes_json") VALUES ('line_bus_child','Kindergarten pickup and drop-off line','bus','Public Bus','[9,10]');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_xinghe','Xinghe Kindergarten Binjiang Campus stop',30.2052,120.2148,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_maple','Maple Lane Entrance',30.2034,120.2176,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_river','Riverside Garden East Gate',30.2071,120.2112,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_sunbay','Chengwan Apartments on Jianghong Road',30.2102,120.2218,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_qianjiang','Qianjiang New City CBD Station',30.2491,120.2201,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_orange','Orange Garden South Gate',30.1982,120.2131,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_green','Greenfield Phase Two',30.1901,120.201,'Hangzhou');
INSERT INTO "transit_stops" ("stop_id","name","lat","lng","city") VALUES ('stop_lake','Riverside Garden',30.2151,120.2072,'Hangzhou');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (1,'line_006','stop_river','Qianjiang New City CBD direction',1,'08:00');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (2,'line_006','stop_sunbay','Qianjiang New City CBD direction',2,'08:10');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (3,'line_006','stop_xinghe','Qianjiang New City CBD direction',3,'08:18');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (4,'line_006','stop_qianjiang','Qianjiang New City CBD direction',4,'08:46');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (5,'line_bus_child','stop_maple','Xinghe Kindergarten Binjiang Campus direction',1,'07:50');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (6,'line_bus_child','stop_orange','Xinghe Kindergarten Binjiang Campus direction',2,'07:55');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (7,'line_bus_child','stop_xinghe','Xinghe Kindergarten Binjiang Campus direction',3,'08:03');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (8,'line_bus_child','stop_green','Xinghe Kindergarten Binjiang Campus direction',1,'07:35');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (9,'line_bus_child','stop_lake','Xinghe Kindergarten Binjiang Campus direction',2,'07:52');
INSERT INTO "transit_schedule" ("schedule_id","line_id","stop_id","direction","stop_seq","time") VALUES (10,'line_bus_child','stop_xinghe','Xinghe Kindergarten Binjiang Campus direction',3,'08:08');
COMMIT;
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
('pl_binjiang_library','Binjiang District Library','library',30.2086,120.2054,'CN','Hangzhou',4.6,1,'{"mon":"closed","tue-sun":"09:00-20:30"}','0571-86521018','','200 Tai''an Road, Binjiang District, Hangzhou'),
('pl_children_clinic','Binjiang Maternal and Child Healthcare Clinic','clinic',30.2018,120.2197,'CN','Hangzhou',4.2,2,'{"daily":"08:00-17:00"}','0571-86620120','','1511 Jianghong Road, Binjiang District, Hangzhou'),
('pl_riverside_fire_station','Changhe Fire and Rescue Station','fire_station',30.1964,120.2088,'CN','Hangzhou',4.8,1,'{"daily":"00:00-24:00"}','119','','Changhe Road Fire Station, Binjiang District, Hangzhou'),
('pl_jiangnan_market','Jiangnan Farmers'' Market','market',30.2059,120.2245,'CN','Hangzhou',4.1,1,'{"daily":"06:00-19:30"}','0571-86041203','','East section of Jiangnan Avenue, Binjiang District, Hangzhou'),
('pl_baima_lake_park','Baima Lake Park North Gate','park',30.1748,120.1982,'CN','Hangzhou',4.7,1,'{"daily":"06:00-22:00"}',NULL,NULL,'North Gate, Baima Lake Road, Binjiang District, Hangzhou'),
('pl_binsheng_pharmacy','Binsheng Road Community Pharmacy','pharmacy',30.2141,120.2126,'CN','Hangzhou',4.4,1,'{"daily":"07:30-22:30"}','0571-86673518',NULL,'1468 Binsheng Road, Binjiang District, Hangzhou'),
('pl_xixing_station','Xixing Metro Station','transit_station',30.1905,120.2142,'CN','Hangzhou',4.3,1,'{"daily":"05:55-23:10"}',NULL,NULL,'Xixing Road Metro Line 5, Binjiang District, Hangzhou'),
('pl_changhe_station','Changhe Metro Station','transit_station',30.2012,120.2061,'CN','Hangzhou',4.5,1,'{"daily":"06:00-23:05"}',NULL,NULL,'Changhe Road Metro Line 5, Binjiang District, Hangzhou'),
('pl_caihong_school','Caihongcheng Primary School','school',30.1879,120.2036,'CN','Hangzhou',4.4,1,'{}','0571-86627105',NULL,'Caihongcheng Primary School, Binwen Road, Binjiang District, Hangzhou'),
('pl_star_supermarket','Starlight Department Store Supermarket','supermarket',30.2107,120.2188,'CN','Hangzhou',4.0,2,'{"daily":"08:00-22:00"}','0571-86720116',NULL,'Phase II, Xingguang Avenue, Binjiang District, Hangzhou'),
('pl_community_pool','Riverside Community Swimming Pool','sports_center',30.2063,120.2094,'CN','Hangzhou',4.1,2,'{"weekday":"13:00-21:00","weekend":"09:00-21:00"}','0571-86590244',NULL,'Riverside Community Center, Binjiang District, Hangzhou'),
('pl_pediatric_dentist','Little Sprout Children''s Dentistry','dentist',30.2037,120.2211,'CN','Hangzhou',4.6,3,'{"daily":"09:00-18:00"}','0571-86993321',NULL,'Children''s Dental Clinic, Jianghong Road, Binjiang District, Hangzhou');
INSERT INTO place_reviews(place_id,author,rating,text,time) VALUES
('pl_binjiang_library','Family Reader Su Ning',5,'Seats in the picture-book area are limited on weekend mornings; the basement garage elevator goes directly to the second floor.','2026-05-09T10:20:00+08:00'),
('pl_children_clinic','Parent Cheng Lu',4,'The child healthcare queue numbers are called on time, and parking is more available in the afternoon than in the morning.','2026-04-18T15:10:00+08:00'),
('pl_jiangnan_market','Changhe Resident',4,'The vegetable stalls are best stocked before 7:00, and the east gate ramp is fairly smooth for pushing a stroller.','2026-05-22T07:15:00+08:00'),
('pl_baima_lake_park','Running Resident',5,'It takes about twelve minutes to walk from the north gate to the children''s lawn; it is windy by the lake.','2026-06-01T18:30:00+08:00'),
('pl_binsheng_pharmacy','Customer Yao Jie',4,'The stock of commonly used medicines is stable at night, but there is no ramp at the steps by the entrance.','2026-04-27T21:05:00+08:00'),
('pl_xixing_station','Commuter Zhou Ming',3,'The gates are crowded at 8:00 on weekdays, and trains toward Chengzhan are packed.','2026-06-12T08:12:00+08:00'),
('pl_star_supermarket','Nearby Resident',4,'The fresh food section is restocked at 9:00, and checkout lines take about ten minutes on Friday evenings.','2026-05-30T19:40:00+08:00'),
('pl_community_pool','Student''s Parent',3,'The children''s pool has a comfortable water temperature, but there are few hair dryers in the changing room.','2026-06-08T16:25:00+08:00');
INSERT INTO roads(road_id,name,city,geom_json) VALUES
('road_binsheng_west','West Section of Binsheng Road','Hangzhou','[[30.2141,120.2042],[30.2129,120.2148]]'),
('road_jianghong_north','North Section of Jianghong Road','Hangzhou','[[30.2019,120.2198],[30.2138,120.2219]]'),
('road_changhe_school','School Section of Changhe Road','Hangzhou','[[30.1982,120.2077],[30.2050,120.2150]]'),
('road_xixing_bridge','Underpass beneath Xixing Road Bridge','Hangzhou','[[30.1889,120.2114],[30.1938,120.2160]]');
INSERT INTO transit_stops(stop_id,name,lat,lng,city) VALUES
('stop_library','Tai''an Road Library','30.2085,120.2056,'Hangzhou'),
('stop_jiangnan_market','Jiangnan Market','30.2057,120.2242,'Hangzhou'),
('stop_changhe_metro','Changhe Metro Station Exit C','30.2014,120.2064,'Hangzhou'),
('stop_xixing_metro','Xixing Metro Station Exit D','30.1908,120.2145,'Hangzhou');
INSERT INTO transit_lines(line_id,name,mode,operator,segment_minutes_json) VALUES
('line_bus_1505','1505 Community Bus','bus','Hangzhou Public Transit','[6,9,7]'),
('line_walk_greenway','Binjiang Riverside Shuttle Line','bus','Binjiang Community Transit','[12,14,11]');
INSERT INTO transit_schedule(schedule_id,line_id,stop_id,direction,stop_seq,time) VALUES
(41,'line_bus_1505','stop_xixing_metro','Jiangnan Market direction',1,'07:18'),
(42,'line_walk_greenway','stop_library','Xinghe direction',2,'07:26'),
(43,'line_bus_1505','stop_changhe_metro','Xixing direction',3,'08:11'),
(44,'line_walk_greenway','stop_jiangnan_market','Changhe direction',1,'17:45'),
(45,'line_bus_1505','stop_jiangnan_market','Jiangnan Market direction',4,'07:39'),
(46,'line_walk_greenway','stop_changhe_metro','Xinghe direction',3,'18:02');
INSERT INTO road_events(event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
('rd_binsheng_drainage_spring','road_binsheng_west','2026-04-06T22:00:00+08:00','2026-04-12T05:30:00+08:00','heavy_traffic',0.7,'Nighttime storm-drain desilting; lanes will be restored during the day.',0),
('rd_xixing_marking_may','road_xixing_bridge','2026-05-16T09:00:00+08:00','2026-05-16T17:00:00+08:00','closure',0.5,'The road markings under the bridge will be repainted; one motor-vehicle lane will remain open that day.',0);
INSERT INTO transit_events(event_id,line_id,stop_id,start_dt,end_dt,kind,note,active) VALUES
('te_bus_1505_detour_apr','line_bus_1505','stop_jiangnan_market','2026-04-21T06:00:00+08:00','2026-04-23T23:00:00+08:00','delayed','During construction at the market''s east entrance, the bus will stop at a temporary stop on the west side.',0),
('te_greenway_flood_jun','line_walk_greenway','stop_library','2026-06-19T05:30:00+08:00','2026-06-19T14:00:00+08:00','suspended','The low-lying riverside section will be temporarily closed after heavy rainfall.',0);
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
('pl_binjiang_night_clinic','Binjiang Children''s Night Clinic','clinic',30.2076,120.2169,'CN','Hangzhou',4.2,2,'{"weekday":"18:00-22:00","weekend":"09:00-22:00"}','0571-86745290',NULL,'First floor, 1888 Jianghui Road, Binjiang District, Hangzhou'),
('pl_changhe_service_center','Changhe Subdistrict Citizen Service Center','government',30.2018,120.2112,'CN','Hangzhou',4.1,1,'{"weekday":"08:30-17:00"}','0571-86621871',NULL,'22 Changjiang North Road, Binjiang District, Hangzhou'),
('pl_jianghan_indoor_play','Jianghan Road Parent-Child Sports Center','sports_center',30.2115,120.2196,'CN','Hangzhou',4.3,3,'{"weekday":"13:00-20:30","weekend":"09:00-20:30"}','0571-86573142',NULL,'Third floor, 1515 Jianghan Road, Binjiang District, Hangzhou'),
('pl_xixing_bike_repair','Old Zhou''s Xixing Bicycle Repair','bicycle_repair',30.1917,120.2158,'CN','Hangzhou',4.6,1,'{"daily":"07:00-19:30"}','13758190426',NULL,'64 Guanhe Road, Binjiang District, Hangzhou'),
('pl_baima_fresh_market','Baima Lake Neighborhood Fresh Market','supermarket',30.1819,120.1927,'CN','Hangzhou',4.0,2,'{"daily":"06:30-21:30"}','0571-86091733',NULL,'South Gate, Baima Lake Residential Community, Binjiang District, Hangzhou'),
('pl_puyan_family_restroom','Puyan Riverside Park Parent-and-Baby Room','public_service',30.1678,120.1671,'CN','Hangzhou',4.5,1,'{"daily":"07:00-21:00"}',NULL,NULL,'Puyan Riverside Park Service Station, Wentao Road, Binjiang District, Hangzhou');
INSERT INTO place_reviews(place_id,author,rating,text,time) VALUES
('pl_binjiang_night_clinic','Parent Yu An',4,'Evening fever appointments are assigned in order of arrival, and the lab stops accepting samples at 9:30 p.m.','2026-05-18T21:12:00+08:00'),
('pl_jianghan_indoor_play','Member parent',3,'The trampoline area is crowded on Sunday afternoons; the toddler balance area and the older-children''s area are separated by a soft partition.','2026-06-14T16:38:00+08:00'),
('pl_xixing_bike_repair','Cycling commuter',5,'The child-seat mounting bolts are in stock, and replacing a brake cable usually takes half an hour.','2026-04-09T08:20:00+08:00'),
('pl_puyan_family_restroom','Resident out for a walk',4,'The parent-and-baby room has a fold-down changing table, and the water dispenser is routinely cleaned on Monday mornings.','2026-06-22T10:05:00+08:00');
INSERT INTO roads(road_id,name,city,geom_json) VALUES
('road_jianghui_clinic','Jianghui Road Clinic Section','Hangzhou','[[30.2048,120.2140],[30.2096,120.2188]]'),
('road_baima_south_gate','Baima Lake Community South Gate Branch Road','Hangzhou','[[30.1798,120.1905],[30.1836,120.1944]]'),
('road_wentao_puyan','Wentao Road Puyan Section','Hangzhou','[[30.1642,120.1618],[30.1714,120.1726]]');
INSERT INTO road_events(event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
('rd_jianghui_tree_trim_feb','road_jianghui_clinic','2026-02-24T09:30:00+08:00','2026-02-24T16:20:00+08:00','heavy_traffic',0.4,'Roadside tree pruning occupies the non-motorized lane on the hospital side.',0),
('rd_baima_gate_paving_mar','road_baima_south_gate','2026-03-11T07:00:00+08:00','2026-03-13T18:00:00+08:00','closure',0.6,'The south gate entrance is being repaved with permeable bricks; pedestrians should use the eastern footpath.',0),
('rd_wentao_race_may','road_wentao_puyan','2026-05-24T05:30:00+08:00','2026-05-24T11:30:00+08:00','closure',0.8,'During the riverside running event, motor vehicles should detour via Dongxin Avenue.',0);
COMMIT;
