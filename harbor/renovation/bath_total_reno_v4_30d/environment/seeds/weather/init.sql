-- Weather history visible at the task's 2026-06-15 Stage 0.
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_qbath', '{"jun_high": 29, "jun_low": 22}', '{"may": 0.34, "jun": 0.48}', 13.0, 74.0, '{"good": 48, "moderate": 39, "unhealthy": 13}', 'renovation project detail，renovation project detail');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_qbath', 'renovation project detail', 'CN', 31.2304, 121.4737, 'Asia/Shanghai', 'cp_qbath', 'district');

INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_qbath', '2026-05-18', 19, 27, 'sunny', 0.0, 0.05, 9),
  ('geo_qbath', '2026-05-21', 20, 26, 'cloudy', 0.6, 0.18, 12),
  ('geo_qbath', '2026-05-24', 18, 23, 'light_rain', 7.4, 0.62, 16),
  ('geo_qbath', '2026-05-29', 21, 28, 'partly_cloudy', 0.2, 0.12, 10),
  ('geo_qbath', '2026-06-01', 22, 27, 'overcast', 1.3, 0.28, 13),
  ('geo_qbath', '2026-06-03', 21, 25, 'drizzle', 4.6, 0.58, 11),
  ('geo_qbath', '2026-06-05', 22, 29, 'sunny', 0.0, 0.08, 8),
  ('geo_qbath', '2026-06-08', 23, 28, 'shower', 9.2, 0.66, 17),
  ('geo_qbath', '2026-06-11', 24, 31, 'partly_cloudy', 0.0, 0.15, 12),
  ('geo_qbath', '2026-06-13', 23, 27, 'rain', 13.8, 0.72, 19);

INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES
  ('alr_qbath_storm', 'wind', 'blue', '2026-05-16T06:00:00+08:00', '2026-05-17T12:00:00+08:00', '["renovation project detail"]', 'renovation project detail：renovation project detail，17 renovation project detail。', 0, '2026-05-16T05:35:00+08:00', 'SHMET-20260516-WD7K');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES
  ('geo_qbath', '2026-05-29', 68, 'moderate', 'o3', '2026-05-29T08:00:00+08:00');

INSERT OR IGNORE INTO daily_weather VALUES
  ('geo_qbath', '2026-05-07', 17, 25, 'sunny', 0.0, 0.04, 7),
  ('geo_qbath', '2026-05-12', 18, 24, 'cloudy', 0.0, 0.16, 10),
  ('geo_qbath', '2026-05-16', 19, 24, 'breezy', 0.8, 0.22, 25),
  ('geo_qbath', '2026-05-26', 20, 25, 'overcast', 2.1, 0.39, 14),
  ('geo_qbath', '2026-06-14', 24, 30, 'cloudy', 0.4, 0.24, 11);
INSERT OR IGNORE INTO alerts VALUES
  ('alr_qbath_humidity', 'humidity', 'yellow', '2026-06-08T00:00:00+08:00', '2026-06-09T23:59:59+08:00', '["renovation project detail"]', 'renovation project detail 85%，9 renovation project detail。', 0, '2026-06-07T18:20:00+08:00', 'SHMET-20260608-HM4Q');
COMMIT;

-- Keep the resolver city aligned with the English task contract.
BEGIN;
UPDATE locations SET city='Pudong New Area' WHERE geo_key='geo_qbath';
COMMIT;
