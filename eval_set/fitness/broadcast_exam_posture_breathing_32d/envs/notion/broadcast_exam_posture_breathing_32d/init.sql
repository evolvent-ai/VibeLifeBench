BEGIN;
INSERT OR REPLACE INTO users (user_id, name, avatar_url, email, type) VALUES ('lin_yu', '林雨', NULL, 'lin.yu@example.com', 'person');
INSERT OR REPLACE INTO workspaces (workspace_id, name, owner_user_id) VALUES ('ws_linyu_broadcast', '林雨播音艺考状态维护', 'lin_yu');
INSERT OR REPLACE INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES ('notion_broadcast_hub', 'workspace', 'ws_linyu_broadcast', '播音主持艺考状态总控', 0, '2026-10-05T19:05:00+08:00', '2026-10-05T19:05:00+08:00', '{}', NULL, NULL);
INSERT OR REPLACE INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES ('blk_broadcast_seed_001', NULL, 'notion_broadcast_hub', 'paragraph', '{"text": "起步模板：目标、计划、风险、授权、天气、数据质量和最终复盘。"}', 0, 0, 1, '2026-10-05T19:05:00+08:00', '2026-10-05T19:05:00+08:00');
INSERT OR REPLACE INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES ('blk_broadcast_seed_002', NULL, 'notion_broadcast_hub', 'paragraph', '{"text": "运行期请追加事实，不预填未来扰动。"}', 0, 0, 2, '2026-10-05T19:06:00+08:00', '2026-10-05T19:06:00+08:00');
INSERT INTO counters (key,value) VALUES ('page_seq',100),('block_seq',100),('database_seq',1),('row_seq',1),('comment_seq',1);
COMMIT;
