-- Stage-0 weather seed: stable location and simulated kickoff only.
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_iscac', '{"jul_high": 33, "jul_low": 26}', '{"jul": 0.45}', 14.0, 78.0, '{"good": 40, "moderate": 35, "unhealthy": 25}', '深圳夏季高温多雨');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_iscac', '深圳市', 'CN', 22.54, 114.06, 'Asia/Shanghai', 'cp_iscac', 'city');
INSERT INTO _sim_clock (id, sim_now) VALUES (1, '2026-06-15T09:00:00+08:00');
COMMIT;
