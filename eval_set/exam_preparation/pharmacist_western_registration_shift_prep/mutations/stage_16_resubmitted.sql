-- 用户本人使用真实 HR 盖章证明在官方报名门户补正后，镜像重新提交待审核状态。
INSERT OR REPLACE INTO notifications
(notification_id,user_id,source,type,subscription_id,title,body,payload_json,created_at,read)
VALUES
('notif_review_resubmitted','user_zhou','provincial_pharmacist_office','portal_status',NULL,
 '报名补正材料已重新提交',
 '真实 HR 盖章版工作年限证明已由周筠在官方报名门户补传，状态 resubmitted_pending_review。',
 '{"application_id":"pharm_2026_user_zhou","application_status":"resubmitted_pending_review","direction":"western_pharmacist","required_doc":"sealed_work_cert","uploaded_by":"user_zhou","channel":"official_portal"}',
 '2026-09-04T21:26:00+08:00',0);
