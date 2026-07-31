BEGIN;
INSERT INTO messages
  (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html,
   is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at)
SELECT 1, '<lending-s4-bank-record@icbc.com.cn>', '电子回单已生成：2023年6月10日转账记录',
       '中国工商银行电子回单 <receipt@icbc.com.cn>', '["wang.fang@gmail.com"]', '[]', '[]',
       '2026-05-24T09:20:00+08:00',
       '王芳女士：你申请调取的历史交易电子回单已生成。记录显示2023年6月10日向陈强尾号8821账户转账人民币360000元，附电子印章，可下载保存；如需纸质盖章流水可到柜台办理。',
       NULL, 0, 1, 1, NULL, NULL, '{"document":"电子回单","amount":360000,"transfer_date":"2023-06-10"}', NULL, 430,
       '2026-05-24T09:20:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id='<lending-s4-bank-record@icbc.com.cn>');
UPDATE folders SET message_count=message_count+changes(), unread_count=unread_count+changes() WHERE id=1;
COMMIT;
