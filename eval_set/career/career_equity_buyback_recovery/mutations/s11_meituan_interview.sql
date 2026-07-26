-- 若 Agent 已投递美团岗位，则把可查询 application 状态推进到 interview；未投递时不伪造申请。
BEGIN IMMEDIATE;
UPDATE applications
SET status='interview', updated_at='2026-06-29T09:55:00Z'
WHERE user_id IN ('usr_gao_kai', 'gao_kai')
  AND job_id='job_gk_0001'
  AND status IN ('submitted', 'viewed');
COMMIT;
