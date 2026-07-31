-- calendar_mock wang_fang_lending — init.sql
-- 王芳的个人日历, 2026年5-6月. 借给老同学陈强的钱要不回来, 正在准备民间借贷诉讼.
-- 既有事件: 已约的律师咨询、女儿家长会(干扰项)、信用卡还款(干扰项).
-- 后续案件节点由用户或协作者按实际送达情况维护.
-- All times Asia/Shanghai (+08:00). Reference frame: 2026-05-20. user_id = wang_fang.

BEGIN;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
 ('cal_wang_fang', 'wang_fang', '王芳 个人', '#DB4437', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');

-- 已约的律师咨询(背景: 王芳已在咨询律师, 但主要靠自己研究判例)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_lawyer_0522', 'cal_wang_fang', '律师咨询(民间借贷)', '带借条、转账记录、微信催收记录、收条', '杭州黄龙某律所',
  '2026-05-22T15:00:00+08:00', '2026-05-22T16:00:00+08:00',
  0, 'confirmed', '2026-05-15T00:00:00Z', '2026-05-15T00:00:00Z', NULL, NULL);

-- 女儿家长会(干扰项, 与案件无关的家庭安排)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_school_0528', 'cal_wang_fang', '女儿期末家长会', '班主任沟通', '杭州市西湖区某小学',
  '2026-05-28T18:30:00+08:00', '2026-05-28T20:00:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

-- 信用卡还款日(干扰项)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_cmb_repay', 'cal_wang_fang', '工商银行信用卡还款', '尾号6677 应还¥3,800', NULL,
  '2026-06-05T00:00:00+08:00', '2026-06-05T23:59:00+08:00',
  1, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);



INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_001', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 001。', '西湖区服装店',
  '2026-03-03T09:15:00+08:00', '2026-03-03T10:15:00+08:00',
  0, 'confirmed', '2026-02-22T00:00:00Z', '2026-02-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_002', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 002。', '视频通话',
  '2026-03-05T10:30:00+08:00', '2026-03-05T11:45:00+08:00',
  0, 'confirmed', '2026-02-23T00:00:00Z', '2026-02-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_003', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 003。', '店里',
  '2026-03-07T11:45:00+08:00', '2026-03-07T13:15:00+08:00',
  0, 'confirmed', '2026-02-24T00:00:00Z', '2026-02-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_004', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 004。', '店里后仓',
  '2026-03-09T12:00:00+08:00', '2026-03-09T12:45:00+08:00',
  0, 'confirmed', '2026-02-25T00:00:00Z', '2026-02-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_005', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 005。', '家里',
  '2026-03-12T14:15:00+08:00', '2026-03-12T15:15:00+08:00',
  0, 'confirmed', '2026-02-27T00:00:00Z', '2026-02-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_006', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 006。', '西湖区社区医院',
  '2026-03-14T15:30:00+08:00', '2026-03-14T16:45:00+08:00',
  0, 'confirmed', '2026-03-06T00:00:00Z', '2026-03-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_007', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 007。', NULL,
  '2026-03-16T16:45:00+08:00', '2026-03-16T18:15:00+08:00',
  0, 'confirmed', '2026-03-07T00:00:00Z', '2026-03-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_008', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 008。', NULL,
  '2026-03-18T18:00:00+08:00', '2026-03-18T18:45:00+08:00',
  0, 'confirmed', '2026-03-08T00:00:00Z', '2026-03-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_009', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 009。', '父母家',
  '2026-03-20T19:15:00+08:00', '2026-03-20T20:15:00+08:00',
  0, 'confirmed', '2026-03-09T00:00:00Z', '2026-03-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_010', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 010。', '西湖区服装店',
  '2026-03-23T08:30:00+08:00', '2026-03-23T09:45:00+08:00',
  0, 'confirmed', '2026-03-11T00:00:00Z', '2026-03-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_011', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 011。', '杭州四季青',
  '2026-03-25T09:45:00+08:00', '2026-03-25T11:15:00+08:00',
  0, 'confirmed', '2026-03-12T00:00:00Z', '2026-03-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_012', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 012。', '店里',
  '2026-03-27T00:00:00+08:00', '2026-03-27T23:59:00+08:00',
  1, 'confirmed', '2026-03-19T00:00:00Z', '2026-03-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_013', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 013。', '西湖区少年宫',
  '2026-03-29T11:15:00+08:00', '2026-03-29T12:15:00+08:00',
  0, 'confirmed', '2026-03-20T00:00:00Z', '2026-03-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_014', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 014。', '西湖区商圈',
  '2026-03-31T12:30:00+08:00', '2026-03-31T13:45:00+08:00',
  0, 'confirmed', '2026-03-21T00:00:00Z', '2026-03-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_015', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 015。', '西湖区服装店',
  '2026-04-03T14:45:00+08:00', '2026-04-03T16:15:00+08:00',
  0, 'confirmed', '2026-03-23T00:00:00Z', '2026-03-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_016', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 016。', '视频通话',
  '2026-04-05T15:00:00+08:00', '2026-04-05T15:45:00+08:00',
  0, 'confirmed', '2026-03-24T00:00:00Z', '2026-03-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_017', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 017。', '店里',
  '2026-04-07T16:15:00+08:00', '2026-04-07T17:15:00+08:00',
  0, 'confirmed', '2026-03-25T00:00:00Z', '2026-03-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_018', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 018。', '店里后仓',
  '2026-04-09T18:30:00+08:00', '2026-04-09T19:45:00+08:00',
  0, 'confirmed', '2026-04-01T00:00:00Z', '2026-04-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_019', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 019。', '家里',
  '2026-04-11T19:45:00+08:00', '2026-04-11T21:15:00+08:00',
  0, 'confirmed', '2026-04-02T00:00:00Z', '2026-04-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_020', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 020。', '西湖区社区医院',
  '2026-04-14T08:00:00+08:00', '2026-04-14T08:45:00+08:00',
  0, 'confirmed', '2026-04-04T00:00:00Z', '2026-04-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_021', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 021。', NULL,
  '2026-04-16T09:15:00+08:00', '2026-04-16T10:15:00+08:00',
  0, 'confirmed', '2026-04-05T00:00:00Z', '2026-04-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_022', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 022。', NULL,
  '2026-04-18T10:30:00+08:00', '2026-04-18T11:45:00+08:00',
  0, 'confirmed', '2026-04-06T00:00:00Z', '2026-04-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_023', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 023。', '父母家',
  '2026-04-20T11:45:00+08:00', '2026-04-20T13:15:00+08:00',
  0, 'confirmed', '2026-04-07T00:00:00Z', '2026-04-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_024', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 024。', '西湖区服装店',
  '2026-04-22T00:00:00+08:00', '2026-04-22T23:59:00+08:00',
  1, 'confirmed', '2026-04-14T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_025', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 025。', '杭州四季青',
  '2026-04-25T14:15:00+08:00', '2026-04-25T15:15:00+08:00',
  0, 'confirmed', '2026-04-16T00:00:00Z', '2026-04-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_026', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 026。', '店里',
  '2026-04-27T15:30:00+08:00', '2026-04-27T16:45:00+08:00',
  0, 'confirmed', '2026-04-17T00:00:00Z', '2026-04-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_027', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 027。', '西湖区少年宫',
  '2026-04-29T16:45:00+08:00', '2026-04-29T18:15:00+08:00',
  0, 'confirmed', '2026-04-18T00:00:00Z', '2026-04-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_028', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 028。', '西湖区商圈',
  '2026-05-01T18:00:00+08:00', '2026-05-01T18:45:00+08:00',
  0, 'confirmed', '2026-04-19T00:00:00Z', '2026-04-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_029', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 029。', '西湖区服装店',
  '2026-05-03T19:15:00+08:00', '2026-05-03T20:15:00+08:00',
  0, 'confirmed', '2026-04-20T00:00:00Z', '2026-04-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_030', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 030。', '视频通话',
  '2026-05-06T08:30:00+08:00', '2026-05-06T09:45:00+08:00',
  0, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_031', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 031。', '店里',
  '2026-05-08T09:45:00+08:00', '2026-05-08T11:15:00+08:00',
  0, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_032', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 032。', '店里后仓',
  '2026-05-10T10:00:00+08:00', '2026-05-10T10:45:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_033', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 033。', '家里',
  '2026-05-12T11:15:00+08:00', '2026-05-12T12:15:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_034', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 034。', '西湖区社区医院',
  '2026-05-14T12:30:00+08:00', '2026-05-14T13:45:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_035', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 035。', NULL,
  '2026-05-17T14:45:00+08:00', '2026-05-17T16:15:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_036', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 036。', NULL,
  '2026-05-19T00:00:00+08:00', '2026-05-19T23:59:00+08:00',
  1, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_037', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 037。', '父母家',
  '2026-05-21T16:15:00+08:00', '2026-05-21T17:15:00+08:00',
  0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_038', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 038。', '西湖区服装店',
  '2026-05-23T18:30:00+08:00', '2026-05-23T19:45:00+08:00',
  0, 'confirmed', '2026-05-13T00:00:00Z', '2026-05-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_039', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 039。', '杭州四季青',
  '2026-05-25T19:45:00+08:00', '2026-05-25T21:15:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_040', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 040。', '店里',
  '2026-05-28T08:00:00+08:00', '2026-05-28T08:45:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_041', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 041。', '西湖区少年宫',
  '2026-05-30T09:15:00+08:00', '2026-05-30T10:15:00+08:00',
  0, 'confirmed', '2026-05-17T00:00:00Z', '2026-05-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_042', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 042。', '西湖区商圈',
  '2026-06-01T10:30:00+08:00', '2026-06-01T11:45:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_043', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 043。', '西湖区服装店',
  '2026-06-03T11:45:00+08:00', '2026-06-03T13:15:00+08:00',
  0, 'confirmed', '2026-05-25T00:00:00Z', '2026-05-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_044', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 044。', '视频通话',
  '2026-06-05T12:00:00+08:00', '2026-06-05T12:45:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_045', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 045。', '店里',
  '2026-06-08T14:15:00+08:00', '2026-06-08T15:15:00+08:00',
  0, 'confirmed', '2026-05-28T00:00:00Z', '2026-05-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_046', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 046。', '店里后仓',
  '2026-06-10T15:30:00+08:00', '2026-06-10T16:45:00+08:00',
  0, 'confirmed', '2026-05-29T00:00:00Z', '2026-05-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_047', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 047。', '家里',
  '2026-06-12T16:45:00+08:00', '2026-06-12T18:15:00+08:00',
  0, 'confirmed', '2026-05-30T00:00:00Z', '2026-05-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_048', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 048。', '西湖区社区医院',
  '2026-06-14T00:00:00+08:00', '2026-06-14T23:59:00+08:00',
  1, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_049', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 049。', NULL,
  '2026-06-16T19:15:00+08:00', '2026-06-16T20:15:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_050', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 050。', NULL,
  '2026-06-19T08:30:00+08:00', '2026-06-19T09:45:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_051', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 051。', '父母家',
  '2026-06-21T09:45:00+08:00', '2026-06-21T11:15:00+08:00',
  0, 'confirmed', '2026-06-10T00:00:00Z', '2026-06-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_052', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 052。', '西湖区服装店',
  '2026-06-23T10:00:00+08:00', '2026-06-23T10:45:00+08:00',
  0, 'confirmed', '2026-06-11T00:00:00Z', '2026-06-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_053', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 053。', '杭州四季青',
  '2026-06-25T11:15:00+08:00', '2026-06-25T12:15:00+08:00',
  0, 'confirmed', '2026-06-12T00:00:00Z', '2026-06-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_054', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 054。', '店里',
  '2026-06-27T12:30:00+08:00', '2026-06-27T13:45:00+08:00',
  0, 'confirmed', '2026-06-19T00:00:00Z', '2026-06-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_055', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 055。', '西湖区少年宫',
  '2026-06-30T14:45:00+08:00', '2026-06-30T16:15:00+08:00',
  0, 'confirmed', '2026-06-21T00:00:00Z', '2026-06-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_056', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 056。', '西湖区商圈',
  '2026-03-02T15:00:00+08:00', '2026-03-02T15:45:00+08:00',
  0, 'confirmed', '2026-02-20T00:00:00Z', '2026-02-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_057', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 057。', '西湖区服装店',
  '2026-03-04T16:15:00+08:00', '2026-03-04T17:15:00+08:00',
  0, 'confirmed', '2026-02-21T00:00:00Z', '2026-02-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_058', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 058。', '视频通话',
  '2026-03-06T18:30:00+08:00', '2026-03-06T19:45:00+08:00',
  0, 'confirmed', '2026-02-22T00:00:00Z', '2026-02-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_059', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 059。', '店里',
  '2026-03-08T19:45:00+08:00', '2026-03-08T21:15:00+08:00',
  0, 'confirmed', '2026-02-23T00:00:00Z', '2026-02-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_060', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 060。', '店里后仓',
  '2026-03-11T00:00:00+08:00', '2026-03-11T23:59:00+08:00',
  1, 'confirmed', '2026-03-03T00:00:00Z', '2026-03-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_061', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 061。', '家里',
  '2026-03-13T09:15:00+08:00', '2026-03-13T10:15:00+08:00',
  0, 'confirmed', '2026-03-04T00:00:00Z', '2026-03-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_062', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 062。', '西湖区社区医院',
  '2026-03-15T10:30:00+08:00', '2026-03-15T11:45:00+08:00',
  0, 'confirmed', '2026-03-05T00:00:00Z', '2026-03-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_063', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 063。', NULL,
  '2026-03-17T11:45:00+08:00', '2026-03-17T13:15:00+08:00',
  0, 'confirmed', '2026-03-06T00:00:00Z', '2026-03-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_064', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 064。', NULL,
  '2026-03-19T12:00:00+08:00', '2026-03-19T12:45:00+08:00',
  0, 'confirmed', '2026-03-07T00:00:00Z', '2026-03-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_065', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 065。', '父母家',
  '2026-03-22T14:15:00+08:00', '2026-03-22T15:15:00+08:00',
  0, 'confirmed', '2026-03-09T00:00:00Z', '2026-03-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_066', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 066。', '西湖区服装店',
  '2026-03-24T15:30:00+08:00', '2026-03-24T16:45:00+08:00',
  0, 'confirmed', '2026-03-16T00:00:00Z', '2026-03-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_067', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 067。', '杭州四季青',
  '2026-03-26T16:45:00+08:00', '2026-03-26T18:15:00+08:00',
  0, 'confirmed', '2026-03-17T00:00:00Z', '2026-03-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_068', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 068。', '店里',
  '2026-03-28T18:00:00+08:00', '2026-03-28T18:45:00+08:00',
  0, 'confirmed', '2026-03-18T00:00:00Z', '2026-03-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_069', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 069。', '西湖区少年宫',
  '2026-03-30T19:15:00+08:00', '2026-03-30T20:15:00+08:00',
  0, 'confirmed', '2026-03-19T00:00:00Z', '2026-03-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_070', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 070。', '西湖区商圈',
  '2026-04-02T08:30:00+08:00', '2026-04-02T09:45:00+08:00',
  0, 'confirmed', '2026-03-21T00:00:00Z', '2026-03-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_071', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 071。', '西湖区服装店',
  '2026-04-04T09:45:00+08:00', '2026-04-04T11:15:00+08:00',
  0, 'confirmed', '2026-03-22T00:00:00Z', '2026-03-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_072', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 072。', '视频通话',
  '2026-04-06T00:00:00+08:00', '2026-04-06T23:59:00+08:00',
  1, 'confirmed', '2026-03-29T00:00:00Z', '2026-03-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_073', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 073。', '店里',
  '2026-04-08T11:15:00+08:00', '2026-04-08T12:15:00+08:00',
  0, 'confirmed', '2026-03-30T00:00:00Z', '2026-03-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_074', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 074。', '店里后仓',
  '2026-04-10T12:30:00+08:00', '2026-04-10T13:45:00+08:00',
  0, 'confirmed', '2026-03-31T00:00:00Z', '2026-03-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_075', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 075。', '家里',
  '2026-04-13T14:45:00+08:00', '2026-04-13T16:15:00+08:00',
  0, 'confirmed', '2026-04-02T00:00:00Z', '2026-04-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_076', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 076。', '西湖区社区医院',
  '2026-04-15T15:00:00+08:00', '2026-04-15T15:45:00+08:00',
  0, 'confirmed', '2026-04-03T00:00:00Z', '2026-04-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_077', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 077。', NULL,
  '2026-04-17T16:15:00+08:00', '2026-04-17T17:15:00+08:00',
  0, 'confirmed', '2026-04-04T00:00:00Z', '2026-04-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_078', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 078。', NULL,
  '2026-04-19T18:30:00+08:00', '2026-04-19T19:45:00+08:00',
  0, 'confirmed', '2026-04-11T00:00:00Z', '2026-04-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_079', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 079。', '父母家',
  '2026-04-21T19:45:00+08:00', '2026-04-21T21:15:00+08:00',
  0, 'confirmed', '2026-04-12T00:00:00Z', '2026-04-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_080', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 080。', '西湖区服装店',
  '2026-04-24T08:00:00+08:00', '2026-04-24T08:45:00+08:00',
  0, 'confirmed', '2026-04-14T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_081', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 081。', '杭州四季青',
  '2026-04-26T09:15:00+08:00', '2026-04-26T10:15:00+08:00',
  0, 'confirmed', '2026-04-15T00:00:00Z', '2026-04-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_082', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 082。', '店里',
  '2026-04-28T10:30:00+08:00', '2026-04-28T11:45:00+08:00',
  0, 'confirmed', '2026-04-16T00:00:00Z', '2026-04-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_083', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 083。', '西湖区少年宫',
  '2026-04-30T11:45:00+08:00', '2026-04-30T13:15:00+08:00',
  0, 'confirmed', '2026-04-17T00:00:00Z', '2026-04-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_084', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 084。', '西湖区商圈',
  '2026-05-02T00:00:00+08:00', '2026-05-02T23:59:00+08:00',
  1, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_085', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 085。', '西湖区服装店',
  '2026-05-05T14:15:00+08:00', '2026-05-05T15:15:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_086', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 086。', '视频通话',
  '2026-05-07T15:30:00+08:00', '2026-05-07T16:45:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_087', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 087。', '店里',
  '2026-05-09T16:45:00+08:00', '2026-05-09T18:15:00+08:00',
  0, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_088', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 088。', '店里后仓',
  '2026-05-11T18:00:00+08:00', '2026-05-11T18:45:00+08:00',
  0, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_089', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 089。', '家里',
  '2026-05-13T19:15:00+08:00', '2026-05-13T20:15:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_090', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 090。', '西湖区社区医院',
  '2026-05-16T08:30:00+08:00', '2026-05-16T09:45:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_091', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 091。', NULL,
  '2026-05-18T09:45:00+08:00', '2026-05-18T11:15:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_092', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 092。', NULL,
  '2026-05-20T10:00:00+08:00', '2026-05-20T10:45:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_093', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 093。', '父母家',
  '2026-05-22T11:15:00+08:00', '2026-05-22T12:15:00+08:00',
  0, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_094', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 094。', '西湖区服装店',
  '2026-05-24T12:30:00+08:00', '2026-05-24T13:45:00+08:00',
  0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_095', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 095。', '杭州四季青',
  '2026-05-27T14:45:00+08:00', '2026-05-27T16:15:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_096', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 096。', '店里',
  '2026-05-29T00:00:00+08:00', '2026-05-29T23:59:00+08:00',
  1, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_097', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 097。', '西湖区少年宫',
  '2026-05-31T16:15:00+08:00', '2026-05-31T17:15:00+08:00',
  0, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_098', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 098。', '西湖区商圈',
  '2026-06-02T18:30:00+08:00', '2026-06-02T19:45:00+08:00',
  0, 'confirmed', '2026-05-23T00:00:00Z', '2026-05-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_099', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 099。', '西湖区服装店',
  '2026-06-04T19:45:00+08:00', '2026-06-04T21:15:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_100', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 100。', '视频通话',
  '2026-06-07T08:00:00+08:00', '2026-06-07T08:45:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_101', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 101。', '店里',
  '2026-06-09T09:15:00+08:00', '2026-06-09T10:15:00+08:00',
  0, 'confirmed', '2026-05-27T00:00:00Z', '2026-05-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_102', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 102。', '店里后仓',
  '2026-06-11T10:30:00+08:00', '2026-06-11T11:45:00+08:00',
  0, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_103', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 103。', '家里',
  '2026-06-13T11:45:00+08:00', '2026-06-13T13:15:00+08:00',
  0, 'confirmed', '2026-06-04T00:00:00Z', '2026-06-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_104', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 104。', '西湖区社区医院',
  '2026-06-15T12:00:00+08:00', '2026-06-15T12:45:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_105', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 105。', NULL,
  '2026-06-18T14:15:00+08:00', '2026-06-18T15:15:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_106', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 106。', NULL,
  '2026-06-20T15:30:00+08:00', '2026-06-20T16:45:00+08:00',
  0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_107', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 107。', '父母家',
  '2026-06-22T16:45:00+08:00', '2026-06-22T18:15:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_108', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 108。', '西湖区服装店',
  '2026-06-24T00:00:00+08:00', '2026-06-24T23:59:00+08:00',
  1, 'confirmed', '2026-06-16T00:00:00Z', '2026-06-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_109', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 109。', '杭州四季青',
  '2026-06-26T19:15:00+08:00', '2026-06-26T20:15:00+08:00',
  0, 'confirmed', '2026-06-17T00:00:00Z', '2026-06-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_110', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 110。', '店里',
  '2026-06-29T08:30:00+08:00', '2026-06-29T09:45:00+08:00',
  0, 'confirmed', '2026-06-19T00:00:00Z', '2026-06-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_111', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 111。', '西湖区少年宫',
  '2026-03-01T09:45:00+08:00', '2026-03-01T11:15:00+08:00',
  0, 'confirmed', '2026-02-18T00:00:00Z', '2026-02-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_112', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 112。', '西湖区商圈',
  '2026-03-03T10:00:00+08:00', '2026-03-03T10:45:00+08:00',
  0, 'confirmed', '2026-02-19T00:00:00Z', '2026-02-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_113', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 113。', '西湖区服装店',
  '2026-03-05T11:15:00+08:00', '2026-03-05T12:15:00+08:00',
  0, 'confirmed', '2026-02-20T00:00:00Z', '2026-02-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_114', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 114。', '视频通话',
  '2026-03-07T12:30:00+08:00', '2026-03-07T13:45:00+08:00',
  0, 'confirmed', '2026-02-27T00:00:00Z', '2026-02-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_115', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 115。', '店里',
  '2026-03-10T14:45:00+08:00', '2026-03-10T16:15:00+08:00',
  0, 'confirmed', '2026-03-01T00:00:00Z', '2026-03-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_116', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 116。', '店里后仓',
  '2026-03-12T15:00:00+08:00', '2026-03-12T15:45:00+08:00',
  0, 'confirmed', '2026-03-02T00:00:00Z', '2026-03-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_117', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 117。', '家里',
  '2026-03-14T16:15:00+08:00', '2026-03-14T17:15:00+08:00',
  0, 'confirmed', '2026-03-03T00:00:00Z', '2026-03-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_118', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 118。', '西湖区社区医院',
  '2026-03-16T18:30:00+08:00', '2026-03-16T19:45:00+08:00',
  0, 'confirmed', '2026-03-04T00:00:00Z', '2026-03-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_119', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 119。', NULL,
  '2026-03-18T19:45:00+08:00', '2026-03-18T21:15:00+08:00',
  0, 'confirmed', '2026-03-05T00:00:00Z', '2026-03-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_120', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 120。', NULL,
  '2026-03-21T00:00:00+08:00', '2026-03-21T23:59:00+08:00',
  1, 'confirmed', '2026-03-13T00:00:00Z', '2026-03-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_121', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 121。', '父母家',
  '2026-03-23T09:15:00+08:00', '2026-03-23T10:15:00+08:00',
  0, 'confirmed', '2026-03-14T00:00:00Z', '2026-03-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_122', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 122。', '西湖区服装店',
  '2026-03-25T10:30:00+08:00', '2026-03-25T11:45:00+08:00',
  0, 'confirmed', '2026-03-15T00:00:00Z', '2026-03-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_123', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 123。', '杭州四季青',
  '2026-03-27T11:45:00+08:00', '2026-03-27T13:15:00+08:00',
  0, 'confirmed', '2026-03-16T00:00:00Z', '2026-03-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_124', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 124。', '店里',
  '2026-03-29T12:00:00+08:00', '2026-03-29T12:45:00+08:00',
  0, 'confirmed', '2026-03-17T00:00:00Z', '2026-03-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_125', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 125。', '西湖区少年宫',
  '2026-04-01T14:15:00+08:00', '2026-04-01T15:15:00+08:00',
  0, 'confirmed', '2026-03-19T00:00:00Z', '2026-03-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_126', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 126。', '西湖区商圈',
  '2026-04-03T15:30:00+08:00', '2026-04-03T16:45:00+08:00',
  0, 'confirmed', '2026-03-26T00:00:00Z', '2026-03-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_127', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 127。', '西湖区服装店',
  '2026-04-05T16:45:00+08:00', '2026-04-05T18:15:00+08:00',
  0, 'confirmed', '2026-03-27T00:00:00Z', '2026-03-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_128', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 128。', '视频通话',
  '2026-04-07T18:00:00+08:00', '2026-04-07T18:45:00+08:00',
  0, 'confirmed', '2026-03-28T00:00:00Z', '2026-03-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_129', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 129。', '店里',
  '2026-04-09T19:15:00+08:00', '2026-04-09T20:15:00+08:00',
  0, 'confirmed', '2026-03-29T00:00:00Z', '2026-03-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_130', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 130。', '店里后仓',
  '2026-04-12T08:30:00+08:00', '2026-04-12T09:45:00+08:00',
  0, 'confirmed', '2026-03-31T00:00:00Z', '2026-03-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_131', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 131。', '家里',
  '2026-04-14T09:45:00+08:00', '2026-04-14T11:15:00+08:00',
  0, 'confirmed', '2026-04-01T00:00:00Z', '2026-04-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_132', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 132。', '西湖区社区医院',
  '2026-04-16T00:00:00+08:00', '2026-04-16T23:59:00+08:00',
  1, 'confirmed', '2026-04-08T00:00:00Z', '2026-04-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_133', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 133。', NULL,
  '2026-04-18T11:15:00+08:00', '2026-04-18T12:15:00+08:00',
  0, 'confirmed', '2026-04-09T00:00:00Z', '2026-04-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_134', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 134。', NULL,
  '2026-04-20T12:30:00+08:00', '2026-04-20T13:45:00+08:00',
  0, 'confirmed', '2026-04-10T00:00:00Z', '2026-04-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_135', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 135。', '父母家',
  '2026-04-23T14:45:00+08:00', '2026-04-23T16:15:00+08:00',
  0, 'confirmed', '2026-04-12T00:00:00Z', '2026-04-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_136', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 136。', '西湖区服装店',
  '2026-04-25T15:00:00+08:00', '2026-04-25T15:45:00+08:00',
  0, 'confirmed', '2026-04-13T00:00:00Z', '2026-04-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_137', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 137。', '杭州四季青',
  '2026-04-27T16:15:00+08:00', '2026-04-27T17:15:00+08:00',
  0, 'confirmed', '2026-04-14T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_138', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 138。', '店里',
  '2026-04-29T18:30:00+08:00', '2026-04-29T19:45:00+08:00',
  0, 'confirmed', '2026-04-21T00:00:00Z', '2026-04-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_139', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 139。', '西湖区少年宫',
  '2026-05-01T19:45:00+08:00', '2026-05-01T21:15:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_140', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 140。', '西湖区商圈',
  '2026-05-04T08:00:00+08:00', '2026-05-04T08:45:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_141', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 141。', '西湖区服装店',
  '2026-05-06T09:15:00+08:00', '2026-05-06T10:15:00+08:00',
  0, 'confirmed', '2026-04-25T00:00:00Z', '2026-04-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_142', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 142。', '视频通话',
  '2026-05-08T10:30:00+08:00', '2026-05-08T11:45:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_143', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 143。', '店里',
  '2026-05-10T11:45:00+08:00', '2026-05-10T13:15:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_144', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 144。', '店里后仓',
  '2026-05-12T00:00:00+08:00', '2026-05-12T23:59:00+08:00',
  1, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_145', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 145。', '家里',
  '2026-05-15T14:15:00+08:00', '2026-05-15T15:15:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_146', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 146。', '西湖区社区医院',
  '2026-05-17T15:30:00+08:00', '2026-05-17T16:45:00+08:00',
  0, 'confirmed', '2026-05-07T00:00:00Z', '2026-05-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_147', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 147。', NULL,
  '2026-05-19T16:45:00+08:00', '2026-05-19T18:15:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_148', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 148。', NULL,
  '2026-05-21T18:00:00+08:00', '2026-05-21T18:45:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_149', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 149。', '父母家',
  '2026-05-23T19:15:00+08:00', '2026-05-23T20:15:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_150', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 150。', '西湖区服装店',
  '2026-05-26T08:30:00+08:00', '2026-05-26T09:45:00+08:00',
  0, 'confirmed', '2026-05-18T00:00:00Z', '2026-05-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_151', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 151。', '杭州四季青',
  '2026-05-28T09:45:00+08:00', '2026-05-28T11:15:00+08:00',
  0, 'confirmed', '2026-05-19T00:00:00Z', '2026-05-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_152', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 152。', '店里',
  '2026-05-30T10:00:00+08:00', '2026-05-30T10:45:00+08:00',
  0, 'confirmed', '2026-05-20T00:00:00Z', '2026-05-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_153', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 153。', '西湖区少年宫',
  '2026-06-01T11:15:00+08:00', '2026-06-01T12:15:00+08:00',
  0, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_154', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 154。', '西湖区商圈',
  '2026-06-03T12:30:00+08:00', '2026-06-03T13:45:00+08:00',
  0, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_155', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 155。', '西湖区服装店',
  '2026-06-06T14:45:00+08:00', '2026-06-06T16:15:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_156', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 156。', '视频通话',
  '2026-06-08T00:00:00+08:00', '2026-06-08T23:59:00+08:00',
  1, 'confirmed', '2026-05-31T00:00:00Z', '2026-05-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_157', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 157。', '店里',
  '2026-06-10T16:15:00+08:00', '2026-06-10T17:15:00+08:00',
  0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_158', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 158。', '店里后仓',
  '2026-06-12T18:30:00+08:00', '2026-06-12T19:45:00+08:00',
  0, 'confirmed', '2026-06-02T00:00:00Z', '2026-06-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_159', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 159。', '家里',
  '2026-06-14T19:45:00+08:00', '2026-06-14T21:15:00+08:00',
  0, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_160', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 160。', '西湖区社区医院',
  '2026-06-17T08:00:00+08:00', '2026-06-17T08:45:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_161', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 161。', NULL,
  '2026-06-19T09:15:00+08:00', '2026-06-19T10:15:00+08:00',
  0, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_162', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 162。', NULL,
  '2026-06-21T10:30:00+08:00', '2026-06-21T11:45:00+08:00',
  0, 'confirmed', '2026-06-13T00:00:00Z', '2026-06-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_163', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 163。', '父母家',
  '2026-06-23T11:45:00+08:00', '2026-06-23T13:15:00+08:00',
  0, 'confirmed', '2026-06-14T00:00:00Z', '2026-06-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_164', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 164。', '西湖区服装店',
  '2026-06-25T12:00:00+08:00', '2026-06-25T12:45:00+08:00',
  0, 'confirmed', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_165', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 165。', '杭州四季青',
  '2026-06-28T14:15:00+08:00', '2026-06-28T15:15:00+08:00',
  0, 'confirmed', '2026-06-17T00:00:00Z', '2026-06-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_166', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 166。', '店里',
  '2026-06-30T15:30:00+08:00', '2026-06-30T16:45:00+08:00',
  0, 'confirmed', '2026-06-18T00:00:00Z', '2026-06-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_167', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 167。', '西湖区少年宫',
  '2026-03-02T16:45:00+08:00', '2026-03-02T18:15:00+08:00',
  0, 'confirmed', '2026-02-17T00:00:00Z', '2026-02-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_168', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 168。', '西湖区商圈',
  '2026-03-04T00:00:00+08:00', '2026-03-04T23:59:00+08:00',
  1, 'confirmed', '2026-02-24T00:00:00Z', '2026-02-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_169', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 169。', '西湖区服装店',
  '2026-03-06T19:15:00+08:00', '2026-03-06T20:15:00+08:00',
  0, 'confirmed', '2026-02-25T00:00:00Z', '2026-02-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_170', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 170。', '视频通话',
  '2026-03-09T08:30:00+08:00', '2026-03-09T09:45:00+08:00',
  0, 'confirmed', '2026-02-27T00:00:00Z', '2026-02-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_171', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 171。', '店里',
  '2026-03-11T09:45:00+08:00', '2026-03-11T11:15:00+08:00',
  0, 'confirmed', '2026-02-28T00:00:00Z', '2026-02-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_172', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 172。', '店里后仓',
  '2026-03-13T10:00:00+08:00', '2026-03-13T10:45:00+08:00',
  0, 'confirmed', '2026-03-01T00:00:00Z', '2026-03-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_173', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 173。', '家里',
  '2026-03-15T11:15:00+08:00', '2026-03-15T12:15:00+08:00',
  0, 'confirmed', '2026-03-02T00:00:00Z', '2026-03-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_174', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 174。', '西湖区社区医院',
  '2026-03-17T12:30:00+08:00', '2026-03-17T13:45:00+08:00',
  0, 'confirmed', '2026-03-09T00:00:00Z', '2026-03-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_175', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 175。', NULL,
  '2026-03-20T14:45:00+08:00', '2026-03-20T16:15:00+08:00',
  0, 'confirmed', '2026-03-11T00:00:00Z', '2026-03-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_176', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 176。', NULL,
  '2026-03-22T15:00:00+08:00', '2026-03-22T15:45:00+08:00',
  0, 'confirmed', '2026-03-12T00:00:00Z', '2026-03-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_177', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 177。', '父母家',
  '2026-03-24T16:15:00+08:00', '2026-03-24T17:15:00+08:00',
  0, 'confirmed', '2026-03-13T00:00:00Z', '2026-03-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_178', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 178。', '西湖区服装店',
  '2026-03-26T18:30:00+08:00', '2026-03-26T19:45:00+08:00',
  0, 'confirmed', '2026-03-14T00:00:00Z', '2026-03-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_179', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 179。', '杭州四季青',
  '2026-03-28T19:45:00+08:00', '2026-03-28T21:15:00+08:00',
  0, 'confirmed', '2026-03-15T00:00:00Z', '2026-03-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_180', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 180。', '店里',
  '2026-03-31T00:00:00+08:00', '2026-03-31T23:59:00+08:00',
  1, 'confirmed', '2026-03-23T00:00:00Z', '2026-03-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_181', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 181。', '西湖区少年宫',
  '2026-04-02T09:15:00+08:00', '2026-04-02T10:15:00+08:00',
  0, 'confirmed', '2026-03-24T00:00:00Z', '2026-03-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_182', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 182。', '西湖区商圈',
  '2026-04-04T10:30:00+08:00', '2026-04-04T11:45:00+08:00',
  0, 'confirmed', '2026-03-25T00:00:00Z', '2026-03-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_183', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 183。', '西湖区服装店',
  '2026-04-06T11:45:00+08:00', '2026-04-06T13:15:00+08:00',
  0, 'confirmed', '2026-03-26T00:00:00Z', '2026-03-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_184', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 184。', '视频通话',
  '2026-04-08T12:00:00+08:00', '2026-04-08T12:45:00+08:00',
  0, 'confirmed', '2026-03-27T00:00:00Z', '2026-03-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_185', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 185。', '店里',
  '2026-04-11T14:15:00+08:00', '2026-04-11T15:15:00+08:00',
  0, 'confirmed', '2026-03-29T00:00:00Z', '2026-03-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_186', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 186。', '店里后仓',
  '2026-04-13T15:30:00+08:00', '2026-04-13T16:45:00+08:00',
  0, 'confirmed', '2026-04-05T00:00:00Z', '2026-04-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_187', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 187。', '家里',
  '2026-04-15T16:45:00+08:00', '2026-04-15T18:15:00+08:00',
  0, 'confirmed', '2026-04-06T00:00:00Z', '2026-04-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_188', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 188。', '西湖区社区医院',
  '2026-04-17T18:00:00+08:00', '2026-04-17T18:45:00+08:00',
  0, 'confirmed', '2026-04-07T00:00:00Z', '2026-04-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_189', 'cal_wang_fang', '信用卡账单核对', '核对近一周期刷卡消费和自动还款。备注：安排记录 189。', NULL,
  '2026-04-19T19:15:00+08:00', '2026-04-19T20:15:00+08:00',
  0, 'confirmed', '2026-04-08T00:00:00Z', '2026-04-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_190', 'cal_wang_fang', '水电燃气提醒', '检查店铺和家里的水电燃气缴费情况。备注：安排记录 190。', NULL,
  '2026-04-22T08:30:00+08:00', '2026-04-22T09:45:00+08:00',
  0, 'confirmed', '2026-04-10T00:00:00Z', '2026-04-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_191', 'cal_wang_fang', '家庭聚餐', '和父母吃饭，顺便聊最近家里的事。备注：安排记录 191。', '父母家',
  '2026-04-24T09:45:00+08:00', '2026-04-24T11:15:00+08:00',
  0, 'confirmed', '2026-04-11T00:00:00Z', '2026-04-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_192', 'cal_wang_fang', '快递签收提醒', '留意门店快递与样衣包裹签收。备注：安排记录 192。', '西湖区服装店',
  '2026-04-26T00:00:00+08:00', '2026-04-26T23:59:00+08:00',
  1, 'confirmed', '2026-04-18T00:00:00Z', '2026-04-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_193', 'cal_wang_fang', '批发市场拿货', '去四季青看看新货和价格。备注：安排记录 193。', '杭州四季青',
  '2026-04-28T11:15:00+08:00', '2026-04-28T12:15:00+08:00',
  0, 'confirmed', '2026-04-19T00:00:00Z', '2026-04-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_194', 'cal_wang_fang', '店员排班确认', '确认周末排班、调休和加班餐。备注：安排记录 194。', '店里',
  '2026-04-30T12:30:00+08:00', '2026-04-30T13:45:00+08:00',
  0, 'confirmed', '2026-04-20T00:00:00Z', '2026-04-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_195', 'cal_wang_fang', '女儿兴趣班接送', '安排周末接送和课后晚饭。备注：安排记录 195。', '西湖区少年宫',
  '2026-05-03T14:45:00+08:00', '2026-05-03T16:15:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_196', 'cal_wang_fang', '美容美发预约', '例行护理，顺便休息一下。备注：安排记录 196。', '西湖区商圈',
  '2026-05-05T15:00:00+08:00', '2026-05-05T15:45:00+08:00',
  0, 'confirmed', '2026-04-23T00:00:00Z', '2026-04-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_197', 'cal_wang_fang', '服装店上新盘点', '核对本周到货款式、尺码和补货需求。备注：安排记录 197。', '西湖区服装店',
  '2026-05-07T16:15:00+08:00', '2026-05-07T17:15:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_198', 'cal_wang_fang', '供应商对款', '跟进尾款、退换货和下批发货节奏。备注：安排记录 198。', '视频通话',
  '2026-05-09T18:30:00+08:00', '2026-05-09T19:45:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_199', 'cal_wang_fang', '直播看款', '看批发市场直播选秋装新款。备注：安排记录 199。', '店里',
  '2026-05-11T19:45:00+08:00', '2026-05-11T21:15:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_200', 'cal_wang_fang', '店铺营业复盘', '记录本周客流、连带销售和滞销款。备注：安排记录 200。', '店里后仓',
  '2026-05-14T08:00:00+08:00', '2026-05-14T08:45:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_201', 'cal_wang_fang', '家长会准备', '整理女儿学校通知和老师沟通事项。备注：安排记录 201。', '家里',
  '2026-05-16T09:15:00+08:00', '2026-05-16T10:15:00+08:00',
  0, 'confirmed', '2026-05-05T00:00:00Z', '2026-05-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_202', 'cal_wang_fang', '社区医院复诊', '常规复诊，顺便问睡眠和颈椎问题。备注：安排记录 202。', '西湖区社区医院',
  '2026-05-18T10:30:00+08:00', '2026-05-18T11:45:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO _counters (key, value) VALUES
 ('event_seq', 500),
 ('attendee_seq', 0),
 ('reminder_seq', 0);

-- Stage 0 仅加载参考日前已经存在的日历记录；未来安排可以保留，但创建元数据不得晚于参考日。
UPDATE events
SET created_at = '2026-05-19T08:00:00Z',
    updated_at = CASE
      WHEN updated_at > '2026-05-20T23:59:59' THEN '2026-05-19T08:00:00Z'
      ELSE updated_at
    END
WHERE event_id LIKE 'evt_bg_%'
  AND created_at > '2026-05-20T23:59:59';

COMMIT;
