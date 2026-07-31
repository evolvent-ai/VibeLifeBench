-- Stage 10（2026-08-24）：药事管理与法规科目考试内容调整公告正式发布。
-- 原实现把这条公告放在 init.sql（published_at 2026-08-03），从 stage 0 起就能被
-- list_official_accounts / get_account_feed 查到，比 S10 事件早 21 天 —— 属手册
-- §3.8.10 第 2 类泄露"后续事实虽未提醒，但已经能通过查询接口查到"。
-- 现改为在本 stage 由事件驱动进入环境，published_at 与 S10 事件时间一致。
INSERT OR REPLACE INTO official_account_posts VALUES (
  'post_law_update_2026',
  'acct_pharm_exam',
  '2026 年度药事管理与法规科目考试内容调整公告',
  '根据法规修订情况，REG_GSP_IMPL_2016 已于 2026 年 1 月废止，相关内容不再列入考试范围；新增 REG_DRUG_TRACE_2026 药品追溯管理与 REG_RX_FLOW_2026 处方流转管理两项内容，考生复习时请以最新大纲为准。',
  'https://notice.pharm-exam.example.test/posts/post_law_update_2026',
  '2026-08-24T10:20:00+08:00'
);
