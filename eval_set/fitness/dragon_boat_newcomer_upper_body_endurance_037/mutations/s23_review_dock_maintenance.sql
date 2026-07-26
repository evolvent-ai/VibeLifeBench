BEGIN;
UPDATE merchants
SET tags = CASE
  WHEN instr(tags, 'maintenance_2026_08_06_08_07') > 0 THEN tags
  ELSE tags || ';maintenance_2026_08_06_08_07;dock_closed;indoor_slot_available'
END
WHERE merchant_id = 'venue_river_dock_037';
INSERT OR REPLACE INTO merchant_qa
  (qa_id, merchant_id, user_id, question, answer, answered_by, created_at)
VALUES
  ('qa_dock_maintenance_0805_037', 'venue_river_dock_037', 'user_chen_shan',
   '8 月 6-7 日码头是否可训练？',
   '码头维护关闭，建议改室内测功或居家核心；预约需本人确认。',
   'dock_ops', '2026-08-05T09:00:00+08:00');
COMMIT;
