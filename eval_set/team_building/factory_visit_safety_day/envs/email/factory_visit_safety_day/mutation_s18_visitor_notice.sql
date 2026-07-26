INSERT OR IGNORE INTO messages(id,folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 3028,1,'<visitor-final@factory>','嘉兴智造：最终访客须知（请转达全员）','security@factory.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-19T08:45:00+08:00','当天流程：八点四十门岗登记领访客证，九点安全交底二十分钟，之后分两组进车间。冲压区连续高分贝声响较大，请全员佩戴耳塞；打磨区有粉尘，经过时戴口罩并快速通过。叉车通道以黄线为界，任何情况不得跨越。客户样机区全线禁止拍摄，大厅合影点可以拍。中途身体不适举手示意，安全员会带到休息区，不需要说明原因。','',0,1,1,'{}',3028,520,'2026-07-19T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE id = 3028)
  AND NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<visitor-final@factory>');
INSERT INTO messages(folder_id,message_id,subject,from_addr,to_addr_json,cc_addr_json,bcc_addr_json,date,body_text,body_html,is_read,is_important,is_flagged,headers_json,uid,size,created_at)
SELECT 1,'<visitor-final@factory>','嘉兴智造：最终访客须知（请转达全员）','security@factory.example.invalid','["wei.ran@example.invalid"]','[]','[]','2026-07-19T08:45:00+08:00','当天流程：八点四十门岗登记领访客证，九点安全交底二十分钟，之后分两组进车间。冲压区连续高分贝声响较大，请全员佩戴耳塞；打磨区有粉尘，经过时戴口罩并快速通过。叉车通道以黄线为界，任何情况不得跨越。客户样机区全线禁止拍摄，大厅合影点可以拍。中途身体不适举手示意，安全员会带到休息区，不需要说明原因。','',0,1,1,'{}',3028,520,'2026-07-19T00:45:00Z'
WHERE NOT EXISTS (SELECT 1 FROM messages WHERE message_id = '<visitor-final@factory>');
