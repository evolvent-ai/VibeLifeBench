BEGIN;
INSERT OR REPLACE INTO users (user_id, name, avatar_url, email, type) VALUES ('lin_yu', 'Lin Yu', NULL, 'lin.yu@example.com', 'person');
INSERT OR REPLACE INTO workspaces (workspace_id, name, owner_user_id) VALUES ('ws_linyu_broadcast', 'Lin Yu broadcast-arts exam status maintenance', 'lin_yu');
INSERT OR REPLACE INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES ('notion_broadcast_hub', 'workspace', 'ws_linyu_broadcast', 'Broadcast-arts exam control hub', 0, '2026-10-05T19:05:00+08:00', '2026-10-05T19:05:00+08:00', '{}', NULL, NULL);
INSERT OR REPLACE INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES ('blk_broadcast_seed_001', NULL, 'notion_broadcast_hub', 'paragraph', '{"text": "Starter template: goals, plan, risks, authorization, weather, data quality, and final review."}', 0, 0, 1, '2026-10-05T19:05:00+08:00', '2026-10-05T19:05:00+08:00');
INSERT OR REPLACE INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES ('blk_broadcast_seed_002', NULL, 'notion_broadcast_hub', 'paragraph', '{"text": "During operation, append facts; do not prefill future disturbances."}', 0, 0, 2, '2026-10-05T19:06:00+08:00', '2026-10-05T19:06:00+08:00');
INSERT INTO counters (key,value) VALUES ('page_seq',100),('block_seq',100),('database_seq',1),('row_seq',1),('comment_seq',1);
COMMIT;
