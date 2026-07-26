-- 用户本人在官方报名门户支付后，镜像官方 paid 状态与收据标识。
INSERT OR REPLACE INTO notifications
(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read)
VALUES
('notif_payment_complete','user_zhou','provincial_pharmacist_office','portal_status',NULL,
 '西药类报名费支付成功',
 '官方报名费 CNY 244 已由周筠本人在官方报名门户支付，状态 paid。',
 '{"application_id":"pharm_2026_user_zhou","application_status":"paid","direction":"western_pharmacist","fee_minor":24400,"paid_minor":24400,"paid_by":"user_zhou","channel":"official_portal","receipt_id":"receipt_pharm_2026_user_zhou"}',
 '2026-09-18T21:11:00+08:00',0);
