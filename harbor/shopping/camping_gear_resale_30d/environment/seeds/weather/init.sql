-- Generated weather seed for camping_gear_resale_30d
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_rstent', '{"jul_high": 33, "jul_low": 26}', '{"jul": 0.45}', 14.0, 78.0, '{"aqi":64,"dominant":"pm2.5"}', char(26757)||char(38632)||'/'||char(21488)||char(39118)||char(23395));
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_rstent', char(21414)||char(38376)||char(24066), 'CN', 31.23, 121.47, 'Asia/Shanghai', 'cp_rstent', 'city');
INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_rstent', '2026-07-02', 26, 31, 'rainstorm', 48.0, 0.92, 34),
  ('geo_rstent', '2026-07-03', 25, 30, 'rainstorm', 55.0, 0.95, 38),
  ('geo_rstent', '2026-07-04', 26, 32, 'heavy_rain', 30.0, 0.8, 26),
  ('geo_rstent', '2026-07-05', 27, 34, 'cloudy', 4.0, 0.3, 14),
  ('geo_rstent', '2026-07-06', 28, 35, 'sunny', 0.0, 0.1, 10);
INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('alr_rstent_storm', 'rainstorm', 'orange', '2026-07-02T00:00:00+08:00', '2026-07-04T23:59:59+08:00', '["geo_rstent","'||char(21414)||char(38376)||char(24066)||'"]', char(21414)||char(38376)||char(24066)||char(26292)||char(38632)||char(27225)||char(33394)||char(39044)||char(35686)||'：'||char(36830)||char(32493)||char(24378)||char(38477)||char(27700)||char(23558)||char(24433)||char(21709)||char(24080)||char(31735)||char(25645)||char(24314)||char(27979)||char(35797)||char(21644)||char(23492)||char(36865)||char(26102)||char(25928)||'，'||char(24314)||char(35758)||char(36873)||char(25321)||char(24178)||char(29157)||char(26102)||char(27573)||char(24182)||char(39044)||char(30041)||char(24179)||char(21488)||char(20030)||char(35777)||char(26102)||char(38388)||'。', 0, '2026-07-01T18:00:00+08:00', 'meiyu_2026');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES ('geo_rstent', '2026-07-02', 168, 'unhealthy', 'pm2.5', '2026-07-02T08:00:00+08:00');
INSERT INTO _sim_clock (id,sim_now) VALUES (1,'2026-06-15T09:00:00+08:00');
COMMIT;

-- ：、、。
BEGIN TRANSACTION;
UPDATE locations SET lat=24.4798,lng=118.0894 WHERE geo_key='geo_rstent';

