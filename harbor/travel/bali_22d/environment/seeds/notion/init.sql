BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    avatar_url TEXT,
    email TEXT,
    type TEXT DEFAULT 'person'
);

CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id TEXT PRIMARY KEY,
    name TEXT,
    owner_user_id TEXT
);

CREATE TABLE IF NOT EXISTS pages (
    page_id TEXT PRIMARY KEY,
    parent_type TEXT CHECK(parent_type IN ('workspace', 'page_id', 'database_id')),
    parent_id TEXT,
    title TEXT DEFAULT '',
    archived INTEGER DEFAULT 0,
    created_time TEXT,
    last_edited_time TEXT,
    properties_json TEXT DEFAULT '{}',
    icon TEXT,
    cover TEXT
);

CREATE TABLE IF NOT EXISTS databases (
    database_id TEXT PRIMARY KEY,
    parent_type TEXT CHECK(parent_type IN ('workspace', 'page_id')),
    parent_id TEXT,
    title TEXT DEFAULT '',
    schema_json TEXT DEFAULT '{}',
    archived INTEGER DEFAULT 0,
    created_time TEXT,
    last_edited_time TEXT
);

CREATE TABLE IF NOT EXISTS database_rows (
    row_id TEXT PRIMARY KEY,
    database_id TEXT,
    properties_json TEXT DEFAULT '{}',
    created_time TEXT,
    last_edited_time TEXT,
    archived INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS blocks (
    block_id TEXT PRIMARY KEY,
    parent_block_id TEXT,
    parent_page_id TEXT,
    type TEXT,
    content_json TEXT DEFAULT '{}',
    has_children INTEGER DEFAULT 0,
    archived INTEGER DEFAULT 0,
    position INTEGER DEFAULT 0,
    created_time TEXT,
    last_edited_time TEXT
);

INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
('usr_chen_yu', 'Chen Yu (Chen Yu)', 'https://avatar.example.com/chenyu.jpg', 'chen.yu@gmail.com', 'person'),
('usr_notion_bot', 'Notion Bot', NULL, NULL, 'bot');

INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
('ws_chen_personal', 'Chen Yu''s Personal Workspace', 'usr_chen_yu');

INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
('pg_bali_journal', 'workspace', 'ws_chen_personal', 'Bali Trip 2026 -- Journal', 0, '2026-05-15T10:00:00Z', '2026-05-23T14:30:00Z', '{}', '🏝️', NULL),
('pg_game_dev_notes', 'workspace', 'ws_chen_personal', 'Game Dev Notes', 0, '2024-08-15T09:00:00Z', '2026-05-20T16:45:00Z', '{}', '🎮', NULL),
('pg_reading_list', 'workspace', 'ws_chen_personal', 'Reading List', 0, '2024-06-01T10:00:00Z', '2026-05-10T12:00:00Z', '{}', '📚', NULL),
('pg_trip_research', 'workspace', 'ws_chen_personal', 'Trip Research', 0, '2026-05-10T11:00:00Z', '2026-05-18T15:20:00Z', '{}', '✈️', NULL);

INSERT INTO databases (database_id, parent_type, parent_id, title, schema_json, archived, created_time, last_edited_time) VALUES
('db_tasks', 'page_id', 'pg_bali_journal', 'Tasks', '{"Name": {"type": "title"}, "Status": {"type": "select", "options": ["todo", "in_progress", "done"]}, "Due Date": {"type": "date"}, "Priority": {"type": "select", "options": ["high", "medium", "low"]}}', 0, '2026-05-15T10:30:00Z', '2026-05-23T14:30:00Z');

INSERT INTO database_rows (row_id, database_id, properties_json, created_time, last_edited_time, archived) VALUES
('row_task_flights', 'db_tasks', '{"Name": {"title": [{"text": {"content": "Compare refundable Bali flights"}}]}, "Status": {"select": {"name": "in_progress"}}, "Due Date": {"date": {"start": "2026-06-06"}}, "Priority": {"select": {"name": "high"}}}', '2026-05-15T10:35:00Z', '2026-05-23T14:30:00Z', 0),
('row_task_activities', 'db_tasks', '{"Name": {"title": [{"text": {"content": "Research activities and attractions"}}]}, "Status": {"select": {"name": "in_progress"}}, "Due Date": {"date": {"start": "2026-05-25"}}, "Priority": {"select": {"name": "medium"}}}', '2026-05-15T10:40:00Z', '2026-05-23T14:30:00Z', 0),
('row_task_insurance', 'db_tasks', '{"Name": {"title": [{"text": {"content": "Get travel insurance"}}]}, "Status": {"select": {"name": "todo"}}, "Due Date": {"date": {"start": "2026-05-30"}}, "Priority": {"select": {"name": "high"}}}', '2026-05-15T10:45:00Z', '2026-05-15T10:45:00Z', 0);

INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
('blk_bali_heading1', NULL, 'pg_bali_journal', 'heading_1', '{"rich_text": [{"type": "text", "text": {"content": "Trip Overview"}}]}', 0, 0, 0, '2026-05-15T10:10:00Z', '2026-05-15T10:10:00Z'),
('blk_bali_para1', NULL, 'pg_bali_journal', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "Planning our babymoon trip to Bali from June 10 to July 1, 2026. Meilin is 6 months pregnant, so we need to keep activities relaxing and safe."}}]}', 0, 0, 1, '2026-05-15T10:12:00Z', '2026-05-15T10:12:00Z'),
('blk_bali_heading2', NULL, 'pg_bali_journal', 'heading_2', '{"rich_text": [{"type": "text", "text": {"content": "Accommodation"}}]}', 0, 0, 2, '2026-05-15T10:15:00Z', '2026-05-15T10:15:00Z'),
('blk_bali_para2', NULL, 'pg_bali_journal', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "Shortlisting refundable Seminyak stays with reliable cooling, humidity control, and practical access to a hospital; no room is reserved yet."}}]}', 0, 0, 3, '2026-05-15T10:16:00Z', '2026-05-23T14:30:00Z'),
('blk_gamedev_heading1', NULL, 'pg_game_dev_notes', 'heading_1', '{"rich_text": [{"type": "text", "text": {"content": "Unity Optimization Tips"}}]}', 0, 0, 0, '2024-08-15T09:10:00Z', '2024-08-15T09:10:00Z'),
('blk_gamedev_list1', NULL, 'pg_game_dev_notes', 'bulleted_list_item', '{"rich_text": [{"type": "text", "text": {"content": "Use object pooling for frequently spawned objects"}}]}', 0, 0, 1, '2024-08-15T09:15:00Z', '2024-08-15T09:15:00Z'),
('blk_gamedev_list2', NULL, 'pg_game_dev_notes', 'bulleted_list_item', '{"rich_text": [{"type": "text", "text": {"content": "Optimize mesh complexity and use LOD systems"}}]}', 0, 0, 2, '2024-08-15T09:16:00Z', '2024-08-15T09:16:00Z'),
('blk_reading_heading1', NULL, 'pg_reading_list', 'heading_2', '{"rich_text": [{"type": "text", "text": {"content": "Currently Reading"}}]}', 0, 0, 0, '2024-06-01T10:10:00Z', '2024-06-01T10:10:00Z'),
('blk_reading_list1', NULL, 'pg_reading_list', 'to_do', '{"rich_text": [{"type": "text", "text": {"content": "Clean Code by Robert Martin"}}], "checked": true}', 0, 0, 1, '2024-06-01T10:15:00Z', '2026-03-10T15:30:00Z'),
('blk_trip_heading1', NULL, 'pg_trip_research', 'heading_1', '{"rich_text": [{"type": "text", "text": {"content": "Bali Must-See Places"}}]}', 0, 0, 0, '2026-05-10T11:10:00Z', '2026-05-10T11:10:00Z'),
('blk_trip_para1', NULL, 'pg_trip_research', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "Researching safe activities for pregnant women. Focus on beaches, temples (easy access), spa treatments, and cultural experiences."}}]}', 0, 0, 1, '2026-05-10T11:15:00Z', '2026-05-18T15:20:00Z');

COMMIT;
