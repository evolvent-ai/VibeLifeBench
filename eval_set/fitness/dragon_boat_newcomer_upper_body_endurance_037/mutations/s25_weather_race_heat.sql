BEGIN;
UPDATE alerts SET active = 0 WHERE alert_id = 'alert_shanghai_thunder_0718';
INSERT OR REPLACE INTO daily_weather
  (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh)
VALUES
  ('geo_shanghai_river', '2026-08-16', 29, 36, 'heat_thunderstorm_watch', 8.0, 0.78, 28);
INSERT OR REPLACE INTO hourly_weather
  (geo_key, datetime, temp_c, humidity, condition, precip_mm, wind_kmh)
VALUES
  ('geo_shanghai_river', '2026-08-16T08:00:00+08:00', 32, 76, 'heat_lightning_watch', 1.0, 24),
  ('geo_shanghai_river', '2026-08-16T09:00:00+08:00', 34, 73, 'heat_lightning_watch', 2.0, 27),
  ('geo_shanghai_river', '2026-08-16T10:00:00+08:00', 35, 71, 'heat_lightning_watch', 3.0, 30),
  ('geo_shanghai_river', '2026-08-16T11:00:00+08:00', 35, 72, 'heat_lightning_watch', 3.0, 30),
  ('geo_shanghai_river', '2026-08-16T12:00:00+08:00', 35, 74, 'heat_lightning_watch', 3.5, 31),
  ('geo_shanghai_river', '2026-08-16T13:00:00+08:00', 34, 77, 'heat_lightning_watch', 4.0, 31),
  ('geo_shanghai_river', '2026-08-16T14:00:00+08:00', 33, 79, 'heat_lightning_watch', 4.5, 30);
INSERT OR REPLACE INTO alerts
  (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event)
VALUES
  ('alert_shanghai_heat_lightning_0816', 'heat_thunderstorm', 'yellow',
   '2026-08-16T08:00:00+08:00', '2026-08-16T14:00:00+08:00',
   '["geo_shanghai_river"]',
   '赛前高温叠加雷阵雨观察，需减量并列出取消条件。',
   1, '2026-08-15T07:58:00+08:00', 's25_race_weather_update');
COMMIT;
