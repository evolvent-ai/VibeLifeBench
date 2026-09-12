-- Generated weather seed for community_household_groupbuy_30d
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_homtg', '{"jul_high": 33, "jul_low": 26}', '{"jul": 0.45}', 14.0, 78.0, '{"good": 40, "moderate": 35, "unhealthy": 25}', 'plum rain/typhoon season');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_homtg', 'Nanjing', 'CN', 31.23, 121.47, 'Asia/Shanghai', 'cp_homtg', 'city');
INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_homtg', '2026-06-26', 26, 31, 'rainstorm', 48.0, 0.92, 34),
  ('geo_homtg', '2026-06-28', 25, 30, 'rainstorm', 55.0, 0.95, 38),
  ('geo_homtg', '2026-06-30', 26, 32, 'heavy_rain', 30.0, 0.8, 26),
  ('geo_homtg', '2026-07-02', 27, 34, 'cloudy', 4.0, 0.3, 14),
  ('geo_homtg', '2026-07-04', 28, 35, 'sunny', 0.0, 0.1, 10);
INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES ('alr_homtg_storm', 'rainstorm', 'orange', '2026-06-26T00:00:00+08:00', '2026-06-30T23:59:59+08:00', '["Nanjing"]', 'Nanjingrainstormorange alert：continuous heavy rain，delivery may be delayed，consider off-peak pickup or changing the pickup point。', 1, '2026-06-25T18:00:00+08:00', 'meiyu_2026');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES ('geo_homtg', '2026-06-26', 168, 'unhealthy', 'pm2.5', '2026-06-26T08:00:00+08:00');
COMMIT;
