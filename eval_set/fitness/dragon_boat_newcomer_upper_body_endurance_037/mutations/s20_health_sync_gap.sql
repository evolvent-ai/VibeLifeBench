BEGIN;
INSERT OR REPLACE INTO metrics
  (metric_id, user_id, type, value, value_text, unit, recorded_at)
VALUES
  ('health_sync_gap_0730_037', 'user_chen_shan', 'steps', 0,
   '设备仅完成部分同步；7 月 30 日步数和训练 RPE 未上传，状态待设备或本人补录。', 'count',
   '2026-07-30T23:00:00+08:00'),
  ('health_sync_gap_0731_037', 'user_chen_shan', 'heart_rate', 0,
   '设备仅完成部分同步；7 月 31 日心率和训练 RPE 未上传，状态待设备或本人补录。', 'bpm',
   '2026-07-31T23:00:00+08:00');
COMMIT;
