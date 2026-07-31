BEGIN;
INSERT OR IGNORE INTO official_account_posts
  (post_id, account_id, title, summary, url, published_at) VALUES
  ('oap_food_s4_20260524', 'oa_pudong_court', '网购食品案件证据和实物保管提示',
   '当事人应保留订单、支付记录、商品页面、客服沟通、开箱材料和涉案食品实物；涉及食品安全专门问题的，可依法申请具备资质的机构检验。',
   'https://court.pudong.gov.cn/notice/evidence-20260524', '2026-05-24T09:45:00+08:00');
INSERT OR IGNORE INTO notifications
  (notification_id, user_id, source, type, subscription_id, title, body, payload_json, created_at, read) VALUES
  ('ntf_food_s4_evidence', 'usr_zhao_meng', 'gov_policy', 'policy_update', 'sub_000002',
   '网购食品案件证据保管提示',
   '法院提示妥善保存食品实物、订单支付、商品页面、客服沟通、开箱材料和医疗票据。',
   '{"account_id":"oa_pudong_court","post_id":"oap_food_s4_20260524"}', '2026-05-24T09:50:00+08:00', 0);
UPDATE _counters SET value = CASE WHEN value < 500 THEN 500 ELSE value END WHERE key='notification_seq';
COMMIT;
