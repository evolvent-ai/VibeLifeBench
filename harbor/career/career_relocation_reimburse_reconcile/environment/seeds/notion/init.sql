-- notion_mock career_relocation_reimburse_reconcile -- init.sql
-- Kuai BaiEnglish text Notion workspace, anchored 2026-06-08. Clean: English textboard(agent mustEnglish text/English textboard).
-- English text, English text campus English text(parent page English text agent English text).
BEGIN;
INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
  ('11111111-1111-4111-8111-111111111111', 'Career Assistant Bot', NULL, NULL, 'bot'),
  ('33333333-3333-4333-8333-333333333333', 'Kuai Bai', NULL, 'gaokai_dev@163.com', 'person');
INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
  ('00000000-0000-4000-8000-000000000000', 'Kuai BaiEnglish text', '33333333-3333-4333-8333-333333333333');
INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000001','workspace','workspace','Notes',0,
   '2026-01-01T08:00:00.000Z','2026-06-01T10:00:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Notes","link":null},"plain_text":"Notes"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000002','workspace','workspace','Personal',0,
   '2026-01-01T08:00:00.000Z','2026-06-01T10:00:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Personal","link":null},"plain_text":"Personal"}]}}',NULL,NULL);
INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000003','workspace','workspace','publicLabor Lawsourcerecord',0,
   '2026-06-02T09:00:00.000Z','2026-06-02T09:00:00.000Z',
   '{"source_url":"https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394622.html","locator":"English text","fact":"English textcompensationEnglish textsalaryEnglish textsalary；English text","verified_at":"2026-06-02","status":"official_source"}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000004','workspace','workspace','departureEnglish textmethod',0,
   '2026-06-03T09:00:00.000Z','2026-06-03T09:00:00.000Z',
   '{"method":"distinguishcompanyEnglish textplan、salarytransactionsfacts、English textpubliclegalbasis；anysigningEnglish textauthorization","status":"standing_practice"}',NULL,NULL);
COMMIT;
