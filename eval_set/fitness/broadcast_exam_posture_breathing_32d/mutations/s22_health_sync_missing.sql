BEGIN;
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_sleep_20261030_available', 'lin_yu', 'sleep_minutes', 402, NULL, 'min', '2026-10-30T06:40:00+08:00');
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_sleep_20261031_available', 'lin_yu', 'sleep_minutes', 395, NULL, 'min', '2026-10-31T06:40:00+08:00');
INSERT OR REPLACE INTO workouts (workout_id, user_id, type, duration_min, calories, distance_m, started_at) VALUES ('health_sync_gap_20261030_31', 'lin_yu', 'wearable_sync_partial_steps_rpe_missing', 0, 0, NULL, '2026-10-31T07:30:00+08:00');
COMMIT;
