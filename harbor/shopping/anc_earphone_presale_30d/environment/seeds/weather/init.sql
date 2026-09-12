PRAGMA foreign_keys=ON;

-- Stage 0 [translated note]：[translated note] 2026-06-15 09:00 [translated note]；7 [translated note]。
INSERT INTO climate_profiles VALUES
('cp_psea_bj','{"summer_high":32,"summer_low":22,"winter_high":4,"winter_low":-7}','{"jun":0.32,"jul":0.38}',12.0,58.0,'{"good":52,"moderate":36,"unhealthy":12}',char(21326) || char(21271) || char(28201) || char(24102) || char(23395) || char(39118) || char(27668) || char(20505) || '，' || char(22799) || char(23395) || char(23545) || char(27969) || char(24615) || char(38477) || char(27700) || char(36739) || char(22810)),
('cp_psea_tj','{"summer_high":31,"summer_low":23,"winter_high":3,"winter_low":-6}','{"jun":0.30,"jul":0.36}',14.0,61.0,'{"good":48,"moderate":39,"unhealthy":13}',char(27839) || char(28023) || char(24179) || char(21407) || char(39118) || char(21147) || char(30053) || char(39640) || '，' || char(39044) || char(25253) || char(29992) || char(20110) || char(37051) || char(36817) || char(22478) || char(24066) || char(23492) || char(36882) || char(21442) || char(29031));
INSERT INTO locations VALUES
('geo_psea',char(21271) || char(20140) || char(24066),'CN',39.9042,116.4074,'Asia/Shanghai','cp_psea_bj','city'),
('geo_psea_tj',char(22825) || char(27941) || char(24066),'CN',39.0842,117.2009,'Asia/Shanghai','cp_psea_tj','city');
INSERT INTO daily_weather VALUES
('geo_psea','2026-06-15',21,29,'showers',6.2,0.65,18),
('geo_psea','2026-06-16',20,30,'partly_cloudy',0.5,0.20,13),
('geo_psea','2026-06-17',22,32,'sunny',0.0,0.08,11),
('geo_psea','2026-06-18',23,33,'cloudy',0.0,0.18,12),
('geo_psea','2026-06-19',22,30,'thunderstorm',13.0,0.72,24),
('geo_psea','2026-06-20',21,28,'light_rain',4.8,0.58,17),
('geo_psea','2026-06-21',22,31,'partly_cloudy',0.3,0.18,12),
('geo_psea_tj','2026-06-15',22,29,'light_rain',3.5,0.54,21),
('geo_psea_tj','2026-06-16',21,30,'cloudy',0.2,0.16,18),
('geo_psea_tj','2026-06-17',23,31,'sunny',0.0,0.06,16),
('geo_psea_tj','2026-06-18',24,32,'partly_cloudy',0.0,0.12,17),
('geo_psea_tj','2026-06-19',22,29,'thunderstorm',11.2,0.68,27),
('geo_psea_tj','2026-06-20',21,27,'showers',5.1,0.60,22),
('geo_psea_tj','2026-06-21',22,30,'cloudy',0.4,0.22,17);
INSERT INTO hourly_weather VALUES
('geo_psea','2026-06-15T09:00:00+08:00',24.0,72,'cloudy',0.0,12),
('geo_psea','2026-06-15T10:00:00+08:00',25.0,69,'cloudy',0.0,13),
('geo_psea','2026-06-15T11:00:00+08:00',26.0,66,'light_rain',0.6,15),
('geo_psea','2026-06-15T12:00:00+08:00',26.5,68,'showers',1.8,18),
('geo_psea','2026-06-15T13:00:00+08:00',27.0,65,'showers',1.2,20),
('geo_psea','2026-06-15T14:00:00+08:00',27.5,61,'cloudy',0.2,17),
('geo_psea','2026-06-15T15:00:00+08:00',28.0,58,'partly_cloudy',0.0,15),
('geo_psea','2026-06-15T16:00:00+08:00',27.0,60,'partly_cloudy',0.0,14);
INSERT INTO alerts VALUES
('wx-BJ-260615-CV6P','thunderstorm','yellow','2026-06-15T10:30:00+08:00','2026-06-15T15:30:00+08:00','["' || char(21271) || char(20140) || char(24066) || char(19996) || char(37096) || '","' || char(21271) || char(20140) || char(24066) || char(21335) || char(37096) || '"]',char(21320) || char(38388) || char(21487) || char(33021) || char(20986) || char(29616) || char(30701) || char(26102) || char(38647) || char(38453) || char(38632) || char(21644) || char(38453) || char(39118) || '，' || char(30005) || char(23376) || char(35774) || char(22791) || char(22806) || char(20986) || char(25658) || char(24102) || char(27880) || char(24847) || char(38450) || char(27700) || '。',1,'2026-06-15T07:20:00+08:00','convective_20260615'),
('wx-BJ-260608-HT7K','heat','yellow','2026-06-08T12:00:00+08:00','2026-06-09T18:00:00+08:00','["' || char(21271) || char(20140) || char(24066) || '"]',char(21069) || char(26399) || char(39640) || char(28201) || char(25552) || char(31034) || char(24050) || char(32467) || char(26463) || '。',0,'2026-06-08T08:00:00+08:00','heat_20260608');
INSERT INTO alert_subscriptions VALUES
('wsub_psea_main','geo_psea','notification_hub','2026-06-02T07:30:00+08:00',1),
('wsub_psea_backup','geo_psea_tj','email','2026-06-03T08:00:00+08:00',1);
INSERT INTO notifications(created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
('2026-06-15T07:22:00+08:00','notification_hub','wsub_psea_main','wx-BJ-260615-CV6P','{"title":"' || char(38647) || char(38453) || char(38632) || char(25552) || char(31034) || '","geo_key":"geo_psea","action":"' || char(20851) || char(27880) || char(21320) || char(38388) || char(20986) || char(34892) || '"}',1),
('2026-06-08T08:05:00+08:00','notification_hub','wsub_psea_main','wx-BJ-260608-HT7K','{"title":"' || char(39640) || char(28201) || char(25552) || char(31034) || '","geo_key":"geo_psea"}',1);
INSERT INTO daily_aqi VALUES
('geo_psea','2026-06-09',78,'moderate','ozone','2026-06-09T08:00:00+08:00'),
('geo_psea','2026-06-10',64,'moderate','pm10','2026-06-10T08:00:00+08:00'),
('geo_psea','2026-06-11',52,'moderate','pm2.5','2026-06-11T08:00:00+08:00'),
('geo_psea','2026-06-12',46,'good','pm2.5','2026-06-12T08:00:00+08:00'),
('geo_psea','2026-06-13',55,'moderate','ozone','2026-06-13T08:00:00+08:00'),
('geo_psea','2026-06-14',61,'moderate','ozone','2026-06-14T08:00:00+08:00'),
('geo_psea','2026-06-15',58,'moderate','pm10','2026-06-15T08:00:00+08:00');
INSERT INTO _counters VALUES ('alerts',2),('notifications',2),('weather_updates',0);
INSERT INTO _sim_clock VALUES (1,'2026-06-15T09:00:00+08:00');
