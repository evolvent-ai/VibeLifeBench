PRAGMA journal_mode = DELETE;
BEGIN TRANSACTION;
INSERT INTO account_config (email, name, created_at) VALUES ('zhou_mu@startup-coo.example.com', 'zhou_mu@startup-coo.example.com', '2026-01-01T00:00:00+08:00');
INSERT OR IGNORE INTO folders (id, name, delimiter, flags_json, message_count, unread_count) VALUES (1, 'INBOX', '/', '[]', 4, 4);
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-shenpin-quote-20260702@startup-coo.example>', '【CN-textcommercial space】Lujiazui 4F 300㎡ fit-out quote v0', 'CN-textcommercial space business development <hi@shenpin-cs.example.com>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-02T10:00:00+08:00', 'Zhou MuMr.Hello,

CN-textcommercial space (prov_v3_002_commercial_design_build): Lujiazui/beforeCN-term CN-textbuildingCN-text, BIM CN-text, fire safetyCN-text, 5 yearCN-textconcealed workswarranty, qualification construction Grade I + decoration design Grade A.

CN-text 300㎡ + 30 people + 1 CN-termmeeting room + 1 CN-termmeeting room + CN-text + CN-text initialCN-text, quote v0 total price ¥760,000 (excludingdesignCN-term ¥40,000, excluding property management fit-up deposit ¥30,000, excluding contractors all-risk insurance, excluding demolitionhaul-away ¥8,000). including strong-current and low-voltage systems ≥4kW/100㎡ + emergency lighting 24 CN-term + formaldehyde ≤0.05 finish materials.

availablewindow 2026-08-01..10-15 — CN-textaccepts only ≥300㎡ project, depositnotCN-term. quote validity 2026-07-10.

CN-textcommercial space / sales department CN-termmanager / 138-0000-9002', NULL, 0, 1, 0, NULL, NULL, '{"X-Fitout-Template":"EML-001","X-Fitout-Provider-Id":"prov_v3_002_commercial_design_build","X-Fitout-Quote-Total":"760000","X-Fitout-Valid-Until":"2026-07-10"}', NULL, 380, '2026-07-02T10:00:00+08:00');
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-property-fitup-20260701@startup-coo.example>', '【Pudong Lujiazui Financial Centerproperty management】CN-termunit 4F fit-up CN-term start CN-textchecklist', 'Pudong Lujiazui Financial Centerproperty managementservice center <management@lujiazui-fc.example.com>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-01T14:30:00+08:00', 'Zhou MuMr.:

confirmCN-termunit 4F (300㎡) lease fit-up CN-term 2026-07-06..08-31 (6 CN-term hard window), occupancy D-day 2026-09-01. fit-up startbefore mustcompleted:

(1) Jingan One-stop decoration and renovation filing CN-text one-stop filing case-ID filing + CN-termproperty management CN-text;
(2) contractors all-risk insurance policy atCN-term (CN-textpolicy CN-termrelease site entry);
(3) fit-up deposit ¥30,000 CN-text (CN-text nonecomplaint CN-text);
(4) lead designer BIM CN-term + fire safety CN-text + strong-current and low-voltage systems load calculation property managementCN-text (≤ 5 dayCN-text);
(5) inside the buildingnoise only 09:00-19:00 weekday; 19:00 after CN-text; weekendmust 48h CN-text.

CN-text fire-safety inspection and acceptance passed after, deposit CN-text + occupancy access pass CN-text. CN-text fit-up CN-text CN-text 8-31 ddl, ownerCN-text 09-01 CN-term CN-text.

Pudong Lujiazui Financial Centerproperty management / CN-termmanager / 5588-3000', NULL, 0, 1, 1, NULL, NULL, '{"X-Fitout-Template":"EML-007","X-Fitout-Linked-Rule":"rule_property_v3_005,rule_property_v3_013"}', NULL, 420, '2026-07-01T14:30:00+08:00');
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-insurance-broker-20260701@startup-coo.example>', '【CN-textinsurance broker】Lujiazui fit-out contractors all-risk insurance CN-text + comparison', 'CN-textinsurance broker commercialCN-term CN-termmanager <broker@safehands-insurance.example.com>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-01T16:15:00+08:00', 'Zhou MuMr.:

CN-text 300㎡ Lujiazui fit-out project (works amount ¥80 CN-term) CN-text, CN-text 3 CN-termcomparison:

A. ins_v3_001 Ping-Equiv fit-outcontractors all-risk insurance standardCN-term:
   ¥4,000 / yearCN-term (0.5% × ¥80 CN-term); works amount ≤¥200 CN-term CN-text; includingworksCN-text + No.CN-text;
   excluding Jingan one-stop filing project CN-text + fire safetycorrection CN-text.

