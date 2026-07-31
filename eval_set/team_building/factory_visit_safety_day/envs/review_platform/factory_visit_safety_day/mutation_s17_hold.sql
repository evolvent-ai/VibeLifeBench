UPDATE deals SET status='active' WHERE deal_id='deal_factory_013_visit';
INSERT OR IGNORE INTO merchant_qa(qa_id,merchant_id,user_id,question,answer,answered_by,created_at) VALUES ('qa_factory_credential_ok','mer_7a4c19d2','vendor','保险附件补齐了吗？','已补齐并通过平台复核，参访名额恢复为可预留状态。','merchant','2026-07-18T00:30:00Z');
