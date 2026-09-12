-- Generated weather seed for camping_trip_procure_30d
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_camp', '{"jul_high": 33, "jul_low": 26}', '{"jul": 0.45}', 14.0, 78.0, '{"good": 40, "moderate": 35, "unhealthy": 25}', 'plum-rain and typhoon season');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_camp', 'Kunming', 'CN', 31.23, 121.47, 'Asia/Shanghai', 'cp_camp', 'city');
INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_camp', '2026-07-02', 24, 30, 'rainstorm', 48.0, 0.92, 34),
  ('geo_camp', '2026-07-03', 23, 29, 'heavy_rain', 55.0, 0.95, 38),
  ('geo_camp', '2026-07-04', 25, 31, 'cloudy', 8.0, 0.55, 22);
INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('alr_camp_storm', 'rainstorm', 'orange', '2026-07-02T00:00:00+08:00', '2026-07-04T23:59:59+08:00', '["geo_camp"]', 'Rainstorm orange alert: heavy rainfall may delay delivery; use off-peak receipt or carrier pickup.', 1, '2026-07-01T18:00:00+08:00', 'camp_delivery_weather');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES ('geo_camp', '2026-07-02', 168, 'unhealthy', 'pm2.5', '2026-07-02T08:00:00+08:00');
COMMIT;
