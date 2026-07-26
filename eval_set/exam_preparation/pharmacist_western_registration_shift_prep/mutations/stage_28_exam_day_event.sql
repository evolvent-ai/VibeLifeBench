-- Stage 28（2026-10-10 考前一天）：考试当天的全天日程进入日历。
-- 对应 event.yaml S28_event「【日历】明天有一个全天日程：2026 年执业药师考试」——
-- 原实现只有通知文本、日历里没有任何 10 月事件，属手册 §3.4 明令禁止的
-- "Notification 称某事已发生，但对应服务中不存在该对象"。
-- 时间/考点/座位与 stage_27 准考证状态（notif_ticket_ready）保持一致，跨服务可相互印证。
INSERT OR REPLACE INTO events (event_id,calendar_id,summary,description,location,start_dt,end_dt,all_day,status,created_at,updated_at) VALUES
 ('evt_exam_day_1011','cal_zhou_exam','2026 年执业药师职业资格考试','西药类四科；凭准考证与身份证入场，座位 12-08。','市职业教育中心A楼','2026-10-11T00:00:00+08:00','2026-10-11T23:59:00+08:00',1,'confirmed','2026-10-08T09:10:00+08:00','2026-10-08T09:10:00+08:00');
