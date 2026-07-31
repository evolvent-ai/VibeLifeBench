BEGIN;
INSERT OR REPLACE INTO workouts
  (workout_id, user_id, type, duration_min, calories, distance_m, started_at)
VALUES
  ('workout_race_result_20260817_037', 'user_chen_shan',
   'dragon_boat_first_heat_completed_rpe6_shoulder_pain2_no_sharp_pain',
   18, 132, 500, '2026-08-17T09:10:00+08:00');
INSERT OR REPLACE INTO metrics
  (metric_id, user_id, type, value, value_text, unit, recorded_at)
VALUES
  ('health_race_rpe_20260817_037', 'user_chen_shan', 'score', 6,
   '友谊赛第一轮赛后 RPE 6/10。', 'score', '2026-08-17T09:20:00+08:00'),
  ('health_race_shoulder_20260817_037', 'user_chen_shan', 'score', 2,
   '赛后肩痛 2/10，无锐痛；未自行追加高强度。', 'score', '2026-08-17T09:21:00+08:00');
COMMIT;
