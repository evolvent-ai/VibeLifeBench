BEGIN;
INSERT OR REPLACE INTO metrics
  (metric_id, user_id, type, value, value_text, unit, recorded_at)
VALUES
  ('health_pre_exam_sleep_20261102', 'lin_yu', 'sleep_minutes', 414, '近三天恢复记录第 1 天', 'min', '2026-11-02T06:45:00+08:00'),
  ('health_pre_exam_sleep_20261103', 'lin_yu', 'sleep_minutes', 426, '近三天恢复记录第 2 天', 'min', '2026-11-03T06:45:00+08:00'),
  ('health_pre_exam_sleep_20261104', 'lin_yu', 'sleep_minutes', 420, '近三天恢复记录第 3 天', 'min', '2026-11-04T06:45:00+08:00'),
  ('health_pre_exam_voice_score_20261104', 'lin_yu', 'score', 2, '嗓音疲劳自评 2/10，轻度；肩颈紧张自评 2/10，状态较前期稳定。', 'score', '2026-11-04T18:55:00+08:00');
INSERT OR REPLACE INTO workouts
  (workout_id, user_id, type, duration_min, calories, distance_m, started_at)
VALUES
  ('health_pre_exam_recovery_20261104', 'lin_yu', 'pre_exam_recovery_snapshot_voice_mild_shoulder_stable', 0, 0, NULL, '2026-11-04T18:56:00+08:00');
COMMIT;
