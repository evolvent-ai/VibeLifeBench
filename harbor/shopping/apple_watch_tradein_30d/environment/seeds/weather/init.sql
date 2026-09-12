PRAGMA foreign_keys=ON;

-- Stage 0  translated text ： translated text  2026-06-15 09:00  translated text ； translated text shipment translated text alert translated text item translated text 。
INSERT INTO climate_profiles VALUES
('cp_awch_sh','{"summer_high":32,"summer_low":25,"winter_high":10,"winter_low":3}','{"jun":0.50,"jul":0.44}',15.0,78.0,'{"good":55,"moderate":36,"unhealthy":9}',' translated text ， translated text heavy precipitation'),
('cp_awch_sz','{"summer_high":32,"summer_low":25,"winter_high":9,"winter_low":2}','{"jun":0.52,"jul":0.42}',12.0,76.0,'{"good":57,"moderate":35,"unhealthy":8}',' translated text ， translated text ');
INSERT INTO locations VALUES
('geo_awch','Shanghai','CN',31.2304,121.4737,'Asia/Shanghai','cp_awch_sh','city'),
('geo_awch_sz','Suzhou','CN',31.2989,120.5853,'Asia/Shanghai','cp_awch_sz','city');
INSERT INTO daily_weather VALUES
('geo_awch','2026-06-15',24,29,'showers',7.8,0.70,19),
('geo_awch','2026-06-16',24,30,'cloudy',0.8,0.30,15),
('geo_awch','2026-06-17',25,31,'thunderstorm',14.2,0.77,25),
('geo_awch','2026-06-18',24,29,'heavy_rain',26.0,0.88,29),
('geo_awch','2026-06-19',24,29,'light_rain',6.4,0.64,20),
('geo_awch','2026-06-20',25,31,'cloudy',0.6,0.26,16),
('geo_awch','2026-06-21',25,32,'partly_cloudy',0.1,0.16,15),
('geo_awch_sz','2026-06-15',23,29,'light_rain',5.9,0.66,15),
('geo_awch_sz','2026-06-16',23,30,'cloudy',0.6,0.28,12),
('geo_awch_sz','2026-06-17',24,30,'thunderstorm',13.0,0.75,22),
('geo_awch_sz','2026-06-18',23,28,'heavy_rain',24.0,0.86,25),
('geo_awch_sz','2026-06-19',23,29,'showers',7.0,0.67,17),
('geo_awch_sz','2026-06-20',24,31,'cloudy',0.5,0.24,13),
('geo_awch_sz','2026-06-21',25,32,'partly_cloudy',0.0,0.14,12);
INSERT INTO hourly_weather VALUES
('geo_awch','2026-06-15T09:00:00+08:00',26.0,82,'cloudy',0.0,13),
('geo_awch','2026-06-15T10:00:00+08:00',26.5,80,'light_rain',0.6,15),
('geo_awch','2026-06-15T11:00:00+08:00',27.0,79,'showers',1.5,18),
('geo_awch','2026-06-15T12:00:00+08:00',27.5,77,'showers',1.7,20),
('geo_awch','2026-06-15T13:00:00+08:00',28.0,74,'cloudy',0.3,19),
('geo_awch','2026-06-15T14:00:00+08:00',28.5,71,'cloudy',0.0,17),
('geo_awch','2026-06-15T15:00:00+08:00',28.0,72,'partly_cloudy',0.0,16),
('geo_awch','2026-06-15T16:00:00+08:00',27.5,74,'partly_cloudy',0.0,15);
INSERT INTO alerts VALUES
('wx-SH-260615-RN5M','thunderstorm','yellow','2026-06-15T10:30:00+08:00','2026-06-15T15:00:00+08:00','["Shanghai translated text ","Pudong"]',' translated text ， translated text itemnote translated text 。',1,'2026-06-15T07:05:00+08:00','convective_20260615'),
('wx-SH-260606-WD8Q','strong_wind','blue','2026-06-06T12:00:00+08:00','2026-06-07T08:00:00+08:00','["Shanghai translated text "]',' translated text 。',0,'2026-06-06T10:30:00+08:00','wind_20260606');
INSERT INTO alert_subscriptions VALUES
('wsub_awch_main','geo_awch','notification_hub','2026-06-02T07:15:00+08:00',1),
('wsub_awch_backup','geo_awch_sz','email','2026-06-03T08:05:00+08:00',1);
INSERT INTO notifications(created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
('2026-06-15T07:07:00+08:00','notification_hub','wsub_awch_main','wx-SH-260615-RN5M','{"title":" translated text ","geo_key":"geo_awch","action":" translated text note translated text "}',1),
('2026-06-06T10:35:00+08:00','notification_hub','wsub_awch_main','wx-SH-260606-WD8Q','{"title":" translated text ","geo_key":"geo_awch"}',1);
INSERT INTO daily_aqi VALUES
('geo_awch','2026-06-09',45,'good','pm2.5','2026-06-09T08:00:00+08:00'),
('geo_awch','2026-06-10',51,'moderate','ozone','2026-06-10T08:00:00+08:00'),
('geo_awch','2026-06-11',57,'moderate','ozone','2026-06-11T08:00:00+08:00'),
('geo_awch','2026-06-12',48,'good','pm2.5','2026-06-12T08:00:00+08:00'),
('geo_awch','2026-06-13',43,'good','pm2.5','2026-06-13T08:00:00+08:00'),
('geo_awch','2026-06-14',46,'good','pm10','2026-06-14T08:00:00+08:00'),
('geo_awch','2026-06-15',50,'good','pm10','2026-06-15T08:00:00+08:00');
INSERT INTO _counters VALUES ('alerts',2),('notifications',2),('weather_updates',0);
INSERT INTO _sim_clock VALUES (1,'2026-06-15T09:00:00+08:00');
