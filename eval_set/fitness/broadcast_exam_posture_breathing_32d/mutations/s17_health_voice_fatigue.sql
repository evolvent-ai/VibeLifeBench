BEGIN;
INSERT OR REPLACE INTO metrics (metric_id, user_id, type, value, value_text, unit, recorded_at) VALUES ('health_sleep_20261023_voice', 'lin_yu', 'sleep_minutes', 336, NULL, 'min', '2026-10-23T06:40:00+08:00');
INSERT OR REPLACE INTO workouts (workout_id, user_id, type, duration_min, calories, distance_m, started_at) VALUES ('health_voice_fatigue_20261023', 'lin_yu', 'voice_fatigue_note_level_6', 0, 0, NULL, '2026-10-23T07:00:00+08:00');
COMMIT;
