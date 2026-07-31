-- Generated calendar seed for central_ac_install_30d
BEGIN;
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_iscac_main', 'usr_luo_wei', 'Personal', '#4285F4', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');
INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES ('cal_iscac_task', 'usr_luo_wei', 'CoolMax 三室一厅中央空调送装计划', '#0B8043', 'Asia/Shanghai', 0, '2026-05-01T00:00:00Z');
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('evt_iscac_c1', 'cal_iscac_task', '结案截止日', '结案截止日硬节点，出发前所有采购、退货、转卖、出运须完成。', '', '2026-07-15T10:30:00+08:00', '2026-07-15T13:00:00+08:00', 0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('evt_iscac_c2', 'cal_iscac_main', '信用卡还款日', '账单还款截止日，出发前需结清或安排还款。', '', '2026-07-08T09:00:00+08:00', '2026-07-08T09:30:00+08:00', 0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);
INSERT INTO events (event_id, calendar_id, summary, description, location, start_dt, end_dt, all_day, status, created_at, updated_at, recurrence_rule, parent_event_id) VALUES ('evt_iscac_c3', 'cal_iscac_task', '转运出运截止(预估)', '集运出运的预估截止窗口，需在此前确认受管制物品申报与运输方式。', '集英转运仓(线上)', '2026-07-02T18:00:00+08:00', '2026-07-02T18:30:00+08:00', 0, 'tentative', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);
INSERT INTO reminders (event_id,method,minutes_before) VALUES ('evt_iscac_c1','popup',2880),('evt_iscac_c2','popup',1440),('evt_iscac_c3','popup',1440);
INSERT INTO _counters (key,value) VALUES ('event_seq',3);
COMMIT;
