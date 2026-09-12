-- Reviewed Stage 0 map corpus: 55 places, reviews, roads and public-transit records.
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
 ('place_pek','Beijing Capital International Airport','airport',40.0799,116.6031,'China','Beijing',4.2,NULL,'{"open":"00:00-24:00"}',NULL,NULL,'PEK'),
 ('place_sha','Shanghai Hongqiaoscenario text','airport',31.1979,121.3363,'China','Shanghai',4.2,NULL,'{"open":"00:00-24:00"}',NULL,NULL,'SHA'),
 ('place_sh_hongqiao_rail','Shanghai Hongqiao Station','rail_station',31.1940,121.3180,'China','Shanghai',4.4,NULL,'{"open":"05:00-23:30"}',NULL,NULL,'Shanghai Hongqiao'),
 ('place_suzhou_funeral','Suzhou Funeral Service Center','funeral_home',31.2590,120.6310,'China','Suzhou',4.1,NULL,'{"service":"08:00-16:30"}',NULL,NULL,'SuzhouWuzhong'),
 ('place_sh_window','ShanghaiJing’anscenario textverification window','government',31.2350,121.4550,'China','Shanghai',4.0,NULL,'{"weekday":"08:30-16:30"}',NULL,NULL,'ShanghaiJing’an'),
 ('place_ningbo_station','Ningbo Station','rail_station',29.8690,121.5360,'China','Ningbo',4.5,NULL,'{"open":"05:30-23:00"}',NULL,NULL,'Ningbo Station');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<14)
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted)
SELECT printf('place_east_%02d',n),
       CASE n WHEN 1 THEN 'Suzhou Station North Square' WHEN 2 THEN 'Suzhou South Bus Station' WHEN 3 THEN 'Wuzhong People’s Hospital' WHEN 4 THEN 'Panmen Community Pharmacy' WHEN 5 THEN 'Shanghai Station South Square' WHEN 6 THEN 'Jing’an Temple Metro Station' WHEN 7 THEN 'Shanghai North Hospital' WHEN 8 THEN 'Hongqiao taxi pickup point' WHEN 9 THEN 'Ningbo Station North Square' WHEN 10 THEN 'Haishu District Government Center' WHEN 11 THEN 'Ningbo South Bus Station' WHEN 12 THEN 'Beijing South Station' WHEN 13 THEN 'Capital Airport transport center' ELSE 'Dongcheng community service station' END,
       CASE n%5 WHEN 0 THEN 'government' WHEN 1 THEN 'rail_station' WHEN 2 THEN 'transit' WHEN 3 THEN 'hospital' ELSE 'pharmacy' END,
       29.75+n*0.13,116.2+n*0.39,'China',CASE WHEN n<=4 THEN 'Suzhou' WHEN n<=8 THEN 'Shanghai' WHEN n<=11 THEN 'Ningbo' ELSE 'Beijing' END,
       3.8+(n%7)*0.1,CASE n%4 WHEN 0 THEN NULL ELSE n%4 END,'{"weekday":"07:00-21:00"}',NULL,NULL,
       CASE WHEN n<=4 THEN 'Suzhou city service point' WHEN n<=8 THEN 'Shanghai transport and public service point' WHEN n<=11 THEN 'Ningbo meeting-area service point' ELSE 'Beijing return-transport service point' END
FROM seq;

