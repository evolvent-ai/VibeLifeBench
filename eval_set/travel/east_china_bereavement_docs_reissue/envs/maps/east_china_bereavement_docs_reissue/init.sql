-- Reviewed Stage 0 map corpus: 55 places, reviews, roads and public-transit records.
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
 ('place_pek','北京首都国际机场','airport',40.0799,116.6031,'中国','北京',4.2,NULL,'{"open":"00:00-24:00"}',NULL,NULL,'PEK'),
 ('place_sha','上海虹桥机场','airport',31.1979,121.3363,'中国','上海',4.2,NULL,'{"open":"00:00-24:00"}',NULL,NULL,'SHA'),
 ('place_sh_hongqiao_rail','上海虹桥站','rail_station',31.1940,121.3180,'中国','上海',4.4,NULL,'{"open":"05:00-23:30"}',NULL,NULL,'上海虹桥'),
 ('place_suzhou_funeral','苏州市殡仪服务中心','funeral_home',31.2590,120.6310,'中国','苏州',4.1,NULL,'{"service":"08:00-16:30"}',NULL,NULL,'苏州吴中'),
 ('place_sh_window','上海静安证件核验窗口','government',31.2350,121.4550,'中国','上海',4.0,NULL,'{"weekday":"08:30-16:30"}',NULL,NULL,'上海静安'),
 ('place_ningbo_station','宁波站','rail_station',29.8690,121.5360,'中国','宁波',4.5,NULL,'{"open":"05:30-23:00"}',NULL,NULL,'宁波站');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<14)
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted)
SELECT printf('place_east_%02d',n),
       CASE n WHEN 1 THEN '苏州站北广场' WHEN 2 THEN '苏州汽车南站' WHEN 3 THEN '吴中人民医院' WHEN 4 THEN '盘门社区药房' WHEN 5 THEN '上海站南广场' WHEN 6 THEN '静安寺地铁站' WHEN 7 THEN '上海市北医院' WHEN 8 THEN '虹桥出租车上客点' WHEN 9 THEN '宁波站北广场' WHEN 10 THEN '海曙区政务中心' WHEN 11 THEN '宁波汽车南站' WHEN 12 THEN '北京南站' WHEN 13 THEN '首都机场交通中心' ELSE '东城区社区服务站' END,
       CASE n%5 WHEN 0 THEN 'government' WHEN 1 THEN 'rail_station' WHEN 2 THEN 'transit' WHEN 3 THEN 'hospital' ELSE 'pharmacy' END,
       29.75+n*0.13,116.2+n*0.39,'中国',CASE WHEN n<=4 THEN '苏州' WHEN n<=8 THEN '上海' WHEN n<=11 THEN '宁波' ELSE '北京' END,
       3.8+(n%7)*0.1,CASE n%4 WHEN 0 THEN NULL ELSE n%4 END,'{"weekday":"07:00-21:00"}',NULL,NULL,
       CASE WHEN n<=4 THEN '苏州城市服务点' WHEN n<=8 THEN '上海交通与公共服务点' WHEN n<=11 THEN '宁波接站周边服务点' ELSE '北京返程交通服务点' END
FROM seq;

INSERT INTO roads(road_id,name,city,geom_json) VALUES
 ('road_sh_window_walk','上海窗口步行通道','上海','[[121.455,31.235],[121.459,31.238]]'),
 ('road_suz_funeral_access','苏州殡仪服务中心接驳路','苏州','[[120.631,31.259],[120.642,31.268]]'),
 ('road_hongqiao_transfer','虹桥机场至铁路站连廊','上海','[[121.336,31.198],[121.318,31.194]]'),
 ('road_suz_station_south','苏州站南广场通道','苏州','[[120.606,31.329],[120.610,31.324]]'),
 ('road_ningbo_north_pickup','宁波站北广场接站道','宁波','[[121.536,29.869],[121.532,29.874]]'),
 ('road_ningbo_taxi_lane','宁波站出租车候客道','宁波','[[121.538,29.868],[121.541,29.866]]'),
 ('road_pek_terminal_link','首都机场航站楼连接线','北京','[[116.603,40.080],[116.610,40.084]]'),
 ('road_beijing_ring_access','北京东二环进场道路','北京','[[116.430,39.920],[116.445,39.925]]'),
 ('road_sh_station_access','上海站南广场进场道','上海','[[121.458,31.249],[121.462,31.246]]'),
 ('road_suz_wuzhong_local','吴中区医院联络路','苏州','[[120.620,31.250],[120.629,31.258]]');

