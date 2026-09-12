-- emails-mcp env -- career_equity_buyback_recovery -- init.sql
-- Ji Chen (gaokai) personal mailbox. Reference 2026-06-08.
-- Narrative emails are injected by event.yaml at runtime (id 101..108); seed emails have id < 100.
BEGIN;
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES (1,'gaokai_dev@163.com','Ji Chen','2018-08-01T00:00:00Z');
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1,1,'<hr-notice@yiweicloud.com>','[Yiwei Data] Written notice regarding role optimization','Yiwei Data HR Song Ke <hr.songke@yiweicloud.com>','["gaokai_dev@163.com"]','2026-06-08T02:00:00Z',
   'Hello Ji Chen: Due to business restructuring, the Trading Middle Platform team you belong to has been dissolved as a whole. Pursuant to Article 40 of the Labor Contract Law, the company has decided to terminate your labor contract, with your last working day being 2026-06-30. A separate equity repurchase notice covering the shortfall plan and signing arrangements will be sent. Please be advised.',1,1,'{}',120,'2026-06-08T02:00:00Z'),
  (2,1,'<welcome@lagou.com>','Lagou Jobs: New positions recommended for you','Lagou <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-06-09T00:00:00Z',
   'Based on your resume, we recommended several Shanghai backend positions for you this week. Log in to view them.',1,0,'{}',45,'2026-06-09T00:00:00Z'),
  (3,1,'<promo@peixun.com>','[Limited time] Labor arbitration representation - win guaranteed, no fee if you lose','A Legal Consulting Firm <promo@laodong-vip.com>','["gaokai_dev@163.com"]','2026-06-10T01:00:00Z',
   'Professional labor arbitration representation. Pay a 2999 yuan materials fee up front, guaranteed to win! Add WeChat xxxx to proceed immediately. (Ad)',0,0,'{}',52,'2026-06-10T01:00:00Z'),
  (4,1,'<newsletter@infoq.cn>','InfoQ Architecture Picks This Week','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-06-11T00:00:00Z',
   'This week''s featured articles on distributed systems and stability...',1,0,'{}',30,'2026-06-11T00:00:00Z'),
  (5,1,'<wife@family.com>','Remember to accompany me to next week''s prenatal checkup','Shu Yao <linyue@family.com>','["gaokai_dev@163.com"]','2026-06-11T11:00:00Z',
   'Honey, the prenatal checkup is next Wednesday morning, please come with me. Don''t stress too much about work, we''ll get through it together.',1,0,'{}',40,'2026-06-11T11:00:00Z');