INSERT INTO climate_profiles (profile_id,seasonal_temp_means_json,precip_freq_json,wind_baseline_kmh,humidity_baseline_pct,aqi_baseline_json,notes) VALUES
('cp_camp_quanzhou','{"spring":{"high":25,"low":18},"summer":{"high":32,"low":25}}','{"spring":0.38,"summer":0.44}',15.2,76.0,'{"aqi":46,"dominant":"pm2.5"}',char(27839)||char(28023)||char(22478)||char(24066)||'，'||char(28023)||char(39118)||char(26126)||char(26174)||'，'||char(21021)||char(22799)||char(21320)||char(21518)||char(23545)||char(27969)||char(22686)||char(22810)||'。'),
('cp_camp_zhangzhou','{"spring":{"high":27,"low":19},"summer":{"high":34,"low":25}}','{"spring":0.42,"summer":0.47}',10.6,79.0,'{"aqi":53,"dominant":"ozone"}',char(27827)||char(35895)||char(19982)||char(27839)||char(28023)||char(27668)||char(20505)||char(24182)||char(23384)||'，'||char(22812)||char(38388)||char(28287)||char(24230)||char(36739)||char(39640)||'。'),
('cp_camp_fuzhou','{"spring":{"high":26,"low":18},"summer":{"high":35,"low":26}}','{"spring":0.45,"summer":0.49}',11.8,78.0,'{"aqi":61,"dominant":"ozone"}',char(30406)||char(22320)||char(22799)||char(23395)||char(38391)||char(28909)||'，'||char(30701)||char(26102)||char(24378)||char(38477)||char(27700)||char(24120)||char(24433)||char(21709)||char(21608)||char(36793)||char(23665)||char(22320)||'。'),
('cp_camp_longyan','{"spring":{"high":25,"low":16},"summer":{"high":33,"low":23}}','{"spring":0.46,"summer":0.51}',8.9,81.0,'{"aqi":34,"dominant":"pm10"}',char(20869)||char(38470)||char(23665)||char(22320)||char(26172)||char(22812)||char(28201)||char(24046)||char(36739)||char(27839)||char(28023)||char(22823)||'，'||char(28165)||char(26216)||char(26131)||char(26377)||char(20302)||char(20113)||'。'),
('cp_camp_putian','{"spring":{"high":25,"low":18},"summer":{"high":33,"low":25}}','{"spring":0.39,"summer":0.46}',14.4,77.0,'{"aqi":42,"dominant":"pm2.5"}',char(28392)||char(28023)||char(39118)||char(36895)||char(36739)||char(39640)||'，'||char(28023)||char(23707)||char(21644)||char(22478)||char(21306)||char(22825)||char(27668)||char(21487)||char(33021)||char(19981)||char(21516)||char(27493)||'。'),
('cp_camp_sanming','{"spring":{"high":25,"low":15},"summer":{"high":34,"low":23}}','{"spring":0.48,"summer":0.53}',7.6,82.0,'{"aqi":29,"dominant":"pm2.5"}',char(22810)||char(23665)||char(20869)||char(38470)||'，'||char(23616)||char(22320)||char(38453)||char(38632)||char(21644)||char(26216)||char(38654)||char(23545)||char(24466)||char(27493)||char(36335)||char(32447)||char(24433)||char(21709)||char(36739)||char(22823)||'。'),
('cp_camp_ningde','{"spring":{"high":24,"low":17},"summer":{"high":32,"low":24}}','{"spring":0.44,"summer":0.50}',13.7,80.0,'{"aqi":38,"dominant":"pm10"}',char(23665)||char(28023)||char(20132)||char(38169)||'，'||char(27839)||char(28023)||char(38453)||char(39118)||char(19982)||char(23665)||char(21306)||char(38477)||char(27700)||char(38656)||char(20998)||char(21035)||char(21028)||char(26029)||'。'),
('cp_camp_wuyishan','{"spring":{"high":23,"low":14},"summer":{"high":31,"low":21}}','{"spring":0.51,"summer":0.56}',6.8,84.0,'{"aqi":24,"dominant":"pm2.5"}',char(26223)||char(21306)||char(23665)||char(22320)||char(28287)||char(28070)||'，'||char(28330)||char(35895)||char(26216)||char(38654)||char(21644)||char(38647)||char(38453)||char(38632)||char(20250)||char(25913)||char(21464)||char(27493)||char(36947)||char(26465)||char(20214)||'。');

INSERT INTO locations (geo_key,city,country,lat,lng,timezone,climate_profile_id,kind) VALUES
('geo_camp_quanzhou',char(27849)||char(24030)||char(24066),'CN',24.8741,118.6757,'Asia/Shanghai','cp_camp_quanzhou','city'),
('geo_camp_zhangzhou',char(28467)||char(24030)||char(24066),'CN',24.5130,117.6471,'Asia/Shanghai','cp_camp_zhangzhou','city'),
('geo_camp_fuzhou',char(31119)||char(24030)||char(24066),'CN',26.0745,119.2965,'Asia/Shanghai','cp_camp_fuzhou','city'),
('geo_camp_longyan',char(40857)||char(23721)||char(24066),'CN',25.0750,117.0173,'Asia/Shanghai','cp_camp_longyan','city'),
('geo_camp_putian',char(33670)||char(30000)||char(24066),'CN',25.4541,119.0077,'Asia/Shanghai','cp_camp_putian','city'),
('geo_camp_sanming',char(19977)||char(26126)||char(24066),'CN',26.2634,117.6389,'Asia/Shanghai','cp_camp_sanming','city'),
('geo_camp_ningde',char(23425)||char(24503)||char(24066),'CN',26.6657,119.5479,'Asia/Shanghai','cp_camp_ningde','city'),
('geo_camp_wuyishan',char(27494)||char(22839)||char(23665)||char(24066),'CN',27.7566,118.0353,'Asia/Shanghai','cp_camp_wuyishan','scenic_area');