INSERT INTO place_reviews(place_id,author,rating,text,time) VALUES
 ('place_sh_hongqiao_rail','出行记录员甲',4,'机场与铁路站距离不远，但携带行李时应预留室内步行时间。','2026-02-10T10:00:00+08:00'),
 ('place_suzhou_funeral','本地服务观察员',4,'院内指引较清楚，家属集中到场时入口车辆会短时排队。','2026-02-11T10:00:00+08:00'),
 ('place_sh_window','办事体验记录员',4,'预约核验按时段放行，迟到后可能需要重新取号。','2026-02-12T10:00:00+08:00'),
 ('place_ningbo_station','接站志愿者',5,'北广场标识清楚，晚高峰临停车辆应提前约定上客点。','2026-02-13T10:00:00+08:00'),
 ('place_east_01','铁路通勤者',4,'北广场出租车排队比南广场短，雨天仍需注意遮雨路线。','2026-02-14T10:00:00+08:00'),
 ('place_east_03','陪诊家属',4,'门诊楼有电梯和轮椅借用点，取药窗口午间人较少。','2026-02-15T10:00:00+08:00'),
 ('place_east_06','地铁乘客',5,'站内换乘标识完整，从出口到政务窗口步行约十分钟。','2026-02-16T10:00:00+08:00'),
 ('place_east_08','夜间到达旅客',4,'出租车上客区照明充足，航班集中到达时排队会变长。','2026-02-17T10:00:00+08:00'),
 ('place_east_09','宁波居民',4,'北广场适合接老人，约定固定柱号可以减少寻找时间。','2026-02-18T10:00:00+08:00'),
 ('place_east_12','商务旅客',4,'北京南站进站口较多，应根据车次检票口选择下车位置。','2026-02-19T10:00:00+08:00');

INSERT INTO transit_lines(line_id,name,mode,operator,segment_minutes_json) VALUES
 ('line_sh_metro_2','上海地铁2号线','subway','上海申通地铁','[8,7,6,9]'),
 ('line_sh_metro_13','上海地铁13号线','subway','上海申通地铁','[6,5,7,8]'),
 ('line_suz_bus_1','苏州公交1路','bus','苏州公交集团','[9,8,11,7]'),
 ('line_nb_metro_2','宁波轨道交通2号线','subway','宁波轨道交通','[7,6,8,9]'),
 ('line_bj_airport','北京机场快轨','train','北京市轨道交通','[12,18,10]');
INSERT INTO transit_stops(stop_id,name,lat,lng,city) VALUES
 ('stop_hongqiao','虹桥火车站',31.194,121.318,'上海'),('stop_jingan','静安寺',31.224,121.445,'上海'),
 ('stop_suz_station','苏州站',31.329,120.606,'苏州'),('stop_nb_station','宁波火车站',29.869,121.536,'宁波'),('stop_pek_t2','首都机场T2',40.080,116.603,'北京');
INSERT INTO transit_schedule(line_id,stop_id,direction,stop_seq,time) VALUES
 ('line_sh_metro_2','stop_hongqiao','市区方向',1,'08:10'),('line_sh_metro_13','stop_jingan','长宁方向',3,'08:24'),
 ('line_suz_bus_1','stop_suz_station','吴中方向',1,'09:05'),('line_nb_metro_2','stop_nb_station','栎社方向',2,'19:58'),
 ('line_bj_airport','stop_pek_t2','东直门方向',1,'20:45');
