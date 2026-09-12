PRAGMA foreign_keys=ON;

-- Stage 0 English business note：historicalEnglish business noteand 2026-06-15 09:00 English business notequeryofHangzhouEnglish business noteforecast；7 monthtrade-inshipmentEnglish business notenoneEnglish business notealert。
INSERT INTO climate_profiles VALUES
('cp_andt_hz','{"summer_high":33,"summer_low":25,"winter_high":10,"winter_low":3}','{"jun":0.55,"jul":0.48}',12.0,76.0,'{"good":58,"moderate":34,"unhealthy":8}','English business note，English business noteandEnglish business noteheavy precipitationriskEnglish business note'),
('cp_andt_nb','{"summer_high":32,"summer_low":25,"winter_high":10,"winter_low":4}','{"jun":0.52,"jul":0.46}',16.0,79.0,'{"good":61,"moderate":32,"unhealthy":7}','English business noteHangzhou，English business noteandEnglish business note');
INSERT INTO locations VALUES
('geo_andt','Hangzhou City','CN',30.2741,120.1551,'Asia/Shanghai','cp_andt_hz','city'),
('geo_andt_nb','English business note','CN',29.8683,121.5440,'Asia/Shanghai','cp_andt_nb','city');
INSERT INTO daily_weather VALUES
('geo_andt','2026-06-15',23,29,'showers',8.6,0.72,16),
('geo_andt','2026-06-16',23,30,'cloudy',1.0,0.35,12),
('geo_andt','2026-06-17',24,31,'thunderstorm',15.0,0.78,22),
('geo_andt','2026-06-18',24,30,'heavy_rain',24.0,0.86,25),
('geo_andt','2026-06-19',23,29,'light_rain',5.8,0.62,17),
('geo_andt','2026-06-20',24,32,'cloudy',0.8,0.28,13),
('geo_andt','2026-06-21',25,33,'partly_cloudy',0.2,0.18,12),
('geo_andt_nb','2026-06-15',23,28,'light_rain',5.2,0.64,20),
('geo_andt_nb','2026-06-16',23,29,'cloudy',0.7,0.30,18),
('geo_andt_nb','2026-06-17',24,30,'thunderstorm',12.4,0.74,26),
('geo_andt_nb','2026-06-18',23,29,'heavy_rain',21.0,0.83,28),
('geo_andt_nb','2026-06-19',23,28,'showers',7.1,0.68,21),
('geo_andt_nb','2026-06-20',24,31,'cloudy',0.4,0.24,18),
('geo_andt_nb','2026-06-21',25,32,'partly_cloudy',0.0,0.14,16);
INSERT INTO hourly_weather VALUES
('geo_andt','2026-06-15T09:00:00+08:00',25.0,84,'cloudy',0.0,10),
('geo_andt','2026-06-15T10:00:00+08:00',26.0,81,'light_rain',0.5,12),
('geo_andt','2026-06-15T11:00:00+08:00',26.5,82,'showers',1.4,15),
('geo_andt','2026-06-15T12:00:00+08:00',27.0,79,'showers',1.8,17),
('geo_andt','2026-06-15T13:00:00+08:00',27.5,77,'cloudy',0.3,16),
('geo_andt','2026-06-15T14:00:00+08:00',28.0,74,'cloudy',0.0,14),
('geo_andt','2026-06-15T15:00:00+08:00',28.5,72,'partly_cloudy',0.0,13),
('geo_andt','2026-06-15T16:00:00+08:00',28.0,74,'partly_cloudy',0.0,12);
INSERT INTO alerts VALUES
('wx-HZ-260615-TR8K','thunderstorm','yellow','2026-06-15T10:00:00+08:00','2026-06-15T14:30:00+08:00','["Hangzhou CityEnglish business note","Binjiang District"]','English business note，English business noteandEnglish business note。',1,'2026-06-15T07:10:00+08:00','convective_20260615'),
('wx-HZ-260607-FG4M','fog','yellow','2026-06-07T05:30:00+08:00','2026-06-07T09:30:00+08:00','["Hangzhou CityEnglish business note"]','English business notealreadyEnglish business note。',0,'2026-06-07T05:00:00+08:00','fog_20260607');
INSERT INTO alert_subscriptions VALUES
('wsub_andt_main','geo_andt','notification_hub','2026-06-02T07:20:00+08:00',1),
('wsub_andt_backup','geo_andt_nb','email','2026-06-03T08:10:00+08:00',1);
INSERT INTO notifications(created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
('2026-06-15T07:12:00+08:00','notification_hub','wsub_andt_main','wx-HZ-260615-TR8K','{"title":"English business note","geo_key":"geo_andt","action":"shipmentEnglish business note"}',1),
('2026-06-07T05:05:00+08:00','notification_hub','wsub_andt_main','wx-HZ-260607-FG4M','{"title":"English business note","geo_key":"geo_andt"}',1);
INSERT INTO daily_aqi VALUES
('geo_andt','2026-06-09',42,'good','pm2.5','2026-06-09T08:00:00+08:00'),
('geo_andt','2026-06-10',48,'good','pm2.5','2026-06-10T08:00:00+08:00'),
('geo_andt','2026-06-11',55,'moderate','ozone','2026-06-11T08:00:00+08:00'),
('geo_andt','2026-06-12',51,'moderate','pm10','2026-06-12T08:00:00+08:00'),
('geo_andt','2026-06-13',46,'good','pm2.5','2026-06-13T08:00:00+08:00'),
('geo_andt','2026-06-14',44,'good','pm2.5','2026-06-14T08:00:00+08:00'),
('geo_andt','2026-06-15',49,'good','pm10','2026-06-15T08:00:00+08:00');
INSERT INTO _counters VALUES ('alerts',2),('notifications',2),('weather_updates',0);
INSERT INTO _sim_clock VALUES (1,'2026-06-15T09:00:00+08:00');
