BEGIN;
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_sleep_20261013', 'lin_yu', 'sleep_minutes', 312, NULL, 'min', '2026-10-13T06:40:00+08:00');
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_sleep_20261014', 'lin_yu', 'sleep_minutes', 324, NULL, 'min', '2026-10-14T06:40:00+08:00');
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_sleep_20261015', 'lin_yu', 'sleep_minutes', 300, NULL, 'min', '2026-10-15T06:40:00+08:00');
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_hr_20261015_fatigue', 'lin_yu', 'heart_rate', 82, NULL, 'bpm', '2026-10-15T07:00:00+08:00');
INSERT OR REPLACE INTO workouts (workout_id, user_id, type, duration_min, calories, distance_m, started_at) VALUES ('health_cycle_fatigue_20261015', 'lin_yu', 'premenstrual_fatigue_note', 0, 0, NULL, '2026-10-15T07:05:00+08:00');
COMMIT;
