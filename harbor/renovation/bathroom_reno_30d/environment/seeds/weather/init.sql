-- Weather history visible at the task's 2026-06-15 Stage 0.
BEGIN TRANSACTION;
INSERT INTO climate_profiles (profile_id, seasonal_temp_means_json, precip_freq_json, wind_baseline_kmh, humidity_baseline_pct, aqi_baseline_json, notes) VALUES ('cp_r2bth', '{"jun_high":30,"jun_low":23}', '{"may":0.31,"jun":0.46}', 12.0, 76.0, '{"good":52,"moderate":36,"unhealthy":12}', 'Early summer in Xuhui, with alternating afternoon convection and rainy weather');
INSERT INTO locations (geo_key, city, country, lat, lng, timezone, climate_profile_id, kind) VALUES ('geo_r2bth', 'Xuhui District, Shanghai', 'CN', 31.1883, 121.4365, 'Asia/Shanghai', 'cp_r2bth', 'district');

INSERT INTO daily_weather (geo_key, date, tmin, tmax, condition, precip_mm, precip_prob, wind_kmh) VALUES
  ('geo_r2bth', '2026-05-17', 18, 25, 'cloudy', 0.0, 0.14, 9),
  ('geo_r2bth', '2026-05-20', 20, 28, 'sunny', 0.0, 0.06, 8),
  ('geo_r2bth', '2026-05-23', 19, 24, 'shower', 6.8, 0.59, 15),
  ('geo_r2bth', '2026-05-28', 21, 26, 'overcast', 1.6, 0.32, 11),
  ('geo_r2bth', '2026-05-31', 22, 29, 'sunny', 0.0, 0.09, 7),
  ('geo_r2bth', '2026-06-02', 22, 26, 'drizzle', 3.9, 0.51, 10),
  ('geo_r2bth', '2026-06-04', 23, 29, 'cloudy', 0.3, 0.19, 12),
  ('geo_r2bth', '2026-06-07', 22, 27, 'thunderstorm', 11.5, 0.69, 21),
  ('geo_r2bth', '2026-06-10', 24, 31, 'partly_cloudy', 0.0, 0.13, 9),
  ('geo_r2bth', '2026-06-13', 23, 28, 'rain', 10.7, 0.67, 17);

INSERT INTO alerts (alert_id, kind, severity, start_dt, end_dt, areas_json, description, active, created_at, source_event) VALUES
  ('alr_r2bth_storm', 'thunderstorm', 'blue', '2026-05-22T14:00:00+08:00', '2026-05-23T02:00:00+08:00', '["Xuhui District, Shanghai"]', 'Historical record of the Xuhui blue lightning alert: Brief showers and level-six gusts occurred at night; the alert was lifted in the early hours of the 23rd.', 0, '2026-05-22T13:42:00+08:00', 'SHMET-20260522-TS8P');
INSERT INTO daily_aqi (geo_key, date, aqi, category, dominant_pollutant, observed_at) VALUES
  ('geo_r2bth', '2026-06-10', 54, 'moderate', 'pm10', '2026-06-10T08:00:00+08:00');

INSERT OR IGNORE INTO daily_weather VALUES
  ('geo_r2bth', '2026-05-08', 18, 26, 'haze', 0.0, 0.07, 6),
  ('geo_r2bth', '2026-05-13', 17, 23, 'windy', 0.4, 0.21, 23),
  ('geo_r2bth', '2026-05-18', 19, 24, 'light_rain', 5.2, 0.55, 14),
  ('geo_r2bth', '2026-05-26', 21, 29, 'sunny', 0.0, 0.05, 8),
  ('geo_r2bth', '2026-06-14', 24, 29, 'overcast', 1.1, 0.31, 13);
INSERT OR IGNORE INTO alerts VALUES
  ('alr_r2bth_humidity', 'humidity', 'yellow', '2026-06-06T00:00:00+08:00', '2026-06-07T23:59:59+08:00', '["Xuhui District, Shanghai"]', 'Historical weather records: The two-day average relative humidity in Xuhui was between 84%—88%; it returned to the normal seasonal range on the morning of the 8th.', 0, '2026-06-05T17:55:00+08:00', 'SHMET-20260606-RH3N');
COMMIT;
