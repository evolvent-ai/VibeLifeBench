PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id,seasonal_temp_means_json,precip_freq_json,wind_baseline_kmh,humidity_baseline_pct,aqi_baseline_json,notes) VALUES
('jp_kanto_july','{"7":27.0}','{"7":0.34}',14,72,'{"7":42}','July planning baseline for Tokyo-area travel; live warnings and transport status remain authoritative.');
INSERT INTO locations (geo_key,city,country,lat,lng,timezone,climate_profile_id,kind) VALUES
('geo_tokyo','Tokyo','Japan',35.6762,139.6503,'Asia/Tokyo','jp_kanto_july','city'),
('geo_narita','Narita','Japan',35.7720,140.3929,'Asia/Tokyo','jp_kanto_july','airport');
INSERT INTO daily_weather (geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh) VALUES
('geo_tokyo','2026-07-15',24,31,'humid partly cloudy',1.0,0.25,12),
('geo_narita','2026-07-15',23,30,'humid partly cloudy',1.5,0.30,16),
('geo_tokyo','2026-07-16',24,30,'scattered showers',5.0,0.55,15),
('geo_tokyo','2026-07-17',24,30,'showers easing',3.0,0.45,14),
('geo_tokyo','2026-07-18',25,31,'humid with afternoon showers',6.0,0.55,18),
('geo_narita','2026-07-18',24,30,'cloudy with intermittent rain',8.0,0.60,22),
('geo_tokyo','2026-07-19',24,28,'showers and gusty intervals',10.0,0.65,24),
('geo_narita','2026-07-19',23,27,'periods of rain',12.0,0.70,27),
('geo_tokyo','2026-07-20',24,29,'warm with scattered showers',5.0,0.45,19),
('geo_tokyo','2026-07-21',24,31,'partly cloudy',2.0,0.25,17),
('geo_narita','2026-07-21',23,30,'partly cloudy',2.0,0.25,20);
INSERT INTO daily_weather (geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh) VALUES
('geo_tokyo','2026-06-29',22,28,'cloudy with a brief shower',2.4,0.40,13),
('geo_narita','2026-06-30',21,27,'morning rain then overcast',6.8,0.65,18);
INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
('wx_kanto_7f3c','weather_monitoring','information','2026-07-01T00:00:00+09:00','2026-07-01T23:59:00+09:00','["geo_tokyo","geo_narita"]','No active severe-weather warning is attached to this transport monitoring record. Check live authority and airline status before travel.',0,'2026-07-01T00:00:00+09:00',NULL);
INSERT INTO _counters (name,value) VALUES ('subscription_seq',9000),('notification_seq',9000);
INSERT INTO _sim_clock (id,sim_now) VALUES (1,'2026-07-01T09:00:00+09:00');
COMMIT;
