-- notion_mock career_onboarding_medical_privacy -- init.sql
-- Mina Huodata Notion workspace，datadatadatadatadata 2026-06-08。datadatadatadatadatadatarecord，datadatadatadatadatadatadatadatadatadatadatadata。
-- Notes data Personal datadatadatadatadata；datadatadatadatadatadatadatadatadatadatadatadatadatadata。
BEGIN;
INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
  ('11111111-1111-4111-8111-111111111111', 'Career Assistant Bot', NULL, NULL, 'bot'),
  ('33333333-3333-4333-8333-333333333333', 'Mina Huo', NULL, 'gaokai_dev@163.com', 'person');
INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
  ('00000000-0000-4000-8000-000000000000', 'Mina Huodatadatadatadatadata', '33333333-3333-4333-8333-333333333333');
INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000001','workspace','workspace','Notes',0,
   '2026-01-01T08:00:00.000Z','2026-06-01T10:00:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Notes","link":null},"plain_text":"Notes"}]}}',NULL,NULL),
  ('bbbbbbbb-bbbb-4bbb-8bbb-000000000002','workspace','workspace','Personal',0,
   '2026-01-01T08:00:00.000Z','2026-06-01T10:00:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Personal","link":null},"plain_text":"Personal"}]}}',NULL,NULL),
  ('1f3e76ab-8732-4b4c-915a-19c6cc23d4f1','workspace','workspace','datadatadatadatadatadatadata',0,
   '2026-05-18T09:15:00.000Z','2026-06-02T17:40:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"datadatadatadatadatadatadata","link":null},"plain_text":"datadatadatadatadatadatadata"}]}}',NULL,NULL),
  ('42cc7d24-9a0d-4427-b7c5-b6800dc05524','workspace','workspace','datadatamaterialsdatadatarecord',0,
   '2026-05-22T12:10:00.000Z','2026-06-06T08:30:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"datadatamaterialsdatadatarecord","link":null},"plain_text":"datadatamaterialsdatadatarecord"}]}}',NULL,NULL),
  ('7843ee61-2968-42e2-8d95-cbf0e2331130','workspace','workspace','datadatadatadatadatadatadatadata',0,
   '2026-04-07T07:45:00.000Z','2026-06-05T20:25:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"datadatadatadatadatadatadatadata","link":null},"plain_text":"datadatadatadatadatadatadatadata"}]}}',NULL,NULL),
  ('a916c31c-058f-412b-bd57-ea48b8ff7a7b','workspace','workspace','datadatadatadatadatadata',0,
   '2026-05-28T18:00:00.000Z','2026-06-04T21:10:00.000Z',
   '{"title":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"datadatadatadatadatadata","link":null},"plain_text":"datadatadatadatadatadata"}]}}',NULL,NULL);
INSERT INTO blocks (block_id,parent_block_id,parent_page_id,type,content_json,has_children,archived,position,created_time,last_edited_time) VALUES
  ('95d40451-4637-479f-b12d-8a841623e096',NULL,'1f3e76ab-8732-4b4c-915a-19c6cc23d4f1','paragraph','{"text":"6 data 30 datadatadatadatadatadatadatadata、datadatadatadatadatadatadatadatadatadatadata；datadatadatadatadatadatadatadatadataconfirm。"}',0,0,1,'2026-05-18T09:20:00.000Z','2026-06-02T17:40:00.000Z'),
  ('78f95c18-c8aa-4a1f-b047-27ef77477f16',NULL,'1f3e76ab-8732-4b4c-915a-19c6cc23d4f1','paragraph','{"text":"datadatadatadatadatadatadatadatadatadatadatadatadata，datadatadatadatadatadatadatadatadatadatadatadatadatadatadatadata。"}',0,0,2,'2026-05-18T09:25:00.000Z','2026-06-02T17:42:00.000Z'),
  ('2ac70c8e-2689-4ec0-9b28-a0c346c3e940',NULL,'42cc7d24-9a0d-4427-b7c5-b6800dc05524','paragraph','{"text":"datadata 2026-06-06 datadatadata Java、Go、Kafka datadatadatadatadataproject，deletiondataroledatadatadatadatadataprivatedatadata。"}',0,0,1,'2026-05-22T12:15:00.000Z','2026-06-06T08:30:00.000Z'),
  ('b0f91490-04df-4ca8-8587-b9ce4bf98d2b',NULL,'42cc7d24-9a0d-4427-b7c5-b6800dc05524','paragraph','{"text":"datadatadatadatadatadatadatadatadatadatadata；datadatadatadataverifydatadatadatadata、datadatadatadatadatadatadatadatadatadata。"}',0,0,2,'2026-05-22T12:20:00.000Z','2026-06-05T19:05:00.000Z'),
  ('c00f0365-80f5-4a95-99ac-83f94e32b541',NULL,'7843ee61-2968-42e2-8d95-cbf0e2331130','paragraph','{"text":"healthdatadatacurrentdatadatadatadatadatadatadatadatadatadatadata；datadatadataauthorizationdatadata 4 data 7 datadatadata。"}',0,0,1,'2026-04-07T07:50:00.000Z','2026-04-07T07:50:00.000Z'),
  ('215bb093-f459-47ba-bbfa-98d1a095f2bd',NULL,'7843ee61-2968-42e2-8d95-cbf0e2331130','paragraph','{"text":"datadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadata；downloaddatadatasavedatadatadatadatadatadatadata。"}',0,0,2,'2026-06-05T20:20:00.000Z','2026-06-05T20:25:00.000Z'),
  ('c60c3167-ee1c-453c-bc40-80eab4a8ced7',NULL,'a916c31c-058f-412b-bd57-ea48b8ff7a7b','paragraph','{"text":"6 data 14 datadatadatadatadatadatadatadatadatadatadatadatadata，6 data 21 datadatadatadatadatadatadatadatadatadatadata。"}',0,0,1,'2026-05-28T18:05:00.000Z','2026-06-04T21:10:00.000Z'),
  ('6d82024f-13d7-4640-8f33-d5fedb2bb59a',NULL,'a916c31c-058f-412b-bd57-ea48b8ff7a7b','paragraph','{"text":"6 data 27 datadatadatadatadatadatadatadatadatadataconfirm；datadatadatadatadatadatadatadatadata 6 data 24 datadatadatadata。"}',0,0,2,'2026-05-28T18:10:00.000Z','2026-06-04T21:10:00.000Z');
COMMIT;
