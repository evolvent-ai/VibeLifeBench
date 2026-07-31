-- 若 Agent 已投递美团岗位，则把申请状态推进到 offer；未投递时仅保留外部招聘邮件，不伪造申请。
BEGIN IMMEDIATE;
UPDATE applications
SET status='offer', updated_at='2026-07-20T09:55:00Z'
WHERE user_id IN ('usr_gao_kai', 'gao_kai')
  AND job_id='job_gk_0001'
  AND status IN ('submitted', 'viewed', 'interview');
COMMIT;
