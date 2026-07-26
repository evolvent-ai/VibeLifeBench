BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s10_defense', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"系统送达登记：陈强提交答辩，主张第一笔借条虽写40万元但实际到账36万元，本金应按实际交付认定；并否认第二笔20万元现金已实际交付。相关答辩、转账回单和现金交付材料待逐项质证。","link":null},"plain_text":"系统送达登记：陈强提交答辩，主张第一笔借条虽写40万元但实际到账36万元，本金应按实际交付认定；并否认第二笔20万元现金已实际交付。相关答辩、转账回单和现金交付材料待逐项质证。"}]}}',
   0, 0, 100, '2026-06-04T09:00:00.000+08:00', '2026-06-04T09:00:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
