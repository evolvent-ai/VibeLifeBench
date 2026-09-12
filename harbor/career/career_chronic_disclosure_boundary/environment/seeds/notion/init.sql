-- Curated Stage-0 seed for career_chronic_disclosure_boundary / notion.

BEGIN;

INSERT INTO users (user_id, name, avatar_url, email, type) VALUES
  ('11111111-1111-4111-8111-111111111111', 'Career Assistant Bot', NULL, NULL, 'bot'),
  ('44444444-4444-4444-8444-444444444444', 'Evan Feng', NULL, 'feng.yi@163.com', 'person');

INSERT INTO workspaces (workspace_id, name, owner_user_id) VALUES
  ('00000000-0000-4000-8000-000000000001', 'English text', '44444444-4444-4444-8444-444444444444');

INSERT INTO pages (page_id, parent_type, parent_id, title, archived, created_time, last_edited_time, properties_json, icon, cover) VALUES
  ('notion_fy_home', 'workspace', 'workspace', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_weekly', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_public_resume', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_handover', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_job_template', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_legal_questions', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_finance', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL),
  ('notion_fy_learning', 'page_id', 'notion_fy_home', 'English text', 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z', '{"title": {"id": "title", "type": "title", "title": [{"type": "text", "text": {"content": "English text", "link": null}, "plain_text": "English text"}]}}', NULL, NULL);

INSERT INTO blocks (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('block_notion_fy_home', NULL, 'notion_fy_home', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text、English text，English text。", "link": null}, "plain_text": "English text、English text，English text。"}]}', 0, 0, 0, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_weekly', NULL, 'notion_fy_weekly', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "6 English text 10 English text；English text，English text。", "link": null}, "plain_text": "6 English text 10 English text；English text，English text。"}]}', 0, 0, 1, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_public_resume', NULL, 'notion_fy_public_resume', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text Java、Go、Kafka English text，English text。", "link": null}, "plain_text": "English text Java、Go、Kafka English text，English text。"}]}', 0, 0, 2, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_handover', NULL, 'notion_fy_handover', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text，English text，English text。", "link": null}, "plain_text": "English text，English text，English text。"}]}', 0, 0, 3, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_job_template', NULL, 'notion_fy_job_template', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text、English text，English text。", "link": null}, "plain_text": "English text、English text，English text。"}]}', 0, 0, 4, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_legal_questions', NULL, 'notion_fy_legal_questions', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text、English text，English text。", "link": null}, "plain_text": "English text、English text，English text。"}]}', 0, 0, 5, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_finance', NULL, 'notion_fy_finance', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text、English text，English text。", "link": null}, "plain_text": "English text、English text，English text。"}]}', 0, 0, 6, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z'),
  ('block_notion_fy_learning', NULL, 'notion_fy_learning', 'paragraph', '{"rich_text": [{"type": "text", "text": {"content": "English text，English text。", "link": null}, "plain_text": "English text，English text。"}]}', 0, 0, 7, '2026-05-01T08:00:00.000Z', '2026-06-07T08:00:00.000Z');

INSERT INTO counters (key, value) VALUES
  ('page', 8),
  ('block', 8),
  ('database', 0);

COMMIT;
