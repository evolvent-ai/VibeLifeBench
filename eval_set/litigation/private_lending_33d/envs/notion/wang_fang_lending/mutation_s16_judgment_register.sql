BEGIN;
INSERT OR IGNORE INTO blocks
  (block_id, parent_block_id, parent_page_id, type, content_json, has_children, archived, position, created_time, last_edited_time) VALUES
  ('lending_sys_s16_judgment', NULL, 'lending_case_home', 'paragraph',
   '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"一审判决送达登记：法院认定第一笔实际出借本金36万元，利息按合同成立时一年期LPR四倍计算并扣除已还2万元；第二笔20万元现金借款、配偶刘敏与担保人周国华共同清偿、精神损失费及误工费请求未获支持。送达日为2026年6月16日。","link":null},"plain_text":"一审判决送达登记：法院认定第一笔实际出借本金36万元，利息按合同成立时一年期LPR四倍计算并扣除已还2万元；第二笔20万元现金借款、配偶刘敏与担保人周国华共同清偿、精神损失费及误工费请求未获支持。送达日为2026年6月16日。"}]}}',
   0, 0, 160, '2026-06-16T09:50:00.000+08:00', '2026-06-16T09:50:00.000+08:00');
UPDATE counters SET value = CASE WHEN value < 9000 THEN 9000 ELSE value END WHERE key='block_seq';
COMMIT;
