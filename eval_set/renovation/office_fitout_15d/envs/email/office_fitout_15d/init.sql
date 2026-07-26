BEGIN TRANSACTION;
INSERT INTO account_config (email, name, created_at) VALUES ('zhou_mu@startup-coo.example.com', 'zhou_mu@startup-coo.example.com', '2026-01-01T00:00:00+08:00');
INSERT OR IGNORE INTO folders (id, name, delimiter, flags_json, message_count, unread_count) VALUES (1, 'INBOX', '/', '[]', 4, 4);
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-shenpin-quote-20260702@startup-coo.example>', '【申品商业空间】陆家嘴 4F 300㎡ fit-out 报价 v0', '申品商业空间 商务部 <hi@shenpin-cs.example.com>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-02T10:00:00+08:00', '周牧先生您好,

申品商业空间 (prov_v3_002_commercial_design_build): 陆家嘴/前滩 写字楼专项, BIM 出图, 消防协助验收, 5 年水电隐蔽工程质保, 资质 建装一级 + 装饰甲级.

根据 300㎡ + 30 人 + 1 大会议室 + 1 小会议室 + 接待 + 休息 初步需求, 报价 v0 总价 ¥760,000 (不含设计费 ¥40,000, 不含 物业 fit-up 押金 ¥30,000, 不含 工程一切险, 不含 拆除清运 ¥8,000). 含 强弱电 ≥4kW/100㎡ + 应急照明 24 灯 + 甲醛 ≤0.05 主材.

可用窗口 2026-08-01..10-15 — 我方仅承接 ≥300㎡ 项目, 定金不退. 报价有效期 2026-07-10.

申品商业空间 / 销售部 林经理 / 138-0000-9002', NULL, 0, 1, 0, NULL, NULL, '{"X-Fitout-Template":"EML-001","X-Fitout-Provider-Id":"prov_v3_002_commercial_design_build","X-Fitout-Quote-Total":"760000","X-Fitout-Valid-Until":"2026-07-10"}', NULL, 380, '2026-07-02T10:00:00+08:00');
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-property-fitup-20260701@startup-coo.example>', '【陆家嘴金融中心物业】您单元 4F fit-up 期 启动 准备清单', '陆家嘴金融中心物业服务中心 <management@lujiazui-fc.example.com>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-01T14:30:00+08:00', '周牧先生:

确认您单元 4F (300㎡) 租约 fit-up 期 2026-07-06..08-31 (6 周 hard window), 入驻 D-day 2026-09-01. fit-up 启动前 必须完成:

(1) 静安 装饰装修一件事 平台 一件事 case-ID 备案 + 我物业 留档;
(2) 工程一切险 保单 在保 (我方见保单 才放行 进场);
(3) fit-up 押金 ¥30,000 缴纳 (完工 无投诉 退还);
(4) 主案设计师 BIM 图 + 消防 平面 + 强弱电 负荷计算书 物业初审 (≤ 5 天回复);
(5) 楼内噪音 仅 09:00-19:00 工作日; 19:00 后 严禁; 周末须 48h 报批.

完工 消防验收 通过 后, 押金 退还 + 入驻 通行证 发放. 任何 fit-up 延期 超过 8-31 ddl, 业主承担 09-01 起 租金损失.

陆家嘴金融中心物业 / 张经理 / 5588-3000', NULL, 0, 1, 1, NULL, NULL, '{"X-Fitout-Template":"EML-007","X-Fitout-Linked-Rule":"rule_property_v3_005,rule_property_v3_013"}', NULL, 420, '2026-07-01T14:30:00+08:00');
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-insurance-broker-20260701@startup-coo.example>', '【慧择保险经纪】陆家嘴 fit-out 工程一切险 询价 + 比较', '慧择保险经纪 商业部 王经理 <broker@safehands-insurance.example.com>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-01T16:15:00+08:00', '周牧先生:

根据您 300㎡ 陆家嘴 fit-out 项目 (工程款 ¥80 万) 询价, 整理 3 档比较:

