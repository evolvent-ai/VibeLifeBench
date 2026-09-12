-- Generated weather seed for garden_total_reno_v4_30d
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_qgrd', '{"jul_high": 34, "jul_low": 22}', '{"jul": 0.31, "convective_rain": true}', 11.0, 65.0, '{"good": 44, "moderate": 38, "unhealthy": 18}', 'Xi''an has a warm-temperate, semi-humid continental monsoon climate; convective rain in summer coexists with relatively long dry intervals. The figures are baseline values for a synthetic scenario; current assessment should follow daily weather and released warnings.');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_qgrd', 'Xi''an City', 'CN', 31.23, 121.47, 'Asia/Shanghai', 'cp_qgrd', 'city');
INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_qgrd', '2026-06-26', 26, 31, 'rainstorm', 48.0, 0.92, 34),
  ('geo_qgrd', '2026-06-28', 25, 30, 'rainstorm', 55.0, 0.95, 38),
  ('geo_qgrd', '2026-06-30', 26, 32, 'heavy_rain', 30.0, 0.8, 26),
  ('geo_qgrd', '2026-07-02', 27, 34, 'cloudy', 4.0, 0.3, 14),
  ('geo_qgrd', '2026-07-04', 28, 35, 'sunny', 0.0, 0.1, 10);
INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('alr_qgrd_storm', 'rainstorm', 'orange', '2026-06-26T00:00:00+08:00', '2026-06-30T23:59:59+08:00', '["Xi''an City"]', 'Xi''an City orange rainstorm warning: sustained heavy rainfall may delay deliveries; consider receiving packages outside peak hours or changing the delivery location to a pickup point.', 1, '2026-06-25T18:00:00+08:00', 'meiyu_2026');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES ('geo_qgrd', '2026-06-14', 81, 'moderate', 'o3', '2026-06-14T17:05:00+08:00');
COMMIT;
BEGIN;
UPDATE locations SET lat=34.3416,lng=108.9398 WHERE geo_key='geo_qgrd';
UPDATE daily_weather SET date=CASE date WHEN '2026-06-26' THEN '2026-05-10' WHEN '2026-06-28' THEN '2026-05-17' WHEN '2026-06-30' THEN '2026-05-24' WHEN '2026-07-02' THEN '2026-06-01' ELSE '2026-06-08' END WHERE geo_key='geo_qgrd';
UPDATE alerts SET active=0,start_dt='2026-05-17T00:00:00+08:00',end_dt='2026-05-17T23:59:59+08:00',created_at='2026-05-16T10:00:00+08:00',description='Historical heavy-rainfall record: used to compare drainage observation methods and does not represent future weather.' WHERE alert_id='alr_qgrd_storm';
COMMIT;
-- 2026-07-30 cross-service richness remediation: varied historical weather for drainage and plant context.
BEGIN;
INSERT INTO daily_weather (geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh) VALUES
 ('geo_qgrd','2026-01-04',-4.0,5.0,'sunny',0.0,0.05,11.0),
 ('geo_qgrd','2026-01-11',-2.0,4.0,'haze',0.0,0.12,6.0),
 ('geo_qgrd','2026-01-18',0.0,7.0,'light_snow',1.4,0.58,13.0),
 ('geo_qgrd','2026-01-28',-1.0,8.0,'cloudy',0.0,0.20,9.0),
 ('geo_qgrd','2026-02-05',2.0,11.0,'overcast',0.0,0.25,8.0),
 ('geo_qgrd','2026-02-13',3.0,14.0,'partly_cloudy',0.0,0.11,12.0),
 ('geo_qgrd','2026-02-22',4.0,10.0,'light_rain',3.1,0.64,15.0),
 ('geo_qgrd','2026-03-03',6.0,17.0,'cloudy',0.0,0.24,10.0),
 ('geo_qgrd','2026-03-10',8.0,21.0,'sunny',0.0,0.07,14.0),
 ('geo_qgrd','2026-03-16',7.0,16.0,'drizzle',1.6,0.55,9.0),
 ('geo_qgrd','2026-03-27',10.0,23.0,'partly_cloudy',0.0,0.18,17.0),
 ('geo_qgrd','2026-04-04',11.0,19.0,'moderate_rain',8.9,0.76,20.0),
 ('geo_qgrd','2026-04-12',13.0,26.0,'sunny',0.0,0.06,13.0),
 ('geo_qgrd','2026-04-21',14.0,22.0,'light_rain',4.2,0.62,16.0),
 ('geo_qgrd','2026-04-29',16.0,29.0,'cloudy',0.0,0.21,12.0),
 ('geo_qgrd','2026-05-05',17.0,25.0,'thunder_shower',10.8,0.71,25.0),
 ('geo_qgrd','2026-05-14',18.0,30.0,'partly_cloudy',0.0,0.16,14.0),
 ('geo_qgrd','2026-05-28',19.0,24.0,'heavy_rain',24.6,0.86,28.0),
 ('geo_qgrd','2026-06-05',20.0,32.0,'sunny',0.0,0.08,11.0),
 ('geo_qgrd','2026-06-13',21.0,29.0,'light_rain',5.1,0.59,18.0);
