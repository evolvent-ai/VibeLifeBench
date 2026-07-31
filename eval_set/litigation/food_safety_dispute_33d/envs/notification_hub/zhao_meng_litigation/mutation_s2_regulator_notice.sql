BEGIN;
INSERT OR IGNORE INTO official_account_posts
  (post_id, account_id, title, summary, url, published_at) VALUES
  ('oap_food_s2_20260522', 'oa_sh_scjg', '进口预包装食品中文标签与非法添加检查提示',
   '上海市场监管部门提示经营者核对进口预包装食品中文标签、境内代理商和配料信息，并持续检查普通食品违法宣称疾病治疗作用及非法添加风险。',
   'https://scjgj.sh.gov.cn/food/20260522', '2026-05-22T09:15:00+08:00');
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s2_regulator', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '进口食品标签和非法添加检查提示',
   '市场监管部门发布进口食品中文标签和普通食品违法功效宣传检查提示。',
   '{"account_id":"oa_sh_scjg","post_id":"oap_food_s2_20260522"}', '2026-05-22T09:20:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
