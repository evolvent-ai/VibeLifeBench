PRAGMA foreign_keys = ON;
INSERT INTO places (place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
('pl_nrt','Narita International Airport','airport',35.7719,140.3929,'Japan','Narita',4.2,3,'{"daily":"24h"}',NULL,'internal://tokyo/maps/nrt','Narita International Airport, Chiba, Japan'),
('pl_narita_t1','Narita Airport Terminal 1 Station','station',35.7648,140.3863,'Japan','Narita',4.1,2,'{"daily":"05:00-24:00"}',NULL,'internal://tokyo/maps/narita-t1','Narita Airport Terminal 1 Station, Japan'),
('pl_keisei_ueno','Keisei Ueno Station','station',35.7115,139.7730,'Japan','Tokyo',4.0,2,'{"daily":"05:00-24:00"}',NULL,'internal://tokyo/maps/keisei-ueno','Keisei Ueno Station, Tokyo, Japan'),
('pl_tokyo_station','Tokyo Station','station',35.6812,139.7671,'Japan','Tokyo',4.3,2,'{"daily":"04:30-24:00"}',NULL,'internal://tokyo/maps/tokyo-station','Tokyo Station, Tokyo, Japan'),
('pl_roppongi_hotel','Roppongi Business Hotel','hotel',35.6635,139.7323,'Japan','Tokyo',4.4,3,'{"daily":"24h"}',NULL,'internal://tokyo/maps/roppongi-hotel','Roppongi, Minato City, Tokyo, Japan'),
('pl_roppongi_conference','Roppongi Conference Center','conference_center',35.6628,139.7315,'Japan','Tokyo',4.5,3,'{"event_days":"08:00-19:00"}',NULL,'internal://tokyo/maps/roppongi-conference','Roppongi Conference Center, Tokyo, Japan'),
('pl_shimbashi_client','ABC Corporation Shimbashi Office','office',35.6663,139.7585,'Japan','Tokyo',4.2,2,'{"weekdays":"09:00-18:00"}',NULL,'internal://tokyo/maps/shimbashi-client','Shimbashi, Minato City, Tokyo, Japan'),
('pl_akasaka_hotel','Akasaka Metro Stay','hotel',35.6744,139.7366,'Japan','Tokyo',4.5,3,'{"daily":"24h"}',NULL,'internal://tokyo/maps/akasaka-hotel','Akasaka, Minato City, Tokyo, Japan'),
('pl_hnd','Haneda Airport','airport',35.5494,139.7798,'Japan','Tokyo',4.4,3,'{"daily":"24h"}',NULL,'internal://tokyo/maps/hnd','Haneda Airport, Tokyo, Japan'),
('pl_ueno_spring_inn','Ueno Spring Inn','hotel',35.7138,139.7773,'Japan','Tokyo',4.0,2,'{"daily":"24h"}',NULL,'internal://tokyo/maps/ueno-spring-inn','Ueno, Tokyo, Japan');
INSERT INTO roads (road_id,name,city,geom_json) VALUES
('road_nrt_roppongi','Narita to Roppongi road corridor','Tokyo','{"typical_minutes":85,"mode":"road","toll":true}'),
('road_shimbashi_roppongi','Shimbashi to Roppongi','Tokyo','{"typical_minutes":20,"mode":"road"}');
INSERT INTO transit_stops (stop_id,name,lat,lng,city) VALUES
('stop_nrt_t1','Narita Airport Terminal 1',35.7648,140.3863,'Narita'),
('stop_ueno','Keisei Ueno',35.7115,139.7730,'Tokyo'),
('stop_roppongi','Roppongi',35.6628,139.7315,'Tokyo'),
('stop_tokyo','Tokyo Station',35.6812,139.7671,'Tokyo');
INSERT INTO transit_lines (line_id,name,mode,operator,segment_minutes_json) VALUES
('line_skyliner','Keisei Skyliner','train','Keisei','{"stop_nrt_t1-stop_ueno":44}'),
('line_nex','Narita Express','train','JR East','{"stop_nrt_t1-stop_tokyo":55}'),
('line_hibiya','Hibiya Line','subway','Tokyo Metro','{"stop_ueno-stop_roppongi":28}');
INSERT INTO transit_schedule (line_id,stop_id,direction,stop_seq,time) VALUES
('line_skyliner','stop_nrt_t1','Tokyo',1,'13:40'),('line_skyliner','stop_ueno','Tokyo',2,'14:24'),
('line_nex','stop_nrt_t1','Tokyo',1,'13:55'),('line_nex','stop_tokyo','Tokyo',2,'14:50'),
('line_hibiya','stop_ueno','Roppongi',1,'14:35'),('line_hibiya','stop_roppongi','Roppongi',2,'15:03');
INSERT INTO road_events (event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
('road_nrt_peak_0715','road_nrt_roppongi','2026-07-15T15:00:00+09:00','2026-07-15T19:30:00+09:00','heavy_traffic',0.65,'Weekday evening congestion can extend airport-road transfer time.',1);