INSERT INTO hourly_weather (geo_key,datetime,temp_c,humidity,condition,precip_mm,wind_kmh) VALUES
 ('geo_qgrd','2026-04-21T09:20:00+08:00',15.8,72.0,'light_rain',0.7,12.0),
 ('geo_qgrd','2026-04-21T14:10:00+08:00',20.4,58.0,'cloudy',0.0,15.0),
 ('geo_qgrd','2026-05-28T08:00:00+08:00',19.6,88.0,'heavy_rain',6.1,22.0),
 ('geo_qgrd','2026-05-28T16:20:00+08:00',22.2,76.0,'moderate_rain',2.5,18.0),
 ('geo_qgrd','2026-06-07T11:20:00+08:00',27.8,42.0,'sunny',0.0,10.0),
 ('geo_qgrd','2026-06-09T14:10:00+08:00',29.4,38.0,'partly_cloudy',0.0,13.0),
 ('geo_qgrd','2026-06-10T10:10:00+08:00',25.7,51.0,'cloudy',0.0,9.0),
 ('geo_qgrd','2026-06-14T18:20:00+08:00',27.1,55.0,'overcast',0.0,12.0);
INSERT INTO daily_aqi (geo_key,date,aqi,category,dominant_pollutant,observed_at) VALUES
 ('geo_qgrd','2026-01-11',128,'unhealthy','pm2.5','2026-01-11T16:10:00+08:00'),
 ('geo_qgrd','2026-02-22',56,'moderate','pm10','2026-02-22T15:20:00+08:00'),
 ('geo_qgrd','2026-03-10',77,'moderate','pm2.5','2026-03-10T17:05:00+08:00'),
 ('geo_qgrd','2026-04-04',44,'good','pm10','2026-04-04T14:15:00+08:00'),
 ('geo_qgrd','2026-04-29',89,'moderate','o3','2026-04-29T16:50:00+08:00'),
 ('geo_qgrd','2026-05-28',38,'good','pm10','2026-05-28T18:20:00+08:00'),
 ('geo_qgrd','2026-06-05',96,'moderate','o3','2026-06-05T15:35:00+08:00'),
 ('geo_qgrd','2026-06-10',68,'moderate','pm10','2026-06-10T13:30:00+08:00');
INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
 ('alr_qgrd_winter_haze','air_pollution','yellow','2026-01-11T06:00:00+08:00','2026-01-11T20:00:00+08:00','["Xi''an"]','Historical haze alert: outdoor sample observation was moved to the following day, without changing the garden project elevation or drainage judgment.',0,'2026-01-11T05:32:00+08:00','winter_haze_record'),
 ('alr_qgrd_spring_gust','gale','blue','2026-04-04T07:10:00+08:00','2026-04-04T19:30:00+08:00','["Xi''an Yanta District"]','Historical gale alert: tree-support removal was suspended and lightweight samples were secured; no actual-rain observation was conducted that day.',0,'2026-04-04T06:38:00+08:00','spring_gust_record'),
 ('alr_qgrd_may_storm','rainstorm','yellow','2026-05-28T05:40:00+08:00','2026-05-28T21:40:00+08:00','["Xi''an Yanta District"]','Historical heavy-rain alert: property management suspended pallet and nursery-stock unloading; the rainfall served only as observation context and did not directly assign construction responsibility.',0,'2026-05-28T05:16:00+08:00','may_storm_record');
INSERT INTO alert_subscriptions (sub_id,geo_key,sink,created_at,active) VALUES
 ('wsub_qgrd_site_email','geo_qgrd','email:yong.wei.reno4@gmail.com','2026-03-29T09:18:00+08:00',1),
 ('wsub_qgrd_property_hook','geo_qgrd','webhook:https://project.example/hooks/garden-weather','2026-05-23T14:12:00+08:00',1);
INSERT INTO notifications (created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
 ('2026-01-11T05:36:00+08:00','email','wsub_qgrd_site_email','alr_qgrd_winter_haze','{"action":"reschedule_color_viewing","business_effect":"samples_only"}',1),
 ('2026-04-04T06:42:00+08:00','email','wsub_qgrd_site_email','alr_qgrd_spring_gust','{"action":"secure_light_materials","inspection":"no_rain_test"}',1),
 ('2026-05-28T05:20:00+08:00','webhook','wsub_qgrd_property_hook','alr_qgrd_may_storm','{"action":"pause_pallet_and_tree_unloading","status":"acknowledged_by_property"}',1);
COMMIT;
