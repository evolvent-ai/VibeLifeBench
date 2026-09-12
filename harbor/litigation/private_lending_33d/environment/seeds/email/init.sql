-- emails-mcp wang_fang_lending — init.sql
-- Wang FangofCJK_4E2A_CJK_4EBA_CJK_90AE_CJK_7BB1_CJK_5FEB_CJK_7167_, private lendingCJK_8FFD_CJK_507F_CJK_573A_CJK_666F_. Reference frame: 2026-05-20.
-- CJK_90AE_CJK_4EF6_CJK_57CB_CJK_7740_caseCJK_5173_CJK_952E_CJK_4E8B_CJK_5B9E_(CJK_9690_CJK_542B_CJK_7EA6_CJK_675F_CJK_4F9D_CJK_636E_), CJK_7EDD_CJK_4E0D_CJK_76F4_CJK_63A5_CJK_70B9_CJK_660E_CJK_6CD5_CJK_5F8B_CJK_7ED3_CJK_8BBA_。CJK_672C_CJK_6848_is"CJK_53CD_CJK_76F4_CJK_89C9_CJK_96F7_CJK_533A_":
-- CJK_90AE_CJK_4EF6_CJK_4FDD_CJK_7559_CJK_5F53_CJK_4E8B_CJK_4EBA_ofCJK_539F_CJK_59CB_CJK_8BF4_CJK_6CD5_andCJK_4E0D_CJK_786E_CJK_5B9A_CJK_8BA4_CJK_8BC6_，needCJK_7ED3_CJK_5408_CJK_5176_CJK_4ED6_materialsCJK_4EA4_CJK_53C9_verify。
--
-- CJK_6848_CJK_60C5_: Wang Fang(CJK_51FA_CJK_501F_CJK_4EBA_, HangzhouCJK_897F_CJK_6E56_CJK_533A_)CJK_501F_CJK_94B1_CJK_7ED9_CJK_8001_CJK_540C_CJK_5B66_Chen Qiang(loanCJK_4EBA_, Ningbo), Chen QiangCJK_4E0D_CJK_8FD8_, prepareCJK_8D77_CJK_8BC9_CJK_8FFD_CJK_507F_。
-- CJK_6838_CJK_5FC3_CJK_9677_CJK_9631_(CJK_6BCF_CJK_4E2A_CJK_90FD_has email CJK_4E8B_CJK_5B9E_CJK_4F9D_CJK_636E_ + legal_search precedentCJK_951A_CJK_70B9_):
--   ① CJK_780D_CJK_5934_CJK_606F_CJK_9677_CJK_9631_: No.CJK_4E00_CJK_7B14_IOUCJK_8F7D_CJK_660E_40CJK_4E07_, CJK_4F46_CJK_8F6C_CJK_8D26_CJK_65F6_CJK_9884_CJK_5148_CJK_6263_CJK_4E86_4CJK_4E07_interest, actually received36CJK_4E07_ →
--      principalunderactually received36CJK_4E07_CJK_8BA4_CJK_5B9A_(CJK_951A_ case_001 / art_mcc_670 / art_jd_26), CJK_800C_CJK_975E_IOU40CJK_4E07_。
--   ② CJK_5927_CJK_989D_cashCJK_4EA4_CJK_4ED8_CJK_9677_CJK_9631_: No.CJK_4E8C_CJK_7B14_IOUCJK_8F7D_CJK_660E_20CJK_4E07_CJK_79F0_CJK_4EE5_"cash"CJK_4EA4_CJK_4ED8_, CJK_4F46_noneCJK_4EFB_CJK_4F55_CJK_53D6_CJK_73B0_/CJK_8F6C_CJK_8D26_CJK_51ED_CJK_8BC1_ →
--      CJK_4E3E_CJK_8BC1_CJK_56F0_CJK_96BE_, canCJK_80FD_CJK_88AB_CJK_8BA4_CJK_5B9A_CJK_4EA4_CJK_4ED8_CJK_4E0D_CJK_80FD_CJK_6210_CJK_7ACB_(CJK_951A_ case_003 CJK_53CD_CJK_9762_ / art_zj_cash), CJK_987B_CJK_5982_CJK_5B9E_CJK_63D0_CJK_793A_CJK_98CE_CJK_9669_。
--   ③ CJK_65F6_CJK_6548_CJK_9677_CJK_9631_: loan2024-06-10maturity, CJK_8DDD_CJK_4ECA_CJK_7EA6_2year, CJK_6BCD_CJK_4EB2_CJK_8BEF_CJK_4F20_"CJK_4E24_yearCJK_591A_CJK_5FEB_CJK_8FC7_CJK_671F_CJK_4E86_"(CJK_9519_, CJK_65F6_CJK_6548_3year);
--      CJK_4E14_Chen Qiang2025-02CJK_90E8_CJK_5206_repayment2CJK_4E07_+WeChat"CJK_5269_CJK_4E0B_ofCJK_6211_CJK_4F1A_CJK_8FD8_" → CJK_65F6_CJK_6548_inCJK_65AD_, CJK_81EA_2025-02CJK_91CD_CJK_65B0_CJK_8BA1_3year → CJK_8FDC_atCJK_65F6_CJK_6548_within。
--   ④ CJK_4FDD_CJK_8BC1_CJK_671F_CJK_95F4_CJK_9677_CJK_9631_: No.CJK_4E00_CJK_7B14_IOUCJK_4E0A_CJK_8001_CJK_5468_CJK_7B7E_"security"notCJK_5199_CJK_65B9_CJK_5F0F_/CJK_671F_CJK_95F4_ → CJK_7EA6_CJK_5B9A_CJK_4E0D_CJK_660E_underCJK_4E00_CJK_822C_CJK_4FDD_CJK_8BC1_(CJK_5148_CJK_8BC9_CJK_6297_CJK_8FA9_CJK_6743_),
--      notCJK_7EA6_CJK_5B9A_CJK_4FDD_CJK_8BC1_CJK_671F_CJK_95F4_=CJK_4E3B_CJK_503A_CJK_52A1_maturity(2024-06-10)CJK_540E_6CJK_4E2A_monthto2024-12-10; Wang FangfromnotatCJK_671F_CJK_95F4_withinCJK_5355_CJK_72EC_CJK_5411_CJK_8001_CJK_5468_
--      CJK_4E3B_CJK_5F20_ → CJK_4FDD_CJK_8BC1_CJK_671F_CJK_95F4_CJK_5C4A_CJK_6EE1_, CJK_8001_CJK_5468_CJK_514D_CJK_8D23_(CJK_951A_ case_004)。CJK_53CD_CJK_76F4_CJK_89C9_: Wang FangCJK_4EE5_is"hasguarantorCJK_5C31_CJK_7A33_CJK_4E86_"。
--   ⑤ CJK_592B_CJK_59BB_CJK_5171_CJK_540C_CJK_503A_CJK_52A1_CJK_9677_CJK_9631_: Chen QiangalreadyCJK_5A5A_, loanCJK_7528_CJK_4E8E_CJK_5176_CJK_4E2A_CJK_4EBA_CJK_7092_CJK_80A1_CJK_4E8F_CJK_635F_(CJK_8D85_CJK_51FA_CJK_5BB6_CJK_5EAD_dayCJK_5E38_、CJK_975E_CJK_5171_CJK_540C_CJK_7ECF_CJK_8425_),
--      Wang FangnoneevidenceCJK_8BC1_CJK_660E_CJK_7528_CJK_4E8E_CJK_592B_CJK_59BB_CJK_5171_CJK_540C_CJK_751F_CJK_6D3B_ → CJK_4E0D_CJK_80FD_requirespouseCJK_5218_CJK_67D0_CJK_5171_CJK_540C_CJK_8FD8_(CJK_951A_ case_006)。
--   CJK_5229_CJK_7387_: CJK_7EA6_CJK_5B9A_monthly interest2%(year24%)CJK_8D85_CJK_8FC7_CJK_5408_CJK_540C_CJK_6210_CJK_7ACB_CJK_65F6_(2023-06)CJK_4E00_yearCJK_671F_LPRCJK_56DB_CJK_500D_ → CJK_8D85_CJK_51FA_CJK_90E8_CJK_5206_CJK_4E0D_CJK_652F_CJK_6301_(CJK_951A_ case_002)。
-- body_text only. id CJK_624B_CJK_52A8_CJK_6307_CJK_5B9A_CJK_4EE5_CJK_4FBF_CJK_590D_CJK_73B0_。

PRAGMA journal_mode = DELETE;

BEGIN;

DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'wang.fang@gmail.com', 'Wang Fang (Wang Fang)', '2018-03-15T00:00:00Z');

DELETE FROM folders;
INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam'),
  (6, 'Family'),
  (7, 'Lending');

-- =========================================================================
-- INBOX (folder_id = 1)
-- =========================================================================

-- No.CJK_4E00_CJK_7B14_IOU(CJK_5173_CJK_952E_!) — 2023-06-10 IOUCJK_8F7D_CJK_660E_40CJK_4E07_, monthly interest2%, CJK_8001_CJK_5468_"security"notCJK_5199_CJK_65B9_CJK_5F0F_/CJK_671F_CJK_95F4_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20230610-iou1-bak@wang-fang>', '【CJK_5907_CJK_4EFD_】Chen QiangIOU(No.CJK_4E00_CJK_7B14_)CJK_62CD_CJK_7167_', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2023-06-10T21:00:00Z',
   'CJK_5907_CJK_4EFD_No.CJK_4E00_CJK_7B14_IOU(CJK_539F_CJK_4EF6_atCJK_6211_CJK_624B_CJK_91CC_)。IOUcontent："CJK_4ECA_CJK_501F_CJK_5230_Wang FangCNYCJK_8086_CJK_62FE_ten-thousand CNYCJK_6574_(400000CNY)，monthCJK_5229_CJK_7387_2%，CJK_501F_CJK_671F_CJK_4E00_year，CJK_4E8E_2024year6month10dayCJK_524D_CJK_8FD8_CJK_6E05_。loanCJK_4EBA_：Chen Qiang。guarantor：Zhou Guohua(CJK_7B7E_CJK_5B57_)。2023year6month10day。"——CJK_6CE8_:CJK_8001_CJK_5468_(Zhou Guohua)CJK_53EA_atCJK_4E0B_CJK_9762_CJK_7B7E_CJK_4E86_CJK_540D_CJK_5199_CJK_4E86_"security"CJK_4E24_CJK_4E2A_CJK_5B57_，CJK_6CA1_CJK_5199_isCJK_8FDE_CJK_5E26_CJK_8FD8_isCJK_4E00_CJK_822C_，CJK_4E5F_CJK_6CA1_CJK_5199_securityCJK_591A_CJK_4E45_。',
   1, 1, '{}', 300, '2023-06-10T21:00:00Z');

-- No.CJK_4E00_CJK_7B14_actually received(CJK_780D_CJK_5934_CJK_606F_CJK_9677_CJK_9631_CJK_5173_CJK_952E_!) — CJK_8F6C_CJK_8D26_40CJK_4E07_CJK_4F46_CJK_9884_CJK_5148_CJK_6263_CJK_4E86_4CJK_4E07_interest, actually received36CJK_4E07_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (2, 1, '<20230610-transfer@icbc.com>', '【CJK_5DE5_CJK_5546_bank】transfer receipt', 'notice@icbc.com.cn', '["wang.fang@gmail.com"]',
   '2023-06-10T15:30:00Z',
   'CJK_5C0A_CJK_656C_ofWang FangCJK_5973_CJK_58EB_：CJK_60A8_CJK_4E8E_2023year6month10dayCJK_5411_CJK_6536_CJK_6B3E_CJK_4EBA_Chen Qiang(CJK_5C3E_No.8821)CJK_8F6C_CJK_8D26_CNY360000CNY，CJK_8F6C_CJK_8D26_CJK_6210_CJK_529F_。CJK_5907_CJK_6CE8_:loan。——CJK_6E29_CJK_99A8_CJK_63D0_CJK_793A_:CJK_672C_CJK_6B21_CJK_8F6C_CJK_8D26_CJK_91D1_CJK_989D_is36ten-thousand CNY。(Wang FangCJK_81EA_CJK_6CE8_:IOUCJK_5199_ofis40CJK_4E07_，CJK_4F46_Chen QiangCJK_5F53_CJK_573A_CJK_8BF4_"CJK_5934_CJK_4E24_CJK_4E2A_monthinterestCJK_5148_CJK_6263_CJK_4E86_"，CJK_8BA9_CJK_6211_CJK_53EA_CJK_8F6C_CJK_4E86_36CJK_4E07_，CJK_90A3_4CJK_4E07_CJK_7B97_isCJK_5148_CJK_4ED8_ofinterest。)',
   1, 1, '{}', 320, '2023-06-10T15:30:00Z');

