-- notion_mock li_wei_workspace — init.sql
-- Li Wei's personal Notion workspace as visible before the 2026-04-17 kickoff.
-- All ids are real UUIDs (dashed) to match Notion's API surface.

BEGIN;

-- Users: one bot (the agent) + one human (Li Wei).
INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
  ('11111111-1111-4111-8111-111111111111', 'Trip Assistant Bot', NULL, NULL, 'bot'),
  ('22222222-2222-4222-8222-222222222222', 'Li Wei', NULL, 'li.wei@example.com', 'person');

-- Workspace.
INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
  ('00000000-0000-4000-8000-000000000000', 'Li Weitranslated content', '22222222-2222-4222-8222-222222222222');

-- ===========================================================================
-- Pages (top-level)
-- ===========================================================================

-- 1) Trip Journal — central living document for the Japan trip benchmark.
INSERT INTO pages (page_id, parent_type, parent_id, title, archived,
                   created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'workspace', 'workspace',
   'Japan Trip Journal (2026-05)',
   0,
   '2026-04-15T09:00:00.000Z', '2026-04-16T14:32:11.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Japan Trip Journal (2026-05)","link":null},"plain_text":"Japan Trip Journal (2026-05)"}]}}',
   '{"type":"emoji","emoji":"🗾"}',
   NULL);

-- 2) Reading List — personal carry-over from before the trip.
INSERT INTO pages (page_id, parent_type, parent_id, title, archived,
                   created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000002',
   'workspace', 'workspace',
   'Reading List',
   0,
   '2025-08-01T10:00:00.000Z', '2026-04-16T20:11:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Reading List","link":null},"plain_text":"Reading List"}]}}',
   '{"type":"emoji","emoji":"📚"}',
   NULL);

-- 3) Project Goals 2026 — annual planning doc.
INSERT INTO pages (page_id, parent_type, parent_id, title, archived,
                   created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000003',
   'workspace', 'workspace',
   'Project Goals 2026',
   0,
   '2026-01-05T08:30:00.000Z', '2026-03-14T11:22:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Project Goals 2026","link":null},"plain_text":"Project Goals 2026"}]}}',
   '{"type":"emoji","emoji":"🎯"}',
   NULL);

-- 4) Notes — parent page containing 2 sub-pages.
INSERT INTO pages (page_id, parent_type, parent_id, title, archived,
                   created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000004',
   'workspace', 'workspace',
   'Notes',
   0,
   '2025-06-10T09:00:00.000Z', '2026-04-16T16:05:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Notes","link":null},"plain_text":"Notes"}]}}',
   '{"type":"emoji","emoji":"📓"}',
   NULL);

-- 4a) Notes / Tokyo Restaurants
INSERT INTO pages (page_id, parent_type, parent_id, title, archived,
                   created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000005',
   'page_id', 'aaaaaaaa-aaaa-4aaa-8aaa-000000000004',
   'Tokyo Restaurants',
   0,
   '2026-03-20T19:00:00.000Z', '2026-04-16T22:10:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Tokyo Restaurants","link":null},"plain_text":"Tokyo Restaurants"}]}}',
   NULL, NULL);

-- 4b) Notes / Meeting Notes 2026-04
INSERT INTO pages (page_id, parent_type, parent_id, title, archived,
                   created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000006',
   'page_id', 'aaaaaaaa-aaaa-4aaa-8aaa-000000000004',
   'Meeting Notes 2026-04',
   0,
   '2026-04-02T09:00:00.000Z', '2026-04-16T16:05:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Meeting Notes 2026-04","link":null},"plain_text":"Meeting Notes 2026-04"}]}}',
   NULL, NULL);

-- ===========================================================================
-- Databases
-- ===========================================================================

-- Tasks database (workspace-level).
INSERT INTO databases (database_id, parent_type, parent_id, title,
                       schema_json, archived, created_time, last_edited_time) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   'workspace', 'workspace',
   'Tasks',
   '{
     "Name": {"id":"title","name":"Name","type":"title","title":{}},
     "Status": {"id":"status","name":"Status","type":"select","select":{"options":[
        {"name":"Todo","color":"gray"},
        {"name":"In Progress","color":"blue"},
        {"name":"Done","color":"green"}
     ]}},
     "Done": {"id":"done","name":"Done","type":"checkbox","checkbox":{}},
     "Due": {"id":"due","name":"Due","type":"date","date":{}}
   }',
   0,
   '2026-01-08T10:00:00.000Z', '2026-04-16T08:00:00.000Z');

-- Books database (workspace-level).
INSERT INTO databases (database_id, parent_type, parent_id, title,
                       schema_json, archived, created_time, last_edited_time) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000002',
   'workspace', 'workspace',
   'Books',
   '{
     "Title": {"id":"title","name":"Title","type":"title","title":{}},
     "Author": {"id":"author","name":"Author","type":"rich_text","rich_text":{}},
     "Rating": {"id":"rating","name":"Rating","type":"number","number":{"format":"number"}}
   }',
   0,
   '2025-09-01T08:00:00.000Z', '2026-04-10T13:00:00.000Z');

-- ===========================================================================
-- Database rows
-- ===========================================================================