INSERT INTO daily_weather VALUES
('geo_camp_quanzhou','2026-06-01',23,29,'partly_cloudy',0.0,0.18,17),
('geo_camp_quanzhou','2026-06-02',24,30,'cloudy',0.4,0.32,19),
('geo_camp_quanzhou','2026-06-04',23,27,'light_rain',6.8,0.72,21),
('geo_camp_quanzhou','2026-06-05',22,26,'moderate_rain',18.6,0.84,24),
('geo_camp_quanzhou','2026-06-07',24,30,'overcast',1.2,0.38,15),
('geo_camp_quanzhou','2026-06-09',25,32,'sunny',0.0,0.09,12),
('geo_camp_quanzhou','2026-06-10',25,31,'thunderstorm',12.4,0.67,28),
('geo_camp_quanzhou','2026-06-12',24,29,'showers',4.1,0.55,20),
('geo_camp_quanzhou','2026-06-13',25,33,'partly_cloudy',0.0,0.21,16),
('geo_camp_quanzhou','2026-06-15',26,34,'sunny',0.0,0.08,14),
('geo_camp_zhangzhou','2026-06-01',24,31,'cloudy',0.0,0.24,10),
('geo_camp_zhangzhou','2026-06-02',24,32,'partly_cloudy',0.0,0.16,11),
('geo_camp_zhangzhou','2026-06-04',23,29,'showers',7.5,0.69,13),
('geo_camp_zhangzhou','2026-06-05',23,28,'thunderstorm',22.8,0.88,20),
('geo_camp_zhangzhou','2026-06-07',24,31,'overcast',1.0,0.35,9),
('geo_camp_zhangzhou','2026-06-09',25,34,'sunny',0.0,0.07,8),
('geo_camp_zhangzhou','2026-06-10',25,33,'cloudy',0.6,0.31,12),
('geo_camp_zhangzhou','2026-06-12',24,30,'moderate_rain',15.3,0.79,17),
('geo_camp_zhangzhou','2026-06-13',25,32,'light_rain',3.7,0.52,14),
('geo_camp_zhangzhou','2026-06-15',26,35,'partly_cloudy',0.0,0.18,9),
('geo_camp_fuzhou','2026-06-01',23,30,'overcast',0.8,0.36,11),
('geo_camp_fuzhou','2026-06-02',24,32,'sunny',0.0,0.12,10),
('geo_camp_fuzhou','2026-06-04',24,31,'cloudy',1.3,0.44,12),
('geo_camp_fuzhou','2026-06-05',23,27,'rainstorm',41.2,0.94,25),
('geo_camp_fuzhou','2026-06-07',24,29,'light_rain',5.6,0.63,13),
('geo_camp_fuzhou','2026-06-09',25,34,'partly_cloudy',0.0,0.19,9),
('geo_camp_fuzhou','2026-06-10',26,35,'hot',0.0,0.08,8),
('geo_camp_fuzhou','2026-06-12',25,32,'thunderstorm',11.9,0.71,19),
('geo_camp_fuzhou','2026-06-13',25,31,'showers',6.2,0.58,14),
('geo_camp_fuzhou','2026-06-15',26,36,'sunny',0.0,0.06,9),
('geo_camp_longyan','2026-06-01',20,28,'mist',0.2,0.28,6),
('geo_camp_longyan','2026-06-02',21,30,'partly_cloudy',0.0,0.17,7),
('geo_camp_longyan','2026-06-04',21,27,'light_rain',8.4,0.74,8),
('geo_camp_longyan','2026-06-05',20,26,'moderate_rain',19.7,0.86,11),
('geo_camp_longyan','2026-06-07',21,29,'cloudy',0.7,0.33,7),
('geo_camp_longyan','2026-06-09',22,32,'sunny',0.0,0.10,6),
('geo_camp_longyan','2026-06-10',22,31,'thunderstorm',13.6,0.76,16),
('geo_camp_longyan','2026-06-12',21,28,'showers',5.9,0.61,9),
('geo_camp_longyan','2026-06-13',22,30,'overcast',0.4,0.29,8),
('geo_camp_longyan','2026-06-15',23,33,'partly_cloudy',0.0,0.15,7),
('geo_camp_putian','2026-06-01',23,29,'cloudy',0.3,0.31,15),
('geo_camp_putian','2026-06-02',24,31,'partly_cloudy',0.0,0.18,16),
('geo_camp_putian','2026-06-04',23,28,'showers',6.1,0.66,19),
('geo_camp_putian','2026-06-05',22,27,'moderate_rain',17.4,0.82,23),
('geo_camp_putian','2026-06-07',24,30,'overcast',0.9,0.37,14),
('geo_camp_putian','2026-06-09',25,32,'sunny',0.0,0.11,13),
('geo_camp_putian','2026-06-10',25,31,'thunderstorm',10.8,0.64,27),
('geo_camp_putian','2026-06-12',24,29,'light_rain',4.7,0.57,18),
('geo_camp_putian','2026-06-13',25,33,'partly_cloudy',0.0,0.20,15),
('geo_camp_putian','2026-06-15',26,34,'sunny',0.0,0.07,12),
('geo_camp_sanming','2026-06-01',19,27,'fog',0.1,0.25,5),
('geo_camp_sanming','2026-06-02',20,29,'cloudy',0.0,0.23,6),
('geo_camp_sanming','2026-06-04',20,26,'moderate_rain',14.2,0.81,8),
('geo_camp_sanming','2026-06-05',19,25,'heavy_rain',32.6,0.91,12),
('geo_camp_sanming','2026-06-07',20,28,'mist',0.5,0.34,5),
('geo_camp_sanming','2026-06-09',21,31,'sunny',0.0,0.09,6),
('geo_camp_sanming','2026-06-10',21,29,'thunderstorm',16.8,0.79,15),
('geo_camp_sanming','2026-06-12',20,27,'showers',7.1,0.65,9),
('geo_camp_sanming','2026-06-13',21,30,'partly_cloudy',0.0,0.21,7),
('geo_camp_sanming','2026-06-15',22,32,'cloudy',0.2,0.27,6),
('geo_camp_ningde','2026-06-01',22,28,'partly_cloudy',0.0,0.19,14),
('geo_camp_ningde','2026-06-02',23,29,'cloudy',0.6,0.35,16),
('geo_camp_ningde','2026-06-04',22,27,'light_rain',9.3,0.73,20),
('geo_camp_ningde','2026-06-05',21,26,'heavy_rain',29.4,0.90,26),
('geo_camp_ningde','2026-06-07',23,29,'overcast',1.1,0.42,15),
('geo_camp_ningde','2026-06-09',24,31,'sunny',0.0,0.10,12),
('geo_camp_ningde','2026-06-10',24,30,'thunderstorm',14.1,0.75,29),
('geo_camp_ningde','2026-06-12',23,28,'showers',5.2,0.59,18),
('geo_camp_ningde','2026-06-13',24,32,'partly_cloudy',0.0,0.22,14),
('geo_camp_ningde','2026-06-15',25,33,'sunny',0.0,0.08,13),
('geo_camp_wuyishan','2026-06-01',18,25,'fog',0.2,0.30,4),
('geo_camp_wuyishan','2026-06-02',19,27,'partly_cloudy',0.0,0.18,5),
('geo_camp_wuyishan','2026-06-04',19,24,'moderate_rain',16.5,0.83,7),
('geo_camp_wuyishan','2026-06-05',18,23,'rainstorm',38.8,0.93,13),
('geo_camp_wuyishan','2026-06-07',19,26,'mist',0.8,0.39,5),
('geo_camp_wuyishan','2026-06-09',20,29,'sunny',0.0,0.08,4),
('geo_camp_wuyishan','2026-06-10',20,27,'thunderstorm',18.2,0.82,17),
('geo_camp_wuyishan','2026-06-12',19,25,'showers',8.7,0.68,8),
('geo_camp_wuyishan','2026-06-13',20,28,'cloudy',0.4,0.33,6),
('geo_camp_wuyishan','2026-06-15',21,30,'partly_cloudy',0.0,0.17,5);