INSERT INTO roads(road_id,name,city,geom_json) VALUES
 ('road_sh_window_walk','Shanghai window pedestrian route','Shanghai','[[121.455,31.235],[121.459,31.238]]'),
 ('road_suz_funeral_access','Suzhou funeral service center access road','Suzhou','[[120.631,31.259],[120.642,31.268]]'),
 ('road_hongqiao_transfer','Hongqiao Airport to railway concourse','Shanghai','[[121.336,31.198],[121.318,31.194]]'),
 ('road_suz_station_south','Suzhou Station South Square route','Suzhou','[[120.606,31.329],[120.610,31.324]]'),
 ('road_ningbo_north_pickup','Ningbo Station North Square meeting road','Ningbo','[[121.536,29.869],[121.532,29.874]]'),
 ('road_ningbo_taxi_lane','Ningbo Station taxi queue road','Ningbo','[[121.538,29.868],[121.541,29.866]]'),
 ('road_pek_terminal_link','Capital Airport terminal link','Beijing','[[116.603,40.080],[116.610,40.084]]'),
 ('road_beijing_ring_access','Beijing East 2nd Ring approach','Beijing','[[116.430,39.920],[116.445,39.925]]'),
 ('road_sh_station_access','Shanghai Station South Square approach','Shanghai','[[121.458,31.249],[121.462,31.246]]'),
 ('road_suz_wuzhong_local','Wuzhong hospital connector','Suzhou','[[120.620,31.250],[120.629,31.258]]');

INSERT INTO place_reviews(place_id,author,rating,text,time) VALUES
 ('place_sh_hongqiao_rail','Travel observer A',4,'scenario text，scenario texttime。','2026-02-10T10:00:00+08:00'),
 ('place_suzhou_funeral','Local service observer',4,'scenario text，family memberscenario text。','2026-02-11T10:00:00+08:00'),
 ('place_sh_window','Service-window observer',4,'scenario text，scenario text。','2026-02-12T10:00:00+08:00'),
 ('place_ningbo_station','Meeting volunteer',5,'North Squarescenario text，scenario text。','2026-02-13T10:00:00+08:00'),
 ('place_east_01','Rail commuter',4,'North Squarescenario text，scenario textroute。','2026-02-14T10:00:00+08:00'),
 ('place_east_03','Family clinic escort',4,'scenario text，scenario textservice windowscenario text。','2026-02-15T10:00:00+08:00'),
 ('place_east_06','Metro passenger',5,'scenario text，scenario textservice windowscenario text。','2026-02-16T10:00:00+08:00'),
 ('place_east_08','Night arrival traveler',4,'scenario text，scenario text。','2026-02-17T10:00:00+08:00'),
 ('place_east_09','Ningbo resident',4,'North Squarescenario textelder，scenario texttime。','2026-02-18T10:00:00+08:00'),
 ('place_east_12','Business traveler',4,'Beijing South Stationscenario text，scenario text。','2026-02-19T10:00:00+08:00');

INSERT INTO transit_lines(line_id,name,mode,operator,segment_minutes_json) VALUES
 ('line_sh_metro_2','Shanghai Metro2scenario text','subway','Shanghai Shentong Metro','[8,7,6,9]'),
 ('line_sh_metro_13','Shanghai Metro13scenario text','subway','Shanghai Shentong Metro','[6,5,7,8]'),
 ('line_suz_bus_1','Suzhou Bus1scenario text','bus','Suzhou Bus Group','[9,8,11,7]'),
 ('line_nb_metro_2','Ningbo Rail Transit2scenario text','subway','Ningbo Rail Transit','[7,6,8,9]'),
 ('line_bj_airport','Beijing Airport Express','train','Beijing Urban Rail','[12,18,10]');
INSERT INTO transit_stops(stop_id,name,lat,lng,city) VALUES
 ('stop_hongqiao','Hongqiao Railway Station',31.194,121.318,'Shanghai'),('stop_jingan','Jing’anscenario text',31.224,121.445,'Shanghai'),
 ('stop_suz_station','Suzhou Station',31.329,120.606,'Suzhou'),('stop_nb_station','Ningboscenario text',29.869,121.536,'Ningbo'),('stop_pek_t2','Capital Airport T2',40.080,116.603,'Beijing');
INSERT INTO transit_schedule(line_id,stop_id,direction,stop_seq,time) VALUES
 ('line_sh_metro_2','stop_hongqiao','scenario text',1,'08:10'),('line_sh_metro_13','stop_jingan','Changningscenario text',3,'08:24'),
 ('line_suz_bus_1','stop_suz_station','Wuzhongscenario text',1,'09:05'),('line_nb_metro_2','stop_nb_station','scenario text',2,'19:58'),
 ('line_bj_airport','stop_pek_t2','scenario text',1,'20:45');