-- No.CJK_4E8C_CJK_7B14_IOU(CJK_5927_CJK_989D_cashCJK_4EA4_CJK_4ED8_CJK_9677_CJK_9631_!) — 2023-09-15 IOUCJK_8F7D_CJK_660E_20CJK_4E07_, CJK_79F0_cashCJK_4EA4_CJK_4ED8_, noneCJK_4EFB_CJK_4F55_CJK_51ED_CJK_8BC1_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (3, 1, '<20230915-iou2-bak@wang-fang>', '【CJK_5907_CJK_4EFD_】Chen QiangIOU(No.CJK_4E8C_CJK_7B14_)CJK_62CD_CJK_7167_', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2023-09-15T20:30:00Z',
   'CJK_5907_CJK_4EFD_No.CJK_4E8C_CJK_7B14_IOU。IOUcontent："CJK_4ECA_CJK_501F_CJK_5230_Wang FangCNYCJK_8D30_CJK_62FE_ten-thousand CNYCJK_6574_(200000CNY)cash，monthCJK_5229_CJK_7387_2%，CJK_501F_CJK_671F_CJK_4E00_year。loanCJK_4EBA_：Chen Qiang。2023year9month15day。"——CJK_8FD9_20CJK_4E07_isCJK_6211_CJK_90A3_CJK_9635_CJK_5B50_CJK_653E_CJK_5BB6_CJK_91CC_ofcash，CJK_5206_CJK_51E0_CJK_6B21_CJK_53D6_ofCJK_96F6_CJK_94B1_CJK_51D1_of，CJK_76F4_CJK_63A5_CJK_5F53_CJK_9762_CJK_7ED9_ofChen Qiang，CJK_6CA1_CJK_8D70_bankCJK_8F6C_CJK_8D26_，CJK_4E5F_CJK_6CA1_CJK_8BA9_CJK_4ED6_CJK_5199_CJK_6536_CJK_6761_。CJK_5F53_CJK_65F6_CJK_60F3_CJK_7740_CJK_90FD_isCJK_8001_CJK_540C_CJK_5B66_，CJK_6CA1_CJK_90A3_CJK_4E48_CJK_591A_CJK_8BB2_CJK_7A76_。',
   1, 1, '{}', 300, '2023-09-15T20:30:00Z');

-- WeChatcollection + Chen QiangCJK_90E8_CJK_5206_repayment(CJK_65F6_CJK_6548_inCJK_65AD_CJK_9677_CJK_9631_CJK_5173_CJK_952E_!) — 2025-02 CJK_8FD8_2CJK_4E07_ + "CJK_5269_CJK_4E0B_ofCJK_6211_CJK_4F1A_CJK_8FD8_"
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (4, 1, '<20250215-wechat-bak@wang-fang>', '【CJK_5907_CJK_4EFD_】Chen QiangrepaymentCJK_548C_collectionWeChatrecord', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-02-15T22:00:00Z',
   'CJK_5907_CJK_4EFD_collectionrecord(WeChatCJK_539F_CJK_59CB_recordatCJK_624B_CJK_673A_CJK_91CC_)。2024year6monthmaturityCJK_540E_Chen QiangCJK_4E00_CJK_76F4_CJK_62D6_。2025year2month15dayCJK_4ED6_CJK_8F6C_CJK_7ED9_CJK_6211_2ten-thousand CNY(WeChatCJK_8F6C_CJK_8D26_recordCJK_6211_CJK_7559_CJK_7740_)，andCJK_53D1_CJK_6D88_CJK_606F_CJK_8BF4_:"CJK_82B3_CJK_59D0_CJK_5BF9_CJK_4E0D_CJK_4F4F_，CJK_6700_CJK_8FD1_CJK_624B_CJK_5934_CJK_7D27_，CJK_5148_CJK_8FD8_CJK_4F60_2CJK_4E07_shouldshouldCJK_6025_，CJK_5269_CJK_4E0B_ofCJK_6211_CJK_80AF_CJK_5B9A_CJK_4F1A_CJK_8FD8_，CJK_518D_CJK_5BBD_CJK_9650_CJK_6211_CJK_70B9_CJK_65F6_CJK_95F4_。"——CJK_4E4B_CJK_540E_CJK_53C8_CJK_62D6_CJK_5230_CJK_73B0_at，CJK_50AC_CJK_4E86_CJK_597D_CJK_51E0_CJK_6B21_CJK_90FD_CJK_8BF4_CJK_6CA1_CJK_94B1_。',
   1, 1, '{}', 300, '2025-02-15T22:00:00Z');

-- CJK_6BCD_CJK_4EB2_(CJK_5E72_CJK_6270_ + CJK_8BEF_CJK_5BFC_: "CJK_4E24_yearCJK_591A_CJK_4E86_CJK_8FD8_CJK_80FD_CJK_8981_CJK_5417_" → CJK_5F3A_CJK_5316_CJK_65F6_CJK_6548_CJK_5047_CJK_8C61_)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (5, 1, '<20260510-mom@family.local>', 'Chen QiangCJK_90A3_CJK_7B14_CJK_94B1_', 'CJK_674E_CJK_79C0_CJK_82F1_ <lixiuying.mom@163.com>', '["wang.fang@gmail.com"]',
   '2026-05-10T19:30:00Z',
   'CJK_82B3_CJK_82B3_，Chen QiangCJK_501F_CJK_4F60_CJK_90A3_CJK_7B14_CJK_94B1_CJK_90FD_CJK_4E24_yearCJK_591A_CJK_4E86_，CJK_4F60_CJK_8205_CJK_8BF4_CJK_544A_CJK_4EBA_hasdeadline，CJK_8D85_CJK_8FC7_CJK_4E24_yearisCJK_4E0D_isCJK_5C31_CJK_8981_CJK_4E0D_CJK_56DE_CJK_6765_CJK_4E86_？CJK_8981_CJK_5F04_CJK_5C31_CJK_8D76_CJK_7D27_，CJK_522B_CJK_62D6_CJK_6CA1_CJK_4E86_。CJK_8FD8_hasCJK_4ED6_CJK_8001_CJK_5A46_CJK_4E0D_isCJK_4E5F_CJK_8BE5_CJK_4E00_CJK_8D77_CJK_8FD8_CJK_5417_？CJK_4F60_CJK_4EEC_CJK_4E24_CJK_53E3_CJK_5B50_ofCJK_503A_。CJK_6CE8_CJK_610F_CJK_8EAB_CJK_4F53_。 — CJK_5988_',
   1, 0, '{}', 200, '2026-05-10T19:30:00Z');

-- Chen QiangCJK_5356_CJK_623F_CJK_7EBF_CJK_7D22_(property preservationCJK_4F9D_CJK_636E_) — inCJK_4ECB_CJK_7FA4_CJK_6D88_CJK_606F_CJK_8F6C_CJK_53D1_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (6, 1, '<20260517-house@friend.local>', 'Chen QiangisCJK_4E0D_isCJK_8981_CJK_628A_CJK_623F_CJK_5B50_CJK_5356_CJK_4E86_', 'CJK_8D75_CJK_59D0_ <zhao.jie@qq.com>', '["wang.fang@gmail.com"]',
   '2026-05-17T12:00:00Z',
   'CJK_82B3_CJK_554A_，CJK_6211_atNingboCJK_4E8C_CJK_624B_CJK_623F_inCJK_4ECB_CJK_7FA4_CJK_91CC_CJK_770B_CJK_5230_Chen QiangCJK_540D_CJK_4E0B_CJK_6D77_CJK_66D9_CJK_90A3_CJK_5957_CJK_623F_CJK_5B50_CJK_6302_CJK_724C_CJK_6025_CJK_552E_，CJK_6807_CJK_6CE8_"CJK_8BDA_CJK_610F_CJK_5356_、canCJK_4F4E_CJK_4E8E_CJK_5E02_CJK_573A_CJK_4EF7_"。CJK_4ED6_isCJK_4E0D_isCJK_60F3_CJK_628A_CJK_623F_CJK_5B50_CJK_5904_CJK_7406_CJK_4E86_CJK_8DD1_CJK_8DEF_CJK_554A_？CJK_4F60_CJK_90A3_CJK_94B1_canCJK_5F97_CJK_8D76_CJK_7D27_CJK_60F3_CJK_529E_CJK_6CD5_，CJK_522B_CJK_7B49_CJK_4ED6_CJK_628A_CJK_623F_CJK_5B50_CJK_8FC7_CJK_6237_CJK_4E86_CJK_5C31_CJK_6293_CJK_4E0D_CJK_7740_CJK_4E86_。',
   1, 1, '{}', 200, '2026-05-17T12:00:00Z');

-- CJK_524D_CJK_540C_CJK_4E8B_(loanCJK_7528_CJK_9014_CJK_7EBF_CJK_7D22_: Chen QiangCJK_7528_CJK_4E8E_CJK_4E2A_CJK_4EBA_CJK_7092_CJK_80A1_CJK_4E8F_CJK_635F_, CJK_975E_CJK_5BB6_CJK_5EAD_/CJK_5171_CJK_540C_CJK_7ECF_CJK_8425_)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (7, 1, '<20260514-classmate@old.local>', 'Chen QiangofCJK_4E8B_CJK_6211_CJK_77E5_CJK_9053_CJK_70B9_', 'CJK_8001_CJK_540C_CJK_5B66_CJK_6797_CJK_6D9B_ <lintao@163.com>', '["wang.fang@gmail.com"]',
   '2026-05-14T21:00:00Z',
   'Wang Fang，CJK_542C_CJK_8BF4_Chen QiangCJK_6B20_CJK_4F60_CJK_94B1_CJK_4E0D_CJK_8FD8_。CJK_8DDF_CJK_4F60_CJK_8BF4_CJK_53E5_CJK_5B9E_CJK_8BDD_，CJK_4ED6_CJK_501F_ofCJK_94B1_CJK_6839_CJK_672C_CJK_4E0D_isCJK_505A_CJK_4EC0_CJK_4E48_CJK_751F_CJK_610F_CJK_5468_CJK_8F6C_，isCJK_62FF_CJK_53BB_CJK_7092_CJK_80A1_CJK_52A0_CJK_6760_CJK_6746_，CJK_5168_CJK_4E8F_CJK_8FDB_CJK_53BB_CJK_4E86_，CJK_4ED6_CJK_8001_CJK_5A46_Liu MinCJK_5F53_CJK_65F6_CJK_8FD8_CJK_8DDF_CJK_4ED6_CJK_5927_CJK_5435_，CJK_8BF4_CJK_8FD9_isCJK_4ED6_CJK_81EA_CJK_5DF1_CJK_778E_CJK_641E_of，CJK_4E0D_CJK_8BA4_CJK_8FD9_CJK_4E2A_CJK_8D26_。CJK_4F60_CJK_8981_CJK_6253_CJK_5B98_CJK_53F8_CJK_6211_canCJK_4EE5_CJK_5E2E_CJK_4F60_CJK_8BF4_CJK_8BF4_CJK_5F53_CJK_65F6_ofCJK_60C5_CJK_51B5_。',
   1, 0, '{}', 220, '2026-05-14T21:00:00Z');

-- Wang FangCJK_81EA_CJK_5DF1_of"CJK_627E_lawyerCJK_9884_CJK_7B97_"CJK_5907_CJK_5FD8_(CJK_672C_CJK_4EBA_CJK_5907_CJK_4EFD_) — lawyerCJK_9009_CJK_8058_ofCJK_786C_CJK_7EA6_CJK_675F_CJK_4F9D_CJK_636E_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (10, 1, '<20260516-budget-bak@wang-fang>', '【CJK_5907_CJK_4EFD_】CJK_627E_lawyerofCJK_9884_CJK_7B97_CJK_548C_CJK_60F3_CJK_6CD5_', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-16T22:00:00Z',
   'Chen QiangCJK_8FD9_CJK_4E8B_CJK_6211_CJK_60F3_formalCJK_627E_CJK_4E2A_lawyerrepresentation。CJK_6211_CJK_5F00_CJK_670D_CJK_88C5_CJK_5C0F_CJK_5E97_CJK_6536_CJK_5165_CJK_4E0D_CJK_7A33_，CJK_501F_CJK_51FA_CJK_53BB_ofCJK_94B1_CJK_672C_CJK_6765_CJK_5C31_isCJK_79EF_CJK_84C4_，CJK_73B0_atCJK_624B_CJK_5934_CJK_5F88_CJK_7D27_。CJK_627E_lawyerCJK_51E0_CJK_4E2A_CJK_5E95_CJK_7EBF_：①CJK_524D_CJK_671F_CJK_9884_CJK_4ED8_oflawyerCJK_8D39_CJK_6211_CJK_6700_CJK_591A_CJK_62FF_CJK_5F97_CJK_51FA_8000CJK_5757_(¥8000)，CJK_518D_CJK_591A_CJK_771F_CJK_6CA1_has；②CJK_6700_CJK_597D_CJK_80FD_CJK_98CE_CJK_9669_representation(CJK_7B49_CJK_628A_CJK_94B1_CJK_8FFD_CJK_56DE_CJK_6765_CJK_518D_fromCJK_56DE_CJK_6B3E_CJK_91CC_CJK_4ED8_)，CJK_524D_CJK_671F_CJK_538B_CJK_529B_CJK_5C0F_；③CJK_5F97_isHangzhouCJK_80FD_CJK_529E_private lending/CJK_5408_CJK_540C_CJK_7EA0_CJK_7EB7_oflawyer，CJK_6848_CJK_5B50_CJK_8981_atCJK_6211_CJK_8FD9_CJK_8FB9_ofCJK_897F_CJK_6E56_CJK_533A_courtCJK_6253_；④CJK_5343_CJK_4E07_CJK_522B_CJK_627E_CJK_8DDF_Chen QianghasCJK_7275_CJK_8FDE_of。CJK_5148_atlegal services platformCJK_540D_CJK_5F55_CJK_91CC_CJK_5E2E_CJK_6211_CJK_7B5B_CJK_7B5B_CJK_9760_CJK_8C31_CJK_53C8_CJK_4ED8_CJK_5F97_CJK_8D77_of。',
   1, 0, '{}', 340, '2026-05-16T22:00:00Z');

