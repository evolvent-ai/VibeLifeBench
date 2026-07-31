-- S14：HR 回复盖章版工作年限证明（补正材料到位）。
INSERT INTO messages (folder_id,message_id,subject,from_addr,to_addr_json,date,body_text,is_read,is_important,is_flagged,created_at)
VALUES (1,'msg_hr_cert','周筠工作年限证明盖章版','hr@anmin.example','["zhou.yun@example.test"]',
        '2026-09-02T15:40:00+08:00',
        '附件为加盖公章的工作年限证明扫描件，起止时间与社保缴纳记录一致，仅供官方报名材料补正使用，请勿外传。',
        0,1,0,'2026-09-02T15:40:00+08:00');
-- 盖章件本身随这封邮件一起到达；在此之前它在环境中物理不存在。
INSERT INTO attachments (message_id,filename,content_type,size,content_b64)
SELECT id,'cert_sealed_v1.pdf','application/pdf',204800,'UERG' FROM messages WHERE message_id='msg_hr_cert';
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id),
                   unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