INSERT INTO hourly_weather VALUES
('geo_camp_quanzhou','2026-06-10T07:00:00+08:00',26,82,'cloudy',0.0,15),
('geo_camp_quanzhou','2026-06-10T10:30:00+08:00',29,73,'showers',1.6,21),
('geo_camp_quanzhou','2026-06-10T14:20:00+08:00',30,70,'thunderstorm',7.8,31),
('geo_camp_quanzhou','2026-06-10T18:45:00+08:00',27,86,'light_rain',3.0,23),
('geo_camp_zhangzhou','2026-06-05T06:40:00+08:00',24,90,'overcast',0.4,8),
('geo_camp_zhangzhou','2026-06-05T09:50:00+08:00',26,84,'showers',2.3,12),
('geo_camp_zhangzhou','2026-06-05T13:35:00+08:00',27,81,'thunderstorm',11.6,22),
('geo_camp_zhangzhou','2026-06-05T19:10:00+08:00',24,92,'moderate_rain',8.5,15),
('geo_camp_fuzhou','2026-06-05T05:55:00+08:00',24,91,'rain',3.2,14),
('geo_camp_fuzhou','2026-06-05T09:15:00+08:00',25,88,'heavy_rain',12.7,22),
('geo_camp_fuzhou','2026-06-05T12:40:00+08:00',26,86,'rainstorm',18.9,29),
('geo_camp_fuzhou','2026-06-05T17:25:00+08:00',24,93,'moderate_rain',6.4,18),
('geo_camp_longyan','2026-06-10T06:25:00+08:00',22,89,'mist',0.0,5),
('geo_camp_longyan','2026-06-10T10:05:00+08:00',27,76,'cloudy',0.0,8),
('geo_camp_longyan','2026-06-10T14:55:00+08:00',29,72,'thunderstorm',9.4,19),
('geo_camp_longyan','2026-06-10T20:20:00+08:00',24,87,'showers',4.2,10),
('geo_camp_putian','2026-06-10T07:35:00+08:00',26,84,'cloudy',0.0,17),
('geo_camp_putian','2026-06-10T11:10:00+08:00',29,75,'partly_cloudy',0.0,20),
('geo_camp_putian','2026-06-10T15:05:00+08:00',30,73,'thunderstorm',6.9,30),
('geo_camp_putian','2026-06-10T19:40:00+08:00',27,85,'light_rain',3.1,22),
('geo_camp_sanming','2026-06-05T06:10:00+08:00',20,94,'fog',0.1,4),
('geo_camp_sanming','2026-06-05T09:30:00+08:00',22,89,'moderate_rain',5.8,7),
('geo_camp_sanming','2026-06-05T13:50:00+08:00',24,86,'heavy_rain',14.6,14),
('geo_camp_sanming','2026-06-05T18:15:00+08:00',21,93,'rain',7.2,10),
('geo_camp_ningde','2026-06-05T05:45:00+08:00',22,92,'overcast',0.5,13),
('geo_camp_ningde','2026-06-05T08:55:00+08:00',24,87,'showers',3.6,19),
('geo_camp_ningde','2026-06-05T13:10:00+08:00',25,85,'heavy_rain',13.8,28),
('geo_camp_ningde','2026-06-05T18:50:00+08:00',23,91,'moderate_rain',6.1,21),
('geo_camp_wuyishan','2026-06-05T06:30:00+08:00',19,96,'fog',0.2,3),
('geo_camp_wuyishan','2026-06-05T10:20:00+08:00',21,92,'moderate_rain',6.7,6),
('geo_camp_wuyishan','2026-06-05T14:30:00+08:00',22,90,'rainstorm',17.3,15),
('geo_camp_wuyishan','2026-06-05T19:35:00+08:00',20,95,'rain',8.1,9);

INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
('alr_camp_quanzhou_coast','gale','yellow','2026-06-10T12:10:00+08:00','2026-06-10T21:30:00+08:00','["geo_camp_quanzhou","'||char(27849)||char(24030)||char(24066)||char(27839)||char(28023)||'","'||char(23815)||char(27494)||char(21322)||char(23707)||'"]',char(27839)||char(28023)||char(38453)||char(39118)||char(22686)||char(24378)||'，'||char(22825)||char(24149)||char(24212)||char(38477)||char(20302)||char(33829)||char(26609)||char(24182)||char(22686)||char(21152)||char(25239)||char(39118)||char(32499)||'；'||char(36817)||char(23736)||char(27963)||char(21160)||char(24403)||char(22825)||char(21462)||char(28040)||'。',0,'2026-06-10T09:42:00+08:00','coastal_wind_quanzhou'),
('alr_camp_zhangzhou_storm','thunderstorm','orange','2026-06-05T11:20:00+08:00','2026-06-05T20:40:00+08:00','["geo_camp_zhangzhou","'||char(28467)||char(24030)||char(24066)||char(40857)||char(25991)||char(21306)||'","'||char(21335)||char(38742)||char(23665)||char(21306)||'"]',char(38647)||char(26292)||char(20276)||char(30701)||char(26102)||char(24378)||char(38477)||char(27700)||'，'||char(28330)||char(35895)||char(33829)||char(22320)||char(23384)||char(22312)||char(28072)||char(27700)||char(39118)||char(38505)||'，'||char(24050)||char(24314)||char(35758)||char(38431)||char(20237)||char(25764)||char(31163)||char(27827)||char(28393)||'。',0,'2026-06-05T09:08:00+08:00','convective_zhangzhou'),
('alr_camp_fuzhou_rain','rainstorm','orange','2026-06-05T07:35:00+08:00','2026-06-05T18:10:00+08:00','["geo_camp_fuzhou","'||char(31119)||char(24030)||char(24066)||char(40723)||char(27004)||char(21306)||'","'||char(26187)||char(23433)||char(21306)||char(21271)||char(23792)||'"]',char(25345)||char(32493)||char(24378)||char(38477)||char(27700)||char(36896)||char(25104)||char(37096)||char(20998)||char(23665)||char(36335)||char(36793)||char(22369)||char(28287)||char(28369)||'，'||char(38706)||char(33829)||char(35013)||char(22791)||char(27966)||char(36865)||char(19982)||char(21271)||char(23792)||char(24466)||char(27493)||char(22343)||char(38656)||char(25913)||char(26399)||'。',0,'2026-06-05T06:12:00+08:00','rain_fuzhou_basin'),
('alr_camp_longyan_lightning','lightning','yellow','2026-06-10T13:40:00+08:00','2026-06-10T19:50:00+08:00','["geo_camp_longyan","'||char(40857)||char(23721)||char(24066)||char(26032)||char(32599)||char(21306)||'","'||char(27743)||char(23665)||char(38215)||'"]',char(23665)||char(21306)||char(38647)||char(30005)||char(27963)||char(21160)||char(39057)||char(32321)||'，'||char(23665)||char(33034)||char(36335)||char(32447)||char(19981)||char(23452)||char(20572)||char(30041)||'，'||char(37329)||char(23646)||char(30331)||char(23665)||char(26454)||char(24212)||char(25910)||char(32435)||char(21518)||char(23613)||char(24555)||char(19979)||char(38477)||'。',0,'2026-06-10T11:23:00+08:00','lightning_longyan'),
('alr_camp_putian_squall','gale','blue','2026-06-10T14:15:00+08:00','2026-06-10T20:05:00+08:00','["geo_camp_putian","'||char(33670)||char(30000)||char(24066)||char(28228)||char(27954)||char(28286)||'","'||char(33620)||char(22478)||char(21306)||'"]',char(39121)||char(32447)||char(32463)||char(36807)||char(26102)||char(38453)||char(39118)||char(36739)||char(24378)||'，'||char(33829)||char(28783)||char(21644)||char(26700)||char(26885)||char(24212)||char(25910)||char(20837)||char(24080)||char(20869)||'，'||char(28023)||char(36793)||char(33829)||char(20301)||char(26242)||char(20572)||char(25645)||char(24314)||'。',0,'2026-06-10T12:36:00+08:00','squall_putian'),
('alr_camp_sanming_flood','rainstorm','orange','2026-06-05T08:50:00+08:00','2026-06-06T01:20:00+08:00','["geo_camp_sanming","'||char(19977)||char(26126)||char(24066)||char(19977)||char(20803)||char(21306)||'","'||char(27801)||char(21439)||char(21306)||char(23665)||char(35895)||'"]',char(19978)||char(28216)||char(32047)||char(35745)||char(38632)||char(37327)||char(36739)||char(22823)||'，'||char(20302)||char(27964)||char(33829)||char(22320)||char(21644)||char(20020)||char(28330)||char(27493)||char(36947)||char(20851)||char(38381)||'，'||char(24050)||char(36890)||char(30693)||char(39044)||char(35746)||char(32773)||char(26356)||char(25442)||char(39640)||char(22320)||char(33829)||char(20301)||'。',0,'2026-06-05T07:18:00+08:00','mountain_rain_sanming'),
('alr_camp_ningde_windrain','rainstorm','yellow','2026-06-05T10:05:00+08:00','2026-06-05T22:15:00+08:00','["geo_camp_ningde","'||char(23425)||char(24503)||char(24066)||char(34121)||char(22478)||char(21306)||'","'||char(19977)||char(37117)||char(28595)||'"]',char(39118)||char(38632)||char(21472)||char(21152)||char(24433)||char(21709)||char(36718)||char(28193)||char(21644)||char(36328)||char(28023)||char(37197)||char(36865)||'，'||char(38450)||char(27700)||char(34955)||char(35746)||char(21333)||char(25913)||char(30001)||char(27425)||char(26085)||char(19978)||char(21320)||char(22797)||char(26680)||char(32447)||char(36335)||'。',0,'2026-06-05T08:41:00+08:00','wind_rain_ningde'),
('alr_camp_wuyishan_trail','landslide_risk','orange','2026-06-05T09:30:00+08:00','2026-06-06T12:00:00+08:00','["geo_camp_wuyishan","'||char(27494)||char(22839)||char(23665)||char(24066)||char(26223)||char(21306)||char(21271)||char(37096)||'","'||char(26704)||char(26408)||char(20851)||char(21608)||char(36793)||'"]',char(36830)||char(32493)||char(38477)||char(38632)||char(21518)||char(22303)||char(22756)||char(21547)||char(27700)||char(37327)||char(39640)||'，'||char(26410)||char(24320)||char(25918)||char(25903)||char(32447)||char(19981)||char(24471)||char(36827)||char(20837)||'，'||char(25143)||char(22806)||char(38431)||char(24050)||char(25913)||char(36208)||char(38138)||char(35013)||char(20027)||char(36335)||'。',0,'2026-06-05T07:52:00+08:00','trail_risk_wuyishan');

