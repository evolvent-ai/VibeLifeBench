INSERT OR IGNORE INTO messages
  (id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
VALUES
  (8006,1,'msg_lab_initial_0716','evidence record：evidence record','lab@kunlun-qc.example','["aygul.store@example.invalid"]','[]','[]','2026-07-16T13:50:00+08:00','evidence record NT-0712 evidence record；evidence record ML-0705 evidence record。evidence record、evidence record。',NULL,0,1,1,'{"source":"lab_initial_report"}',8006,82,'2026-07-16T13:50:00+08:00');
INSERT OR IGNORE INTO attachments
  (id,message_id,filename,content_type,size,content_b64,content_id)
VALUES
  (8104,8006,'lab_nt_0712_initial.txt','text/plain',122,'TlQtMDcxMiDlnZrmnpzljIXoo4Xlj5fmva7vvIzkuI3lrpzkuIrmnrbvvJvlu7rorq7miqXlup/miJbpgIDmjaLjgILkvLDnrpflvbHlk40gOTM2MC4wMCDlhYPjgILlrqLmiL/nlLXor50gMTM5MDAwMDExMTHjgII=','cid_lab_initial_0716');
UPDATE folders SET message_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id), unread_count=(SELECT COUNT(*) FROM messages WHERE folder_id=folders.id AND is_read=0);