-- Tasks rows
INSERT INTO database_rows (row_id, database_id, properties_json,
                           created_time, last_edited_time, archived) VALUES
  ('cccccccc-cccc-4ccc-8ccc-000000000001',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Record passport expiry dates and verify current entry-document rules","link":null},"plain_text":"Record passport expiry dates and verify current entry-document rules"}]},
     "Status": {"id":"status","type":"select","select":{"name":"Todo","color":"gray"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-04-19","end":null}}
   }',
   '2026-04-10T10:00:00.000Z','2026-04-16T11:00:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000002',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Pack medical kit (insulin, glucose strips)","link":null},"plain_text":"Pack medical kit (insulin, glucose strips)"}]},
     "Status": {"id":"status","type":"select","select":{"name":"In Progress","color":"blue"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-05-07","end":null}}
   }',
   '2026-04-12T09:00:00.000Z','2026-04-16T07:15:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000003',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Buy Hakone Free Pass","link":null},"plain_text":"Buy Hakone Free Pass"}]},
     "Status": {"id":"status","type":"select","select":{"name":"Todo","color":"gray"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-05-13","end":null}}
   }',
   '2026-04-12T09:00:00.000Z','2026-04-12T09:00:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000004',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Confirm mother passport pickup status and re-check carrier document rules","link":null},"plain_text":"Confirm mother passport pickup status and re-check carrier document rules"}]},
     "Status": {"id":"status","type":"select","select":{"name":"In Progress","color":"blue"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-04-21","end":null}}
   }',
   '2026-04-13T08:20:00.000Z','2026-04-16T10:35:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000005',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Compare travel insurance exclusions and medical assistance contacts","link":null},"plain_text":"Compare travel insurance exclusions and medical assistance contacts"}]},
     "Status": {"id":"status","type":"select","select":{"name":"Todo","color":"gray"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-04-24","end":null}}
   }',
   '2026-04-13T08:25:00.000Z','2026-04-13T08:25:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000006',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Verify insulin product handling and ask shortlisted hotels about usable storage","link":null},"plain_text":"Verify insulin product handling and ask shortlisted hotels about usable storage"}]},
     "Status": {"id":"status","type":"select","select":{"name":"Todo","color":"gray"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-04-26","end":null}}
   }',
   '2026-04-14T12:10:00.000Z','2026-04-16T09:10:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000007',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000001',
   '{
     "Name": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Prepare work handover and international connectivity fallback","link":null},"plain_text":"Prepare work handover and international connectivity fallback"}]},
     "Status": {"id":"status","type":"select","select":{"name":"Todo","color":"gray"}},
     "Done": {"id":"done","type":"checkbox","checkbox":false},
     "Due": {"id":"due","type":"date","date":{"start":"2026-04-29","end":null}}
   }',
   '2026-04-14T12:15:00.000Z','2026-04-14T12:15:00.000Z',0);

-- Books rows
INSERT INTO database_rows (row_id, database_id, properties_json,
                           created_time, last_edited_time, archived) VALUES
  ('cccccccc-cccc-4ccc-8ccc-000000000010',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000002',
   '{
     "Title": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Sapiens","link":null},"plain_text":"Sapiens"}]},
     "Author": {"id":"author","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Yuval Noah Harari","link":null},"plain_text":"Yuval Noah Harari"}]},
     "Rating": {"id":"rating","type":"number","number":4}
   }',
   '2025-09-12T20:00:00.000Z','2025-12-30T19:00:00.000Z',0),
  ('cccccccc-cccc-4ccc-8ccc-000000000011',
   'bbbbbbbb-bbbb-4bbb-8bbb-000000000002',
   '{
     "Title": {"id":"title","type":"title","title":[{"type":"text","text":{"content":"Norwegian Wood","link":null},"plain_text":"Norwegian Wood"}]},
     "Author": {"id":"author","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Haruki Murakami","link":null},"plain_text":"Haruki Murakami"}]},
     "Rating": {"id":"rating","type":"number","number":5}
   }',
   '2025-10-05T20:00:00.000Z','2026-01-10T10:00:00.000Z',0);

-- ===========================================================================
-- Blocks
-- ===========================================================================

