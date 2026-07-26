BEGIN;
INSERT OR REPLACE INTO hourly_weather (geo_key, datetime, temp_c, humidity, condition, precip_mm, wind_kmh) VALUES ('beijing_broadcast_campus', '2026-10-19T18:00:00+08:00', 6, 63, 'cold_windy', 0.0, 32);
INSERT OR REPLACE INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('weather_cold_front_20261019', 'cold_wind', 'moderate', '2026-10-19T12:00:00+08:00', '2026-10-19T22:00:00+08:00', '["beijing_broadcast_campus"]', '傍晚体感温度约 6℃，阵风 5 级，户外训练需改室内或延长热身。', 1, '2026-10-19T06:20:00+08:00', 'cold_front_update');
COMMIT;
