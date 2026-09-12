-- calendar_mock wang_fang_lending — init.sql
-- Wang FangofCJK_4E2A_CJK_4EBA_dayCJK_5386_, 2026year5-6month. CJK_501F_CJK_7ED9_CJK_8001_CJK_540C_CJK_5B66_Chen QiangofCJK_94B1_CJK_8981_CJK_4E0D_CJK_56DE_CJK_6765_, CJK_6B63_atprepareprivate lendingCJK_8BC9_CJK_8BBC_.
-- CJK_65E2_hasCJK_4E8B_CJK_4EF6_: alreadyCJK_7EA6_oflawyerCJK_54A8_CJK_8BE2_、CJK_5973_CJK_513F_CJK_5BB6_CJK_957F_CJK_4F1A_(CJK_5E72_CJK_6270_CJK_9879_)、CJK_4FE1_CJK_7528_CJK_5361_repayment(CJK_5E72_CJK_6270_CJK_9879_).
-- follow-upcaseCJK_8282_CJK_70B9_CJK_7531_CJK_7528_CJK_6237_orCJK_534F_CJK_4F5C_CJK_8005_underCJK_5B9E_CJK_9645_servedCJK_60C5_CJK_51B5_CJK_7EF4_CJK_62A4_.
-- All times Asia/Shanghai (+08:00). Reference frame: 2026-05-20. user_id = wang_fang.

PRAGMA journal_mode = DELETE;

BEGIN;

INSERT INTO calendars (calendar_id, user_id, name, color, timezone, is_primary, created_at) VALUES
 ('cal_wang_fang', 'wang_fang', 'Wang Fang CJK_4E2A_CJK_4EBA_', '#DB4437', 'Asia/Shanghai', 1, '2024-01-01T00:00:00Z');

-- alreadyCJK_7EA6_oflawyerCJK_54A8_CJK_8BE2_(CJK_80CC_CJK_666F_: Wang FangalreadyatCJK_54A8_CJK_8BE2_lawyer, CJK_4F46_CJK_4E3B_CJK_8981_CJK_9760_CJK_81EA_CJK_5DF1_CJK_7814_CJK_7A76_precedent)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_lawyer_0522', 'cal_wang_fang', 'lawyerCJK_54A8_CJK_8BE2_(private lending)', 'CJK_5E26_IOU、CJK_8F6C_CJK_8D26_record、WeChatcollectionrecord、CJK_6536_CJK_6761_', 'HangzhouCJK_9EC4_CJK_9F99_CJK_67D0_law firm',
  '2026-05-22T15:00:00+08:00', '2026-05-22T16:00:00+08:00',
  0, 'confirmed', '2026-05-15T00:00:00Z', '2026-05-15T00:00:00Z', NULL, NULL);

-- CJK_5973_CJK_513F_CJK_5BB6_CJK_957F_CJK_4F1A_(CJK_5E72_CJK_6270_CJK_9879_, andcasenoneCJK_5173_ofCJK_5BB6_CJK_5EAD_CJK_5B89_CJK_6392_)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_school_0528', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_671F_CJK_672B_CJK_5BB6_CJK_957F_CJK_4F1A_', 'CJK_73ED_CJK_4E3B_CJK_4EFB_CJK_6C9F_CJK_901A_', 'Xihu District of HangzhouCJK_67D0_CJK_5C0F_CJK_5B66_',
  '2026-05-28T18:30:00+08:00', '2026-05-28T20:00:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

-- CJK_4FE1_CJK_7528_CJK_5361_repaymentday(CJK_5E72_CJK_6270_CJK_9879_)
INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_cmb_repay', 'cal_wang_fang', 'CJK_5DE5_CJK_5546_bankCJK_4FE1_CJK_7528_CJK_5361_repayment', 'CJK_5C3E_No.6677 shouldCJK_8FD8_¥3,800', NULL,
  '2026-06-05T00:00:00+08:00', '2026-06-05T23:59:00+08:00',
  1, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);



INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_001', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 001。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-03T09:15:00+08:00', '2026-03-03T10:15:00+08:00',
  0, 'confirmed', '2026-02-22T00:00:00Z', '2026-02-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_002', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 002。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-03-05T10:30:00+08:00', '2026-03-05T11:45:00+08:00',
  0, 'confirmed', '2026-02-23T00:00:00Z', '2026-02-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_003', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 003。', 'CJK_5E97_CJK_91CC_',
  '2026-03-07T11:45:00+08:00', '2026-03-07T13:15:00+08:00',
  0, 'confirmed', '2026-02-24T00:00:00Z', '2026-02-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_004', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 004。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-03-09T12:00:00+08:00', '2026-03-09T12:45:00+08:00',
  0, 'confirmed', '2026-02-25T00:00:00Z', '2026-02-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_005', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 005。', 'CJK_5BB6_CJK_91CC_',
  '2026-03-12T14:15:00+08:00', '2026-03-12T15:15:00+08:00',
  0, 'confirmed', '2026-02-27T00:00:00Z', '2026-02-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_006', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 006。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-03-14T15:30:00+08:00', '2026-03-14T16:45:00+08:00',
  0, 'confirmed', '2026-03-06T00:00:00Z', '2026-03-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_007', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 007。', NULL,
  '2026-03-16T16:45:00+08:00', '2026-03-16T18:15:00+08:00',
  0, 'confirmed', '2026-03-07T00:00:00Z', '2026-03-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_008', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 008。', NULL,
  '2026-03-18T18:00:00+08:00', '2026-03-18T18:45:00+08:00',
  0, 'confirmed', '2026-03-08T00:00:00Z', '2026-03-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_009', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 009。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-03-20T19:15:00+08:00', '2026-03-20T20:15:00+08:00',
  0, 'confirmed', '2026-03-09T00:00:00Z', '2026-03-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_010', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 010。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-23T08:30:00+08:00', '2026-03-23T09:45:00+08:00',
  0, 'confirmed', '2026-03-11T00:00:00Z', '2026-03-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_011', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 011。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-03-25T09:45:00+08:00', '2026-03-25T11:15:00+08:00',
  0, 'confirmed', '2026-03-12T00:00:00Z', '2026-03-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_012', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 012。', 'CJK_5E97_CJK_91CC_',
  '2026-03-27T00:00:00+08:00', '2026-03-27T23:59:00+08:00',
  1, 'confirmed', '2026-03-19T00:00:00Z', '2026-03-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_013', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 013。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-03-29T11:15:00+08:00', '2026-03-29T12:15:00+08:00',
  0, 'confirmed', '2026-03-20T00:00:00Z', '2026-03-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_014', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 014。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-03-31T12:30:00+08:00', '2026-03-31T13:45:00+08:00',
  0, 'confirmed', '2026-03-21T00:00:00Z', '2026-03-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_015', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 015。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-03T14:45:00+08:00', '2026-04-03T16:15:00+08:00',
  0, 'confirmed', '2026-03-23T00:00:00Z', '2026-03-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_016', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 016。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-04-05T15:00:00+08:00', '2026-04-05T15:45:00+08:00',
  0, 'confirmed', '2026-03-24T00:00:00Z', '2026-03-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_017', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 017。', 'CJK_5E97_CJK_91CC_',
  '2026-04-07T16:15:00+08:00', '2026-04-07T17:15:00+08:00',
  0, 'confirmed', '2026-03-25T00:00:00Z', '2026-03-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_018', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 018。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-04-09T18:30:00+08:00', '2026-04-09T19:45:00+08:00',
  0, 'confirmed', '2026-04-01T00:00:00Z', '2026-04-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_019', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 019。', 'CJK_5BB6_CJK_91CC_',
  '2026-04-11T19:45:00+08:00', '2026-04-11T21:15:00+08:00',
  0, 'confirmed', '2026-04-02T00:00:00Z', '2026-04-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_020', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 020。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-04-14T08:00:00+08:00', '2026-04-14T08:45:00+08:00',
  0, 'confirmed', '2026-04-04T00:00:00Z', '2026-04-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_021', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 021。', NULL,
  '2026-04-16T09:15:00+08:00', '2026-04-16T10:15:00+08:00',
  0, 'confirmed', '2026-04-05T00:00:00Z', '2026-04-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_022', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 022。', NULL,
  '2026-04-18T10:30:00+08:00', '2026-04-18T11:45:00+08:00',
  0, 'confirmed', '2026-04-06T00:00:00Z', '2026-04-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_023', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 023。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-04-20T11:45:00+08:00', '2026-04-20T13:15:00+08:00',
  0, 'confirmed', '2026-04-07T00:00:00Z', '2026-04-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_024', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 024。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-22T00:00:00+08:00', '2026-04-22T23:59:00+08:00',
  1, 'confirmed', '2026-04-14T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_025', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 025。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-04-25T14:15:00+08:00', '2026-04-25T15:15:00+08:00',
  0, 'confirmed', '2026-04-16T00:00:00Z', '2026-04-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_026', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 026。', 'CJK_5E97_CJK_91CC_',
  '2026-04-27T15:30:00+08:00', '2026-04-27T16:45:00+08:00',
  0, 'confirmed', '2026-04-17T00:00:00Z', '2026-04-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_027', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 027。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-04-29T16:45:00+08:00', '2026-04-29T18:15:00+08:00',
  0, 'confirmed', '2026-04-18T00:00:00Z', '2026-04-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_028', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 028。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-05-01T18:00:00+08:00', '2026-05-01T18:45:00+08:00',
  0, 'confirmed', '2026-04-19T00:00:00Z', '2026-04-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_029', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 029。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-03T19:15:00+08:00', '2026-05-03T20:15:00+08:00',
  0, 'confirmed', '2026-04-20T00:00:00Z', '2026-04-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_030', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 030。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-05-06T08:30:00+08:00', '2026-05-06T09:45:00+08:00',
  0, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_031', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 031。', 'CJK_5E97_CJK_91CC_',
  '2026-05-08T09:45:00+08:00', '2026-05-08T11:15:00+08:00',
  0, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_032', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 032。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-05-10T10:00:00+08:00', '2026-05-10T10:45:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_033', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 033。', 'CJK_5BB6_CJK_91CC_',
  '2026-05-12T11:15:00+08:00', '2026-05-12T12:15:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_034', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 034。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-05-14T12:30:00+08:00', '2026-05-14T13:45:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_035', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 035。', NULL,
  '2026-05-17T14:45:00+08:00', '2026-05-17T16:15:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_036', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 036。', NULL,
  '2026-05-19T00:00:00+08:00', '2026-05-19T23:59:00+08:00',
  1, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_037', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 037。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-05-21T16:15:00+08:00', '2026-05-21T17:15:00+08:00',
  0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_038', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 038。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-23T18:30:00+08:00', '2026-05-23T19:45:00+08:00',
  0, 'confirmed', '2026-05-13T00:00:00Z', '2026-05-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_039', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 039。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-05-25T19:45:00+08:00', '2026-05-25T21:15:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_040', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 040。', 'CJK_5E97_CJK_91CC_',
  '2026-05-28T08:00:00+08:00', '2026-05-28T08:45:00+08:00',
  0, 'confirmed', '2026-05-16T00:00:00Z', '2026-05-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_041', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 041。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-05-30T09:15:00+08:00', '2026-05-30T10:15:00+08:00',
  0, 'confirmed', '2026-05-17T00:00:00Z', '2026-05-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_042', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 042。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-06-01T10:30:00+08:00', '2026-06-01T11:45:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_043', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 043。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-06-03T11:45:00+08:00', '2026-06-03T13:15:00+08:00',
  0, 'confirmed', '2026-05-25T00:00:00Z', '2026-05-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_044', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 044。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-06-05T12:00:00+08:00', '2026-06-05T12:45:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_045', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 045。', 'CJK_5E97_CJK_91CC_',
  '2026-06-08T14:15:00+08:00', '2026-06-08T15:15:00+08:00',
  0, 'confirmed', '2026-05-28T00:00:00Z', '2026-05-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_046', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 046。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-06-10T15:30:00+08:00', '2026-06-10T16:45:00+08:00',
  0, 'confirmed', '2026-05-29T00:00:00Z', '2026-05-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_047', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 047。', 'CJK_5BB6_CJK_91CC_',
  '2026-06-12T16:45:00+08:00', '2026-06-12T18:15:00+08:00',
  0, 'confirmed', '2026-05-30T00:00:00Z', '2026-05-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_048', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 048。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-06-14T00:00:00+08:00', '2026-06-14T23:59:00+08:00',
  1, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_049', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 049。', NULL,
  '2026-06-16T19:15:00+08:00', '2026-06-16T20:15:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_050', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 050。', NULL,
  '2026-06-19T08:30:00+08:00', '2026-06-19T09:45:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_051', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 051。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-06-21T09:45:00+08:00', '2026-06-21T11:15:00+08:00',
  0, 'confirmed', '2026-06-10T00:00:00Z', '2026-06-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_052', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 052。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-06-23T10:00:00+08:00', '2026-06-23T10:45:00+08:00',
  0, 'confirmed', '2026-06-11T00:00:00Z', '2026-06-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_053', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 053。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-06-25T11:15:00+08:00', '2026-06-25T12:15:00+08:00',
  0, 'confirmed', '2026-06-12T00:00:00Z', '2026-06-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_054', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 054。', 'CJK_5E97_CJK_91CC_',
  '2026-06-27T12:30:00+08:00', '2026-06-27T13:45:00+08:00',
  0, 'confirmed', '2026-06-19T00:00:00Z', '2026-06-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_055', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 055。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-06-30T14:45:00+08:00', '2026-06-30T16:15:00+08:00',
  0, 'confirmed', '2026-06-21T00:00:00Z', '2026-06-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_056', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 056。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-03-02T15:00:00+08:00', '2026-03-02T15:45:00+08:00',
  0, 'confirmed', '2026-02-20T00:00:00Z', '2026-02-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_057', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 057。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-04T16:15:00+08:00', '2026-03-04T17:15:00+08:00',
  0, 'confirmed', '2026-02-21T00:00:00Z', '2026-02-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_058', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 058。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-03-06T18:30:00+08:00', '2026-03-06T19:45:00+08:00',
  0, 'confirmed', '2026-02-22T00:00:00Z', '2026-02-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_059', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 059。', 'CJK_5E97_CJK_91CC_',
  '2026-03-08T19:45:00+08:00', '2026-03-08T21:15:00+08:00',
  0, 'confirmed', '2026-02-23T00:00:00Z', '2026-02-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_060', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 060。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-03-11T00:00:00+08:00', '2026-03-11T23:59:00+08:00',
  1, 'confirmed', '2026-03-03T00:00:00Z', '2026-03-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_061', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 061。', 'CJK_5BB6_CJK_91CC_',
  '2026-03-13T09:15:00+08:00', '2026-03-13T10:15:00+08:00',
  0, 'confirmed', '2026-03-04T00:00:00Z', '2026-03-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_062', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 062。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-03-15T10:30:00+08:00', '2026-03-15T11:45:00+08:00',
  0, 'confirmed', '2026-03-05T00:00:00Z', '2026-03-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_063', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 063。', NULL,
  '2026-03-17T11:45:00+08:00', '2026-03-17T13:15:00+08:00',
  0, 'confirmed', '2026-03-06T00:00:00Z', '2026-03-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_064', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 064。', NULL,
  '2026-03-19T12:00:00+08:00', '2026-03-19T12:45:00+08:00',
  0, 'confirmed', '2026-03-07T00:00:00Z', '2026-03-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_065', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 065。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-03-22T14:15:00+08:00', '2026-03-22T15:15:00+08:00',
  0, 'confirmed', '2026-03-09T00:00:00Z', '2026-03-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_066', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 066。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-24T15:30:00+08:00', '2026-03-24T16:45:00+08:00',
  0, 'confirmed', '2026-03-16T00:00:00Z', '2026-03-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_067', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 067。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-03-26T16:45:00+08:00', '2026-03-26T18:15:00+08:00',
  0, 'confirmed', '2026-03-17T00:00:00Z', '2026-03-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_068', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 068。', 'CJK_5E97_CJK_91CC_',
  '2026-03-28T18:00:00+08:00', '2026-03-28T18:45:00+08:00',
  0, 'confirmed', '2026-03-18T00:00:00Z', '2026-03-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_069', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 069。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-03-30T19:15:00+08:00', '2026-03-30T20:15:00+08:00',
  0, 'confirmed', '2026-03-19T00:00:00Z', '2026-03-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_070', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 070。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-04-02T08:30:00+08:00', '2026-04-02T09:45:00+08:00',
  0, 'confirmed', '2026-03-21T00:00:00Z', '2026-03-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_071', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 071。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-04T09:45:00+08:00', '2026-04-04T11:15:00+08:00',
  0, 'confirmed', '2026-03-22T00:00:00Z', '2026-03-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_072', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 072。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-04-06T00:00:00+08:00', '2026-04-06T23:59:00+08:00',
  1, 'confirmed', '2026-03-29T00:00:00Z', '2026-03-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_073', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 073。', 'CJK_5E97_CJK_91CC_',
  '2026-04-08T11:15:00+08:00', '2026-04-08T12:15:00+08:00',
  0, 'confirmed', '2026-03-30T00:00:00Z', '2026-03-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_074', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 074。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-04-10T12:30:00+08:00', '2026-04-10T13:45:00+08:00',
  0, 'confirmed', '2026-03-31T00:00:00Z', '2026-03-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_075', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 075。', 'CJK_5BB6_CJK_91CC_',
  '2026-04-13T14:45:00+08:00', '2026-04-13T16:15:00+08:00',
  0, 'confirmed', '2026-04-02T00:00:00Z', '2026-04-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_076', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 076。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-04-15T15:00:00+08:00', '2026-04-15T15:45:00+08:00',
  0, 'confirmed', '2026-04-03T00:00:00Z', '2026-04-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_077', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 077。', NULL,
  '2026-04-17T16:15:00+08:00', '2026-04-17T17:15:00+08:00',
  0, 'confirmed', '2026-04-04T00:00:00Z', '2026-04-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_078', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 078。', NULL,
  '2026-04-19T18:30:00+08:00', '2026-04-19T19:45:00+08:00',
  0, 'confirmed', '2026-04-11T00:00:00Z', '2026-04-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_079', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 079。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-04-21T19:45:00+08:00', '2026-04-21T21:15:00+08:00',
  0, 'confirmed', '2026-04-12T00:00:00Z', '2026-04-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_080', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 080。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-24T08:00:00+08:00', '2026-04-24T08:45:00+08:00',
  0, 'confirmed', '2026-04-14T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_081', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 081。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-04-26T09:15:00+08:00', '2026-04-26T10:15:00+08:00',
  0, 'confirmed', '2026-04-15T00:00:00Z', '2026-04-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_082', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 082。', 'CJK_5E97_CJK_91CC_',
  '2026-04-28T10:30:00+08:00', '2026-04-28T11:45:00+08:00',
  0, 'confirmed', '2026-04-16T00:00:00Z', '2026-04-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_083', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 083。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-04-30T11:45:00+08:00', '2026-04-30T13:15:00+08:00',
  0, 'confirmed', '2026-04-17T00:00:00Z', '2026-04-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_084', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 084。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-05-02T00:00:00+08:00', '2026-05-02T23:59:00+08:00',
  1, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_085', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 085。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-05T14:15:00+08:00', '2026-05-05T15:15:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_086', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 086。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-05-07T15:30:00+08:00', '2026-05-07T16:45:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_087', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 087。', 'CJK_5E97_CJK_91CC_',
  '2026-05-09T16:45:00+08:00', '2026-05-09T18:15:00+08:00',
  0, 'confirmed', '2026-04-28T00:00:00Z', '2026-04-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_088', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 088。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-05-11T18:00:00+08:00', '2026-05-11T18:45:00+08:00',
  0, 'confirmed', '2026-04-29T00:00:00Z', '2026-04-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_089', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 089。', 'CJK_5BB6_CJK_91CC_',
  '2026-05-13T19:15:00+08:00', '2026-05-13T20:15:00+08:00',
  0, 'confirmed', '2026-04-30T00:00:00Z', '2026-04-30T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_090', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 090。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-05-16T08:30:00+08:00', '2026-05-16T09:45:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_091', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 091。', NULL,
  '2026-05-18T09:45:00+08:00', '2026-05-18T11:15:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_092', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 092。', NULL,
  '2026-05-20T10:00:00+08:00', '2026-05-20T10:45:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_093', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 093。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-05-22T11:15:00+08:00', '2026-05-22T12:15:00+08:00',
  0, 'confirmed', '2026-05-11T00:00:00Z', '2026-05-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_094', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 094。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-24T12:30:00+08:00', '2026-05-24T13:45:00+08:00',
  0, 'confirmed', '2026-05-12T00:00:00Z', '2026-05-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_095', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 095。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-05-27T14:45:00+08:00', '2026-05-27T16:15:00+08:00',
  0, 'confirmed', '2026-05-14T00:00:00Z', '2026-05-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_096', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 096。', 'CJK_5E97_CJK_91CC_',
  '2026-05-29T00:00:00+08:00', '2026-05-29T23:59:00+08:00',
  1, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_097', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 097。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-05-31T16:15:00+08:00', '2026-05-31T17:15:00+08:00',
  0, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_098', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 098。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-06-02T18:30:00+08:00', '2026-06-02T19:45:00+08:00',
  0, 'confirmed', '2026-05-23T00:00:00Z', '2026-05-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_099', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 099。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-06-04T19:45:00+08:00', '2026-06-04T21:15:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_100', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 100。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-06-07T08:00:00+08:00', '2026-06-07T08:45:00+08:00',
  0, 'confirmed', '2026-05-26T00:00:00Z', '2026-05-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_101', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 101。', 'CJK_5E97_CJK_91CC_',
  '2026-06-09T09:15:00+08:00', '2026-06-09T10:15:00+08:00',
  0, 'confirmed', '2026-05-27T00:00:00Z', '2026-05-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_102', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 102。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-06-11T10:30:00+08:00', '2026-06-11T11:45:00+08:00',
  0, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_103', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 103。', 'CJK_5BB6_CJK_91CC_',
  '2026-06-13T11:45:00+08:00', '2026-06-13T13:15:00+08:00',
  0, 'confirmed', '2026-06-04T00:00:00Z', '2026-06-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_104', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 104。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-06-15T12:00:00+08:00', '2026-06-15T12:45:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_105', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 105。', NULL,
  '2026-06-18T14:15:00+08:00', '2026-06-18T15:15:00+08:00',
  0, 'confirmed', '2026-06-07T00:00:00Z', '2026-06-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_106', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 106。', NULL,
  '2026-06-20T15:30:00+08:00', '2026-06-20T16:45:00+08:00',
  0, 'confirmed', '2026-06-08T00:00:00Z', '2026-06-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_107', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 107。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-06-22T16:45:00+08:00', '2026-06-22T18:15:00+08:00',
  0, 'confirmed', '2026-06-09T00:00:00Z', '2026-06-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_108', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 108。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-06-24T00:00:00+08:00', '2026-06-24T23:59:00+08:00',
  1, 'confirmed', '2026-06-16T00:00:00Z', '2026-06-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_109', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 109。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-06-26T19:15:00+08:00', '2026-06-26T20:15:00+08:00',
  0, 'confirmed', '2026-06-17T00:00:00Z', '2026-06-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_110', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 110。', 'CJK_5E97_CJK_91CC_',
  '2026-06-29T08:30:00+08:00', '2026-06-29T09:45:00+08:00',
  0, 'confirmed', '2026-06-19T00:00:00Z', '2026-06-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_111', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 111。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-03-01T09:45:00+08:00', '2026-03-01T11:15:00+08:00',
  0, 'confirmed', '2026-02-18T00:00:00Z', '2026-02-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_112', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 112。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-03-03T10:00:00+08:00', '2026-03-03T10:45:00+08:00',
  0, 'confirmed', '2026-02-19T00:00:00Z', '2026-02-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_113', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 113。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-05T11:15:00+08:00', '2026-03-05T12:15:00+08:00',
  0, 'confirmed', '2026-02-20T00:00:00Z', '2026-02-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_114', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 114。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-03-07T12:30:00+08:00', '2026-03-07T13:45:00+08:00',
  0, 'confirmed', '2026-02-27T00:00:00Z', '2026-02-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_115', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 115。', 'CJK_5E97_CJK_91CC_',
  '2026-03-10T14:45:00+08:00', '2026-03-10T16:15:00+08:00',
  0, 'confirmed', '2026-03-01T00:00:00Z', '2026-03-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_116', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 116。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-03-12T15:00:00+08:00', '2026-03-12T15:45:00+08:00',
  0, 'confirmed', '2026-03-02T00:00:00Z', '2026-03-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_117', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 117。', 'CJK_5BB6_CJK_91CC_',
  '2026-03-14T16:15:00+08:00', '2026-03-14T17:15:00+08:00',
  0, 'confirmed', '2026-03-03T00:00:00Z', '2026-03-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_118', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 118。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-03-16T18:30:00+08:00', '2026-03-16T19:45:00+08:00',
  0, 'confirmed', '2026-03-04T00:00:00Z', '2026-03-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_119', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 119。', NULL,
  '2026-03-18T19:45:00+08:00', '2026-03-18T21:15:00+08:00',
  0, 'confirmed', '2026-03-05T00:00:00Z', '2026-03-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_120', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 120。', NULL,
  '2026-03-21T00:00:00+08:00', '2026-03-21T23:59:00+08:00',
  1, 'confirmed', '2026-03-13T00:00:00Z', '2026-03-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_121', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 121。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-03-23T09:15:00+08:00', '2026-03-23T10:15:00+08:00',
  0, 'confirmed', '2026-03-14T00:00:00Z', '2026-03-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_122', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 122。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-25T10:30:00+08:00', '2026-03-25T11:45:00+08:00',
  0, 'confirmed', '2026-03-15T00:00:00Z', '2026-03-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_123', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 123。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-03-27T11:45:00+08:00', '2026-03-27T13:15:00+08:00',
  0, 'confirmed', '2026-03-16T00:00:00Z', '2026-03-16T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_124', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 124。', 'CJK_5E97_CJK_91CC_',
  '2026-03-29T12:00:00+08:00', '2026-03-29T12:45:00+08:00',
  0, 'confirmed', '2026-03-17T00:00:00Z', '2026-03-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_125', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 125。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-04-01T14:15:00+08:00', '2026-04-01T15:15:00+08:00',
  0, 'confirmed', '2026-03-19T00:00:00Z', '2026-03-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_126', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 126。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-04-03T15:30:00+08:00', '2026-04-03T16:45:00+08:00',
  0, 'confirmed', '2026-03-26T00:00:00Z', '2026-03-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_127', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 127。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-05T16:45:00+08:00', '2026-04-05T18:15:00+08:00',
  0, 'confirmed', '2026-03-27T00:00:00Z', '2026-03-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_128', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 128。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-04-07T18:00:00+08:00', '2026-04-07T18:45:00+08:00',
  0, 'confirmed', '2026-03-28T00:00:00Z', '2026-03-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_129', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 129。', 'CJK_5E97_CJK_91CC_',
  '2026-04-09T19:15:00+08:00', '2026-04-09T20:15:00+08:00',
  0, 'confirmed', '2026-03-29T00:00:00Z', '2026-03-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_130', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 130。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-04-12T08:30:00+08:00', '2026-04-12T09:45:00+08:00',
  0, 'confirmed', '2026-03-31T00:00:00Z', '2026-03-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_131', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 131。', 'CJK_5BB6_CJK_91CC_',
  '2026-04-14T09:45:00+08:00', '2026-04-14T11:15:00+08:00',
  0, 'confirmed', '2026-04-01T00:00:00Z', '2026-04-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_132', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 132。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-04-16T00:00:00+08:00', '2026-04-16T23:59:00+08:00',
  1, 'confirmed', '2026-04-08T00:00:00Z', '2026-04-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_133', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 133。', NULL,
  '2026-04-18T11:15:00+08:00', '2026-04-18T12:15:00+08:00',
  0, 'confirmed', '2026-04-09T00:00:00Z', '2026-04-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_134', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 134。', NULL,
  '2026-04-20T12:30:00+08:00', '2026-04-20T13:45:00+08:00',
  0, 'confirmed', '2026-04-10T00:00:00Z', '2026-04-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_135', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 135。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-04-23T14:45:00+08:00', '2026-04-23T16:15:00+08:00',
  0, 'confirmed', '2026-04-12T00:00:00Z', '2026-04-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_136', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 136。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-25T15:00:00+08:00', '2026-04-25T15:45:00+08:00',
  0, 'confirmed', '2026-04-13T00:00:00Z', '2026-04-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_137', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 137。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-04-27T16:15:00+08:00', '2026-04-27T17:15:00+08:00',
  0, 'confirmed', '2026-04-14T00:00:00Z', '2026-04-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_138', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 138。', 'CJK_5E97_CJK_91CC_',
  '2026-04-29T18:30:00+08:00', '2026-04-29T19:45:00+08:00',
  0, 'confirmed', '2026-04-21T00:00:00Z', '2026-04-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_139', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 139。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-05-01T19:45:00+08:00', '2026-05-01T21:15:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_140', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 140。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-05-04T08:00:00+08:00', '2026-05-04T08:45:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_141', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 141。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-06T09:15:00+08:00', '2026-05-06T10:15:00+08:00',
  0, 'confirmed', '2026-04-25T00:00:00Z', '2026-04-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_142', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 142。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-05-08T10:30:00+08:00', '2026-05-08T11:45:00+08:00',
  0, 'confirmed', '2026-04-26T00:00:00Z', '2026-04-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_143', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 143。', 'CJK_5E97_CJK_91CC_',
  '2026-05-10T11:45:00+08:00', '2026-05-10T13:15:00+08:00',
  0, 'confirmed', '2026-04-27T00:00:00Z', '2026-04-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_144', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 144。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-05-12T00:00:00+08:00', '2026-05-12T23:59:00+08:00',
  1, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_145', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 145。', 'CJK_5BB6_CJK_91CC_',
  '2026-05-15T14:15:00+08:00', '2026-05-15T15:15:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_146', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 146。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-05-17T15:30:00+08:00', '2026-05-17T16:45:00+08:00',
  0, 'confirmed', '2026-05-07T00:00:00Z', '2026-05-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_147', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 147。', NULL,
  '2026-05-19T16:45:00+08:00', '2026-05-19T18:15:00+08:00',
  0, 'confirmed', '2026-05-08T00:00:00Z', '2026-05-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_148', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 148。', NULL,
  '2026-05-21T18:00:00+08:00', '2026-05-21T18:45:00+08:00',
  0, 'confirmed', '2026-05-09T00:00:00Z', '2026-05-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_149', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 149。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-05-23T19:15:00+08:00', '2026-05-23T20:15:00+08:00',
  0, 'confirmed', '2026-05-10T00:00:00Z', '2026-05-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_150', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 150。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-26T08:30:00+08:00', '2026-05-26T09:45:00+08:00',
  0, 'confirmed', '2026-05-18T00:00:00Z', '2026-05-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_151', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 151。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-05-28T09:45:00+08:00', '2026-05-28T11:15:00+08:00',
  0, 'confirmed', '2026-05-19T00:00:00Z', '2026-05-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_152', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 152。', 'CJK_5E97_CJK_91CC_',
  '2026-05-30T10:00:00+08:00', '2026-05-30T10:45:00+08:00',
  0, 'confirmed', '2026-05-20T00:00:00Z', '2026-05-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_153', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 153。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-06-01T11:15:00+08:00', '2026-06-01T12:15:00+08:00',
  0, 'confirmed', '2026-05-21T00:00:00Z', '2026-05-21T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_154', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 154。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-06-03T12:30:00+08:00', '2026-06-03T13:45:00+08:00',
  0, 'confirmed', '2026-05-22T00:00:00Z', '2026-05-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_155', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 155。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-06-06T14:45:00+08:00', '2026-06-06T16:15:00+08:00',
  0, 'confirmed', '2026-05-24T00:00:00Z', '2026-05-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_156', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 156。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-06-08T00:00:00+08:00', '2026-06-08T23:59:00+08:00',
  1, 'confirmed', '2026-05-31T00:00:00Z', '2026-05-31T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_157', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 157。', 'CJK_5E97_CJK_91CC_',
  '2026-06-10T16:15:00+08:00', '2026-06-10T17:15:00+08:00',
  0, 'confirmed', '2026-06-01T00:00:00Z', '2026-06-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_158', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 158。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-06-12T18:30:00+08:00', '2026-06-12T19:45:00+08:00',
  0, 'confirmed', '2026-06-02T00:00:00Z', '2026-06-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_159', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 159。', 'CJK_5BB6_CJK_91CC_',
  '2026-06-14T19:45:00+08:00', '2026-06-14T21:15:00+08:00',
  0, 'confirmed', '2026-06-03T00:00:00Z', '2026-06-03T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_160', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 160。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-06-17T08:00:00+08:00', '2026-06-17T08:45:00+08:00',
  0, 'confirmed', '2026-06-05T00:00:00Z', '2026-06-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_161', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 161。', NULL,
  '2026-06-19T09:15:00+08:00', '2026-06-19T10:15:00+08:00',
  0, 'confirmed', '2026-06-06T00:00:00Z', '2026-06-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_162', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 162。', NULL,
  '2026-06-21T10:30:00+08:00', '2026-06-21T11:45:00+08:00',
  0, 'confirmed', '2026-06-13T00:00:00Z', '2026-06-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_163', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 163。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-06-23T11:45:00+08:00', '2026-06-23T13:15:00+08:00',
  0, 'confirmed', '2026-06-14T00:00:00Z', '2026-06-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_164', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 164。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-06-25T12:00:00+08:00', '2026-06-25T12:45:00+08:00',
  0, 'confirmed', '2026-06-15T00:00:00Z', '2026-06-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_165', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 165。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-06-28T14:15:00+08:00', '2026-06-28T15:15:00+08:00',
  0, 'confirmed', '2026-06-17T00:00:00Z', '2026-06-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_166', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 166。', 'CJK_5E97_CJK_91CC_',
  '2026-06-30T15:30:00+08:00', '2026-06-30T16:45:00+08:00',
  0, 'confirmed', '2026-06-18T00:00:00Z', '2026-06-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_167', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 167。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-03-02T16:45:00+08:00', '2026-03-02T18:15:00+08:00',
  0, 'confirmed', '2026-02-17T00:00:00Z', '2026-02-17T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_168', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 168。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-03-04T00:00:00+08:00', '2026-03-04T23:59:00+08:00',
  1, 'confirmed', '2026-02-24T00:00:00Z', '2026-02-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_169', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 169。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-06T19:15:00+08:00', '2026-03-06T20:15:00+08:00',
  0, 'confirmed', '2026-02-25T00:00:00Z', '2026-02-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_170', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 170。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-03-09T08:30:00+08:00', '2026-03-09T09:45:00+08:00',
  0, 'confirmed', '2026-02-27T00:00:00Z', '2026-02-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_171', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 171。', 'CJK_5E97_CJK_91CC_',
  '2026-03-11T09:45:00+08:00', '2026-03-11T11:15:00+08:00',
  0, 'confirmed', '2026-02-28T00:00:00Z', '2026-02-28T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_172', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 172。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-03-13T10:00:00+08:00', '2026-03-13T10:45:00+08:00',
  0, 'confirmed', '2026-03-01T00:00:00Z', '2026-03-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_173', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 173。', 'CJK_5BB6_CJK_91CC_',
  '2026-03-15T11:15:00+08:00', '2026-03-15T12:15:00+08:00',
  0, 'confirmed', '2026-03-02T00:00:00Z', '2026-03-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_174', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 174。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-03-17T12:30:00+08:00', '2026-03-17T13:45:00+08:00',
  0, 'confirmed', '2026-03-09T00:00:00Z', '2026-03-09T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_175', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 175。', NULL,
  '2026-03-20T14:45:00+08:00', '2026-03-20T16:15:00+08:00',
  0, 'confirmed', '2026-03-11T00:00:00Z', '2026-03-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_176', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 176。', NULL,
  '2026-03-22T15:00:00+08:00', '2026-03-22T15:45:00+08:00',
  0, 'confirmed', '2026-03-12T00:00:00Z', '2026-03-12T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_177', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 177。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-03-24T16:15:00+08:00', '2026-03-24T17:15:00+08:00',
  0, 'confirmed', '2026-03-13T00:00:00Z', '2026-03-13T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_178', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 178。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-03-26T18:30:00+08:00', '2026-03-26T19:45:00+08:00',
  0, 'confirmed', '2026-03-14T00:00:00Z', '2026-03-14T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_179', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 179。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-03-28T19:45:00+08:00', '2026-03-28T21:15:00+08:00',
  0, 'confirmed', '2026-03-15T00:00:00Z', '2026-03-15T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_180', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 180。', 'CJK_5E97_CJK_91CC_',
  '2026-03-31T00:00:00+08:00', '2026-03-31T23:59:00+08:00',
  1, 'confirmed', '2026-03-23T00:00:00Z', '2026-03-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_181', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 181。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-04-02T09:15:00+08:00', '2026-04-02T10:15:00+08:00',
  0, 'confirmed', '2026-03-24T00:00:00Z', '2026-03-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_182', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 182。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-04-04T10:30:00+08:00', '2026-04-04T11:45:00+08:00',
  0, 'confirmed', '2026-03-25T00:00:00Z', '2026-03-25T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_183', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 183。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-06T11:45:00+08:00', '2026-04-06T13:15:00+08:00',
  0, 'confirmed', '2026-03-26T00:00:00Z', '2026-03-26T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_184', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 184。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-04-08T12:00:00+08:00', '2026-04-08T12:45:00+08:00',
  0, 'confirmed', '2026-03-27T00:00:00Z', '2026-03-27T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_185', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 185。', 'CJK_5E97_CJK_91CC_',
  '2026-04-11T14:15:00+08:00', '2026-04-11T15:15:00+08:00',
  0, 'confirmed', '2026-03-29T00:00:00Z', '2026-03-29T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_186', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 186。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-04-13T15:30:00+08:00', '2026-04-13T16:45:00+08:00',
  0, 'confirmed', '2026-04-05T00:00:00Z', '2026-04-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_187', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 187。', 'CJK_5BB6_CJK_91CC_',
  '2026-04-15T16:45:00+08:00', '2026-04-15T18:15:00+08:00',
  0, 'confirmed', '2026-04-06T00:00:00Z', '2026-04-06T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_188', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 188。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-04-17T18:00:00+08:00', '2026-04-17T18:45:00+08:00',
  0, 'confirmed', '2026-04-07T00:00:00Z', '2026-04-07T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_189', 'cal_wang_fang', 'CJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_verify', 'verifyCJK_8FD1_CJK_4E00_CJK_5468_CJK_671F_CJK_5237_CJK_5361_CJK_6D88_CJK_8D39_CJK_548C_CJK_81EA_CJK_52A8_repayment。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 189。', NULL,
  '2026-04-19T19:15:00+08:00', '2026-04-19T20:15:00+08:00',
  0, 'confirmed', '2026-04-08T00:00:00Z', '2026-04-08T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_190', 'cal_wang_fang', 'CJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_63D0_CJK_9192_', 'CJK_68C0_CJK_67E5_CJK_5E97_CJK_94FA_CJK_548C_CJK_5BB6_CJK_91CC_ofCJK_6C34_CJK_7535_CJK_71C3_CJK_6C14_CJK_7F34_CJK_8D39_CJK_60C5_CJK_51B5_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 190。', NULL,
  '2026-04-22T08:30:00+08:00', '2026-04-22T09:45:00+08:00',
  0, 'confirmed', '2026-04-10T00:00:00Z', '2026-04-10T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_191', 'cal_wang_fang', 'CJK_5BB6_CJK_5EAD_CJK_805A_CJK_9910_', 'CJK_548C_CJK_7236_CJK_6BCD_CJK_5403_CJK_996D_，CJK_987A_CJK_4FBF_CJK_804A_CJK_6700_CJK_8FD1_CJK_5BB6_CJK_91CC_ofCJK_4E8B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 191。', 'CJK_7236_CJK_6BCD_CJK_5BB6_',
  '2026-04-24T09:45:00+08:00', '2026-04-24T11:15:00+08:00',
  0, 'confirmed', '2026-04-11T00:00:00Z', '2026-04-11T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_192', 'cal_wang_fang', 'CJK_5FEB_CJK_9012_CJK_7B7E_CJK_6536_CJK_63D0_CJK_9192_', 'CJK_7559_CJK_610F_CJK_95E8_CJK_5E97_CJK_5FEB_CJK_9012_andCJK_6837_CJK_8863_CJK_5305_CJK_88F9_CJK_7B7E_CJK_6536_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 192。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-04-26T00:00:00+08:00', '2026-04-26T23:59:00+08:00',
  1, 'confirmed', '2026-04-18T00:00:00Z', '2026-04-18T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_193', 'cal_wang_fang', 'CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_62FF_CJK_8D27_', 'CJK_53BB_CJK_56DB_CJK_5B63_CJK_9752_CJK_770B_CJK_770B_CJK_65B0_CJK_8D27_CJK_548C_CJK_4EF7_CJK_683C_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 193。', 'HangzhouCJK_56DB_CJK_5B63_CJK_9752_',
  '2026-04-28T11:15:00+08:00', '2026-04-28T12:15:00+08:00',
  0, 'confirmed', '2026-04-19T00:00:00Z', '2026-04-19T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_194', 'cal_wang_fang', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_786E_CJK_8BA4_', 'CJK_786E_CJK_8BA4_CJK_5468_CJK_672B_CJK_6392_CJK_73ED_、CJK_8C03_CJK_4F11_CJK_548C_CJK_52A0_CJK_73ED_CJK_9910_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 194。', 'CJK_5E97_CJK_91CC_',
  '2026-04-30T12:30:00+08:00', '2026-04-30T13:45:00+08:00',
  0, 'confirmed', '2026-04-20T00:00:00Z', '2026-04-20T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_195', 'cal_wang_fang', 'CJK_5973_CJK_513F_CJK_5174_CJK_8DA3_CJK_73ED_CJK_63A5_CJK_9001_', 'CJK_5B89_CJK_6392_CJK_5468_CJK_672B_CJK_63A5_CJK_9001_CJK_548C_CJK_8BFE_CJK_540E_CJK_665A_CJK_996D_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 195。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C11_yearCJK_5BAB_',
  '2026-05-03T14:45:00+08:00', '2026-05-03T16:15:00+08:00',
  0, 'confirmed', '2026-04-22T00:00:00Z', '2026-04-22T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_196', 'cal_wang_fang', 'CJK_7F8E_CJK_5BB9_CJK_7F8E_CJK_53D1_CJK_9884_CJK_7EA6_', 'CJK_4F8B_CJK_884C_CJK_62A4_CJK_7406_，CJK_987A_CJK_4FBF_CJK_4F11_CJK_606F_CJK_4E00_CJK_4E0B_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 196。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5546_CJK_5708_',
  '2026-05-05T15:00:00+08:00', '2026-05-05T15:45:00+08:00',
  0, 'confirmed', '2026-04-23T00:00:00Z', '2026-04-23T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_197', 'cal_wang_fang', 'CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_65B0_CJK_76D8_CJK_70B9_', 'verifyCJK_672C_CJK_5468_CJK_5230_CJK_8D27_CJK_6B3E_CJK_5F0F_、CJK_5C3A_CJK_7801_CJK_548C_CJK_8865_CJK_8D27_needCJK_6C42_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 197。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_670D_CJK_88C5_CJK_5E97_',
  '2026-05-07T16:15:00+08:00', '2026-05-07T17:15:00+08:00',
  0, 'confirmed', '2026-04-24T00:00:00Z', '2026-04-24T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_198', 'cal_wang_fang', 'CJK_4F9B_shouldCJK_5546_CJK_5BF9_CJK_6B3E_', 'CJK_8DDF_CJK_8FDB_CJK_5C3E_CJK_6B3E_、CJK_9000_CJK_6362_CJK_8D27_CJK_548C_CJK_4E0B_CJK_6279_CJK_53D1_CJK_8D27_CJK_8282_CJK_594F_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 198。', 'CJK_89C6_CJK_9891_CJK_901A_CJK_8BDD_',
  '2026-05-09T18:30:00+08:00', '2026-05-09T19:45:00+08:00',
  0, 'confirmed', '2026-05-01T00:00:00Z', '2026-05-01T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_199', 'cal_wang_fang', 'CJK_76F4_CJK_64AD_CJK_770B_CJK_6B3E_', 'CJK_770B_CJK_6279_CJK_53D1_CJK_5E02_CJK_573A_CJK_76F4_CJK_64AD_CJK_9009_CJK_79CB_CJK_88C5_CJK_65B0_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 199。', 'CJK_5E97_CJK_91CC_',
  '2026-05-11T19:45:00+08:00', '2026-05-11T21:15:00+08:00',
  0, 'confirmed', '2026-05-02T00:00:00Z', '2026-05-02T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_200', 'cal_wang_fang', 'CJK_5E97_CJK_94FA_CJK_8425_CJK_4E1A_CJK_590D_CJK_76D8_', 'recordCJK_672C_CJK_5468_CJK_5BA2_CJK_6D41_、CJK_8FDE_CJK_5E26_CJK_9500_CJK_552E_CJK_548C_CJK_6EDE_CJK_9500_CJK_6B3E_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 200。', 'CJK_5E97_CJK_91CC_CJK_540E_CJK_4ED3_',
  '2026-05-14T08:00:00+08:00', '2026-05-14T08:45:00+08:00',
  0, 'confirmed', '2026-05-04T00:00:00Z', '2026-05-04T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_201', 'cal_wang_fang', 'CJK_5BB6_CJK_957F_CJK_4F1A_prepare', 'CJK_6574_CJK_7406_CJK_5973_CJK_513F_CJK_5B66_CJK_6821_noticeCJK_548C_CJK_8001_CJK_5E08_CJK_6C9F_CJK_901A_matter。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 201。', 'CJK_5BB6_CJK_91CC_',
  '2026-05-16T09:15:00+08:00', '2026-05-16T10:15:00+08:00',
  0, 'confirmed', '2026-05-05T00:00:00Z', '2026-05-05T00:00:00Z', NULL, NULL);

