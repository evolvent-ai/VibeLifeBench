-- Generated weather seed for bed_total_reno_v4_30d
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_qbed', '{"jul_high": 32, "jul_low": 25, "annual_mean": 15.7}', '{"jul": 0.48, "annual_mm": 1054}', 12.0, 79.0, '{"good": 46, "moderate": 39, "unhealthy": 15}', 'renovation note；renovation note high humidity 。renovation note， current renovation note by  daily  weather  and  has  release  alert  authoritative 。');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_qbed', ' Suzhou ', 'CN', 31.23, 121.47, 'Asia/Shanghai', 'cp_qbed', 'city');
INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_qbed', '2026-06-26', 26, 31, 'rainstorm', 48.0, 0.92, 34),
  ('geo_qbed', '2026-06-28', 25, 30, 'rainstorm', 55.0, 0.95, 38),
  ('geo_qbed', '2026-06-30', 26, 32, 'heavy_rain', 30.0, 0.8, 26),
  ('geo_qbed', '2026-07-02', 27, 34, 'cloudy', 4.0, 0.3, 14),
  ('geo_qbed', '2026-07-04', 28, 35, 'sunny', 0.0, 0.1, 10);
INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('alr_qbed_storm', 'rainstorm', 'orange', '2026-06-26T00:00:00+08:00', '2026-06-30T23:59:59+08:00', '[" Suzhou "]', ' Suzhou renovation note alert ：renovation note heavy precipitation ， delivery renovation note delay ，renovation note off-peak delivery  or renovation note pickup point 。', 1, '2026-06-25T18:00:00+08:00', 'meiyu_2026');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES ('geo_qbed', '2026-06-14', 74, 'moderate', 'o3', '2026-06-14T15:20:00+08:00');
COMMIT;

BEGIN;
UPDATE locations SET lat=31.2989,lng=120.5853 WHERE geo_key='geo_qbed';
UPDATE daily_weather SET date=CASE date WHEN '2026-06-26' THEN '2026-05-12' WHEN '2026-06-28' THEN '2026-05-18' WHEN '2026-06-30' THEN '2026-05-25' WHEN '2026-07-02' THEN '2026-06-02' ELSE '2026-06-08' END WHERE geo_key='geo_qbed';
UPDATE alerts SET active=0,start_dt='2026-05-18T00:00:00+08:00',end_dt='2026-05-18T23:59:59+08:00',created_at='2026-05-17T10:00:00+08:00',description=' historical renovation note rainfall  record ：renovation note reconcile  wood finish  construction renovation note， does not mean  not renovation note weather 。' WHERE alert_id='alr_qbed_storm';
COMMIT;

-- 2026-07-30 cross-service richness remediation: varied historical weather and indoor-work context.
BEGIN;
INSERT INTO daily_weather (geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh) VALUES
 ('geo_qbed','2026-01-06',1.0,8.0,'overcast',0.0,0.18,13.0),
 ('geo_qbed','2026-01-10',-1.0,7.0,'sunny',0.0,0.06,9.0),
 ('geo_qbed','2026-01-19',3.0,10.0,'light_rain',2.6,0.64,16.0),
 ('geo_qbed','2026-01-23',0.0,6.0,'cloudy',0.0,0.24,11.0),
 ('geo_qbed','2026-02-02',4.0,12.0,'mist',0.4,0.38,7.0),
 ('geo_qbed','2026-02-11',6.0,15.0,'partly_cloudy',0.0,0.12,10.0),
 ('geo_qbed','2026-02-17',7.0,13.0,'moderate_rain',11.8,0.82,19.0),
 ('geo_qbed','2026-03-01',8.0,17.0,'cloudy',0.0,0.29,12.0),
 ('geo_qbed','2026-03-09',10.0,20.0,'sunny',0.0,0.08,15.0),
 ('geo_qbed','2026-03-14',9.0,16.0,'drizzle',1.3,0.56,8.0),
 ('geo_qbed','2026-03-25',12.0,22.0,'partly_cloudy',0.0,0.20,14.0),
 ('geo_qbed','2026-04-03',13.0,19.0,'moderate_rain',9.4,0.76,21.0),
 ('geo_qbed','2026-04-11',15.0,25.0,'sunny',0.0,0.07,12.0),
 ('geo_qbed','2026-04-18',16.0,23.0,'light_rain',4.7,0.68,17.0),
 ('geo_qbed','2026-04-28',18.0,28.0,'cloudy',0.0,0.25,11.0),
 ('geo_qbed','2026-05-04',19.0,26.0,'thunder_shower',13.6,0.74,24.0),
 ('geo_qbed','2026-05-14',20.0,29.0,'partly_cloudy',0.2,0.31,13.0),
 ('geo_qbed','2026-05-30',22.0,27.0,'heavy_rain',28.5,0.88,30.0),
 ('geo_qbed','2026-06-05',23.0,31.0,'sunny',0.0,0.10,9.0),
 ('geo_qbed','2026-06-12',24.0,30.0,'light_rain',5.9,0.61,18.0);