-- Trip Journal: heading + paragraph + todo + bulleted list items.
INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type,
                    content_json, has_children, archived, position,
                    created_time, last_edited_time) VALUES
  ('dddddddd-dddd-4ddd-8ddd-000000000001',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'heading_1',
   '{"rich_text":[{"type":"text","text":{"content":"Pre-trip prep","link":null},"plain_text":"Pre-trip prep"}],"color":"default","is_toggleable":false}',
   0, 0, 0,
   '2026-04-15T09:00:00.000Z','2026-04-15T09:00:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000002',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'paragraph',
   '{"rich_text":[{"type":"text","text":{"content":"Travel window 2026-05-01 to 2026-05-16; depart from Shanghai. Tokyo–Kyoto/Nara–Osaka route and lodging still to be selected. Budget cap: ¥60,000.","link":null},"plain_text":"Travel window 2026-05-01 to 2026-05-16; depart from Shanghai. Tokyo–Kyoto/Nara–Osaka route and lodging still to be selected. Budget cap: ¥60,000."}],"color":"default"}',
   0, 0, 1,
   '2026-04-15T09:01:00.000Z','2026-04-15T09:01:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000003',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'to_do',
   '{"rich_text":[{"type":"text","text":{"content":"Check the official Japan visa channel for each traveler","link":null},"plain_text":"Check the official Japan visa channel for each traveler"}],"checked":false,"color":"default"}',
   0, 0, 2,
   '2026-04-15T09:02:00.000Z','2026-04-16T15:00:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000004',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'to_do',
   '{"rich_text":[{"type":"text","text":{"content":"Doctor''s letter (CN + EN)","link":null},"plain_text":"Doctor''s letter (CN + EN)"}],"checked":false,"color":"default"}',
   0, 0, 3,
   '2026-04-15T09:03:00.000Z','2026-04-15T09:03:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000005',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'bulleted_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"Universal adapter","link":null},"plain_text":"Universal adapter"}],"color":"default"}',
   0, 0, 4,
   '2026-04-15T09:04:00.000Z','2026-04-15T09:04:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000006',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000001',
   'bulleted_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"UnionPay + Visa cards, ¥30k cash equivalent","link":null},"plain_text":"UnionPay + Visa cards, ¥30k cash equivalent"}],"color":"default"}',
   0, 0, 5,
   '2026-04-15T09:05:00.000Z','2026-04-15T09:05:00.000Z');

-- Reading List page blocks: paragraph + bulleted list items.
INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type,
                    content_json, has_children, archived, position,
                    created_time, last_edited_time) VALUES
  ('dddddddd-dddd-4ddd-8ddd-000000000010',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000002',
   'paragraph',
   '{"rich_text":[{"type":"text","text":{"content":"Books I want to read this year","link":null},"plain_text":"Books I want to read this year"}],"color":"default"}',
   0, 0, 0,
   '2025-08-01T10:00:00.000Z','2025-08-01T10:00:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000011',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000002',
   'bulleted_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"Deep Work — Cal Newport","link":null},"plain_text":"Deep Work — Cal Newport"}],"color":"default"}',
   0, 0, 1,
   '2025-08-01T10:01:00.000Z','2025-08-01T10:01:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000012',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000002',
   'bulleted_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"The Pragmatic Programmer","link":null},"plain_text":"The Pragmatic Programmer"}],"color":"default"}',
   0, 0, 2,
   '2025-08-01T10:02:00.000Z','2025-08-01T10:02:00.000Z');

-- Project Goals 2026 blocks
INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type,
                    content_json, has_children, archived, position,
                    created_time, last_edited_time) VALUES
  ('dddddddd-dddd-4ddd-8ddd-000000000020',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000003',
   'heading_2',
   '{"rich_text":[{"type":"text","text":{"content":"Q2 — Travel + family","link":null},"plain_text":"Q2 — Travel + family"}],"color":"default","is_toggleable":false}',
   0, 0, 0,
   '2026-01-05T08:30:00.000Z','2026-01-05T08:30:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000021',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000003',
   'numbered_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"Japan 20-day trip with parents (May)","link":null},"plain_text":"Japan 20-day trip with parents (May)"}],"color":"default"}',
   0, 0, 1,
   '2026-01-05T08:31:00.000Z','2026-01-05T08:31:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000022',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000003',
   'numbered_list_item',
   '{"rule":""}',
   0, 0, 2,
   '2026-01-05T08:32:00.000Z','2026-01-05T08:32:00.000Z');

-- Tokyo Restaurants sub-page blocks
INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type,
                    content_json, has_children, archived, position,
                    created_time, last_edited_time) VALUES
  ('dddddddd-dddd-4ddd-8ddd-000000000030',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000005',
   'bulleted_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"Tsuta (ramen, Sugamo)","link":null},"plain_text":"Tsuta (ramen, Sugamo)"}],"color":"default"}',
   0, 0, 0,
   '2026-03-20T19:00:00.000Z','2026-03-20T19:00:00.000Z'),
  ('dddddddd-dddd-4ddd-8ddd-000000000031',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000005',
   'bulleted_list_item',
   '{"rich_text":[{"type":"text","text":{"content":"Sushi Saito (review reservation)","link":null},"plain_text":"Sushi Saito (review reservation)"}],"color":"default"}',
   0, 0, 1,
   '2026-03-20T19:01:00.000Z','2026-03-20T19:01:00.000Z');

-- Meeting Notes sub-page block
INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type,
                    content_json, has_children, archived, position,
                    created_time, last_edited_time) VALUES
  ('dddddddd-dddd-4ddd-8ddd-000000000040',
   NULL, 'aaaaaaaa-aaaa-4aaa-8aaa-000000000006',
   'paragraph',
   '{"rich_text":[{"type":"text","text":{"content":"Standups, retros and 1:1s for April. See dated headings below.","link":null},"plain_text":"Standups, retros and 1:1s for April. See dated headings below."}],"color":"default"}',
   0, 0, 0,
   '2026-04-02T09:00:00.000Z','2026-04-02T09:00:00.000Z');

COMMIT;
