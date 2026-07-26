BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s7-jurisdiction@hzxihu-court.gov.cn>', '电子送达：管辖权异议材料',
       '杭州市西湖区人民法院电子送达 <service@hzxihu-court.gov.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-05-30T09:02:00+08:00',
       '王芳：陈强以住所地位于宁波市海曙区为由提出管辖权异议，请求移送宁波法院。附件为异议申请书及送达回证，请在法院指定时间内提交书面意见。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"管辖权异议申请书","case_no":"（2026）浙0106民初08812号"}', NULL, 460,
       '2026-05-30T09:02:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s7-jurisdiction@hzxihu-court.gov.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