INSERT INTO hourly_weather (geo_key,datetime,temp_c,humidity,condition,precip_mm,wind_kmh) VALUES
 ('geo_qbed','2026-04-18T09:00:00+08:00',18.2,82.0,'light_rain',0.8,11.0),
 ('geo_qbed','2026-04-18T14:00:00+08:00',21.4,71.0,'cloudy',0.0,15.0),
 ('geo_qbed','2026-05-30T08:30:00+08:00',23.1,91.0,'heavy_rain',7.6,24.0),
 ('geo_qbed','2026-05-30T16:10:00+08:00',25.0,84.0,'moderate_rain',3.2,19.0),
 ('geo_qbed','2026-06-09T11:20:00+08:00',27.3,63.0,'partly_cloudy',0.0,8.0),
 ('geo_qbed','2026-06-11T14:10:00+08:00',29.1,68.0,'cloudy',0.0,12.0),
 ('geo_qbed','2026-06-12T10:10:00+08:00',26.6,79.0,'drizzle',0.4,14.0),
 ('geo_qbed','2026-06-14T18:30:00+08:00',28.4,72.0,'overcast',0.0,10.0);
INSERT INTO daily_aqi (geo_key,date,aqi,category,dominant_pollutant,observed_at) VALUES
 ('geo_qbed','2026-01-10',58,'moderate','pm2.5','2026-01-10T16:00:00+08:00'),
 ('geo_qbed','2026-02-17',42,'good','pm10','2026-02-17T15:30:00+08:00'),
 ('geo_qbed','2026-03-09',69,'moderate','o3','2026-03-09T17:10:00+08:00'),
 ('geo_qbed','2026-04-03',37,'good','pm2.5','2026-04-03T14:20:00+08:00'),
 ('geo_qbed','2026-04-28',81,'moderate','o3','2026-04-28T16:45:00+08:00'),
 ('geo_qbed','2026-05-30',33,'good','pm10','2026-05-30T18:00:00+08:00'),
 ('geo_qbed','2026-06-05',92,'moderate','o3','2026-06-05T15:40:00+08:00'),
 ('geo_qbed','2026-06-12',51,'moderate','pm2.5','2026-06-12T13:25:00+08:00');
INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
 ('alr_qbed_winter_fog','fog','yellow','2026-02-02T05:30:00+08:00','2026-02-02T11:00:00+08:00','[" Suzhou "]',' historical renovation note： on renovation note，renovation note after renovation note in renovation note；renovation note record renovation note construction renovation note。',0,'2026-02-02T05:05:00+08:00','winter_fog_record'),
 ('alr_qbed_spring_gust','gale','blue','2026-04-03T07:00:00+08:00','2026-04-03T20:00:00+08:00','[" Suzhou "]',' historical renovation note：renovation note，renovation note record ， not renovation note contract process 。',0,'2026-04-03T06:20:00+08:00','spring_gust_record'),
 ('alr_qbed_may_downpour','rainstorm','yellow','2026-05-30T06:00:00+08:00','2026-05-30T21:30:00+08:00','[" Suzhou  Industrial Park "]',' historical renovation note rainfall renovation note：renovation note， has renovation note materials  not renovation note arrival 。',0,'2026-05-30T05:42:00+08:00','may_downpour_record');
INSERT INTO alert_subscriptions (sub_id,geo_key,sink,created_at,active) VALUES
 ('wsub_qbed_site_email','geo_qbed','email:du.rong.reno4@gmail.com','2026-04-01T09:12:00+08:00',1),
 ('wsub_qbed_property_hook','geo_qbed','webhook:https://project.example/hooks/bed-weather','2026-05-26T14:05:00+08:00',1);
INSERT INTO notifications (created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
 ('2026-02-02T05:08:00+08:00','email','wsub_qbed_site_email','alr_qbed_winter_fog','{"action":"delay_sample_pickup","business_effect":"color_swatches_only"}',1),
 ('2026-04-03T06:24:00+08:00','email','wsub_qbed_site_email','alr_qbed_spring_gust','{"action":"close_north_window","inspection":"indoor_precheck"}',1),
 ('2026-05-30T05:45:00+08:00','webhook','wsub_qbed_property_hook','alr_qbed_may_downpour','{"action":"pause_large_delivery","status":"acknowledged_by_property"}',1);
COMMIT;
