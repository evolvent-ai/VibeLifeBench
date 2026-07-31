-- Stage 13 (2026-07-14): 平台对已关注场馆发起资质复核。
-- 平台在发起复核时会为该场馆建立一条资质审核订阅，通知挂在这条订阅下；
-- notifications.subscription_id 对 subscriptions 有外键，故订阅必须与通知一起写入。
INSERT OR IGNORE INTO subscriptions(subscription_id,user_id,source,type,target,condition_json,status,created_at,updated_at) VALUES ('sub_013_supplier_audit','user_seed_tb_013','review_platform','policy_update','mer_7a4c19d2','{"scope":"qualification"}','active','2026-07-14T00:10:00Z','2026-07-14T00:10:00Z');
INSERT OR IGNORE INTO notifications(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read) VALUES ('ntf_013_cred_gap','user_seed_tb_013','review_platform','policy_update','sub_013_supplier_audit','场馆资质复核中','平台对一家已关注场馆发起资质复核，复核期间部分预留能力受限。','{"scope":"qualification"}','2026-07-14T00:10:00Z',0);
