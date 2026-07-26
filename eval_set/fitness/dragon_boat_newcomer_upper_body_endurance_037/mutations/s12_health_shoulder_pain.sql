BEGIN;
INSERT OR REPLACE INTO metrics
  (metric_id, user_id, type, value, value_text, unit, recorded_at)
VALUES
  ('health_shoulder_pain_20260720_037', 'user_chen_shan', 'heart_rate', 82,
   '肩痛自评 4/10；前次训练 RPE 7/10，今日应结合睡眠与日历复核负荷。', 'bpm',
   '2026-07-20T07:30:00+08:00'),
  ('health_sleep_short_20260720_037', 'user_chen_shan', 'sleep_minutes', 305,
   '昨夜睡眠 5.1 小时；肩痛自评 4/10。', 'min',
   '2026-07-20T07:20:00+08:00');
INSERT OR REPLACE INTO workouts
  (workout_id, user_id, type, duration_min, calories, distance_m, started_at)
VALUES
  ('workout_pain_alert_20260720_037', 'user_chen_shan',
   'shoulder_pain_report_4_of_10_after_dragon_training', 1, 0, NULL,
   '2026-07-20T07:35:00+08:00');
COMMIT;
