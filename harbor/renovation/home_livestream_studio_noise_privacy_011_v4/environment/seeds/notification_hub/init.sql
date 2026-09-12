INSERT INTO official_accounts(account_id,name,category,description) VALUES('acct_safety',' Home translatedequipmentsafetybulletin','safety','Equipment recalls and safety reminders'),('acct_platform','contentplatformlivestream assistant','content','Livestream rules and asset updates');
INSERT INTO notifications(notification_id,user_id,source,type,title,body,payload_json,created_at,read) VALUES
('notif_rules','user_lwq','content_platform','policy_update','livestreampublic assetsrules','public assetsmustrecordsource，must notusebrandconfidentialityimages。','{}','2026-07-01T09:00:00+08:00',0);
INSERT INTO _counters(key,value) VALUES('subscription_seq',100),('notification_seq',100),('alert_seq',100);
