BEGIN;
INSERT OR REPLACE INTO daily_weather
  (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh)
VALUES
  ('beijing_broadcast_campus', '2026-11-05', 5, 11, 'cold_light_rain', 3.2, 0.65, 18);
INSERT OR REPLACE INTO hourly_weather
  (geo_key, datetime, temp_c, humidity, condition, precip_mm, wind_kmh)
VALUES
  ('beijing_broadcast_campus', '2026-11-05T08:00:00+08:00', 7, 82, 'light_rain', 0.8, 17),
  ('beijing_broadcast_campus', '2026-11-05T09:00:00+08:00', 8, 80, 'light_rain', 0.6, 16);
INSERT OR REPLACE INTO alerts
  (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event)
VALUES
  ('weather_exam_cold_rain_20261105', 'exam_day_cold_rain_outlook', 'minor',
   '2026-11-05T06:00:00+08:00', '2026-11-05T12:00:00+08:00',
   '["beijing_broadcast_campus"]',
   '11 月 5 日模拟面试日上午偏冷并有小雨，建议准备保暖外层并安排室内热身。',
   1, '2026-11-01T07:58:00+08:00', 'exam_day_forecast_update');
COMMIT;
