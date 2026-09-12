-- Generated weather seed for floor_total_reno_v4_30d
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_qflr', '{"jul_high": 31, "jul_low": 23}', '{"jul": 0.56, "night_rain_bias": true}', 8.0, 82.0, '{"good": 42, "moderate": 41, "unhealthy": 17}', 'Chengduhumid subtropical Sichuan Basin climate；translated business textandhigh humiditytranslated business textlevelingtranslated business texttime，construction scheduleshouldtranslated business textdailyweatherandvalidalert。');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_qflr', 'Chengdu', 'CN', 31.23, 121.47, 'Asia/Shanghai', 'cp_qflr', 'city');
INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_qflr', '2026-06-26', 26, 31, 'rainstorm', 48.0, 0.92, 34),
  ('geo_qflr', '2026-06-28', 25, 30, 'rainstorm', 55.0, 0.95, 38),
  ('geo_qflr', '2026-06-30', 26, 32, 'heavy_rain', 30.0, 0.8, 26),
  ('geo_qflr', '2026-07-02', 27, 34, 'cloudy', 4.0, 0.3, 14),
  ('geo_qflr', '2026-07-04', 28, 35, 'sunny', 0.0, 0.1, 10);
INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('alr_qflr_storm', 'rainstorm', 'orange', '2026-06-26T00:00:00+08:00', '2026-06-30T23:59:59+08:00', '["Chengdu"]', 'Chengdurainstormtranslated business textalert：continuoustranslated business text，couriercancandelay，translated business textoff-peak receiptorchange pickup point。', 1, '2026-06-25T18:00:00+08:00', 'meiyu_2026');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES ('geo_qflr', '2026-06-13', 62, 'moderate', 'pm2.5', '2026-06-13T09:35:00+08:00');
COMMIT;

BEGIN;
UPDATE locations SET lat=30.5728,lng=104.0668 WHERE geo_key='geo_qflr';
UPDATE daily_weather SET date=CASE date WHEN '2026-06-26' THEN '2026-05-11' WHEN '2026-06-28' THEN '2026-05-18' WHEN '2026-06-30' THEN '2026-05-26' WHEN '2026-07-02' THEN '2026-06-03' ELSE '2026-06-09' END WHERE geo_key='geo_qflr';
UPDATE alerts SET active=0,start_dt='2026-05-18T00:00:00+08:00',end_dt='2026-05-18T23:59:59+08:00',created_at='2026-05-17T10:00:00+08:00',description='5 translated business text 18 translated business texthigh humiditytranslated business textalreadyarchive：translated business textlevelingmaterialsnot yettranslated business text，subsequentconstructionstillaccording tonewdailytranslated business textschedule。' WHERE alert_id='alr_qflr_storm';
COMMIT;

-- 2026-07-30 cross-service richness remediation: varied historical weather relevant to curing and delivery.
BEGIN;
INSERT INTO daily_weather (geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh) VALUES
 ('geo_qflr','2026-01-05',4.0,10.0,'overcast',0.0,0.22,6.0),
 ('geo_qflr','2026-01-12',3.0,9.0,'fog',0.1,0.36,4.0),
 ('geo_qflr','2026-01-20',5.0,12.0,'light_rain',2.2,0.66,8.0),
 ('geo_qflr','2026-01-29',6.0,14.0,'cloudy',0.0,0.28,7.0),
 ('geo_qflr','2026-02-06',7.0,13.0,'drizzle',1.1,0.58,5.0),
 ('geo_qflr','2026-02-14',8.0,17.0,'partly_cloudy',0.0,0.14,9.0),
 ('geo_qflr','2026-02-23',9.0,15.0,'moderate_rain',8.6,0.79,12.0),
 ('geo_qflr','2026-03-02',10.0,18.0,'overcast',0.0,0.31,6.0),
 ('geo_qflr','2026-03-11',12.0,22.0,'sunny',0.0,0.09,10.0),
 ('geo_qflr','2026-03-17',11.0,19.0,'light_rain',3.8,0.63,7.0),
 ('geo_qflr','2026-03-28',14.0,24.0,'cloudy',0.0,0.26,8.0),
 ('geo_qflr','2026-04-05',15.0,21.0,'moderate_rain',10.7,0.81,14.0),
 ('geo_qflr','2026-04-13',16.0,26.0,'partly_cloudy',0.0,0.17,9.0),
 ('geo_qflr','2026-04-22',18.0,24.0,'drizzle',1.9,0.57,6.0),
 ('geo_qflr','2026-04-30',19.0,28.0,'cloudy',0.0,0.33,8.0),
 ('geo_qflr','2026-05-06',20.0,27.0,'thunder_shower',12.4,0.72,18.0),
 ('geo_qflr','2026-05-15',21.0,29.0,'partly_cloudy',0.0,0.19,10.0),
 ('geo_qflr','2026-05-29',22.0,26.0,'heavy_rain',26.8,0.87,20.0),
 ('geo_qflr','2026-06-06',23.0,31.0,'sunny',0.0,0.11,7.0),
 ('geo_qflr','2026-06-13',24.0,29.0,'light_rain',6.3,0.65,11.0);
