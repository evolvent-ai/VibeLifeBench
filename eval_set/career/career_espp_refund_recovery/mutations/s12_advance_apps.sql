-- s12: 卞翎的 canonical 用户投递状态后台推进；显式事务、重复执行无额外变化。
BEGIN IMMEDIATE;
UPDATE applications
SET status='interview', updated_at='2026-07-02T08:00:00Z'
WHERE application_id = (
  SELECT application_id
  FROM applications
  WHERE user_id IN ('usr_gao_kai', 'gao_kai') AND status='submitted'
  ORDER BY applied_at, application_id
  LIMIT 1
);
UPDATE applications
SET status='viewed', updated_at='2026-07-02T08:00:00Z'
WHERE user_id IN ('usr_gao_kai', 'gao_kai') AND status='submitted';
COMMIT;
