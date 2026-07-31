BEGIN;
INSERT OR REPLACE INTO workouts
  (workout_id, user_id, type, duration_min, calories, distance_m, started_at)
VALUES
  ('workout_week1_complete_20260715_037', 'user_chen_shan',
   'dragon_land_foundation_core_stability_rpe5_shoulder_discomfort2of10',
   38, 146, NULL, '2026-07-15T20:10:00+08:00');
INSERT OR REPLACE INTO metrics
  (metric_id, user_id, type, value, value_text, unit, recorded_at)
VALUES
  ('health_week1_rpe_20260715_037', 'user_chen_shan', 'score', 5,
   '首周陆上基础训练完成；RPE 5/10，肩部不适 2/10，无锐痛。', 'score',
   '2026-07-15T20:50:00+08:00');
COMMIT;