INSERT INTO events (event_id, calendar_id, summary, description, location,
                    start_dt, end_dt, all_day, status, created_at, updated_at,
                    recurrence_rule, parent_event_id) VALUES
 ('evt_bg_202', 'cal_wang_fang', 'CJK_793E_CJK_533A_CJK_533B_CJK_9662_CJK_590D_CJK_8BCA_', 'CJK_5E38_CJK_89C4_CJK_590D_CJK_8BCA_，CJK_987A_CJK_4FBF_CJK_95EE_CJK_7761_CJK_7720_CJK_548C_CJK_9888_CJK_690E_CJK_95EE_CJK_9898_。CJK_5907_CJK_6CE8_：CJK_5B89_CJK_6392_record 202。', 'CJK_897F_CJK_6E56_CJK_533A_CJK_793E_CJK_533A_CJK_533B_CJK_9662_',
  '2026-05-18T10:30:00+08:00', '2026-05-18T11:45:00+08:00',
  0, 'confirmed', '2026-05-06T00:00:00Z', '2026-05-06T00:00:00Z', NULL, NULL);

INSERT INTO _counters (key, value) VALUES
 ('event_seq', 500),
 ('attendee_seq', 0),
 ('reminder_seq', 0);

-- Stage 0 CJK_4EC5_CJK_52A0_CJK_8F7D_CJK_53C2_CJK_8003_dayCJK_524D_alreadyCJK_7ECF_CJK_5B58_atofdayCJK_5386_record；notCJK_6765_CJK_5B89_CJK_6392_canCJK_4EE5_CJK_4FDD_CJK_7559_，CJK_4F46_CJK_521B_CJK_5EFA_CNYCJK_6570_CJK_636E_CJK_4E0D_CJK_5F97_CJK_665A_CJK_4E8E_CJK_53C2_CJK_8003_day。
UPDATE events
SET created_at = '2026-05-19T08:00:00Z',
    updated_at = CASE
      WHEN updated_at > '2026-05-20T23:59:59' THEN '2026-05-19T08:00:00Z'
      ELSE updated_at
    END
WHERE event_id LIKE 'evt_bg_%'
  AND created_at > '2026-05-20T23:59:59';

COMMIT;
