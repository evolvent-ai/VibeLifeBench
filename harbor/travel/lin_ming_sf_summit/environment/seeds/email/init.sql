BEGIN TRANSACTION;
INSERT INTO "folders" VALUES(1,'INBOX','/','[]',0,0);
INSERT INTO "folders" VALUES(2,'Sent','/','[]',0,0);
INSERT INTO "folders" VALUES(3,'Drafts','/','[]',0,0);
INSERT INTO "folders" VALUES(4,'Trash','/','[]',0,0);
INSERT INTO "folders" VALUES(5,'Spam','/','[]',0,0);
INSERT INTO account_config VALUES (1, 'liming@company.com', 'Ming Lin', '2026-01-01T00:00:00');
INSERT INTO messages VALUES (1, 1, 'EM001', 'Company Budget Notice Q1 2026', 'hr@company.com', '["liming@company.com"]', '[]', '[]', '2026-01-05T10:00:00', 'Quarterly business trip budget is 15,000 CNY per person. Expenses over 5,000 CNY require prior written approval from your direct manager.', NULL, 1, 0, 0, NULL, NULL, '{}', 1, 200, '2026-01-05T10:00:00');
INSERT INTO messages VALUES (2, 1, 'EM002', '2026 Global Tech Summit Registration Confirmed', 'summit@techconf.com', '["liming@company.com"]', '[]', '[]', '2026-02-20T09:00:00', 'Dear Mr. Li Ming, you have successfully registered for the 2026 Global Tech Summit. Time: March 28-30, 2026. Location: Moscone Center, San Francisco. We look forward to your participation.', NULL, 1, 0, 0, NULL, NULL, '{}', 2, 250, '2026-02-20T09:00:00');
INSERT INTO messages VALUES
(3, 1, 'EM003', 'Security bulletin: fake travel-payment pages', 'security@company.com', '["liming@company.com"]', '[]', '[]', '2026-01-12T15:30:00', 'Routine security reminder: verify travel vendors through the corporate directory and never approve a payment from a shortened link in an unsolicited message.', NULL, 1, 0, 0, NULL, NULL, '{}', 3, 180, '2026-01-12T15:30:00'),
(4, 1, 'EM004', '2025 Global Tech Forum attendance certificate', 'events@industryforum.example', '["liming@company.com"]', '[]', '[]', '2025-11-25T11:20:00', 'Your certificate for the November 2025 online forum is attached in the event portal. This historical event did not include travel arrangements.', NULL, 1, 0, 0, NULL, NULL, '{}', 4, 165, '2025-11-25T11:20:00'),
(5, 1, 'EM005', 'Shanghai client-trip expense claim settled', 'finance@company.com', '["liming@company.com"]', '[]', '[]', '2025-12-18T09:40:00', 'Claim SH-2025-118 has completed review. The approved amount was 2,946 CNY; the taxi receipt exception was documented separately.', NULL, 1, 0, 0, NULL, NULL, '{}', 5, 170, '2025-12-18T09:40:00'),
(6, 1, 'EM006', 'Moscone neighborhood transit guide', 'newsletter@bayareabusiness.example', '["liming@company.com"]', '[]', '[]', '2026-02-26T08:15:00', 'General visitor newsletter with BART and walking information near Moscone Center. It is not a hotel confirmation, ticket, or supplier quote.', NULL, 0, 0, 0, NULL, NULL, '{}', 6, 185, '2026-02-26T08:15:00'),
(7, 1, 'EM007', 'Spring transpacific timetable newsletter', 'updates@airline.example', '["liming@company.com"]', '[]', '[]', '2026-03-02T12:10:00', 'Marketing summary of selected spring routes. Schedules and fares may change; use the booking platform for live availability. No reservation is attached.', NULL, 1, 0, 0, NULL, NULL, '{}', 7, 180, '2026-03-02T12:10:00'),
(8, 1, 'EM008', 'March staffing availability survey', 'zhang_manager@company.com', '["liming@company.com"]', '[]', '[]', '2026-03-06T17:45:00', 'Please mark ordinary office absences and remote-work windows for the last two weeks of March. This survey is not travel approval.', NULL, 1, 0, 0, NULL, NULL, '{}', 8, 165, '2026-03-06T17:45:00'),
(9, 1, 'EM009', 'Hotel loyalty monthly statement', 'account@hotelgroup.example', '["liming@company.com"]', '[]', '[]', '2026-03-10T07:30:00', 'Your February loyalty balance is 12,480 points. This account statement does not reserve a room or guarantee conference-period availability.', NULL, 0, 0, 0, NULL, NULL, '{}', 9, 175, '2026-03-10T07:30:00');
INSERT INTO _counters VALUES ('config', 1), ('message', 9), ('attachment', 0), ('draft', 0);
INSERT INTO "sqlite_sequence" VALUES('folders',5);
INSERT INTO "sqlite_sequence" VALUES('messages',9);
COMMIT;
