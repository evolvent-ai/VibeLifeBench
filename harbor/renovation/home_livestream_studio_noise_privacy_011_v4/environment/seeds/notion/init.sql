INSERT INTO users(user_id,name,email,type) VALUES('user_lwq','Wendy Lin','user_lwq@example.test','person');
INSERT INTO workspaces(workspace_id,name,owner_user_id) VALUES('ws_lwq','Wendy Linlivestreamworkspace','user_lwq');
INSERT INTO pages(page_id,parent_type,parent_id,title,created_time,last_edited_time,properties_json) VALUES('page_project','workspace','ws_lwq','home livestream studiorenovationmaster control','2026-07-01T00:00:00Z','2026-07-01T00:00:00Z','{}');
INSERT INTO blocks(block_id,parent_page_id,type,content_json,position,created_time,last_edited_time) VALUES('blk_project_1','page_project','paragraph','{"text":" Budget  18000；authorizationboundary：4000 CNY 、plan change、brandexternal sharing、more than 6 locationsdrilled holes。"}',1,'2026-07-01T00:00:00Z','2026-07-01T00:00:00Z');
INSERT INTO counters(key,value) VALUES('page_seq',100),('block_seq',100);
