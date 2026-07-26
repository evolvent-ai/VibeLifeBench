BEGIN;
INSERT OR IGNORE INTO events
  (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES
  ('evt_food_sys_hearing_0612', 'cal_zhao_meng', '法院开庭：（2026）沪0115民初18426号',
   '携带身份证明、订单支付材料、商品页面和沟通记录、医疗票据、涉案食品实物及检验材料原件。',
   '上海市浦东新区人民法院第六法庭', '2026-06-12T09:30:00+08:00', '2026-06-12T11:30:00+08:00',
   0, 'confirmed', '2026-06-08T09:41:00+08:00', '2026-06-08T09:41:00+08:00', NULL, NULL);
INSERT OR IGNORE INTO reminders (id, event_id, method, minutes_before) VALUES
  (9121, 'evt_food_sys_hearing_0612', 'popup', 2880),
  (9122, 'evt_food_sys_hearing_0612', 'popup', 180);
UPDATE _counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key IN ('event_seq','reminder_seq');
COMMIT;
