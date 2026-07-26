INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3022,1,'<driver-doc@bus>','沪嘉包车：司机资质补件说明','ops@bus.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-13T08:10:00+08:00','原定的王师傅从业资格证在换证期，纸质件还没下来。我们可以换成李师傅出车，A1证和从业资格都在有效期内，也可以等王师傅的证件下来再定，但那样要拖到十九号。你倾向哪种我们照办。','',0,1,0,'{}',3022,400,'2026-07-13T00:10:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3022)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<driver-doc@bus>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<driver-doc@bus>','沪嘉包车：司机资质补件说明','ops@bus.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-13T08:10:00+08:00','原定的王师傅从业资格证在换证期，纸质件还没下来。我们可以换成李师傅出车，A1证和从业资格都在有效期内，也可以等王师傅的证件下来再定，但那样要拖到十九号。你倾向哪种我们照办。','',0,1,0,'{}',3022,400,'2026-07-13T00:10:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<driver-doc@bus>');
