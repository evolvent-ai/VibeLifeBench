BEGIN;
INSERT OR REPLACE INTO daily_weather
  (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh)
VALUES
  ('beijing_broadcast_campus', '2026-10-19', 6, 15, 'windy_cooling', 0.0, 0.10, 26);
INSERT OR REPLACE INTO hourly_weather
  (geo_key, datetime, temp_c, humidity, condition, precip_mm, wind_kmh)
VALUES
  ('beijing_broadcast_campus', '2026-10-19T18:00:00+08:00', 9, 58, 'windy_cooling', 0.0, 27);
INSERT OR REPLACE INTO alerts
  (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event)
VALUES
  ('weather_cold_wind_watch_20261019', 'cold_wind_watch', 'minor',
   '2026-10-19T16:00:00+08:00', '2026-10-19T21:00:00+08:00',
   '["beijing_broadcast_campus"]',
   '10 月 19 日傍晚北风增强，操场无遮风，户外训练前应复核风力与体感温度。',
   1, '2026-10-18T16:58:00+08:00', 'campus_forecast_update');
COMMIT;
