BEGIN;
INSERT OR REPLACE INTO daily_weather
  (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh)
VALUES
  ('geo_shanghai_river', '2026-07-18', 26, 33, 'thunderstorm_lightning_gust', 18.0, 0.92, 34);
INSERT OR REPLACE INTO hourly_weather
  (geo_key, datetime, temp_c, humidity, condition, precip_mm, wind_kmh)
VALUES
  ('geo_shanghai_river', '2026-07-18T08:00:00+08:00', 29, 82, 'lightning_risk_gust_front', 6.5, 36),
  ('geo_shanghai_river', '2026-07-18T09:00:00+08:00', 29, 84, 'thunderstorm_lightning_gust', 7.0, 38),
  ('geo_shanghai_river', '2026-07-18T10:00:00+08:00', 30, 81, 'thunderstorm_lightning_gust', 5.5, 35),
  ('geo_shanghai_river', '2026-07-18T11:00:00+08:00', 30, 79, 'lightning_risk_gust_front', 4.0, 34),
  ('geo_shanghai_river', '2026-07-18T12:00:00+08:00', 31, 77, 'thunderstorm_lightning_gust', 3.2, 33),
  ('geo_shanghai_river', '2026-07-18T13:00:00+08:00', 31, 75, 'thunderstorm_lightning_gust', 2.5, 32);
INSERT OR REPLACE INTO alerts
  (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event)
VALUES
  ('alert_shanghai_thunder_0718', 'thunderstorm', 'orange',
   '2026-07-18T08:00:00+08:00', '2026-07-18T13:00:00+08:00',
   '["geo_shanghai_river"]',
   '苏州河码头雷电和阵风风险，水上训练不适合，新人应改室内或陆上。',
   1, '2026-07-18T07:25:00+08:00', 's09_weather_update');
COMMIT;
