-- Stable pre-task Notion history. The emergency-trip journal remains minimal for agent creation.
INSERT INTO users(user_id,name,avatar_url,email,type) VALUES ('notion_user_lin','Lin Che',NULL,'lin.che@example.test','person');
INSERT INTO workspaces(workspace_id,name,owner_user_id) VALUES ('workspace_lin_travel','Lin Family Travel Workspace','notion_user_lin');
INSERT INTO pages(page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover) VALUES
 ('page_initial_family_trip','workspace','workspace_lin_travel','familyscenario text',0,'2026-04-01T00:00:00+08:00','2026-04-01T00:00:00+08:00','{"owner":"user_lin_che","status":"empty"}',NULL,NULL);
WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<7)
INSERT INTO pages(page_id,parent_type,parent_id,title,archived,created_time,last_edited_time,properties_json,icon,cover)
SELECT printf('page_history_%02d',n),'workspace','workspace_lin_travel',
       CASE n WHEN 1 THEN 'familyscenario text' WHEN 2 THEN 'scenario text' WHEN 3 THEN 'Beijingscenario text' WHEN 4 THEN 'elderscenario text' WHEN 5 THEN 'scenario text' WHEN 6 THEN 'familyexpensescenario text' ELSE 'scenario text' END,
       0,'2025-01-01T09:00:00+08:00','2026-03-20T09:00:00+08:00',printf('{"category":"history_%02d"}',n),NULL,NULL
FROM seq;

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<25)
INSERT INTO blocks(block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time)
SELECT printf('block_history_%03d',n),NULL,
       CASE WHEN n<=4 THEN 'page_initial_family_trip' ELSE printf('page_history_%02d',1+((n-5)%7)) END,
       CASE n%4 WHEN 0 THEN 'heading_2' ELSE 'paragraph' END,
       json_object('text',CASE n%13 WHEN 0 THEN 'scenario text，scenario text。' WHEN 1 THEN 'scenario text，scenario textStoresscenario text。' WHEN 2 THEN 'scenario text，scenario text。' WHEN 3 THEN 'Beijingscenario text、scenario text。' WHEN 4 THEN 'scenario textelderscenario text、scenario text。' WHEN 5 THEN 'scenario text、scenario texttimescenario textstatus。' WHEN 6 THEN 'familyexpensescenario text、scenario text、scenario text。' WHEN 7 THEN 'scenario text，scenario textcleanup。' WHEN 8 THEN 'scenario text、authorizationscenario texttime。' WHEN 9 THEN 'scenario text，scenario text。' WHEN 10 THEN 'scenario text，scenario text。' WHEN 11 THEN 'elderscenario text，scenario text、time、scenario textmeeting exit。' ELSE 'scenario textcalendar、scenario textreminderscenario text。' END),
       0,0,n,'2025-01-01T09:00:00+08:00','2026-03-20T09:00:00+08:00'
FROM seq;
