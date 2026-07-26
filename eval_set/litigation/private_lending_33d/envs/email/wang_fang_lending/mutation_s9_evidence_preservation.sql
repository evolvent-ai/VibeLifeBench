BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s9-evidence-preservation@hzxihu-court.gov.cn>', '电子送达：举证通知书及财产保全进展',
       '杭州市西湖区人民法院电子送达 <service@hzxihu-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-06-02T09:22:00+08:00',
       '王芳：本案举证期限为收到本通知之日起15日，请提交证据及证据清单。你申请的财产保全已作出裁定，相关查封或冻结手续正在办理；请持续关注保全送达和担保状态。',
       NULL, 0, 1, 1, NULL, NULL, '{"documents":["举证通知书","保全裁定进展"],"evidence_days":15}', NULL, 520,
       '2026-06-02T09:22:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s9-evidence-preservation@hzxihu-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
