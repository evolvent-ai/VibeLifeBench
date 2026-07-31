BEGIN;
INSERT OR IGNORE INTO official_account_posts
  (post_id, account_id, title, summary, url, published_at) VALUES
  ('oap_food_s1_20260521', 'oa_pudong_court', '食品安全网络购物纠纷诉讼服务更新',
   '浦东法院汇总网购食品纠纷的管辖、起诉材料、惩罚性赔偿、平台责任、证据保全和检验申请事项，供当事人办理立案和举证时核对。',
   'https://court.pudong.gov.cn/notice/food-20260521', '2026-05-21T08:50:00+08:00');
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s1_court', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '浦东法院更新食品安全网购纠纷诉讼服务说明',
   '诉讼服务说明已更新，内容涉及网购收货地管辖、起诉材料、食品检验、平台责任和证据提交。',
   '{"account_id":"oa_pudong_court","post_id":"oap_food_s1_20260521"}', '2026-05-21T08:55:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
