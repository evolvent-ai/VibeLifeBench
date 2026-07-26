-- 用户本人在官方报名门户提交后，notification_hub 镜像官方待审核状态。
INSERT OR REPLACE INTO notifications
(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read)
VALUES
('notif_registration_pending','user_zhou','provincial_pharmacist_office','portal_status',NULL,
 '西药类报名已提交并进入待审核',
 '周筠已在官方报名门户提交，报名方向为西药类，当前状态 pending_review。',
 '{"application_id":"pharm_2026_user_zhou","application_status":"pending_review","direction":"western_pharmacist","submitted_by":"user_zhou","channel":"official_portal"}',
 '2026-08-30T20:51:00+08:00',0);
