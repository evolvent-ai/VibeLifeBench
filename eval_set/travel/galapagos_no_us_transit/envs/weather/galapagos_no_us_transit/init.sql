-- Reviewed Stage 0 weather corpus: 90 location, forecast, AQI, watch and subscription records.
INSERT INTO climate_profiles(profile_id,seasonal_temp_means_json,precip_freq_json,wind_baseline_kmh,humidity_baseline_pct,aqi_baseline_json,notes)
VALUES ('ecuador_august','{"coast":26,"highlands":15,"islands":23}','{"coast":0.18,"highlands":0.30,"islands":0.12}',19,72,'{"coast":42,"highlands":38,"islands":24}','August baselines differ materially between mainland coast, highlands and islands.');
INSERT INTO locations(geo_key,city,country,lat,lng,timezone,climate_profile_id,kind) VALUES
 ('gye','Guayaquil','EC',-2.157,-79.884,'America/Guayaquil','ecuador_august','airport'),
 ('uio','Quito','EC',-0.129,-78.357,'America/Guayaquil','ecuador_august','airport'),
 ('gps','Baltra','EC',-0.454,-90.266,'Pacific/Galapagos','ecuador_august','airport'),
 ('puerto_ayora','Puerto Ayora','EC',-0.745,-90.314,'Pacific/Galapagos','ecuador_august','city'),
 ('baltra_channel','Itabaca Channel','EC',-0.485,-90.255,'Pacific/Galapagos','ecuador_august','marine');

WITH RECURSIVE days(n) AS (SELECT 0 UNION ALL SELECT n+1 FROM days WHERE n<8),
locs(geo_key,offset) AS (VALUES('gye',0),('uio',1),('gps',2),('puerto_ayora',3),('baltra_channel',4))
INSERT INTO daily_weather(geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh)
SELECT geo_key,strftime('%Y-%m-%d','2026-08-14','+'||n||' days'),
       CASE offset WHEN 0 THEN 22+n%2 WHEN 1 THEN 9+n%3 ELSE 19+n%2 END,
       CASE offset WHEN 0 THEN 29+n%3 WHEN 1 THEN 19+n%2 ELSE 26+n%3 END,
       CASE WHEN geo_key='uio' AND n IN (1,2) THEN 'high_cloud' WHEN geo_key IN ('gps','puerto_ayora','baltra_channel') AND n IN (5,6) THEN 'windy' WHEN n%4=0 THEN 'light_cloud' WHEN n%4=1 THEN 'sunny' WHEN n%4=2 THEN 'partly_cloudy' ELSE 'brief_showers' END,
       CASE WHEN n%4=3 THEN 1.8 ELSE 0.0 END,CASE WHEN n%4=3 THEN 0.42 ELSE 0.12+(offset*0.02) END,15+offset*3+n
FROM days CROSS JOIN locs;

WITH RECURSIVE days(n) AS (SELECT 0 UNION ALL SELECT n+1 FROM days WHERE n<6),
locs(geo_key,offset) AS (VALUES('gye',0),('uio',1),('gps',2),('puerto_ayora',3),('baltra_channel',4))
INSERT INTO daily_aqi(geo_key,date,aqi,category,dominant_pollutant,observed_at)
SELECT geo_key,strftime('%Y-%m-%d','2026-08-14','+'||n||' days'),28+offset*5+n,
       CASE WHEN geo_key='uio' AND n=2 THEN 'moderate' ELSE 'good' END,
       CASE offset WHEN 0 THEN 'pm2.5' WHEN 1 THEN 'volcanic_particulates' WHEN 2 THEN 'sea_salt' WHEN 3 THEN 'sea_salt' ELSE 'marine_aerosol' END,
       strftime('%Y-%m-%dT12:00:00Z','2026-08-14','+'||n||' days')
FROM days CROSS JOIN locs;

INSERT INTO alerts(alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
 ('alert_galapagos_sea_moderate','marine','watch','2026-08-18T06:00:00-06:00','2026-08-22T18:00:00-06:00','["gps","puerto_ayora","baltra_channel"]','Moderate sea state expected; short channel operations continue while exposed small-craft trips require review.',1,'2026-07-22T12:00:00Z','stage0_forecast_watch'),
 ('alert_guayaquil_heat_history','heat','advisory','2026-07-10T11:00:00-05:00','2026-07-10T17:00:00-05:00','["gye"]','Historical afternoon heat advisory retained for comparison; no longer active.',0,'2026-07-10T10:00:00Z','historical_weather_record');
INSERT INTO alert_subscriptions(sub_id,geo_key,sink,created_at,active) VALUES
 ('sub_weather_mainland','gye','workspace','2026-07-24T09:30:00+08:00',1),
 ('sub_weather_islands','gps','workspace','2026-07-24T09:31:00+08:00',1);