INSERT INTO alert_subscriptions (sub_id,geo_key,sink,created_at,active) VALUES
('wsub_camp_quanzhou','geo_camp_quanzhou','notification_hub','2025-09-14T08:25:00+08:00',1),
('wsub_camp_zhangzhou','geo_camp_zhangzhou','email','2026-02-06T16:18:00+08:00',1),
('wsub_camp_fuzhou','geo_camp_fuzhou','notification_hub','2025-11-21T10:42:00+08:00',1),
('wsub_camp_longyan','geo_camp_longyan','email','2026-03-17T07:55:00+08:00',1),
('wsub_camp_putian','geo_camp_putian','notification_hub','2026-04-09T14:31:00+08:00',1),
('wsub_camp_sanming','geo_camp_sanming','email','2025-12-28T09:06:00+08:00',1),
('wsub_camp_ningde','geo_camp_ningde','notification_hub','2026-05-12T18:24:00+08:00',1),
('wsub_camp_wuyishan','geo_camp_wuyishan','email','2026-01-19T11:47:00+08:00',1);

INSERT INTO notifications (created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
('2026-06-10T09:45:00+08:00','notification_hub','wsub_camp_quanzhou','alr_camp_quanzhou_coast','{"title":"'||char(27849)||char(24030)||char(27839)||char(28023)||char(22823)||char(39118)||'","action":"'||char(38477)||char(20302)||char(22825)||char(24149)||char(24182)||char(21462)||char(28040)||char(36817)||char(23736)||char(27963)||char(21160)||'"}',1),
('2026-06-05T09:12:00+08:00','email','wsub_camp_zhangzhou','alr_camp_zhangzhou_storm','{"title":"'||char(28467)||char(24030)||char(38647)||char(26292)||char(21319)||char(32423)||'","action":"'||char(25764)||char(31163)||char(28330)||char(35895)||char(33829)||char(20301)||'"}',1),
('2026-06-05T06:16:00+08:00','notification_hub','wsub_camp_fuzhou','alr_camp_fuzhou_rain','{"title":"'||char(31119)||char(24030)||char(24378)||char(38477)||char(38632)||'","action":"'||char(21271)||char(23792)||char(34892)||char(31243)||char(25913)||char(26399)||'"}',1),
('2026-06-10T11:27:00+08:00','email','wsub_camp_longyan','alr_camp_longyan_lightning','{"title":"'||char(40857)||char(23721)||char(23665)||char(21306)||char(38647)||char(30005)||'","action":"'||char(36991)||char(24320)||char(23665)||char(33034)||char(24182)||char(25910)||char(32435)||char(37329)||char(23646)||char(26454)||'"}',1),
('2026-06-10T12:40:00+08:00','notification_hub','wsub_camp_putian','alr_camp_putian_squall','{"title":"'||char(28228)||char(27954)||char(28286)||char(39121)||char(32447)||'","action":"'||char(26242)||char(20572)||char(28023)||char(36793)||char(25645)||char(24314)||'"}',1),
('2026-06-05T07:22:00+08:00','email','wsub_camp_sanming','alr_camp_sanming_flood','{"title":"'||char(19977)||char(26126)||char(23665)||char(35895)||char(28072)||char(27700)||char(39118)||char(38505)||'","action":"'||char(26356)||char(25442)||char(39640)||char(22320)||char(33829)||char(20301)||'"}',1),
('2026-06-05T08:45:00+08:00','notification_hub','wsub_camp_ningde','alr_camp_ningde_windrain','{"title":"'||char(23425)||char(24503)||char(39118)||char(38632)||char(24433)||char(21709)||char(36718)||char(28193)||'","action":"'||char(22797)||char(26680)||char(36328)||char(28023)||char(37197)||char(36865)||char(32447)||char(36335)||'"}',1),
('2026-06-05T07:56:00+08:00','email','wsub_camp_wuyishan','alr_camp_wuyishan_trail','{"title":"'||char(27494)||char(22839)||char(23665)||char(27493)||char(36947)||char(39118)||char(38505)||'","action":"'||char(20165)||char(36208)||char(24320)||char(25918)||char(20027)||char(36335)||'"}',1);

INSERT INTO daily_aqi (geo_key,date,aqi,category,dominant_pollutant,observed_at) VALUES
('geo_camp_quanzhou','2026-06-15',46,'good','pm2.5','2026-06-15T08:05:00+08:00'),
('geo_camp_zhangzhou','2026-06-15',53,'moderate','ozone','2026-06-15T08:12:00+08:00'),
('geo_camp_fuzhou','2026-06-15',61,'moderate','ozone','2026-06-15T08:18:00+08:00'),
('geo_camp_longyan','2026-06-15',34,'good','pm10','2026-06-15T08:27:00+08:00'),
('geo_camp_putian','2026-06-15',42,'good','pm2.5','2026-06-15T08:33:00+08:00'),
('geo_camp_sanming','2026-06-15',29,'good','pm2.5','2026-06-15T08:41:00+08:00'),
('geo_camp_ningde','2026-06-15',38,'good','pm10','2026-06-15T08:49:00+08:00'),
('geo_camp_wuyishan','2026-06-15',24,'good','pm2.5','2026-06-15T08:56:00+08:00');
COMMIT;
