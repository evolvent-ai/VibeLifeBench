-- Stable pre-task Notion history. The emergency-trip journal remains minimal for agent creation.
INSERT INTO users(user_id,name,avatar_url,email,type) VALUES ('notion_user_lin','林澈',NULL,'lin.che@example.test','person');
INSERT INTO workspaces(workspace_id,name,owner_user_id) VALUES ('workspace_lin_travel','Lin Family Travel Workspace','notion_user_lin');
INSERT INTO pages(page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover) VALUES
 ('page_initial_family_trip','workspace','workspace_lin_travel','家庭紧急行程工作页',0,'2026-04-01T00:00:00+08:00','2026-04-01T00:00:00+08:00','{"owner":"user_lin_che","status":"empty"}',NULL,NULL);
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<7)
INSERT INTO pages(page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover)
SELECT printf('page_history_%02d',n),'workspace','workspace_lin_travel',
       CASE n WHEN 1 THEN '家庭联系人维护记录' WHEN 2 THEN '年度保险资料索引' WHEN 3 THEN '北京常用交通备忘' WHEN 4 THEN '长辈就医陪同清单' WHEN 5 THEN '工作交接模板' WHEN 6 THEN '家庭费用分类说明' ELSE '证件保管原则' END,
       0,'2025-01-01T09:00:00+08:00','2026-03-20T09:00:00+08:00',printf('{"category":"history_%02d"}',n),NULL,NULL
FROM seq;

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<25)
INSERT INTO blocks(block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time)
SELECT printf('block_history_%03d',n),NULL,
       CASE WHEN n<=4 THEN 'page_initial_family_trip' ELSE printf('page_history_%02d',1+((n-5)%7)) END,
       CASE n%4 WHEN 0 THEN 'heading_2' ELSE 'paragraph' END,
       json_object('text',CASE n%13 WHEN 0 THEN '仅建立目录，具体行程应依据实时交通和用户确认补充。' WHEN 1 THEN '紧急联系人按关系分类，公开记录不保存完整证件信息。' WHEN 2 THEN '保险资料只记录保单入口和报案电话，不复制无关附件。' WHEN 3 THEN '北京常用交通按机场、铁路站和市内接驳分别整理。' WHEN 4 THEN '陪同长辈就医时优先安排电梯、短步行和清晰集合点。' WHEN 5 THEN '工作交接需要记录责任人、截止时间和可恢复状态。' WHEN 6 THEN '家庭费用按照交通、住宿、医疗和日常支出分栏。' WHEN 7 THEN '证件原件固定保管，临时副本使用后应及时清理。' WHEN 8 THEN '重要决定同时记录依据、授权范围和下一次复核时间。' WHEN 9 THEN '对外沟通采用必要字段，避免发送完整银行卡或证件影像。' WHEN 10 THEN '可取消项目可以先保留，不可退付款需要单独确认。' WHEN 11 THEN '老人电子票说明使用大字版，突出车次、时间、座位和接站口。' ELSE '长周期事项在日历、台账和提醒中保持一致。' END),
       0,0,n,'2025-01-01T09:00:00+08:00','2026-03-20T09:00:00+08:00'
FROM seq;