-- ── Background correspondence (work/family/finance/social insurance/community/recruitment/life), including reply threads ──
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (6,1,'<tc-2026q2-plan@yiweicloud.com>','Trading Middle Platform Q2 iteration schedule (with canary window)','Zhou Ming <zhouming@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-07T02:12:00Z',
   'Everyone, I''ve posted the Q2 schedule on the wiki. This round''s focus is wrapping up the order-chain database and table sharding, with the canary window set for the evenings of Monday 4/20 and Monday 5/11. The accounting reconciliation module that Ji Chen owns is in the second batch; please submit your rollback plan one week before the canary.',1,0,NULL,NULL,'{}',249,'2026-04-07T02:12:00Z'),
  (7,1,'<tc-2026q2-plan-re1@yiweicloud.com>','Re: Trading Middle Platform Q2 iteration schedule (with canary window)','Ji Chen <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-07T06:36:00Z',
   'Got it. I''ll write the rollback plan using the template from the last production incident postmortem and post it in the group before Friday. The second canary batch is fine on my end, but I have to attend a prenatal checkup the week of 5/11, so evening canary works, but please move the daytime postmortem meeting to the afternoon.',1,0,'<tc-2026q2-plan@yiweicloud.com>','<tc-2026q2-plan@yiweicloud.com>','{}',219,'2026-04-07T06:36:00Z'),
  (8,1,'<tc-2026q2-plan-re2@yiweicloud.com>','Re: Trading Middle Platform Q2 iteration schedule (with canary window)','Zhou Ming <zhouming@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-07T07:02:00Z',
   'OK, I''ve moved the postmortem meeting to 14:30. Also a heads-up: after this round the architecture team may reassign module ownership; details to be announced.',1,0,'<tc-2026q2-plan@yiweicloud.com>','<tc-2026q2-plan@yiweicloud.com>','{}',129,'2026-04-07T07:02:00Z'),
  (9,1,'<oncall-0412@yiweicloud.com>','[On-call] Handling record for the 4/12 early-morning reconciliation task timeout','Li Zhe <lizhe@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-12T01:30:00Z',
   'Last night''s reconciliation task ran for 3 hours without finishing, so I split the batch in half and reran it. A preliminary look suggests the upstream transaction table''s delta is too large and the index isn''t being used. Ji Chen, you know this area well - next week could you look into whether we should add a time partition?',1,0,NULL,NULL,'{}',219,'2026-04-12T01:30:00Z'),
  (10,1,'<oncall-0412-re1@yiweicloud.com>','Re: [On-call] Handling record for the 4/12 early-morning reconciliation task timeout','Ji Chen <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-13T03:05:00Z',
   'I checked the execution plan and it is indeed a full table scan. I added a partition on posted_at and reduced the batch size from 50,000 to 20,000, and last night''s rerun finished in 22 minutes. The change has been merged to trunk, with the rollback switch kept in place.',1,0,'<oncall-0412@yiweicloud.com>','<oncall-0412@yiweicloud.com>','{}',195,'2026-04-13T03:05:00Z'),
  (11,1,'<arch-review-0421@yiweicloud.com>','Architecture review: the boundary between the accounting module and the settlement domain','Architecture Team <arch@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-21T08:40:00Z',
   'This Thursday at 2 PM we''ll review the domain boundary between accounting and settlement, and discuss module ownership changes. Please review the current-state diagram in the attachment in advance. Ji Chen and Li Zhe must attend.',1,1,NULL,NULL,'{}',180,'2026-04-21T08:40:00Z'),
  (12,1,'<hr-org-survey@yiweicloud.com>','[HR] Organizational effectiveness survey (please complete this week)','Yiwei Data HR <hr@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-28T02:00:00Z',
   'To understand how teams are collaborating, please complete the survey by this Friday. The survey is anonymous, and results are used only for organizational improvement reference.',1,0,NULL,NULL,'{}',117,'2026-04-28T02:00:00Z'),
  (13,1,'<tc-handover-draft@yiweicloud.com>','Accounting reconciliation module handover doc (first draft)','Ji Chen <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-19T10:22:00Z',
   'Per Zhou Ming''s request I put together a first draft of the reconciliation module handover doc, covering batch scheduling, exception compensation, and the finance-side interface conventions. The permission list still has two systems left to sort out; I''ll finish it next week.',1,0,NULL,NULL,'{}',198,'2026-05-19T10:22:00Z'),
  (14,1,'<tc-handover-draft-re1@yiweicloud.com>','Re: Accounting reconciliation module handover doc (first draft)','Li Zhe <lizhe@yiweicloud.com>','["gaokai_dev@163.com"]','2026-05-20T01:15:00Z',
   'Finished reading, it''s quite detailed. One addition: the finance-side month-end closing interface changed its signature method once last year, and the old docs still have the old one. I suggest you flag it in your doc, otherwise whoever takes over will easily trip on it.',1,0,'<tc-handover-draft@yiweicloud.com>','<tc-handover-draft@yiweicloud.com>','{}',189,'2026-05-20T01:15:00Z'),
  (15,1,'<family-checkup-0409@family.com>','Prenatal checkup time changed again','Shu Yao <linyue@family.com>','["gaokai_dev@163.com"]','2026-04-09T12:14:00Z',
   'The doctor says from now on it''s every Wednesday morning, from 9 to 11:30, through October. Block that time out and don''t schedule meetings then. This time the doctor said all indicators are normal, just told me to stop staying up late.',1,1,NULL,NULL,'{}',198,'2026-04-09T12:14:00Z'),
  (16,1,'<family-checkup-0409-re1@family.com>','Re: Prenatal checkup time changed again','Ji Chen <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-09T13:03:00Z',
   'Noted. I''ve locked down Wednesday mornings in my calendar. I already had Zhou Ming move this week''s postmortem meeting to the afternoon.',1,0,'<family-checkup-0409@family.com>','<family-checkup-0409@family.com>','{}',105,'2026-04-09T13:03:00Z'),
  (17,1,'<family-crib@family.com>','Links for the crib and stroller','Shu Yao <linyue@family.com>','["gaokai_dev@163.com"]','2026-05-06T13:40:00Z',
   'My mom says she''ll buy the crib, so let''s just decide on the stroller and the car seat. I''ve got my eye on two brands, let''s look at them together tonight. Also, the agency for the confinement nanny says we should book before the end of June - the good slots go fast.',1,0,NULL,NULL,'{}',201,'2026-05-06T13:40:00Z'),
  (18,1,'<hospital-notice@shjiaotong-hosp.cn>','Obstetrics registration reminder','Shanghai Maternity & Child Health Hospital <no-reply@shjiaotong-hosp.cn>','["gaokai_dev@163.com"]','2026-04-15T00:30:00Z',
   'You have completed your obstetrics registration. For subsequent prenatal checkups, please bring your maternal and child health handbook and arrive at your scheduled time. To reschedule, please do so via the official account at least one business day in advance.',1,0,NULL,NULL,'{}',147,'2026-04-15T00:30:00Z'),
  (19,1,'<cmb-stmt-0410@cmbchina.com>','China Merchants Bank: April statement is out','China Merchants Bank <no-reply@cmbchina.com>','["gaokai_dev@163.com"]','2026-04-09T23:00:00Z',
   'Your credit card ending in 9901 has its April statement generated. Please log in to mobile banking to check the amount due; the final payment date is April 25.',1,0,NULL,NULL,'{}',127,'2026-04-09T23:00:00Z'),
  (20,1,'<cmb-payroll-0510@cmbchina.com>','Salary credit notice','China Merchants Bank <no-reply@cmbchina.com>','["gaokai_dev@163.com"]','2026-05-10T02:05:00Z',
   'Your debit card ending in 8823 received a salary credit on May 10. Please check the transaction details in mobile banking.',1,0,NULL,NULL,'{}',112,'2026-05-10T02:05:00Z'),
  (21,1,'<broker-monthly@guojun-sec.com>','Your securities account April statement','Guojun Securities <service@guojun-sec.com>','["gaokai_dev@163.com"]','2026-05-05T01:20:00Z',
   'Dear customer, your April securities account statement has been generated. You can view your holdings and fund movement details under "My - Statements" in the trading app.',1,0,NULL,NULL,'{}',142,'2026-05-05T01:20:00Z'),
  (22,1,'<broker-risk@guojun-sec.com>','Risk assessment expiry reminder','Guojun Securities <service@guojun-sec.com>','["gaokai_dev@163.com"]','2026-05-22T01:00:00Z',
   'Your investor risk tolerance assessment will expire next month, after which some products will no longer be purchasable. Please re-take the assessment in time.',0,0,NULL,NULL,'{}',123,'2026-05-22T01:00:00Z'),
  (23,1,'<mortgage-rate@ccb.com>','Personal mortgage interest rate adjustment notice','China Construction Bank <no-reply@ccb.com>','["gaokai_dev@163.com"]','2026-04-18T01:00:00Z',
   'Based on the latest LPR quote, the interest rate on your mortgage will be repriced from the next repayment date per the contract, and your monthly payment will be adjusted accordingly.',1,0,NULL,NULL,'{}',137,'2026-04-18T01:00:00Z'),
  (24,1,'<shbao-annual@shrsj.gov.cn>','2026 annual social insurance contribution base filing reminder','Shanghai Human Resources and Social Security <no-reply@shrsj.gov.cn>','["gaokai_dev@163.com"]','2026-05-28T01:00:00Z',
   'The social insurance contribution base filing period this year is June 1 to June 30. Please verify your filing base through your employer or the One-Net-Office portal.',0,0,NULL,NULL,'{}',133,'2026-05-28T01:00:00Z'),
  (25,1,'<gjj-balance@shgjj.gov.cn>','Housing fund account balance change','Shanghai Housing Fund Center <no-reply@shgjj.gov.cn>','["gaokai_dev@163.com"]','2026-05-16T00:00:00Z',
   'Your housing provident fund account had a deposit this month. You can check the details and account balance via the official account or the One-Net-Office portal.',1,0,NULL,NULL,'{}',114,'2026-05-16T00:00:00Z'),
  (26,1,'<infoq-w15@infoq.cn>','InfoQ Architecture Weekly: Three approaches to distributed transactions in practice','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-04-14T00:00:00Z',
   'This issue''s picks: a comparison of transaction approaches, from TCC to Saga, used by several top-tier teams in order and accounting scenarios; plus a practical summary on rebuilding the reconciliation system after database and table sharding.',1,0,NULL,NULL,'{}',172,'2026-04-14T00:00:00Z'),
  (27,1,'<gh-digest@github.com>','GitHub: 3 repositories you follow have new releases','GitHub <noreply@github.com>','["gaokai_dev@163.com"]','2026-04-25T04:00:00Z',
   'Seata released 2.3.0, mainly fixing the hanging issue in AT mode; two other projects you starred also released minor versions.',1,0,NULL,NULL,'{}',121,'2026-04-25T04:00:00Z'),
  (28,1,'<geekbang-course@geekbang.org>','The course you purchased added 2 new lessons','GeekTime <no-reply@geekbang.org>','["gaokai_dev@163.com"]','2026-05-12T12:00:00Z',
   '"Distributed System Design" added 2 new lessons including "Engineering trade-offs of consensus protocols", with a cumulative learning progress of 62%.',0,0,NULL,NULL,'{}',109,'2026-05-12T12:00:00Z'),
  (29,1,'<lagou-rec-0420@lagou.com>','Lagou: 12 positions matched for you this week','Lagou <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-04-20T01:00:00Z',
   'Based on your resume direction (Java/Go backend, distributed systems), we matched 12 Shanghai-area positions for you this week. Log in to view details.',1,0,NULL,NULL,'{}',129,'2026-04-20T01:00:00Z'),
  (30,1,'<boss-view-0509@zhipin.com>','3 companies viewed your resume','BOSS Zhipin <no-reply@zhipin.com>','["gaokai_dev@163.com"]','2026-05-09T10:30:00Z',
   'In the past 7 days, 3 companies viewed your online resume. Completing your project experience can increase the chance of being viewed.',0,0,NULL,NULL,'{}',99,'2026-05-09T10:30:00Z'),
  (31,1,'<maimai-msg@maimai.cn>','Maimai: You have 2 unread direct messages','Maimai <no-reply@maimai.cn>','["gaokai_dev@163.com"]','2026-05-25T13:10:00Z',
   'A headhunter sent you a direct message. Log in to view it.',0,0,NULL,NULL,'{}',48,'2026-05-25T13:10:00Z'),
  (32,1,'<sh-power-0505@sgcc.com.cn>','April electricity bill','State Grid Shanghai Electric Power <no-reply@sgcc.com.cn>','["gaokai_dev@163.com"]','2026-05-05T02:00:00Z',
   'Your April electricity usage was 218 kWh, and the fee was successfully deducted from your linked account.',1,0,NULL,NULL,'{}',68,'2026-05-05T02:00:00Z'),
  (33,1,'<lease-renew@family.com>','The landlord mentioned the lease','Sub-landlord Zhang <zhangsan_landlord@163.com>','["gaokai_dev@163.com"]','2026-05-30T11:20:00Z',
   'Xiao Ji, the lease on your unit expires at the end of August. I''d like to raise the rent a bit, based on the surrounding market rate. If you plan to renew, let me know in advance; if not, tell me early too so I can list it.',0,1,NULL,NULL,'{}',177,'2026-05-30T11:20:00Z'),
  (34,3,'<draft-handover-checklist@163.com>','(Draft) Handover checklist items still to add','Ji Chen <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-21T14:40:00Z',
   'To add: the finance month-end closing interface signature method, the canary switch list, on-call doc permissions, and the latest version of the reconciliation exception handling SOP.',0,0,NULL,NULL,'{}',125,'2026-05-21T14:40:00Z'),
  (35,3,'<draft-resume-update@163.com>','(Draft) Resume update points','Ji Chen <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-06-02T15:15:00Z',
   'To add: the quantified results of the database/table sharding wrap-up, the fact that reconciliation tasks dropped from 3 hours to 22 minutes, and the experience of leading a 5-person team.',0,0,NULL,NULL,'{}',124,'2026-06-02T15:15:00Z'),
  (36,5,'<promo-loan@xinyongdai.example.net>','[Pre-approved] You have a 300,000 credit line awaiting activation','Quick Credit <promo@xinyongdai.example.net>','["gaokai_dev@163.com"]','2026-04-30T03:20:00Z',
   'Congratulations on passing pre-approval. You can borrow up to 300,000, with same-day disbursement. Click the link to activate your credit line.',0,0,NULL,NULL,'{}',88,'2026-04-30T03:20:00Z'),
  (37,5,'<promo-invest@licai-vip.example.net>','12% annualized steady wealth product, limited slots','Wealth Manager <vip@licai-vip.example.net>','["gaokai_dev@163.com"]','2026-05-27T07:45:00Z',
   'A quality project is open for subscription at 12% annualized, with a 50,000 minimum investment. First come, first served.',0,0,NULL,NULL,'{}',70,'2026-05-27T07:45:00Z');
COMMIT;

BEGIN;
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (38,1,'<20240520-rsu-plan@yiweicloud.com>','[Historical document] 2024 restricted stock grant confirmation and departure settlement rules','Yiwei Data Equity Incentive Office <equity@yiweicloud.com>','["gaokai_dev@163.com"]','2024-05-20T01:00:00Z',
   'Hello Ji Chen: The 5000 restricted shares listed in the attachment have completed vesting. According to Section 8.3 of the "2024 Restricted Stock Grant Confirmation" you signed, when an employee leaves, the vested portion is settled at the market closing price that can be queried on the departure buyback reference date; the unvested portion lapses per plan rules. If the company intends to adjust the settlement method for the vested portion, it shall provide a separate written explanation and obtain confirmation from both parties. Please keep this email and the grant confirmation safe.',1,1,NULL,NULL,'{}',430,'2024-05-20T01:00:00Z');
COMMIT;

-- Reserve agent-email id space above the fixed seed (1..38) and narrative (101..108) ranges.
UPDATE sqlite_sequence SET seq = 999999 WHERE name = 'messages';