B. ins_v3_011 Ping-Equiv fit-outcontractors all-risk insurance commercialCN-term (RECOMMENDED):
   ¥8,000 (1.0% × ¥80 CN-term); works amount ≥¥100 CN-term (includingcommercial fit-out project); including Jingan one-stop filing + fire safetycorrection CN-text;
   CN-text CN-termproject (Jingan one-stop + fire safetyrisk).

C. ins_v3_012 GuardOne third-party liability insurance commercial 1000 CN-term:
   ¥4,000 (0.5% × ¥80 CN-term); liabilityCN-text ¥1,000 CN-term; including CN-textinside the buildingpeopleCN-term CN-termoutside;
   recommendationCN-text A or B (CN-textnotCN-term CN-text worksCN-text).

recommended B + C CN-text: ¥12,000 CN-term / projectCN-term CN-text worksCN-text + No.CN-text + Jingan one-stop filing + fire safetycorrection + CN-textinside the buildingpeopleCN-term.

policy mustat fit-up CN-text (7-06) before atCN-term. CN-text to CN-text after 24 hourwithin CN-text.

CN-textinsurance broker / commercialCN-term CN-termmanager / 138-0000-9001', NULL, 0, 1, 0, NULL, NULL, '{"X-Fitout-Template":"EML-019","X-Fitout-Insurance-Standard":"ins_v3_001","X-Fitout-Insurance-Commercial":"ins_v3_011","X-Fitout-Insurance-Liability":"ins_v3_012"}', NULL, 580, '2026-07-01T16:15:00+08:00');
INSERT INTO messages (folder_id, message_id, subject, from_addr, to_addr_json, cc_addr_json, bcc_addr_json, date, body_text, body_html, is_read, is_important, is_flagged, in_reply_to, references_header, headers_json, uid, size, created_at) VALUES (1, '<office-fitout-fire-dept-20260701@startup-coo.example>', '【Jingan Districtfire safetyCN-text】fit-up project fire-safety inspection and acceptance CN-textreminder', 'Jingan Districtfire safetyCN-text CN-text <contact@jingan-fire.gov.cn>', '["zhou_mu@startup-coo.example.com"]', '[]', '[]', '2026-07-01T11:45:00+08:00', 'Zhou Muowner:

CN-term fit-out project (Lujiazui 4F 300㎡) CN-termmid Jingan One-stop decoration and renovation filing CN-text (≥¥100 CN-term OR ≥300 ㎡ CN-text), must CN-term Jingan one-stop filing CN-text CN-termmid CN-text (housing + fire + safety + pass-issuance CN-termwindow).

fire-safety inspection and acceptance application CN-text:
(1) Jingan one-stop filing CN-text submit fire safety CN-text + emergency lighting CN-text + evacuation CN-text + smoke detector CN-text CN-text report + CN-text + fire safety CN-text contact.
(2) CN-text 7 daywithin schedule siteCN-text.
(3) siteCN-text project: emergency lighting CN-text count + spacing + highCN-term; evacuationcorridor widthCN-term ≥1.4m; smoke detector CN-text + CN-text; CN-text CN-text / count / CN-text; fire safety CN-text atCN-term.
(4) passed CN-text fire-safety inspection and acceptance qualifiedfeedbackCN-term; fail CN-text RFI notice, correction review.

emergency lighting CN-text 300㎡ commercial space CN-text 24 CN-term CN-term (spacing ≤8m, includingevacuationcorridor + CN-textexit). strong-current and low-voltage systems load ≥4kW/100㎡ is CN-text beforeCN-term.

recommendation occupancy D-day before toCN-term 7 day completed CN-text, CN-term correction CN-text.

Jingan District fire safetyCN-text / CN-text CN-text / 5588-9119', NULL, 0, 1, 1, NULL, NULL, '{"X-Fitout-Template":"EML-012","X-Fitout-Linked-Rule":"rule_property_v3_005,rule_property_v3_013","X-Fitout-Linked-Standard":"fire_acceptance_commercial_300sqm"}', NULL, 540, '2026-07-01T11:45:00+08:00');
INSERT OR IGNORE INTO folders (id, name, delimiter, flags_json, message_count, unread_count) VALUES (2, 'Sent', '/', '["\\Sent"]', 0, 0);
INSERT OR IGNORE INTO folders (id, name, delimiter, flags_json, message_count, unread_count) VALUES (3, 'Drafts', '/', '["\\Drafts"]', 0, 0);
COMMIT;
