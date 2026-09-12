-- email_mock seed: career_jobhop_tax_reconcile. Stage 0 reference 2026-06-08.
-- record；record、record、record offer record mutation record。
BEGIN;
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES
  (1,'gaokai_dev@163.com','record (Kuang Qiao)','2018-08-01T00:00:00Z');
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1,1,'<20260608-annual-settlement@tax-service.example>','2025 annual settlement prefilled summary','Individual Tax Service <notice@tax-service.example>','["gaokai_dev@163.com"]','2026-06-08T01:35:00Z',
   'Your 2025 annual settlement prefilled summary includes comprehensive income, deductions, and tax withheld. Verify the employer, income period, income category, and withholding before personal submission.',0,1,'{}',430,'2026-06-08T01:35:00Z'),
  (2,1,'<20260118-old-employer-withholding@hanlandata.example>','Hanlan Data 2025 withholding record','Hanlan Data Payroll <payroll@hanlandata.example>','["gaokai_dev@163.com"]','2026-01-18T03:20:00Z',
   'This record covers January through May 2025 salary, the first-quarter one-time bonus, and the May departure settlement. Contact Hanlan Data Payroll to verify the monthly tax withheld.',1,1,'{}',330,'2026-01-18T03:20:00Z'),
  (3,1,'<20250905-deduction-switch@qichencloud.example>','Deduction migration receipt and first payroll cycle','Qichen Cloud Payroll <payroll@qichencloud.example>','["gaokai_dev@163.com"]','2025-09-05T02:10:00Z',
   'The special additional deduction migrated to Qichen Cloud for September 2025. The first payroll cycle began in June; contact Qichen Cloud Payroll to verify the transition months and withholding.',1,0,'{}',280,'2025-09-05T02:10:00Z'),
  (4,1,'<20260605-architecture-weekly@engineering.example>','record：record','record <weekly@engineering.example>','["gaokai_dev@163.com"]','2026-06-05T00:30:00Z',
   'record、record，record。',1,0,'{}',184,'2026-06-05T00:30:00Z'),
  (5,1,'<20260606-school-meeting@family.example>','record','record <family@family.example>','["gaokai_dev@163.com"]','2026-06-06T11:00:00Z',
   'record，record。record，record。',1,0,'{}',176,'2026-06-06T11:00:00Z'),
  (6,1,'<20250322-2024-tax-archive@tax-service.example>','2024 record','record <notice@tax-service.example>','["gaokai_dev@163.com"]','2025-03-22T02:16:00Z',
   'record，record、record。record 2025 record。',1,0,'{}',286,'2025-03-22T02:16:00Z'),
  (7,1,'<20250210-january-payslip@hanlandata.example>','record 2025 record 1 record','record <payroll@hanlandata.example>','["gaokai_dev@163.com"]','2025-02-10T01:42:00Z',
   'record、record、record。record，record，record。',1,0,'{}',274,'2025-02-10T01:42:00Z'),
  (8,1,'<20250603-exit-settlement@hanlandata.example>','record','record <peopleops@hanlandata.example>','["gaokai_dev@163.com"]','2025-06-03T07:18:00Z',
   'record 5 record、record。record；record，record。',1,0,'{}',298,'2025-06-03T07:18:00Z'),
  (9,1,'<20250626-new-hire-pay-cycle@qichencloud.example>','record','record <people@qichencloud.example>','["gaokai_dev@163.com"]','2025-06-26T09:05:00Z',
   '6 record 20 record 7 record，record 6 record 25 record。record，record。',1,0,'{}',306,'2025-06-26T09:05:00Z'),
  (10,1,'<20250411-q1-bonus-note@hanlandata.example>','record','record <payroll@hanlandata.example>','["gaokai_dev@163.com"]','2025-04-11T03:28:00Z',
   'record 3 record，record。record；record。',1,0,'{}',266,'2025-04-11T03:28:00Z'),
  (11,1,'<20260528-card-statement@metrobank.example>','5 record','record <statement@metrobank.example>','["gaokai_dev@163.com"]','2026-05-28T00:48:00Z',
   'record、record，record 6 record 17 record。record，record。',1,0,'{}',228,'2026-05-28T00:48:00Z'),
  (12,1,'<20260602-shanghai-backend-digest@jobs.example>','record：record、record','record <digest@jobs.example>','["gaokai_dev@163.com"]','2026-06-02T23:36:00Z',
   'record，record。record，record、record。',1,0,'{}',258,'2026-06-02T23:36:00Z'),
  (13,1,'<20260604-contractor-role@talentbridge.example>','record','record <consultant@talentbridge.example>','["gaokai_dev@163.com"]','2026-06-04T06:52:00Z',
   'record，record，record。record，record；record。',1,0,'{}',268,'2026-06-04T06:52:00Z'),
  (14,1,'<20260521-observability-meetup@techcommunity.example>','record','record <events@techcommunity.example>','["gaokai_dev@163.com"]','2026-05-21T12:14:00Z',
   'record 6 record 13 record，record、record。record，record。',1,0,'{}',236,'2026-05-21T12:14:00Z'),
  (15,1,'<20260518-property-invoice@residence.example>','record','record <billing@residence.example>','["gaokai_dev@163.com"]','2026-05-18T04:37:00Z',
   'record，record，record 4 record 6 record。record，record。',1,0,'{}',250,'2026-05-18T04:37:00Z'),
  (16,1,'<20260309-school-fee-receipt@school.example>','record','record <finance@school.example>','["gaokai_dev@163.com"]','2026-03-09T02:23:00Z',
   'record，record。record，record。',1,0,'{}',226,'2026-03-09T02:23:00Z'),
  (17,1,'<20260105-annual-bank-statement@metrobank.example>','2025 record','record <account@metrobank.example>','["gaokai_dev@163.com"]','2026-01-05T08:31:00Z',
   'record 2025 record 1 record 1 record 12 record 31 record，record、record、record。record，record。',1,0,'{}',286,'2026-01-05T08:31:00Z'),
  (18,1,'<20260607-mail-security@163-security.example>','record','record <security@163-security.example>','["gaokai_dev@163.com"]','2026-06-07T14:06:00Z',
   'record。record；record。',1,0,'{}',258,'2026-06-07T14:06:00Z'),
  (19,1,'<20240402-2023-refund-receipt@tax-service.example>','2023 record','record <notice@tax-service.example>','["gaokai_dev@163.com"]','2024-04-02T05:11:00Z',
   'record 2024 record 4 record，record。record，record。',1,0,'{}',252,'2024-04-02T05:11:00Z'),
  (20,1,'<20260530-dental-followup@clinic.example>','record','record <appointment@clinic.example>','["gaokai_dev@163.com"]','2026-05-30T03:46:00Z',
   'record 6 record 20 record，record。record，record；record。',1,0,'{}',198,'2026-05-30T03:46:00Z');
COMMIT;