-- Wang FangCJK_81EA_CJK_5DF1_CJK_5217_of"CJK_60F3_CJK_4E00_CJK_8D77_CJK_8FFD_ofCJK_8D26_"CJK_8349_CJK_7A3F_(CJK_8BC9_CJK_6C42_CJK_7B5B_CJK_9009_CJK_77E9_CJK_9635_ofCJK_4E8B_CJK_5B9E_CJK_4F9D_CJK_636E_)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (8, 1, '<20260519-claims-bak@wang-fang>', '【CJK_5907_CJK_4EFD_】CJK_6211_CJK_60F3_CJK_4E00_CJK_8D77_CJK_8FFD_ofCJK_51E0_CJK_7B14_CJK_8D26_', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-19T22:00:00Z',
   'CJK_8FD9_CJK_6B21_CJK_8D77_CJK_8BC9_CJK_628A_CJK_80FD_CJK_8981_ofCJK_90FD_CJK_8981_CJK_56DE_CJK_6765_：①IOUCJK_4E0A_CJK_5199_ofprincipal60CJK_4E07_(CJK_4E3B_) ②CJK_7EA6_CJK_5B9A_ofinterestmonthly interest2%，fromCJK_501F_ofCJK_65F6_CJK_5019_CJK_4E00_CJK_76F4_CJK_7B97_CJK_5230_CJK_8FD8_CJK_6E05_ ③CJK_8BA9_Chen QiangCJK_8001_CJK_5A46_Liu MinCJK_8DDF_CJK_4ED6_CJK_4E00_CJK_8D77_CJK_8FD8_，CJK_4E24_CJK_53E3_CJK_5B50_ofCJK_503A_CJK_8DD1_CJK_4E0D_CJK_6389_ ④CJK_8BA9_guarantorCJK_8001_CJK_5468_(Zhou Guohua)CJK_4E5F_CJK_5F97_CJK_8FD8_，CJK_4ED6_CJK_7B7E_CJK_4E86_securityof ⑤Chen QiangCJK_9A97_CJK_6211_CJK_5BB3_CJK_6211_CJK_62C5_CJK_60CA_CJK_53D7_CJK_6015_，CJK_60F3_CJK_8981_CJK_7B14_emotional-distress damages ⑥CJK_6211_isCJK_8FD9_CJK_4E8B_CJK_5173_CJK_4E86_CJK_597D_CJK_51E0_CJK_5929_CJK_5E97_、CJK_8DD1_law firmCJK_8DD1_court，CJK_8BEF_CJK_5DE5_CJK_635F_CJK_5931_CJK_4E5F_CJK_60F3_CJK_8BA9_CJK_4ED6_CJK_8D54_。CJK_5148_CJK_95EE_CJK_95EE_CJK_52A9_CJK_7406_CJK_8FD9_CJK_4E9B_CJK_80FD_CJK_4E0D_CJK_80FD_CJK_4E00_CJK_8D77_atCJK_8FD9_CJK_4E2A_CJK_6848_CJK_5B50_CJK_91CC_CJK_8981_。',
   1, 0, '{}', 340, '2026-05-19T22:00:00Z');

-- guarantorCJK_8001_CJK_5468_(CJK_6697_CJK_793A_Wang FangfromnotatCJK_4FDD_CJK_8BC1_CJK_671F_CJK_95F4_withinCJK_5355_CJK_72EC_CJK_5411_CJK_8001_CJK_5468_CJK_4E3B_CJK_5F20_CJK_8FC7_CJK_4FDD_CJK_8BC1_CJK_8D23_CJK_4EFB_)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (9, 1, '<20260513-guarantor@old.local>', 'Chen QiangofCJK_4E8B_CJK_522B_CJK_628A_CJK_6211_CJK_626F_CJK_8FDB_CJK_53BB_', 'Zhou Guohua <zhou.gh@126.com>', '["wang.fang@gmail.com"]',
   '2026-05-13T18:00:00Z',
   'Wang Fang，Chen QiangCJK_6B20_CJK_4F60_CJK_94B1_isCJK_4F60_CJK_4FE9_ofCJK_4E8B_。CJK_5F53_CJK_521D_CJK_6211_isCJK_788D_CJK_4E8E_CJK_60C5_CJK_9762_atIOUCJK_4E0A_CJK_7B7E_CJK_4E86_CJK_4E2A_CJK_5B57_，CJK_8FD9_CJK_4E24_yearCJK_4F60_CJK_4E5F_fromCJK_6765_CJK_6CA1_CJK_627E_CJK_8FC7_CJK_6211_CJK_8BF4_CJK_8BA9_CJK_6211_CJK_8FD8_CJK_94B1_ofCJK_4E8B_，CJK_73B0_atCJK_90FD_CJK_8FC7_CJK_53BB_CJK_8FD9_CJK_4E48_CJK_4E45_CJK_4E86_。CJK_6211_CJK_81EA_CJK_5DF1_CJK_4E5F_CJK_4E0D_CJK_5BBD_CJK_88D5_，CJK_8FD9_CJK_4E8B_CJK_4F60_CJK_627E_Chen QiangCJK_53BB_，CJK_522B_CJK_6765_CJK_627E_CJK_6211_。',
   1, 0, '{}', 200, '2026-05-13T18:00:00Z');

-- =========================================================================
-- Sent (folder_id = 2)
-- =========================================================================
-- Wang FangmaturityCJK_540E_CJK_5411_Chen QiangCJK_50AC_CJK_8FC7_CJK_6B3E_(CJK_5BF9_Chen QiangofCJK_50AC_CJK_8BA8_; CJK_4F46_fromnotCJK_5355_CJK_72EC_CJK_5411_guarantorCJK_8001_CJK_5468_CJK_4E3B_CJK_5F20_)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (20, 2, '<20250901-sent-chen@wang-fang>', 'Chen QiangpleaseCJK_5C3D_CJK_5FEB_repayment', 'wang.fang@gmail.com', '["chen.qiang@163.com"]',
   '2025-09-01T09:00:00Z',
   'Chen Qiang：loanCJK_65E9_alreadymaturity，2monthCJK_4F60_CJK_8FD8_CJK_4E86_2CJK_4E07_CJK_540E_CJK_53C8_CJK_8BF4_CJK_4F1A_CJK_8FD8_，CJK_5230_CJK_73B0_atCJK_53C8_CJK_62D6_CJK_4E86_CJK_5927_CJK_534A_year。pleaseCJK_4F60_CJK_52A1_CJK_5FC5_atCJK_672C_monthwithinCJK_628A_CJK_5269_CJK_4F59_loanCJK_672C_CJK_606F_CJK_7ED3_CJK_6E05_，CJK_5426_CJK_5219_CJK_6211_CJK_53EA_CJK_80FD_CJK_8D70_CJK_6CD5_CJK_5F8B_procedureCJK_4E86_。 — Wang Fang',
   1, 0, '{}', 200, '2025-09-01T09:00:00Z');

-- =========================================================================
-- Lending folder (folder_id = 7) — CJK_65E7_CJK_90AE_CJK_4EF6_: loanCJK_80CC_CJK_666F_ + Wang FangCJK_6536_CJK_5165_(CJK_51FA_CJK_501F_CJK_80FD_CJK_529B_CJK_4F50_CJK_8BC1_)
-- =========================================================================
-- loanCJK_7F18_CJK_8D77_(Chen QiangCJK_6C42_CJK_501F_, CJK_79F0_CJK_505A_CJK_751F_CJK_610F_CJK_5468_CJK_8F6C_) — and"CJK_5B9E_CJK_9645_CJK_7528_CJK_4E8E_CJK_7092_CJK_80A1_"CJK_5F62_CJK_6210_CJK_53CD_CJK_5DEE_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (30, 7, '<20230605-borrow@old.local>', 'CJK_82B3_CJK_59D0_CJK_6551_CJK_6025_', 'Chen Qiang <chen.qiang@163.com>', '["wang.fang@gmail.com"]',
   '2023-06-05T10:00:00Z',
   'CJK_82B3_CJK_59D0_，CJK_5B9E_atCJK_6CA1_CJK_529E_CJK_6CD5_CJK_624D_CJK_5F20_CJK_8FD9_CJK_4E2A_CJK_53E3_。CJK_6211_CJK_624B_CJK_4E0A_CJK_4E00_CJK_4E2A_CJK_9879_CJK_76EE_CJK_5468_CJK_8F6C_CJK_4E0D_CJK_5F00_，CJK_60F3_CJK_8DDF_CJK_4F60_CJK_501F_60CJK_4E07_shouldCJK_4E2A_CJK_6025_，CJK_534A_yearCJK_5230_CJK_4E00_yearCJK_51C6_CJK_8FD8_，interestundermonth2CJK_5206_CJK_7ED9_CJK_4F60_。CJK_54B1_CJK_4FE9_CJK_8001_CJK_540C_CJK_5B66_CJK_4F60_CJK_6700_CJK_4E86_CJK_89E3_CJK_6211_，CJK_7EDD_CJK_4E0D_CJK_4F1A_CJK_8BA9_CJK_4F60_CJK_5403_CJK_4E8F_。CJK_5148_CJK_8C22_CJK_8C22_CJK_82B3_CJK_59D0_CJK_4E86_！',
   1, 0, '{}', 180, '2023-06-05T10:00:00Z');

-- Wang FangCJK_670D_CJK_88C5_CJK_5E97_CJK_6D41_CJK_6C34_(CJK_51FA_CJK_501F_CJK_80FD_CJK_529B_/CJK_8D44_CJK_91D1_CJK_6765_CJK_6E90_CJK_4F50_CJK_8BC1_, CJK_5BF9_CJK_5927_CJK_989D_cashCJK_4EA4_CJK_4ED8_hasCJK_610F_CJK_4E49_) — CJK_4F46_cashCJK_90E8_CJK_5206_CJK_4ECD_CJK_7F3A_CJK_53D6_CJK_73B0_CJK_51ED_CJK_8BC1_
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (31, 7, '<20230901-shop@wang-fang>', 'CJK_5C0F_CJK_5E97_2023CJK_4E0A_CJK_534A_yearCJK_8D26_CJK_76EE_', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2023-09-01T10:00:00Z',
   'CJK_8BB0_CJK_4E00_CJK_4E0B_:CJK_670D_CJK_88C5_CJK_5E97_CJK_4E0A_CJK_534A_yearCJK_51C0_CJK_5229_CJK_7EA6_8CJK_4E07_，CJK_52A0_CJK_4E0A_CJK_4E4B_CJK_524D_ofCJK_79EF_CJK_84C4_。No.CJK_4E00_CJK_7B14_CJK_501F_CJK_7ED9_Chen Qiangof36CJK_4E07_CJK_8D70_ofbankCJK_8F6C_CJK_8D26_hasrecord。No.CJK_4E8C_CJK_7B14_20CJK_4E07_isCJK_6211_CJK_9646_CJK_7EED_CJK_653E_atCJK_5BB6_CJK_91CC_ofcashCJK_7ED9_of——CJK_8FD9_CJK_90E8_CJK_5206_CJK_6CA1_CJK_7559_bankCJK_53D6_CJK_73B0_ofCJK_5355_CJK_5B50_，CJK_4E5F_CJK_6CA1_CJK_8BA9_CJK_4ED6_CJK_6253_CJK_6536_CJK_6761_，CJK_73B0_atCJK_60F3_CJK_60F3_CJK_771F_CJK_540E_CJK_6094_。',
   1, 0, '{}', 180, '2023-09-01T10:00:00Z');



INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1000, 1, '<inbox-bg-001@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #001', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-16T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 001）',
   1, 0, '{}', 181, '2025-12-16T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1001, 1, '<inbox-bg-002@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #002', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-17T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 002）',
   1, 0, '{}', 182, '2025-12-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1002, 1, '<inbox-bg-003@mail.local>', 'CJK_5B66_CJK_6821_notice #003', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-18T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 003）',
   1, 0, '{}', 183, '2025-12-18T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1003, 1, '<inbox-bg-004@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #004', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-19T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 004）',
   1, 0, '{}', 184, '2025-12-19T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1004, 1, '<inbox-bg-005@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #005', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-20T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 005）',
   0, 0, '{}', 185, '2025-12-20T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1005, 1, '<inbox-bg-006@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #006', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-21T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 006）',
   1, 0, '{}', 186, '2025-12-21T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1006, 1, '<inbox-bg-007@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #007', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-22T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 007）',
   1, 0, '{}', 187, '2025-12-22T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1007, 1, '<inbox-bg-008@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #008', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-23T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 008）',
   1, 0, '{}', 188, '2025-12-23T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1008, 1, '<inbox-bg-009@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #009', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-24T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 009）',
   1, 0, '{}', 189, '2025-12-24T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1009, 1, '<inbox-bg-010@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #010', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-25T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 010）',
   0, 0, '{}', 190, '2025-12-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1010, 1, '<inbox-bg-011@mail.local>', 'CJK_5B66_CJK_6821_notice #011', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-26T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 011）',
   1, 0, '{}', 191, '2025-12-26T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1011, 1, '<inbox-bg-012@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #012', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-27T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 012）',
   1, 0, '{}', 192, '2025-12-27T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1012, 1, '<inbox-bg-013@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #013', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-28T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 013）',
   1, 0, '{}', 193, '2025-12-28T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1013, 1, '<inbox-bg-014@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #014', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-29T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 014）',
   1, 0, '{}', 194, '2025-12-29T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1014, 1, '<inbox-bg-015@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #015', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-30T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 015）',
   0, 0, '{}', 195, '2025-12-30T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1015, 1, '<inbox-bg-016@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #016', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2025-12-31T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 016）',
   1, 0, '{}', 196, '2025-12-31T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1016, 1, '<inbox-bg-017@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #017', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-01T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 017）',
   1, 0, '{}', 197, '2026-01-01T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1017, 1, '<inbox-bg-018@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #018', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-02T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 018）',
   1, 0, '{}', 198, '2026-01-02T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1018, 1, '<inbox-bg-019@mail.local>', 'CJK_5B66_CJK_6821_notice #019', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-03T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 019）',
   1, 1, '{}', 199, '2026-01-03T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1019, 1, '<inbox-bg-020@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #020', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-04T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 020）',
   0, 0, '{}', 200, '2026-01-04T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1020, 1, '<inbox-bg-021@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #021', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-05T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 021）',
   1, 0, '{}', 201, '2026-01-05T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1021, 1, '<inbox-bg-022@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #022', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-06T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 022）',
   1, 0, '{}', 202, '2026-01-06T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1022, 1, '<inbox-bg-023@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #023', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-07T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 023）',
   1, 0, '{}', 203, '2026-01-07T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1023, 1, '<inbox-bg-024@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #024', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-08T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 024）',
   1, 0, '{}', 204, '2026-01-08T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1024, 1, '<inbox-bg-025@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #025', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-09T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 025）',
   0, 0, '{}', 205, '2026-01-09T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1025, 1, '<inbox-bg-026@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #026', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-10T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 026）',
   1, 0, '{}', 206, '2026-01-10T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1026, 1, '<inbox-bg-027@mail.local>', 'CJK_5B66_CJK_6821_notice #027', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-11T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 027）',
   1, 0, '{}', 207, '2026-01-11T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1027, 1, '<inbox-bg-028@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #028', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-12T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 028）',
   1, 0, '{}', 208, '2026-01-12T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1028, 1, '<inbox-bg-029@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #029', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-13T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 029）',
   1, 0, '{}', 209, '2026-01-13T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1029, 1, '<inbox-bg-030@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #030', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-14T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 030）',
   0, 0, '{}', 210, '2026-01-14T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1030, 1, '<inbox-bg-031@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #031', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-15T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 031）',
   1, 0, '{}', 211, '2026-01-15T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1031, 1, '<inbox-bg-032@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #032', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-16T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 032）',
   1, 0, '{}', 212, '2026-01-16T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1032, 1, '<inbox-bg-033@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #033', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-17T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 033）',
   1, 0, '{}', 213, '2026-01-17T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1033, 1, '<inbox-bg-034@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #034', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-18T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 034）',
   1, 0, '{}', 214, '2026-01-18T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1034, 1, '<inbox-bg-035@mail.local>', 'CJK_5B66_CJK_6821_notice #035', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-19T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 035）',
   0, 0, '{}', 215, '2026-01-19T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1035, 1, '<inbox-bg-036@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #036', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-20T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 036）',
   1, 0, '{}', 216, '2026-01-20T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1036, 1, '<inbox-bg-037@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #037', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-21T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 037）',
   1, 0, '{}', 217, '2026-01-21T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1037, 1, '<inbox-bg-038@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #038', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-22T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 038）',
   1, 1, '{}', 218, '2026-01-22T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1038, 1, '<inbox-bg-039@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #039', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-23T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 039）',
   1, 0, '{}', 219, '2026-01-23T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1039, 1, '<inbox-bg-040@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #040', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-24T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 040）',
   0, 0, '{}', 220, '2026-01-24T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1040, 1, '<inbox-bg-041@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #041', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-25T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 041）',
   1, 0, '{}', 221, '2026-01-25T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1041, 1, '<inbox-bg-042@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #042', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-26T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 042）',
   1, 0, '{}', 222, '2026-01-26T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1042, 1, '<inbox-bg-043@mail.local>', 'CJK_5B66_CJK_6821_notice #043', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-27T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 043）',
   1, 0, '{}', 223, '2026-01-27T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1043, 1, '<inbox-bg-044@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #044', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-28T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 044）',
   1, 0, '{}', 224, '2026-01-28T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1044, 1, '<inbox-bg-045@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #045', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-29T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 045）',
   0, 0, '{}', 225, '2026-01-29T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1045, 1, '<inbox-bg-046@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #046', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-30T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 046）',
   1, 0, '{}', 226, '2026-01-30T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1046, 1, '<inbox-bg-047@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #047', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-01-31T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 047）',
   1, 0, '{}', 227, '2026-01-31T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1047, 1, '<inbox-bg-048@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #048', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-01T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 048）',
   1, 0, '{}', 228, '2026-02-01T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1048, 1, '<inbox-bg-049@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #049', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-02T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 049）',
   1, 0, '{}', 229, '2026-02-02T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1049, 1, '<inbox-bg-050@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #050', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-03T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 050）',
   0, 0, '{}', 230, '2026-02-03T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1050, 1, '<inbox-bg-051@mail.local>', 'CJK_5B66_CJK_6821_notice #051', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-04T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 051）',
   1, 0, '{}', 231, '2026-02-04T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1051, 1, '<inbox-bg-052@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #052', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-05T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 052）',
   1, 0, '{}', 232, '2026-02-05T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1052, 1, '<inbox-bg-053@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #053', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-06T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 053）',
   1, 0, '{}', 233, '2026-02-06T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1053, 1, '<inbox-bg-054@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #054', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-07T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 054）',
   1, 0, '{}', 234, '2026-02-07T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1054, 1, '<inbox-bg-055@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #055', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-08T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 055）',
   0, 0, '{}', 235, '2026-02-08T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1055, 1, '<inbox-bg-056@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #056', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-09T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 056）',
   1, 0, '{}', 236, '2026-02-09T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1056, 1, '<inbox-bg-057@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #057', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-10T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 057）',
   1, 1, '{}', 237, '2026-02-10T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1057, 1, '<inbox-bg-058@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #058', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-11T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 058）',
   1, 0, '{}', 238, '2026-02-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1058, 1, '<inbox-bg-059@mail.local>', 'CJK_5B66_CJK_6821_notice #059', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-12T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 059）',
   1, 0, '{}', 239, '2026-02-12T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1059, 1, '<inbox-bg-060@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #060', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-13T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 060）',
   0, 0, '{}', 180, '2026-02-13T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1060, 1, '<inbox-bg-061@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #061', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-14T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 061）',
   1, 0, '{}', 181, '2026-02-14T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1061, 1, '<inbox-bg-062@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #062', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-15T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 062）',
   1, 0, '{}', 182, '2026-02-15T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1062, 1, '<inbox-bg-063@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #063', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-16T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 063）',
   1, 0, '{}', 183, '2026-02-16T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1063, 1, '<inbox-bg-064@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #064', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-17T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 064）',
   1, 0, '{}', 184, '2026-02-17T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1064, 1, '<inbox-bg-065@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #065', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-18T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 065）',
   0, 0, '{}', 185, '2026-02-18T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1065, 1, '<inbox-bg-066@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #066', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-19T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 066）',
   1, 0, '{}', 186, '2026-02-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1066, 1, '<inbox-bg-067@mail.local>', 'CJK_5B66_CJK_6821_notice #067', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-20T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 067）',
   1, 0, '{}', 187, '2026-02-20T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1067, 1, '<inbox-bg-068@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #068', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-21T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 068）',
   1, 0, '{}', 188, '2026-02-21T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1068, 1, '<inbox-bg-069@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #069', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-22T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 069）',
   1, 0, '{}', 189, '2026-02-22T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1069, 1, '<inbox-bg-070@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #070', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-23T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 070）',
   0, 0, '{}', 190, '2026-02-23T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1070, 1, '<inbox-bg-071@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #071', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-24T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 071）',
   1, 0, '{}', 191, '2026-02-24T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1071, 1, '<inbox-bg-072@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #072', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-25T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 072）',
   1, 0, '{}', 192, '2026-02-25T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1072, 1, '<inbox-bg-073@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #073', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-26T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 073）',
   1, 0, '{}', 193, '2026-02-26T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1073, 1, '<inbox-bg-074@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #074', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-27T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 074）',
   1, 0, '{}', 194, '2026-02-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1074, 1, '<inbox-bg-075@mail.local>', 'CJK_5B66_CJK_6821_notice #075', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-02-28T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 075）',
   0, 0, '{}', 195, '2026-02-28T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1075, 1, '<inbox-bg-076@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #076', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-01T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 076）',
   1, 1, '{}', 196, '2026-03-01T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1076, 1, '<inbox-bg-077@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #077', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-02T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 077）',
   1, 0, '{}', 197, '2026-03-02T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1077, 1, '<inbox-bg-078@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #078', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-03T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 078）',
   1, 0, '{}', 198, '2026-03-03T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1078, 1, '<inbox-bg-079@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #079', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-04T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 079）',
   1, 0, '{}', 199, '2026-03-04T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1079, 1, '<inbox-bg-080@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #080', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-05T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 080）',
   0, 0, '{}', 200, '2026-03-05T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1080, 1, '<inbox-bg-081@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #081', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-06T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 081）',
   1, 0, '{}', 201, '2026-03-06T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1081, 1, '<inbox-bg-082@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #082', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-07T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 082）',
   1, 0, '{}', 202, '2026-03-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1082, 1, '<inbox-bg-083@mail.local>', 'CJK_5B66_CJK_6821_notice #083', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-08T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 083）',
   1, 0, '{}', 203, '2026-03-08T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1083, 1, '<inbox-bg-084@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #084', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-09T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 084）',
   1, 0, '{}', 204, '2026-03-09T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1084, 1, '<inbox-bg-085@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #085', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-10T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 085）',
   0, 0, '{}', 205, '2026-03-10T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1085, 1, '<inbox-bg-086@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #086', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-11T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 086）',
   1, 0, '{}', 206, '2026-03-11T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1086, 1, '<inbox-bg-087@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #087', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-12T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 087）',
   1, 0, '{}', 207, '2026-03-12T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1087, 1, '<inbox-bg-088@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #088', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-13T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 088）',
   1, 0, '{}', 208, '2026-03-13T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1088, 1, '<inbox-bg-089@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #089', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-14T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 089）',
   1, 0, '{}', 209, '2026-03-14T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1089, 1, '<inbox-bg-090@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #090', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-15T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 090）',
   0, 0, '{}', 210, '2026-03-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1090, 1, '<inbox-bg-091@mail.local>', 'CJK_5B66_CJK_6821_notice #091', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-16T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 091）',
   1, 0, '{}', 211, '2026-03-16T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1091, 1, '<inbox-bg-092@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #092', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-17T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 092）',
   1, 0, '{}', 212, '2026-03-17T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1092, 1, '<inbox-bg-093@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #093', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-18T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 093）',
   1, 0, '{}', 213, '2026-03-18T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1093, 1, '<inbox-bg-094@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #094', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-19T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 094）',
   1, 0, '{}', 214, '2026-03-19T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1094, 1, '<inbox-bg-095@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #095', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-20T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 095）',
   0, 1, '{}', 215, '2026-03-20T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1095, 1, '<inbox-bg-096@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #096', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-21T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 096）',
   1, 0, '{}', 216, '2026-03-21T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1096, 1, '<inbox-bg-097@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #097', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-22T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 097）',
   1, 0, '{}', 217, '2026-03-22T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1097, 1, '<inbox-bg-098@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #098', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-23T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 098）',
   1, 0, '{}', 218, '2026-03-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1098, 1, '<inbox-bg-099@mail.local>', 'CJK_5B66_CJK_6821_notice #099', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-24T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 099）',
   1, 0, '{}', 219, '2026-03-24T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1099, 1, '<inbox-bg-100@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #100', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-25T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 100）',
   0, 0, '{}', 220, '2026-03-25T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1100, 1, '<inbox-bg-101@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #101', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-26T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 101）',
   1, 0, '{}', 221, '2026-03-26T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1101, 1, '<inbox-bg-102@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #102', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-27T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 102）',
   1, 0, '{}', 222, '2026-03-27T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1102, 1, '<inbox-bg-103@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #103', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-28T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 103）',
   1, 0, '{}', 223, '2026-03-28T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1103, 1, '<inbox-bg-104@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #104', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-29T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 104）',
   1, 0, '{}', 224, '2026-03-29T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1104, 1, '<inbox-bg-105@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #105', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-30T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 105）',
   0, 0, '{}', 225, '2026-03-30T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1105, 1, '<inbox-bg-106@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #106', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-03-31T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 106）',
   1, 0, '{}', 226, '2026-03-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1106, 1, '<inbox-bg-107@mail.local>', 'CJK_5B66_CJK_6821_notice #107', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-01T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 107）',
   1, 0, '{}', 227, '2026-04-01T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1107, 1, '<inbox-bg-108@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #108', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-02T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 108）',
   1, 0, '{}', 228, '2026-04-02T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1108, 1, '<inbox-bg-109@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #109', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-03T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 109）',
   1, 0, '{}', 229, '2026-04-03T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1109, 1, '<inbox-bg-110@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #110', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-04T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 110）',
   0, 0, '{}', 230, '2026-04-04T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1110, 1, '<inbox-bg-111@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #111', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-05T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 111）',
   1, 0, '{}', 231, '2026-04-05T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1111, 1, '<inbox-bg-112@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #112', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-06T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 112）',
   1, 0, '{}', 232, '2026-04-06T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1112, 1, '<inbox-bg-113@mail.local>', 'bankCJK_8D26_CJK_5355_CJK_63D0_CJK_9192_ #113', 'Industrial and Commercial Bank of China <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-07T09:00:00Z', 'CJK_60A8_ofCJK_4FE1_CJK_7528_CJK_5361_CJK_8D26_CJK_5355_generated，pleaseatmaturitydayCJK_524D_CJK_5B8C_CJK_6210_repaymentandverifyCJK_6D88_CJK_8D39_CJK_660E_CJK_7EC6_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 113）',
   1, 0, '{}', 233, '2026-04-07T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1113, 1, '<inbox-bg-114@mail.local>', 'CJK_7269_CJK_6D41_CJK_5230_CJK_4EF6_CJK_63D0_CJK_9192_ #114', 'CJK_987A_CJK_8054_CJK_901F_CJK_8FD0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-08T10:00:00Z', 'CJK_60A8_hasCJK_670D_CJK_88C5_CJK_6837_CJK_8863_orCJK_5E97_CJK_94FA_CJK_8865_CJK_8D27_CJK_5305_CJK_88F9_CJK_5373_willCJK_6D3E_CJK_9001_，pleaseCJK_4FDD_CJK_6301_CJK_7535_CJK_8BDD_CJK_7545_CJK_901A_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 114）',
   1, 1, '{}', 234, '2026-04-08T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1114, 1, '<inbox-bg-115@mail.local>', 'CJK_5B66_CJK_6821_notice #115', 'CJK_897F_CJK_6E56_CJK_533A_CJK_5C0F_CJK_5B66_CJK_6559_CJK_52A1_CJK_5904_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-09T11:00:00Z', 'pleaseCJK_5BB6_CJK_957F_monitorCJK_8FD1_CJK_671F_CJK_73ED_CJK_7EA7_CJK_6D3B_CJK_52A8_、CJK_5BB6_CJK_957F_CJK_4F1A_CJK_548C_materialsprepare。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 115）',
   0, 0, '{}', 235, '2026-04-09T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1115, 1, '<inbox-bg-116@mail.local>', 'CJK_5E97_CJK_94FA_CJK_8FD0_CJK_8425_CJK_5468_CJK_62A5_ #116', 'CJK_5E73_CJK_53F0_CJK_5546_CJK_5BB6_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-10T12:00:00Z', 'CJK_672C_CJK_5468_CJK_6D41_CJK_91CF_、CJK_8F6C_CJK_5316_CJK_548C_CJK_590D_CJK_8D2D_CJK_60C5_CJK_51B5_alreadyupdate，pleaseandCJK_65F6_CJK_67E5_CJK_770B_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 116）',
   1, 0, '{}', 236, '2026-04-10T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1116, 1, '<inbox-bg-117@mail.local>', 'CJK_4FC3_CJK_9500_CJK_6D3B_CJK_52A8_CJK_9080_please #117', 'CJK_5973_CJK_88C5_CJK_6279_CJK_53D1_CJK_5E73_CJK_53F0_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-11T13:00:00Z', 'CJK_5E73_CJK_53F0_willCJK_5F00_CJK_542F_CJK_590F_CJK_5B63_CJK_6E05_CJK_4ED3_CJK_6D3B_CJK_52A8_，CJK_652F_CJK_6301_CJK_5546_CJK_5BB6_CJK_62A5_CJK_540D_CJK_548C_CJK_76F4_CJK_64AD_CJK_8054_CJK_52A8_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 117）',
   1, 0, '{}', 237, '2026-04-11T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1117, 1, '<inbox-bg-118@mail.local>', 'CJK_7269_CJK_4E1A_CJK_7F34_CJK_8D39_CJK_63D0_CJK_9192_ #118', 'CJK_5C0F_CJK_533A_CJK_7269_CJK_4E1A_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-12T14:00:00Z', 'CJK_672C_monthCJK_7269_CJK_4E1A_CJK_548C_CJK_505C_CJK_8F66_CJK_8D39_CJK_7528_CJK_8D26_CJK_5355_alreadyCJK_51FA_，pleaseunderCJK_65F6_CJK_7F34_CJK_7EB3_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 118）',
   1, 0, '{}', 238, '2026-04-12T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1118, 1, '<inbox-bg-119@mail.local>', 'CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_63D0_CJK_9192_ #119', 'CJK_897F_CJK_6E56_CJK_4F53_CJK_68C0_inCJK_5FC3_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-13T15:00:00Z', 'yearCJK_5EA6_CJK_4F53_CJK_68C0_CJK_9884_CJK_7EA6_CJK_7A97_CJK_53E3_alreadyCJK_5F00_CJK_653E_，canunderneedCJK_6539_CJK_671F_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 119）',
   1, 0, '{}', 239, '2026-04-13T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1119, 1, '<inbox-bg-120@mail.local>', 'CJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_CJK_63D0_CJK_9192_ #120', 'CJK_5546_CJK_6237_CJK_6536_CJK_6B3E_CJK_52A9_CJK_624B_ <auto@mail.local>', '["wang.fang@gmail.com"]',
   '2026-04-14T08:00:00Z', 'CJK_95E8_CJK_5E97_CJK_6628_dayCJK_6536_CJK_6B3E_CJK_6D41_CJK_6C34_alreadyCJK_6C47_CJK_603B_，CJK_9644_CJK_4EF6_CJK_542B_CJK_5206_CJK_7C7B_CJK_7EDF_CJK_8BA1_。（INBOX dayCJK_5E38_CJK_5F80_CJK_6765_ 120）',
   0, 0, '{}', 180, '2026-04-14T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1120, 6, '<family-bg-001@family.local>', 'CJK_5468_CJK_672B_CJK_56DE_CJK_6765_CJK_5403_CJK_996D_CJK_5417_', 'CJK_674E_CJK_79C0_CJK_82F1_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-08T19:00:00Z', 'CJK_4F60_CJK_7238_CJK_4E70_CJK_4E86_CJK_83DC_，CJK_5468_CJK_672B_hasCJK_7A7A_CJK_56DE_CJK_6765_CJK_5403_CJK_987F_CJK_996D_。（Family 001）', 1, 0, '{}', 151, '2026-01-08T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1121, 6, '<family-bg-002@family.local>', 'CJK_5BB6_CJK_65CF_CJK_7FA4_CJK_7167_CJK_7247_', 'CJK_8868_CJK_59D0_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-11T19:00:00Z', 'CJK_628A_CJK_4E0A_CJK_6B21_CJK_5BB6_CJK_5EAD_CJK_805A_CJK_4F1A_ofCJK_7167_CJK_7247_CJK_6574_CJK_7406_CJK_597D_CJK_53D1_CJK_4F60_CJK_7559_CJK_5B58_。（Family 002）', 1, 0, '{}', 152, '2026-01-11T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1122, 6, '<family-bg-003@family.local>', 'CJK_5973_CJK_513F_CJK_5B66_CJK_6821_CJK_5B89_CJK_6392_', 'Wang FangCJK_5F1F_CJK_59B9_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-14T19:00:00Z', 'CJK_4E0B_CJK_5468_CJK_5174_CJK_8DA3_CJK_73ED_CJK_65F6_CJK_95F4_hasCJK_8C03_CJK_6574_，CJK_8BB0_CJK_5F97_CJK_770B_notice。（Family 003）', 1, 0, '{}', 153, '2026-01-14T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1123, 6, '<family-bg-004@family.local>', 'CJK_8EAB_CJK_4F53_CJK_522B_CJK_592A_CJK_7D2F_', 'CJK_5988_CJK_5988_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-17T19:00:00Z', 'CJK_6700_CJK_8FD1_CJK_522B_CJK_8001_CJK_71AC_CJK_591C_，CJK_6253_CJK_5B98_CJK_53F8_ofCJK_4E8B_CJK_4E5F_CJK_8981_CJK_987E_CJK_8EAB_CJK_4F53_。（Family 004）', 1, 0, '{}', 154, '2026-01-17T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1124, 6, '<family-bg-005@family.local>', 'CJK_5468_CJK_672B_CJK_56DE_CJK_6765_CJK_5403_CJK_996D_CJK_5417_', 'CJK_674E_CJK_79C0_CJK_82F1_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-20T19:00:00Z', 'CJK_4F60_CJK_7238_CJK_4E70_CJK_4E86_CJK_83DC_，CJK_5468_CJK_672B_hasCJK_7A7A_CJK_56DE_CJK_6765_CJK_5403_CJK_987F_CJK_996D_。（Family 005）', 1, 0, '{}', 155, '2026-01-20T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1125, 6, '<family-bg-006@family.local>', 'CJK_5BB6_CJK_65CF_CJK_7FA4_CJK_7167_CJK_7247_', 'CJK_8868_CJK_59D0_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-23T19:00:00Z', 'CJK_628A_CJK_4E0A_CJK_6B21_CJK_5BB6_CJK_5EAD_CJK_805A_CJK_4F1A_ofCJK_7167_CJK_7247_CJK_6574_CJK_7406_CJK_597D_CJK_53D1_CJK_4F60_CJK_7559_CJK_5B58_。（Family 006）', 1, 0, '{}', 156, '2026-01-23T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1126, 6, '<family-bg-007@family.local>', 'CJK_5973_CJK_513F_CJK_5B66_CJK_6821_CJK_5B89_CJK_6392_', 'Wang FangCJK_5F1F_CJK_59B9_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-26T19:00:00Z', 'CJK_4E0B_CJK_5468_CJK_5174_CJK_8DA3_CJK_73ED_CJK_65F6_CJK_95F4_hasCJK_8C03_CJK_6574_，CJK_8BB0_CJK_5F97_CJK_770B_notice。（Family 007）', 1, 0, '{}', 157, '2026-01-26T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1127, 6, '<family-bg-008@family.local>', 'CJK_8EAB_CJK_4F53_CJK_522B_CJK_592A_CJK_7D2F_', 'CJK_5988_CJK_5988_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-01-29T19:00:00Z', 'CJK_6700_CJK_8FD1_CJK_522B_CJK_8001_CJK_71AC_CJK_591C_，CJK_6253_CJK_5B98_CJK_53F8_ofCJK_4E8B_CJK_4E5F_CJK_8981_CJK_987E_CJK_8EAB_CJK_4F53_。（Family 008）', 1, 0, '{}', 158, '2026-01-29T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1128, 6, '<family-bg-009@family.local>', 'CJK_5468_CJK_672B_CJK_56DE_CJK_6765_CJK_5403_CJK_996D_CJK_5417_', 'CJK_674E_CJK_79C0_CJK_82F1_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-01T19:00:00Z', 'CJK_4F60_CJK_7238_CJK_4E70_CJK_4E86_CJK_83DC_，CJK_5468_CJK_672B_hasCJK_7A7A_CJK_56DE_CJK_6765_CJK_5403_CJK_987F_CJK_996D_。（Family 009）', 1, 0, '{}', 159, '2026-02-01T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1129, 6, '<family-bg-010@family.local>', 'CJK_5BB6_CJK_65CF_CJK_7FA4_CJK_7167_CJK_7247_', 'CJK_8868_CJK_59D0_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-04T19:00:00Z', 'CJK_628A_CJK_4E0A_CJK_6B21_CJK_5BB6_CJK_5EAD_CJK_805A_CJK_4F1A_ofCJK_7167_CJK_7247_CJK_6574_CJK_7406_CJK_597D_CJK_53D1_CJK_4F60_CJK_7559_CJK_5B58_。（Family 010）', 1, 0, '{}', 160, '2026-02-04T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1130, 6, '<family-bg-011@family.local>', 'CJK_5973_CJK_513F_CJK_5B66_CJK_6821_CJK_5B89_CJK_6392_', 'Wang FangCJK_5F1F_CJK_59B9_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-07T19:00:00Z', 'CJK_4E0B_CJK_5468_CJK_5174_CJK_8DA3_CJK_73ED_CJK_65F6_CJK_95F4_hasCJK_8C03_CJK_6574_，CJK_8BB0_CJK_5F97_CJK_770B_notice。（Family 011）', 1, 0, '{}', 161, '2026-02-07T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1131, 6, '<family-bg-012@family.local>', 'CJK_8EAB_CJK_4F53_CJK_522B_CJK_592A_CJK_7D2F_', 'CJK_5988_CJK_5988_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-10T19:00:00Z', 'CJK_6700_CJK_8FD1_CJK_522B_CJK_8001_CJK_71AC_CJK_591C_，CJK_6253_CJK_5B98_CJK_53F8_ofCJK_4E8B_CJK_4E5F_CJK_8981_CJK_987E_CJK_8EAB_CJK_4F53_。（Family 012）', 1, 0, '{}', 162, '2026-02-10T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1132, 6, '<family-bg-013@family.local>', 'CJK_5468_CJK_672B_CJK_56DE_CJK_6765_CJK_5403_CJK_996D_CJK_5417_', 'CJK_674E_CJK_79C0_CJK_82F1_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-13T19:00:00Z', 'CJK_4F60_CJK_7238_CJK_4E70_CJK_4E86_CJK_83DC_，CJK_5468_CJK_672B_hasCJK_7A7A_CJK_56DE_CJK_6765_CJK_5403_CJK_987F_CJK_996D_。（Family 013）', 1, 0, '{}', 163, '2026-02-13T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1133, 6, '<family-bg-014@family.local>', 'CJK_5BB6_CJK_65CF_CJK_7FA4_CJK_7167_CJK_7247_', 'CJK_8868_CJK_59D0_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-16T19:00:00Z', 'CJK_628A_CJK_4E0A_CJK_6B21_CJK_5BB6_CJK_5EAD_CJK_805A_CJK_4F1A_ofCJK_7167_CJK_7247_CJK_6574_CJK_7406_CJK_597D_CJK_53D1_CJK_4F60_CJK_7559_CJK_5B58_。（Family 014）', 1, 0, '{}', 164, '2026-02-16T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1134, 6, '<family-bg-015@family.local>', 'CJK_5973_CJK_513F_CJK_5B66_CJK_6821_CJK_5B89_CJK_6392_', 'Wang FangCJK_5F1F_CJK_59B9_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-19T19:00:00Z', 'CJK_4E0B_CJK_5468_CJK_5174_CJK_8DA3_CJK_73ED_CJK_65F6_CJK_95F4_hasCJK_8C03_CJK_6574_，CJK_8BB0_CJK_5F97_CJK_770B_notice。（Family 015）', 1, 0, '{}', 165, '2026-02-19T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1135, 6, '<family-bg-016@family.local>', 'CJK_8EAB_CJK_4F53_CJK_522B_CJK_592A_CJK_7D2F_', 'CJK_5988_CJK_5988_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-22T19:00:00Z', 'CJK_6700_CJK_8FD1_CJK_522B_CJK_8001_CJK_71AC_CJK_591C_，CJK_6253_CJK_5B98_CJK_53F8_ofCJK_4E8B_CJK_4E5F_CJK_8981_CJK_987E_CJK_8EAB_CJK_4F53_。（Family 016）', 1, 0, '{}', 166, '2026-02-22T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1136, 6, '<family-bg-017@family.local>', 'CJK_5468_CJK_672B_CJK_56DE_CJK_6765_CJK_5403_CJK_996D_CJK_5417_', 'CJK_674E_CJK_79C0_CJK_82F1_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-25T19:00:00Z', 'CJK_4F60_CJK_7238_CJK_4E70_CJK_4E86_CJK_83DC_，CJK_5468_CJK_672B_hasCJK_7A7A_CJK_56DE_CJK_6765_CJK_5403_CJK_987F_CJK_996D_。（Family 017）', 1, 0, '{}', 167, '2026-02-25T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1137, 6, '<family-bg-018@family.local>', 'CJK_5BB6_CJK_65CF_CJK_7FA4_CJK_7167_CJK_7247_', 'CJK_8868_CJK_59D0_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-02-28T19:00:00Z', 'CJK_628A_CJK_4E0A_CJK_6B21_CJK_5BB6_CJK_5EAD_CJK_805A_CJK_4F1A_ofCJK_7167_CJK_7247_CJK_6574_CJK_7406_CJK_597D_CJK_53D1_CJK_4F60_CJK_7559_CJK_5B58_。（Family 018）', 1, 0, '{}', 168, '2026-02-28T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1138, 6, '<family-bg-019@family.local>', 'CJK_5973_CJK_513F_CJK_5B66_CJK_6821_CJK_5B89_CJK_6392_', 'Wang FangCJK_5F1F_CJK_59B9_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-03-03T19:00:00Z', 'CJK_4E0B_CJK_5468_CJK_5174_CJK_8DA3_CJK_73ED_CJK_65F6_CJK_95F4_hasCJK_8C03_CJK_6574_，CJK_8BB0_CJK_5F97_CJK_770B_notice。（Family 019）', 1, 0, '{}', 169, '2026-03-03T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1139, 6, '<family-bg-020@family.local>', 'CJK_8EAB_CJK_4F53_CJK_522B_CJK_592A_CJK_7D2F_', 'CJK_5988_CJK_5988_ <family@local>', '["wang.fang@gmail.com"]',
   '2026-03-06T19:00:00Z', 'CJK_6700_CJK_8FD1_CJK_522B_CJK_8001_CJK_71AC_CJK_591C_，CJK_6253_CJK_5B98_CJK_53F8_ofCJK_4E8B_CJK_4E5F_CJK_8981_CJK_987E_CJK_8EAB_CJK_4F53_。（Family 020）', 1, 0, '{}', 170, '2026-03-06T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1140, 7, '<lending-bg-001@lending.local>', '【CJK_5907_CJK_4EFD_】collectionCJK_6C9F_CJK_901A_CJK_6574_CJK_7406_ #001', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-03T10:00:00Z', 'CJK_628A_CJK_8FD1_CJK_51E0_CJK_6B21_collectionCJK_6C9F_CJK_901A_CJK_6458_CJK_5F55_CJK_4E00_CJK_4E0B_，CJK_514D_CJK_5F97_CJK_56DE_CJK_5934_CJK_627E_CJK_4E0D_CJK_5230_。（Lending 001）', 1, 0, '{}', 171, '2025-11-03T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1141, 7, '<lending-bg-002@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_65E7_CJK_8D26_CJK_5F80_CJK_6765_CJK_8BF4_CJK_660E_ #002', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-05T10:00:00Z', 'CJK_628A_CJK_548C_Chen QiangrelatedofCJK_65E7_CJK_8D26_、interestCJK_53E3_CJK_5F84_CJK_548C_CJK_804A_CJK_5929_CJK_788E_CJK_7247_CJK_5148_CJK_5F52_CJK_6863_。（Lending 002）', 1, 0, '{}', 172, '2025-11-05T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1142, 7, '<lending-bg-003@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_95E8_CJK_5E97_cashCJK_5B89_CJK_6392_ #003', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-07T10:00:00Z', 'recordCJK_9636_CJK_6BB5_CJK_6027_CJK_624B_CJK_5934_cashCJK_548C_CJK_5E97_CJK_94FA_CJK_5468_CJK_8F6C_CJK_60C5_CJK_51B5_，CJK_7EAF_CJK_5907_CJK_5FD8_。（Lending 003）', 1, 0, '{}', 173, '2025-11-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1143, 7, '<lending-bg-004@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_501F_CJK_8D37_CJK_6559_CJK_8BAD_CJK_6458_CJK_8BB0_ #004', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-09T10:00:00Z', 'CJK_968F_CJK_624B_CJK_8BB0_CJK_51E0_CJK_6761_CJK_501F_CJK_94B1_CJK_6559_CJK_8BAD_，CJK_4E4B_CJK_540E_canCJK_80FD_CJK_5199_CJK_8FDB_CJK_590D_CJK_76D8_。（Lending 004）', 1, 0, '{}', 174, '2025-11-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1144, 7, '<lending-bg-005@lending.local>', '【CJK_5907_CJK_4EFD_】materialsCJK_5F85_CJK_8865_checklist #005', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-11T10:00:00Z', 'CJK_54EA_CJK_4E9B_materialsCJK_9F50_CJK_4E86_、CJK_54EA_CJK_4E9B_CJK_8FD8_CJK_8981_CJK_8865_，CJK_5148_CJK_8BB0_CJK_4E00_CJK_4EFD_。（Lending 005）', 1, 0, '{}', 175, '2025-11-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1145, 7, '<lending-bg-006@lending.local>', '【CJK_5907_CJK_4EFD_】collectionCJK_6C9F_CJK_901A_CJK_6574_CJK_7406_ #006', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-13T10:00:00Z', 'CJK_628A_CJK_8FD1_CJK_51E0_CJK_6B21_collectionCJK_6C9F_CJK_901A_CJK_6458_CJK_5F55_CJK_4E00_CJK_4E0B_，CJK_514D_CJK_5F97_CJK_56DE_CJK_5934_CJK_627E_CJK_4E0D_CJK_5230_。（Lending 006）', 1, 0, '{}', 176, '2025-11-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1146, 7, '<lending-bg-007@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_65E7_CJK_8D26_CJK_5F80_CJK_6765_CJK_8BF4_CJK_660E_ #007', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-15T10:00:00Z', 'CJK_628A_CJK_548C_Chen QiangrelatedofCJK_65E7_CJK_8D26_、interestCJK_53E3_CJK_5F84_CJK_548C_CJK_804A_CJK_5929_CJK_788E_CJK_7247_CJK_5148_CJK_5F52_CJK_6863_。（Lending 007）', 1, 0, '{}', 177, '2025-11-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1147, 7, '<lending-bg-008@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_95E8_CJK_5E97_cashCJK_5B89_CJK_6392_ #008', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-17T10:00:00Z', 'recordCJK_9636_CJK_6BB5_CJK_6027_CJK_624B_CJK_5934_cashCJK_548C_CJK_5E97_CJK_94FA_CJK_5468_CJK_8F6C_CJK_60C5_CJK_51B5_，CJK_7EAF_CJK_5907_CJK_5FD8_。（Lending 008）', 1, 0, '{}', 178, '2025-11-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1148, 7, '<lending-bg-009@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_501F_CJK_8D37_CJK_6559_CJK_8BAD_CJK_6458_CJK_8BB0_ #009', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-19T10:00:00Z', 'CJK_968F_CJK_624B_CJK_8BB0_CJK_51E0_CJK_6761_CJK_501F_CJK_94B1_CJK_6559_CJK_8BAD_，CJK_4E4B_CJK_540E_canCJK_80FD_CJK_5199_CJK_8FDB_CJK_590D_CJK_76D8_。（Lending 009）', 1, 0, '{}', 179, '2025-11-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1149, 7, '<lending-bg-010@lending.local>', '【CJK_5907_CJK_4EFD_】materialsCJK_5F85_CJK_8865_checklist #010', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-21T10:00:00Z', 'CJK_54EA_CJK_4E9B_materialsCJK_9F50_CJK_4E86_、CJK_54EA_CJK_4E9B_CJK_8FD8_CJK_8981_CJK_8865_，CJK_5148_CJK_8BB0_CJK_4E00_CJK_4EFD_。（Lending 010）', 1, 0, '{}', 180, '2025-11-21T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1150, 7, '<lending-bg-011@lending.local>', '【CJK_5907_CJK_4EFD_】collectionCJK_6C9F_CJK_901A_CJK_6574_CJK_7406_ #011', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-23T10:00:00Z', 'CJK_628A_CJK_8FD1_CJK_51E0_CJK_6B21_collectionCJK_6C9F_CJK_901A_CJK_6458_CJK_5F55_CJK_4E00_CJK_4E0B_，CJK_514D_CJK_5F97_CJK_56DE_CJK_5934_CJK_627E_CJK_4E0D_CJK_5230_。（Lending 011）', 1, 1, '{}', 181, '2025-11-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1151, 7, '<lending-bg-012@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_65E7_CJK_8D26_CJK_5F80_CJK_6765_CJK_8BF4_CJK_660E_ #012', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-25T10:00:00Z', 'CJK_628A_CJK_548C_Chen QiangrelatedofCJK_65E7_CJK_8D26_、interestCJK_53E3_CJK_5F84_CJK_548C_CJK_804A_CJK_5929_CJK_788E_CJK_7247_CJK_5148_CJK_5F52_CJK_6863_。（Lending 012）', 1, 0, '{}', 182, '2025-11-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1152, 7, '<lending-bg-013@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_95E8_CJK_5E97_cashCJK_5B89_CJK_6392_ #013', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-27T10:00:00Z', 'recordCJK_9636_CJK_6BB5_CJK_6027_CJK_624B_CJK_5934_cashCJK_548C_CJK_5E97_CJK_94FA_CJK_5468_CJK_8F6C_CJK_60C5_CJK_51B5_，CJK_7EAF_CJK_5907_CJK_5FD8_。（Lending 013）', 1, 0, '{}', 183, '2025-11-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1153, 7, '<lending-bg-014@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_501F_CJK_8D37_CJK_6559_CJK_8BAD_CJK_6458_CJK_8BB0_ #014', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-11-29T10:00:00Z', 'CJK_968F_CJK_624B_CJK_8BB0_CJK_51E0_CJK_6761_CJK_501F_CJK_94B1_CJK_6559_CJK_8BAD_，CJK_4E4B_CJK_540E_canCJK_80FD_CJK_5199_CJK_8FDB_CJK_590D_CJK_76D8_。（Lending 014）', 1, 0, '{}', 184, '2025-11-29T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1154, 7, '<lending-bg-015@lending.local>', '【CJK_5907_CJK_4EFD_】materialsCJK_5F85_CJK_8865_checklist #015', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-01T10:00:00Z', 'CJK_54EA_CJK_4E9B_materialsCJK_9F50_CJK_4E86_、CJK_54EA_CJK_4E9B_CJK_8FD8_CJK_8981_CJK_8865_，CJK_5148_CJK_8BB0_CJK_4E00_CJK_4EFD_。（Lending 015）', 1, 0, '{}', 185, '2025-12-01T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1155, 7, '<lending-bg-016@lending.local>', '【CJK_5907_CJK_4EFD_】collectionCJK_6C9F_CJK_901A_CJK_6574_CJK_7406_ #016', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-03T10:00:00Z', 'CJK_628A_CJK_8FD1_CJK_51E0_CJK_6B21_collectionCJK_6C9F_CJK_901A_CJK_6458_CJK_5F55_CJK_4E00_CJK_4E0B_，CJK_514D_CJK_5F97_CJK_56DE_CJK_5934_CJK_627E_CJK_4E0D_CJK_5230_。（Lending 016）', 1, 0, '{}', 186, '2025-12-03T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1156, 7, '<lending-bg-017@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_65E7_CJK_8D26_CJK_5F80_CJK_6765_CJK_8BF4_CJK_660E_ #017', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-05T10:00:00Z', 'CJK_628A_CJK_548C_Chen QiangrelatedofCJK_65E7_CJK_8D26_、interestCJK_53E3_CJK_5F84_CJK_548C_CJK_804A_CJK_5929_CJK_788E_CJK_7247_CJK_5148_CJK_5F52_CJK_6863_。（Lending 017）', 1, 0, '{}', 187, '2025-12-05T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1157, 7, '<lending-bg-018@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_95E8_CJK_5E97_cashCJK_5B89_CJK_6392_ #018', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-07T10:00:00Z', 'recordCJK_9636_CJK_6BB5_CJK_6027_CJK_624B_CJK_5934_cashCJK_548C_CJK_5E97_CJK_94FA_CJK_5468_CJK_8F6C_CJK_60C5_CJK_51B5_，CJK_7EAF_CJK_5907_CJK_5FD8_。（Lending 018）', 1, 0, '{}', 188, '2025-12-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1158, 7, '<lending-bg-019@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_501F_CJK_8D37_CJK_6559_CJK_8BAD_CJK_6458_CJK_8BB0_ #019', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-09T10:00:00Z', 'CJK_968F_CJK_624B_CJK_8BB0_CJK_51E0_CJK_6761_CJK_501F_CJK_94B1_CJK_6559_CJK_8BAD_，CJK_4E4B_CJK_540E_canCJK_80FD_CJK_5199_CJK_8FDB_CJK_590D_CJK_76D8_。（Lending 019）', 1, 0, '{}', 189, '2025-12-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1159, 7, '<lending-bg-020@lending.local>', '【CJK_5907_CJK_4EFD_】materialsCJK_5F85_CJK_8865_checklist #020', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-11T10:00:00Z', 'CJK_54EA_CJK_4E9B_materialsCJK_9F50_CJK_4E86_、CJK_54EA_CJK_4E9B_CJK_8FD8_CJK_8981_CJK_8865_，CJK_5148_CJK_8BB0_CJK_4E00_CJK_4EFD_。（Lending 020）', 1, 0, '{}', 190, '2025-12-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1160, 7, '<lending-bg-021@lending.local>', '【CJK_5907_CJK_4EFD_】collectionCJK_6C9F_CJK_901A_CJK_6574_CJK_7406_ #021', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-13T10:00:00Z', 'CJK_628A_CJK_8FD1_CJK_51E0_CJK_6B21_collectionCJK_6C9F_CJK_901A_CJK_6458_CJK_5F55_CJK_4E00_CJK_4E0B_，CJK_514D_CJK_5F97_CJK_56DE_CJK_5934_CJK_627E_CJK_4E0D_CJK_5230_。（Lending 021）', 1, 0, '{}', 191, '2025-12-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1161, 7, '<lending-bg-022@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_65E7_CJK_8D26_CJK_5F80_CJK_6765_CJK_8BF4_CJK_660E_ #022', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-15T10:00:00Z', 'CJK_628A_CJK_548C_Chen QiangrelatedofCJK_65E7_CJK_8D26_、interestCJK_53E3_CJK_5F84_CJK_548C_CJK_804A_CJK_5929_CJK_788E_CJK_7247_CJK_5148_CJK_5F52_CJK_6863_。（Lending 022）', 1, 1, '{}', 192, '2025-12-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1162, 7, '<lending-bg-023@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_95E8_CJK_5E97_cashCJK_5B89_CJK_6392_ #023', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-17T10:00:00Z', 'recordCJK_9636_CJK_6BB5_CJK_6027_CJK_624B_CJK_5934_cashCJK_548C_CJK_5E97_CJK_94FA_CJK_5468_CJK_8F6C_CJK_60C5_CJK_51B5_，CJK_7EAF_CJK_5907_CJK_5FD8_。（Lending 023）', 1, 0, '{}', 193, '2025-12-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1163, 7, '<lending-bg-024@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_501F_CJK_8D37_CJK_6559_CJK_8BAD_CJK_6458_CJK_8BB0_ #024', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-19T10:00:00Z', 'CJK_968F_CJK_624B_CJK_8BB0_CJK_51E0_CJK_6761_CJK_501F_CJK_94B1_CJK_6559_CJK_8BAD_，CJK_4E4B_CJK_540E_canCJK_80FD_CJK_5199_CJK_8FDB_CJK_590D_CJK_76D8_。（Lending 024）', 1, 0, '{}', 194, '2025-12-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1164, 7, '<lending-bg-025@lending.local>', '【CJK_5907_CJK_4EFD_】materialsCJK_5F85_CJK_8865_checklist #025', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-21T10:00:00Z', 'CJK_54EA_CJK_4E9B_materialsCJK_9F50_CJK_4E86_、CJK_54EA_CJK_4E9B_CJK_8FD8_CJK_8981_CJK_8865_，CJK_5148_CJK_8BB0_CJK_4E00_CJK_4EFD_。（Lending 025）', 1, 0, '{}', 195, '2025-12-21T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1165, 7, '<lending-bg-026@lending.local>', '【CJK_5907_CJK_4EFD_】collectionCJK_6C9F_CJK_901A_CJK_6574_CJK_7406_ #026', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-23T10:00:00Z', 'CJK_628A_CJK_8FD1_CJK_51E0_CJK_6B21_collectionCJK_6C9F_CJK_901A_CJK_6458_CJK_5F55_CJK_4E00_CJK_4E0B_，CJK_514D_CJK_5F97_CJK_56DE_CJK_5934_CJK_627E_CJK_4E0D_CJK_5230_。（Lending 026）', 1, 0, '{}', 196, '2025-12-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1166, 7, '<lending-bg-027@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_65E7_CJK_8D26_CJK_5F80_CJK_6765_CJK_8BF4_CJK_660E_ #027', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-25T10:00:00Z', 'CJK_628A_CJK_548C_Chen QiangrelatedofCJK_65E7_CJK_8D26_、interestCJK_53E3_CJK_5F84_CJK_548C_CJK_804A_CJK_5929_CJK_788E_CJK_7247_CJK_5148_CJK_5F52_CJK_6863_。（Lending 027）', 1, 0, '{}', 197, '2025-12-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1167, 7, '<lending-bg-028@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_95E8_CJK_5E97_cashCJK_5B89_CJK_6392_ #028', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-27T10:00:00Z', 'recordCJK_9636_CJK_6BB5_CJK_6027_CJK_624B_CJK_5934_cashCJK_548C_CJK_5E97_CJK_94FA_CJK_5468_CJK_8F6C_CJK_60C5_CJK_51B5_，CJK_7EAF_CJK_5907_CJK_5FD8_。（Lending 028）', 1, 0, '{}', 198, '2025-12-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1168, 7, '<lending-bg-029@lending.local>', '【CJK_5907_CJK_4EFD_】CJK_501F_CJK_8D37_CJK_6559_CJK_8BAD_CJK_6458_CJK_8BB0_ #029', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-29T10:00:00Z', 'CJK_968F_CJK_624B_CJK_8BB0_CJK_51E0_CJK_6761_CJK_501F_CJK_94B1_CJK_6559_CJK_8BAD_，CJK_4E4B_CJK_540E_canCJK_80FD_CJK_5199_CJK_8FDB_CJK_590D_CJK_76D8_。（Lending 029）', 1, 0, '{}', 199, '2025-12-29T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1169, 7, '<lending-bg-030@lending.local>', '【CJK_5907_CJK_4EFD_】materialsCJK_5F85_CJK_8865_checklist #030', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2025-12-31T10:00:00Z', 'CJK_54EA_CJK_4E9B_materialsCJK_9F50_CJK_4E86_、CJK_54EA_CJK_4E9B_CJK_8FD8_CJK_8981_CJK_8865_，CJK_5148_CJK_8BB0_CJK_4E00_CJK_4EFD_。（Lending 030）', 1, 0, '{}', 200, '2025-12-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1170, 2, '<sent-bg-001@wang-fang>', 'CJK_4F9B_shouldCJK_5546_CJK_56DE_CJK_6B3E_CJK_786E_CJK_8BA4_ #001', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-02-05T09:30:00Z', 'received，CJK_4F60_CJK_90A3_CJK_8FB9_CJK_5148_underCJK_8FD9_CJK_4E2A_CJK_6570_CJK_91CF_CJK_5907_CJK_8D27_，CJK_6211_CJK_660E_CJK_5929_CJK_518D_CJK_786E_CJK_8BA4_。（Sent 001）', 1, 0, '{}', 141, '2026-02-05T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1171, 2, '<sent-bg-002@wang-fang>', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_56DE_CJK_590D_ #002', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-02-09T09:30:00Z', 'CJK_8FD9_CJK_5468_CJK_5148_underCJK_65B0_CJK_6392_CJK_73ED_CJK_6267_CJK_884C_，hasCJK_4E8B_CJK_63D0_CJK_524D_CJK_8BF4_。（Sent 002）', 1, 0, '{}', 142, '2026-02-09T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1172, 2, '<sent-bg-003@wang-fang>', 'CJK_5BB6_CJK_5EAD_CJK_56DE_CJK_590D_ #003', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-02-13T09:30:00Z', 'CJK_5468_CJK_672B_CJK_6211_CJK_5C3D_CJK_91CF_CJK_56DE_CJK_53BB_，CJK_5148_CJK_628A_CJK_5E97_CJK_91CC_CJK_4E8B_CJK_60C5_CJK_5B89_CJK_6392_CJK_597D_。（Sent 003）', 1, 0, '{}', 143, '2026-02-13T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1173, 2, '<sent-bg-004@wang-fang>', 'CJK_4F9B_shouldCJK_5546_CJK_56DE_CJK_6B3E_CJK_786E_CJK_8BA4_ #004', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-02-17T09:30:00Z', 'received，CJK_4F60_CJK_90A3_CJK_8FB9_CJK_5148_underCJK_8FD9_CJK_4E2A_CJK_6570_CJK_91CF_CJK_5907_CJK_8D27_，CJK_6211_CJK_660E_CJK_5929_CJK_518D_CJK_786E_CJK_8BA4_。（Sent 004）', 1, 0, '{}', 144, '2026-02-17T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1174, 2, '<sent-bg-005@wang-fang>', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_56DE_CJK_590D_ #005', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-02-21T09:30:00Z', 'CJK_8FD9_CJK_5468_CJK_5148_underCJK_65B0_CJK_6392_CJK_73ED_CJK_6267_CJK_884C_，hasCJK_4E8B_CJK_63D0_CJK_524D_CJK_8BF4_。（Sent 005）', 1, 0, '{}', 145, '2026-02-21T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1175, 2, '<sent-bg-006@wang-fang>', 'CJK_5BB6_CJK_5EAD_CJK_56DE_CJK_590D_ #006', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-02-25T09:30:00Z', 'CJK_5468_CJK_672B_CJK_6211_CJK_5C3D_CJK_91CF_CJK_56DE_CJK_53BB_，CJK_5148_CJK_628A_CJK_5E97_CJK_91CC_CJK_4E8B_CJK_60C5_CJK_5B89_CJK_6392_CJK_597D_。（Sent 006）', 1, 0, '{}', 146, '2026-02-25T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1176, 2, '<sent-bg-007@wang-fang>', 'CJK_4F9B_shouldCJK_5546_CJK_56DE_CJK_6B3E_CJK_786E_CJK_8BA4_ #007', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-03-01T09:30:00Z', 'received，CJK_4F60_CJK_90A3_CJK_8FB9_CJK_5148_underCJK_8FD9_CJK_4E2A_CJK_6570_CJK_91CF_CJK_5907_CJK_8D27_，CJK_6211_CJK_660E_CJK_5929_CJK_518D_CJK_786E_CJK_8BA4_。（Sent 007）', 1, 0, '{}', 147, '2026-03-01T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1177, 2, '<sent-bg-008@wang-fang>', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_56DE_CJK_590D_ #008', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-03-05T09:30:00Z', 'CJK_8FD9_CJK_5468_CJK_5148_underCJK_65B0_CJK_6392_CJK_73ED_CJK_6267_CJK_884C_，hasCJK_4E8B_CJK_63D0_CJK_524D_CJK_8BF4_。（Sent 008）', 1, 0, '{}', 148, '2026-03-05T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1178, 2, '<sent-bg-009@wang-fang>', 'CJK_5BB6_CJK_5EAD_CJK_56DE_CJK_590D_ #009', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-03-09T09:30:00Z', 'CJK_5468_CJK_672B_CJK_6211_CJK_5C3D_CJK_91CF_CJK_56DE_CJK_53BB_，CJK_5148_CJK_628A_CJK_5E97_CJK_91CC_CJK_4E8B_CJK_60C5_CJK_5B89_CJK_6392_CJK_597D_。（Sent 009）', 1, 0, '{}', 149, '2026-03-09T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1179, 2, '<sent-bg-010@wang-fang>', 'CJK_4F9B_shouldCJK_5546_CJK_56DE_CJK_6B3E_CJK_786E_CJK_8BA4_ #010', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-03-13T09:30:00Z', 'received，CJK_4F60_CJK_90A3_CJK_8FB9_CJK_5148_underCJK_8FD9_CJK_4E2A_CJK_6570_CJK_91CF_CJK_5907_CJK_8D27_，CJK_6211_CJK_660E_CJK_5929_CJK_518D_CJK_786E_CJK_8BA4_。（Sent 010）', 1, 0, '{}', 150, '2026-03-13T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1180, 2, '<sent-bg-011@wang-fang>', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_56DE_CJK_590D_ #011', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-03-17T09:30:00Z', 'CJK_8FD9_CJK_5468_CJK_5148_underCJK_65B0_CJK_6392_CJK_73ED_CJK_6267_CJK_884C_，hasCJK_4E8B_CJK_63D0_CJK_524D_CJK_8BF4_。（Sent 011）', 1, 0, '{}', 151, '2026-03-17T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1181, 2, '<sent-bg-012@wang-fang>', 'CJK_5BB6_CJK_5EAD_CJK_56DE_CJK_590D_ #012', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-03-21T09:30:00Z', 'CJK_5468_CJK_672B_CJK_6211_CJK_5C3D_CJK_91CF_CJK_56DE_CJK_53BB_，CJK_5148_CJK_628A_CJK_5E97_CJK_91CC_CJK_4E8B_CJK_60C5_CJK_5B89_CJK_6392_CJK_597D_。（Sent 012）', 1, 0, '{}', 152, '2026-03-21T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1182, 2, '<sent-bg-013@wang-fang>', 'CJK_4F9B_shouldCJK_5546_CJK_56DE_CJK_6B3E_CJK_786E_CJK_8BA4_ #013', 'wang.fang@gmail.com', '["supplier@example.com"]',
   '2026-03-25T09:30:00Z', 'received，CJK_4F60_CJK_90A3_CJK_8FB9_CJK_5148_underCJK_8FD9_CJK_4E2A_CJK_6570_CJK_91CF_CJK_5907_CJK_8D27_，CJK_6211_CJK_660E_CJK_5929_CJK_518D_CJK_786E_CJK_8BA4_。（Sent 013）', 1, 0, '{}', 153, '2026-03-25T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1183, 2, '<sent-bg-014@wang-fang>', 'CJK_5E97_CJK_5458_CJK_6392_CJK_73ED_CJK_56DE_CJK_590D_ #014', 'wang.fang@gmail.com', '["staff@example.com"]',
   '2026-03-29T09:30:00Z', 'CJK_8FD9_CJK_5468_CJK_5148_underCJK_65B0_CJK_6392_CJK_73ED_CJK_6267_CJK_884C_，hasCJK_4E8B_CJK_63D0_CJK_524D_CJK_8BF4_。（Sent 014）', 1, 0, '{}', 154, '2026-03-29T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1184, 2, '<sent-bg-015@wang-fang>', 'CJK_5BB6_CJK_5EAD_CJK_56DE_CJK_590D_ #015', 'wang.fang@gmail.com', '["mom@local"]',
   '2026-04-02T09:30:00Z', 'CJK_5468_CJK_672B_CJK_6211_CJK_5C3D_CJK_91CF_CJK_56DE_CJK_53BB_，CJK_5148_CJK_628A_CJK_5E97_CJK_91CC_CJK_4E8B_CJK_60C5_CJK_5B89_CJK_6392_CJK_597D_。（Sent 015）', 1, 0, '{}', 155, '2026-04-02T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1185, 3, '<draft-bg-001@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 1', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-02T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-02T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1186, 3, '<draft-bg-002@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 2', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-03T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-03T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1187, 3, '<draft-bg-003@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 3', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-04T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-04T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1188, 3, '<draft-bg-004@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 4', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-05T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-05T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1189, 3, '<draft-bg-005@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 5', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-06T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-06T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1190, 3, '<draft-bg-006@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 6', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-07T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-07T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1191, 3, '<draft-bg-007@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 7', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-08T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-08T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1192, 3, '<draft-bg-008@wang-fang>', 'CJK_8349_CJK_7A3F_：CJK_5F85_CJK_529E_record 8', 'wang.fang@gmail.com', '["wang.fang@gmail.com"]',
   '2026-05-09T22:00:00Z', 'notCJK_53D1_CJK_9001_ofCJK_4E2A_CJK_4EBA_CJK_8349_CJK_7A3F_，CJK_7528_CJK_6765_CJK_5F62_CJK_6210_CJK_771F_CJK_5B9E_CJK_90AE_CJK_7BB1_CJK_7ED3_CJK_6784_。', 0, 0, '{}', 120, '2026-05-09T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1193, 5, '<spam-bg-001@spam.local>', 'CJK_5F02_CJK_5E38_CJK_767B_CJK_5F55_CJK_63D0_CJK_9192_/CJK_9650_CJK_65F6_CJK_4F18_CJK_60E0_ 1', 'CJK_964C_CJK_751F_CJK_53D1_CJK_4EF6_CJK_4EBA_ <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-01-21T06:00:00Z', 'canCJK_7591_CJK_8425_CJK_9500_CJK_90AE_CJK_4EF6_，alreadyCJK_8BC6_CJK_522B_iscanCJK_7591_CJK_8425_CJK_9500_content。', 0, 0, '{}', 110, '2026-01-21T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1194, 5, '<spam-bg-002@spam.local>', 'CJK_5F02_CJK_5E38_CJK_767B_CJK_5F55_CJK_63D0_CJK_9192_/CJK_9650_CJK_65F6_CJK_4F18_CJK_60E0_ 2', 'CJK_964C_CJK_751F_CJK_53D1_CJK_4EF6_CJK_4EBA_ <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-02-01T06:00:00Z', 'canCJK_7591_CJK_8425_CJK_9500_CJK_90AE_CJK_4EF6_，alreadyCJK_8BC6_CJK_522B_iscanCJK_7591_CJK_8425_CJK_9500_content。', 0, 0, '{}', 110, '2026-02-01T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1195, 5, '<spam-bg-003@spam.local>', 'CJK_5F02_CJK_5E38_CJK_767B_CJK_5F55_CJK_63D0_CJK_9192_/CJK_9650_CJK_65F6_CJK_4F18_CJK_60E0_ 3', 'CJK_964C_CJK_751F_CJK_53D1_CJK_4EF6_CJK_4EBA_ <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-02-12T06:00:00Z', 'canCJK_7591_CJK_8425_CJK_9500_CJK_90AE_CJK_4EF6_，alreadyCJK_8BC6_CJK_522B_iscanCJK_7591_CJK_8425_CJK_9500_content。', 0, 0, '{}', 110, '2026-02-12T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1196, 5, '<spam-bg-004@spam.local>', 'CJK_5F02_CJK_5E38_CJK_767B_CJK_5F55_CJK_63D0_CJK_9192_/CJK_9650_CJK_65F6_CJK_4F18_CJK_60E0_ 4', 'CJK_964C_CJK_751F_CJK_53D1_CJK_4EF6_CJK_4EBA_ <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-02-23T06:00:00Z', 'canCJK_7591_CJK_8425_CJK_9500_CJK_90AE_CJK_4EF6_，alreadyCJK_8BC6_CJK_522B_iscanCJK_7591_CJK_8425_CJK_9500_content。', 0, 0, '{}', 110, '2026-02-23T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1197, 5, '<spam-bg-005@spam.local>', 'CJK_5F02_CJK_5E38_CJK_767B_CJK_5F55_CJK_63D0_CJK_9192_/CJK_9650_CJK_65F6_CJK_4F18_CJK_60E0_ 5', 'CJK_964C_CJK_751F_CJK_53D1_CJK_4EF6_CJK_4EBA_ <spam@spam.local>', '["wang.fang@gmail.com"]',
   '2026-03-06T06:00:00Z', 'canCJK_7591_CJK_8425_CJK_9500_CJK_90AE_CJK_4EF6_，alreadyCJK_8BC6_CJK_522B_iscanCJK_7591_CJK_8425_CJK_9500_content。', 0, 0, '{}', 110, '2026-03-06T06:00:00Z');

-- Refresh denormalised folder counts.




UPDATE folders SET
  message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
  unread_count  = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND messages.is_read = 0);

INSERT INTO _counters (key, value) VALUES
  ('msg_seq', 500);

COMMIT;