INSERT INTO hourly_weather (geo_key,datetime,temp_c,humidity,condition,precip_mm,wind_kmh) VALUES
 ('geo_qflr','2026-04-22T09:30:00+08:00',19.2,86.0,'drizzle',0.3,5.0),
 ('geo_qflr','2026-04-22T14:20:00+08:00',22.8,76.0,'overcast',0.0,7.0),
 ('geo_qflr','2026-05-29T08:10:00+08:00',22.6,94.0,'heavy_rain',6.9,15.0),
 ('geo_qflr','2026-05-29T16:30:00+08:00',24.1,88.0,'moderate_rain',2.8,12.0),
 ('geo_qflr','2026-06-08T11:10:00+08:00',27.0,67.0,'cloudy',0.0,6.0),
 ('geo_qflr','2026-06-10T14:00:00+08:00',28.3,72.0,'overcast',0.0,8.0),
 ('geo_qflr','2026-06-11T10:00:00+08:00',26.9,78.0,'drizzle',0.5,9.0),
 ('geo_qflr','2026-06-14T18:10:00+08:00',27.5,75.0,'cloudy',0.0,5.0);
INSERT INTO daily_aqi (geo_key,date,aqi,category,dominant_pollutant,observed_at) VALUES
 ('geo_qflr','2026-01-12',96,'moderate','pm2.5','2026-01-12T16:20:00+08:00'),
 ('geo_qflr','2026-02-23',48,'good','pm10','2026-02-23T15:10:00+08:00'),
 ('geo_qflr','2026-03-11',73,'moderate','pm2.5','2026-03-11T17:00:00+08:00'),
 ('geo_qflr','2026-04-05',39,'good','pm10','2026-04-05T14:30:00+08:00'),
 ('geo_qflr','2026-04-30',84,'moderate','o3','2026-04-30T16:35:00+08:00'),
 ('geo_qflr','2026-05-29',35,'good','pm2.5','2026-05-29T18:10:00+08:00'),
 ('geo_qflr','2026-06-06',88,'moderate','o3','2026-06-06T15:25:00+08:00'),
 ('geo_qflr','2026-06-11',57,'moderate','pm2.5','2026-06-11T13:40:00+08:00');
INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
 ('alr_qflr_winter_fog','fog','yellow','2026-01-12T05:40:00+08:00','2026-01-12T11:20:00+08:00','["Chengdu"]','historicaltranslated business text：translated business textthen，unchangedtranslated business textcircuittranslated business textorconstructionconclusion。',0,'2026-01-12T05:12:00+08:00','winter_fog_record'),
 ('alr_qflr_spring_humidity','humidity','blue','2026-04-22T06:00:00+08:00','2026-04-23T06:00:00+08:00','["Chengdutranslated business text"]','historicalhigh humiditytranslated business text：levelingmaterialstranslated business textkeeptranslated business text，translated business textandnot yettranslated business textmoisture contentacceptance。',0,'2026-04-22T05:26:00+08:00','spring_humidity_record'),
 ('alr_qflr_may_downpour','rainstorm','yellow','2026-05-29T05:50:00+08:00','2026-05-29T22:00:00+08:00','["Chengdutranslated business text"]','historicaltranslated business textrainfalltranslated business text：translated business text，translated business textstatusandmaterialsacceptancecontinueseparate。',0,'2026-05-29T05:28:00+08:00','may_downpour_record');
INSERT INTO alert_subscriptions (sub_id,geo_key,sink,created_at,active) VALUES
 ('wsub_qflr_site_email','geo_qflr','email:lai.xu.reno4@gmail.com','2026-03-30T09:26:00+08:00',1),
 ('wsub_qflr_property_hook','geo_qflr','webhook:https://project.example/hooks/floor-weather','2026-05-24T14:18:00+08:00',1);
INSERT INTO notifications (created_at,channel,sub_id,alert_id,payload_json,delivered) VALUES
 ('2026-01-12T05:16:00+08:00','email','wsub_qflr_site_email','alr_qflr_winter_fog','{"action":"delay_sample_transport","business_effect":"swatches_only"}',1),
 ('2026-04-22T05:31:00+08:00','email','wsub_qflr_site_email','alr_qflr_spring_humidity','{"action":"keep_screed_bags_raised","inspection":"storage_only"}',1),
 ('2026-05-29T05:32:00+08:00','webhook','wsub_qflr_property_hook','alr_qflr_may_downpour','{"action":"pause_pallet_unloading","status":"acknowledged_by_property"}',1);
COMMIT;
