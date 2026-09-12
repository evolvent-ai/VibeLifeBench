-- notion_mock career_jobhop_tax_reconcile -- init.sql
-- record，record 2026-06-08；record、record，record。
-- record，record。
BEGIN;
INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
  ('11111111-1111-4111-8111-111111111111', 'Career Assistant Bot', NULL, NULL, 'bot'),
  ('33333333-3333-4333-8333-333333333333', 'record', NULL, 'gaokai_dev@163.com', 'person');
INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
  ('00000000-0000-4000-8000-000000000000', 'record', '33333333-3333-4333-8333-333333333333');
INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000001','workspace','workspace','Notes',0,
   '2026-01-01T08:00:00.000Z','2026-06-01T10:00:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Notes","link":null},"plain_text":"Notes"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000002','workspace','workspace','Personal',0,
   '2026-01-01T08:00:00.000Z','2026-06-01T10:00:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Personal","link":null},"plain_text":"Personal"}]}}',NULL,NULL);
INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000003','workspace','workspace','record',0,'2025-11-03T12:20:00.000Z','2026-05-30T14:12:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000004','workspace','workspace','record',0,'2025-09-14T03:10:00.000Z','2026-05-26T11:05:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000005','workspace','workspace','record',0,'2025-05-28T09:40:00.000Z','2025-06-06T08:15:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000006','workspace','workspace','record',0,'2025-12-19T10:00:00.000Z','2026-06-02T09:05:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000007','workspace','workspace','record',0,'2026-01-05T08:40:00.000Z','2026-06-07T13:20:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000008','workspace','workspace','record（record）',0,'2024-10-12T07:25:00.000Z','2025-12-22T16:30:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record（record）","link":null},"plain_text":"record（record）"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000009','workspace','workspace','record',0,'2025-08-02T02:45:00.000Z','2026-06-06T11:15:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000010','workspace','workspace','record',0,'2025-07-09T13:30:00.000Z','2026-05-18T12:00:00.000Z','{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"record","link":null},"plain_text":"record"}]}}',NULL,NULL);
INSERT INTO blocks (block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time) VALUES
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000001',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000003','paragraph','{"type":"paragraph","rich_text":[{"text":"record、record；record。"}]}',0,0,0,'2025-11-03T12:22:00.000Z','2026-05-30T14:12:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000002',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000003','bulleted_list_item','{"type":"bulleted_list_item","rich_text":[{"text":"record：record。"}]}',0,0,1,'2026-05-30T14:12:00.000Z','2026-05-30T14:12:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000003',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000004','paragraph','{"type":"paragraph","rich_text":[{"text":"record、record；record。"}]}',0,0,0,'2025-09-14T03:12:00.000Z','2026-05-26T11:05:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000004',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000005','paragraph','{"type":"paragraph","rich_text":[{"text":"record、record；record。"}]}',0,0,0,'2025-05-28T09:42:00.000Z','2025-06-06T08:15:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000005',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000006','paragraph','{"type":"paragraph","rich_text":[{"text":"6 record 13 record；record、record。"}]}',0,0,0,'2026-05-21T12:20:00.000Z','2026-06-02T09:05:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000006',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000007','paragraph','{"type":"paragraph","rich_text":[{"text":"record；record，record。"}]}',0,0,0,'2026-01-05T08:42:00.000Z','2026-06-07T13:20:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000007',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000008','paragraph','{"type":"paragraph","rich_text":[{"text":"record：record，record、record。"}]}',0,0,0,'2024-10-12T07:27:00.000Z','2025-12-22T16:30:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000008',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000008','paragraph','{"type":"paragraph","rich_text":[{"text":"record：record、record、record。"}]}',0,0,1,'2025-12-22T16:30:00.000Z','2025-12-22T16:30:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000009',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000009','paragraph','{"type":"paragraph","rich_text":[{"text":"record、record，record。"}]}',0,0,0,'2025-08-02T02:47:00.000Z','2026-06-06T11:15:00.000Z'),
  ('aaaaaaaa-aaaa-4aaa-8aaa-000000000010',NULL,'bbbbbbbb-bbbb-4bbb-8bbb-000000000010','paragraph','{"type":"paragraph","rich_text":[{"text":"record、record Go record。"}]}',0,0,0,'2025-07-09T13:32:00.000Z','2026-05-18T12:00:00.000Z');
COMMIT;