A. ins_v3_001 Ping-Equiv 装修工程一切险 标准款:
   ¥4,000 / 年期 (0.5% × ¥80 万); 工程款 ≤¥200 万 适用; 含工程本身损失 + 第三方;
   不含 静安 一件事 项目 专项 + 消防整改 保障.

B. ins_v3_011 Ping-Equiv 装修工程一切险 商业版 (RECOMMENDED):
   ¥8,000 (1.0% × ¥80 万); 工程款 ≥¥100 万 (含商业 fit-out 项目); 含 静安 一件事 + 消防整改 保障;
   适用 您项目 (Jingan one-stop + 消防风险).

C. ins_v3_012 GuardOne 第三方责任险 商业 1000 万:
   ¥4,000 (0.5% × ¥80 万); 责任限额 ¥1,000 万; 含 写字楼内人员 意外;
   建议叠加 A 或 B (单独不够 覆盖 工程本身).

推荐 B + C 组合: ¥12,000 总 / 项目期 覆盖 工程本身 + 第三方 + 静安 一件事 + 消防整改 + 写字楼内人员.

保单 必须在 fit-up 期开始 (7-06) 前 在保. 缴费 至 我方账户 后 24 小时内 出证.

慧择保险经纪 / 商业部 王经理 / 138-0000-9001', NULL, 0, 1, 0, NULL, NULL, '{"X-Fitout-Template":"EML-019","X-Fitout-Insurance-Standard":"ins_v3_001","X-Fitout-Insurance-Commercial":"ins_v3_011","X-Fitout-Insurance-Liability":"ins_v3_012"}', NULL, 580, '2026-07-01T16:15:00+08:00');
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-fire-dept-20260701@startup-coo.example>', '【静安区消防救援支队】fit-up 项目 消防验收 流程提醒', '静安区消防救援支队 验收科 <contact@jingan-fire.gov.cn>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-01T11:45:00+08:00', '周牧业主:

您 fit-out 项目 (陆家嘴 4F 300㎡) 命中 静安 装饰装修一件事 阈值 (≥¥100 万 OR ≥300 ㎡ 非居住), 须 经 静安 一件事 平台 集中 申报 (housing + fire + safety + pass-issuance 单窗口).

消防验收 申请 流程:
(1) 静安 一件事 平台 提交 消防 平面图 + 应急照明 平面 + 疏散 流向 + 烟感 报警 测试 报告 + 灭火器 + 消防 主管 联系人.
(2) 我支队 7 天内 排期 现场验收.
(3) 现场验收 项目: 应急照明 灯具 数量 + 间距 + 高度; 疏散通道 宽度 ≥1.4m; 烟感 全覆盖 + 联动测试; 灭火器 类型 / 数量 / 位置; 消防 主管单位 在场.
(4) 通过 出具 消防验收 合格意见书; fail 出具 RFI 通知, 整改 复审.

应急照明 灯具 300㎡ 商业空间 规范 24 盏 起 (间距 ≤8m, 含疏散通道 + 紧急出口). 强弱电 负荷 ≥4kW/100㎡ 是 验收 前提.

建议 入驻 D-day 前 至少 7 天 完成 验收, 留 整改 余量.

静安区 消防救援支队 / 验收科 朱队 / 5588-9119', NULL, 0, 1, 1, NULL, NULL, '{"X-Fitout-Template":"EML-012","X-Fitout-Linked-Rule":"rule_property_v3_005,rule_property_v3_013","X-Fitout-Linked-Standard":"fire_acceptance_commercial_300sqm"}', NULL, 540, '2026-07-01T11:45:00+08:00');
INSERT OR IGNORE INTO folders (id, name, delimiter, flags_json, message_count, unread_count) VALUES (2, 'Sent', '/', '["\\Sent"]', 0, 0);
INSERT OR IGNORE INTO folders (id, name, delimiter, flags_json, message_count, unread_count) VALUES (3, 'Drafts', '/', '["\\Drafts"]', 0, 0);
COMMIT;
