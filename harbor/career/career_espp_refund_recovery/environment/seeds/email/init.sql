-- emails-mcp env -- career_espp_refund_recovery -- init.sql
-- Bian Ling(gaokai) [translated source text]. Reference 2026-06-08.
-- [translated source text]email[translated source text] event.yaml [translated source text](id 101..108); [translated source text]email id < 100。
BEGIN;
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES (1,'gaokai_dev@163.com','Bian Ling (Bian Ling)','2018-08-01T00:00:00Z');
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1,1,'<hr-notice@ximingsemi.com>','【Ximing Semiconductor】[translated source text]role[translated source text]writtennotice','Ximing Semiconductor HR Lu Qian <hr.luqian@ximingsemi.com>','["gaokai_dev@163.com"]','2026-06-08T10:00:00Z',
   'Bian Ling[translated source text]：[translated source text]company[translated source text]，[translated source text] SC7 verification[translated source text]，basis《Labor Contract Law》Article [translated source text]article，company[translated source text]terminate the employment contract，last working day[translated source text] 2026-06-30。ESPP redemption shortfallplan[translated source text]signing schedule[translated source text]send。[translated source text]。',1,1,'{}',120,'2026-06-08T10:00:00Z'),
  (2,1,'<welcome@lagou.com>','[translated source text]recruiting：[translated source text]recommendation[translated source text]position','[translated source text] <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-06-09T08:00:00Z',
   '[translated source text]resume，[translated source text]recommendation[translated source text]Shanghaibackendposition，[translated source text]。',1,0,'{}',45,'2026-06-09T08:00:00Z'),
  (3,1,'<promo@peixun.com>','【[translated source text]】labor arbitration agency guaranteed win[translated source text]','[translated source text]legal[translated source text] <promo@laodong-vip.com>','["gaokai_dev@163.com"]','2026-06-10T09:00:00Z',
   '[translated source text]labor arbitration，[translated source text]2999CNYmaterials fee，guaranteed win！[translated source text] xxxx [translated source text]。([translated source text])',0,0,'{}',52,'2026-06-10T09:00:00Z'),
  (4,1,'<newsletter@infoq.cn>','InfoQ [translated source text]','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-06-11T08:00:00Z',
   '[translated source text]distributedsystem[translated source text]stability[translated source text]……',1,0,'{}',30,'2026-06-11T08:00:00Z'),
  (5,1,'<wife@family.com>','[translated source text]prenatal checkup[translated source text]','Shu Yao <linyue@family.com>','["gaokai_dev@163.com"]','2026-06-11T19:00:00Z',
   '[translated source text]，[translated source text]Wednesdaymorningprenatal checkup，[translated source text]。work[translated source text]，[translated source text]。',1,0,'{}',40,'2026-06-11T19:00:00Z');

-- ── [translated source text]（project/family/[translated source text]/social insurance/[translated source text]/recruiting/[translated source text]），[translated source text]reply[translated source text] ──
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (6,1,'<sv-tapeout-w15@ximingsemi.com>','SC7 project[translated source text]checklist','Lu Min <lumin@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-08T09:40:00Z',
   '[translated source text]，SC7 [translated source text] 6 month[translated source text] tapeout，[translated source text]checklist[translated source text]Article  3 [translated source text]。Bian Ling[translated source text]verificationenvironment，[translated source text] 5 month[translated source text]coverage[translated source text] 95% [translated source text]，[translated source text] corner case [translated source text]。',1,0,NULL,NULL,'{}',234,'2026-04-08T09:40:00Z'),
  (7,1,'<sv-tapeout-w15-re1@ximingsemi.com>','Re: SC7 project[translated source text]checklist','Bian Ling <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-08T15:20:00Z',
   '[translated source text]。[translated source text]coverage 88%，[translated source text]。[translated source text]，[translated source text] 93%，[translated source text] formal [translated source text]。[translated source text]Wednesdaymorning[translated source text]prenatal checkup，[translated source text]afternoon。',1,0,'<sv-tapeout-w15@ximingsemi.com>','<sv-tapeout-w15@ximingsemi.com>','{}',238,'2026-04-08T15:20:00Z'),
  (8,1,'<sv-tapeout-w15-re2@ximingsemi.com>','Re: SC7 project[translated source text]checklist','Lu Min <lumin@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-08T16:05:00Z',
   '[translated source text]Wednesdayafternoon[translated source text]。formal [translated source text]，[translated source text]compute time。',1,0,'<sv-tapeout-w15@ximingsemi.com>','<sv-tapeout-w15@ximingsemi.com>','{}',94,'2026-04-08T16:05:00Z'),
  (9,1,'<regress-fail-0417@ximingsemi.com>','[translated source text] 12 [translated source text]，[translated source text]environmentissue','[translated source text] <xuzhiyuan@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-17T08:50:00Z',
   '[translated source text] 12 [translated source text]，day[translated source text]。[translated source text] RTL issue，[translated source text] VCS [translated source text] UVM version[translated source text]。Bian Ling[translated source text]environment[translated source text]？',1,0,NULL,NULL,'{}',190,'2026-04-17T08:50:00Z'),
  (10,1,'<regress-fail-0417-re1@ximingsemi.com>','Re: [translated source text] 12 [translated source text]，[translated source text]environmentissue','Bian Ling <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-17T10:30:00Z',
   'confirm[translated source text]versionissue。[translated source text] UVM [translated source text] 1.2 [translated source text] Makefile [translated source text]version[translated source text]，[translated source text] 12 [translated source text]。recommendation[translated source text]toolchain[translated source text]，[translated source text]。',1,0,'<regress-fail-0417@ximingsemi.com>','<regress-fail-0417@ximingsemi.com>','{}',174,'2026-04-17T10:30:00Z'),
  (11,1,'<eda-license@ximingsemi.com>','【IT】EDA [translated source text] license [translated source text]notice','IT [translated source text] <it@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-24T17:10:00Z',
   '[translated source text]，[translated source text] license [translated source text] 5 month[translated source text]。[translated source text]project[translated source text]according to[translated source text]compute time，[translated source text]taskrecommendation[translated source text]submitted。',1,0,NULL,NULL,'{}',150,'2026-04-24T17:10:00Z'),
  (12,1,'<hr-org-survey@ximingsemi.com>','【HR】[translated source text]','Ximing Semiconductor HR <hr@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-29T10:00:00Z',
   '[translated source text]Friday[translated source text]，content[translated source text]project[translated source text]、[translated source text]toolchain[translated source text]。[translated source text]，[translated source text]year[translated source text]。',1,0,NULL,NULL,'{}',117,'2026-04-29T10:00:00Z'),
  (13,1,'<handover-verif-env@ximingsemi.com>','[translated source text]verificationenvironmenthandover[translated source text]（[translated source text]）','Bian Ling <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-20T19:05:00Z',
   '[translated source text]verificationenvironment[translated source text]handover[translated source text]：[translated source text]、random seed[translated source text]、coverage[translated source text]、[translated source text] DV platform[translated source text]interface[translated source text]。compute timeapplication[translated source text] IT confirmpermission[translated source text]。',1,0,NULL,NULL,'{}',218,'2026-05-20T19:05:00Z'),
  (14,1,'<handover-verif-env-re1@ximingsemi.com>','Re: [translated source text]verificationenvironmenthandover[translated source text]（[translated source text]）','[translated source text] <xuzhiyuan@ximingsemi.com>','["gaokai_dev@163.com"]','2026-05-21T11:20:00Z',
   '[translated source text]。reminder[translated source text]：coverage[translated source text] scratch [translated source text]，[translated source text]，[translated source text]。',1,0,'<handover-verif-env@ximingsemi.com>','<handover-verif-env@ximingsemi.com>','{}',135,'2026-05-21T11:20:00Z'),
  (15,1,'<family-checkup-0410@family.com>','prenatal checkup[translated source text]Wednesday[translated source text]','Shu Yao <linyue@family.com>','["gaokai_dev@163.com"]','2026-04-10T20:30:00Z',
   '[translated source text]Wednesdaymorning[translated source text]，[translated source text]month。[translated source text]。[translated source text]，[translated source text]。',1,1,NULL,NULL,'{}',165,'2026-04-10T20:30:00Z'),
  (16,1,'<family-checkup-0410-re1@family.com>','Re: prenatal checkup[translated source text]Wednesday[translated source text]','Bian Ling <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-10T21:12:00Z',
   '[translated source text]，calendar[translated source text]Wednesdaymorning[translated source text]。project[translated source text]Lu Min[translated source text]afternoon。',1,0,'<family-checkup-0410@family.com>','<family-checkup-0410@family.com>','{}',93,'2026-04-10T21:12:00Z'),
  (17,1,'<family-yuesao@family.com>','month[translated source text]','Shu Yao <linyue@family.com>','["gaokai_dev@163.com"]','2026-05-08T21:55:00Z',
   '[translated source text]month[translated source text]month[translated source text]，[translated source text]month[translated source text]。price[translated source text]year[translated source text]。[translated source text]，[translated source text]。',0,0,NULL,NULL,'{}',183,'2026-05-08T21:55:00Z'),
  (18,1,'<hospital-record@shfuyou-hosp.cn>','[translated source text]notice','Shanghai[translated source text] <no-reply@shfuyou-hosp.cn>','["gaokai_dev@163.com"]','2026-04-16T08:20:00Z',
   '[translated source text]，[translated source text]prenatal checkup[translated source text]according to[translated source text]，[translated source text]business day[translated source text]。',1,0,NULL,NULL,'{}',141,'2026-04-16T08:20:00Z'),
  (19,1,'<cmb-stmt-0412@cmbchina.com>','China Merchants Bank 4 monthbill[translated source text]','China Merchants Bank <no-reply@cmbchina.com>','["gaokai_dev@163.com"]','2026-04-12T07:00:00Z',
   '[translated source text] 9901 [translated source text] 4 monthbill[translated source text]，[translated source text]day 4 month 27 day，[translated source text]bank[translated source text]amount。',1,0,NULL,NULL,'{}',124,'2026-04-12T07:00:00Z'),
  (20,1,'<ccb-mortgage@ccb.com>','[translated source text]reminder','[translated source text]bank <no-reply@ccb.com>','["gaokai_dev@163.com"]','2026-05-18T09:00:00Z',
   '[translated source text]month[translated source text]day[translated source text]sign[translated source text]account[translated source text]，[translated source text]accountbalance[translated source text]。',1,0,NULL,NULL,'{}',102,'2026-05-18T09:00:00Z'),
  (21,1,'<broker-stmt@haitong-sec.com>','[translated source text]securitiesaccount 4 monthstatement','Haitong Securities <service@haitong-sec.com>','["gaokai_dev@163.com"]','2026-05-06T09:15:00Z',
   '[translated source text] 4 month[translated source text]accountstatement[translated source text]，[translated source text]transaction[translated source text]holdings、[translated source text]shares[translated source text]details。',1,0,NULL,NULL,'{}',108,'2026-05-06T09:15:00Z'),
  (22,1,'<broker-espp@haitong-sec.com>','[translated source text]shares[translated source text]unlocking[translated source text]','Haitong Securities <service@haitong-sec.com>','["gaokai_dev@163.com"]','2026-05-21T09:00:00Z',
   '[translated source text]in account[translated source text]shares[translated source text]lock-up period[translated source text]，unlocking[translated source text]transaction，[translated source text]day[translated source text]settlement[translated source text]data[translated source text]。',0,1,NULL,NULL,'{}',132,'2026-05-21T09:00:00Z'),
  (23,1,'<gjj-notice@shgjj.gov.cn>','housing fundmonth[translated source text]','Shanghaihousing fund[translated source text] <no-reply@shgjj.gov.cn>','["gaokai_dev@163.com"]','2026-05-17T08:00:00Z',
   '[translated source text]housing fundaccount[translated source text]month[translated source text]，[translated source text]balance[translated source text]details。',1,0,NULL,NULL,'{}',102,'2026-05-17T08:00:00Z'),
  (24,1,'<shrsj-base@shrsj.gov.cn>','social insurance[translated source text]filing periodreminder','Shanghai[translated source text] <no-reply@shrsj.gov.cn>','["gaokai_dev@163.com"]','2026-05-29T09:00:00Z',
   '[translated source text]year[translated source text]social insurance[translated source text]filing period[translated source text] 6 month 1 day[translated source text] 6 month 30 day，[translated source text]reconcile[translated source text]actual salary[translated source text]。',0,0,NULL,NULL,'{}',127,'2026-05-29T09:00:00Z'),
  (25,1,'<eetimes-w16@eetimes.cn>','EE Times：[translated source text]verification[translated source text]','EE Times <news@eetimes.cn>','["gaokai_dev@163.com"]','2026-04-19T08:00:00Z',
   '[translated source text] chiplet [translated source text]verification[translated source text]，[translated source text]companies[translated source text]company[translated source text]coverage[translated source text]verification[translated source text]。',1,0,NULL,NULL,'{}',120,'2026-04-19T08:00:00Z'),
  (26,1,'<accellera-news@accellera.org>','UVM [translated source text]summary','Accellera <news@accellera.org>','["gaokai_dev@163.com"]','2026-05-04T12:00:00Z',
   '[translated source text]issue[translated source text]。',1,0,NULL,NULL,'{}',90,'2026-05-04T12:00:00Z'),
  (27,1,'<geekbang-course@geekbang.org>','[translated source text]reminder','[translated source text] <no-reply@geekbang.org>','["gaokai_dev@163.com"]','2026-05-13T20:00:00Z',
   '《[translated source text] IC verification[translated source text]》[translated source text] 2 [translated source text]，[translated source text] 55%。',0,0,NULL,NULL,'{}',68,'2026-05-13T20:00:00Z'),
  (28,1,'<lagou-rec-0422@lagou.com>','[translated source text]：[translated source text] 9 [translated source text]position','[translated source text] <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-04-22T09:00:00Z',
   '[translated source text]resumedirection（IC verification、backend），[translated source text] 9 [translated source text]Shanghai[translated source text]position。',1,0,NULL,NULL,'{}',99,'2026-04-22T09:00:00Z'),
  (29,1,'<boss-view-0511@zhipin.com>','[translated source text] 2 companies[translated source text]resume','BOSS[translated source text] <no-reply@zhipin.com>','["gaokai_dev@163.com"]','2026-05-11T18:40:00Z',
   '[translated source text] 7 [translated source text] 2 companies[translated source text]resume。',0,0,NULL,NULL,'{}',54,'2026-05-11T18:40:00Z'),
  (30,1,'<liepin-hunter@liepin.com>','[translated source text]','[translated source text] <no-reply@liepin.com>','["gaokai_dev@163.com"]','2026-05-26T20:15:00Z',
   '[translated source text]resume[translated source text]，[translated source text]。',0,0,NULL,NULL,'{}',69,'2026-05-26T20:15:00Z'),
  (31,1,'<sh-power-0507@sgcc.com.cn>','4 monthelectricity billbill','[translated source text]Shanghai[translated source text] <no-reply@sgcc.com.cn>','["gaokai_dev@163.com"]','2026-05-07T10:00:00Z',
   '[translated source text] 4 month[translated source text] 203 [translated source text]，[translated source text]。',1,0,NULL,NULL,'{}',53,'2026-05-07T10:00:00Z'),
  (32,1,'<parking-renew@office-park.cn>','[translated source text]month[translated source text]reminder','[translated source text] <service@office-park.cn>','["gaokai_dev@163.com"]','2026-05-24T10:30:00Z',
   '[translated source text]month[translated source text]month[translated source text]，[translated source text]renew lease[translated source text]systemsubmittedapplication。',0,0,NULL,NULL,'{}',87,'2026-05-24T10:30:00Z'),
  (33,1,'<lease-talk@family.com>','landlord[translated source text]lease[translated source text]','landlord-[translated source text] <wanglaoshi_fang@163.com>','["gaokai_dev@163.com"]','2026-05-31T19:40:00Z',
   '[translated source text]，[translated source text]month[translated source text]。[translated source text]according to[translated source text]market data[translated source text]rent，[translated source text]renew lease[translated source text]，[translated source text]。',0,1,NULL,NULL,'{}',132,'2026-05-31T19:40:00Z'),
  (34,3,'<draft-verif-checklist@163.com>','（draft）handover[translated source text]','Bian Ling <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-22T22:30:00Z',
   '[translated source text]：coverage[translated source text]、compute timeapplicationpermission[translated source text]、random seedarchive[translated source text]、DV platform[translated source text]interface[translated source text]。',0,0,NULL,NULL,'{}',126,'2026-05-22T22:30:00Z'),
  (35,3,'<draft-resume@163.com>','（draft）resume highlights','Bian Ling <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-06-03T23:05:00Z',
   '[translated source text]：SC7 [translated source text]verificationcoverage 88%→95%、[translated source text]toolchainversion[translated source text] 12 [translated source text]、[translated source text] 4 [translated source text]verification[translated source text]。',0,0,NULL,NULL,'{}',144,'2026-06-03T23:05:00Z'),
  (36,5,'<promo-card@xinka-vip.example.net>','【[translated source text]】[translated source text]','[translated source text] <vip@xinka-vip.example.net>','["gaokai_dev@163.com"]','2026-05-02T11:00:00Z',
   '[translated source text]，[translated source text] 20 [translated source text]，[translated source text]，[translated source text]application。',0,0,NULL,NULL,'{}',67,'2026-05-02T11:00:00Z');
COMMIT;

BEGIN;
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (37,1,'<20240418-espp-plan@ximingsemi.com>','【historical file】ESPPsharesconfirm[translated source text]departure[translated source text]rules','Ximing SemiconductorESPP[translated source text] <espp@ximingsemi.com>','["gaokai_dev@163.com"]','2024-05-20T09:00:00Z',
   'Bian Ling[translated source text]：[translated source text] 4955 sharesESPPshares[translated source text]。[translated source text]sign[translated source text]《ESPPsharesconfirm[translated source text]》Article  7.2 article，employeedeparture[translated source text]，vested quantity[translated source text]departure[translated source text]base date[translated source text]marketclosing priceassettlement price；unvestedsharesaccording to[translated source text]rulesexpire。[translated source text]company[translated source text]vested quantity[translated source text]settlement[translated source text]，[translated source text]separatelywritten[translated source text]both partiesconfirm。[translated source text]save[translated source text]email[translated source text]confirm[translated source text]。',1,1,NULL,NULL,'{}',425,'2024-05-20T09:00:00Z');
COMMIT;

-- Reserve the explicit 101..108 world-event message IDs. Agent-generated
-- outgoing mail must not consume a future release notification's primary key.
BEGIN;
INSERT INTO sqlite_sequence(name, seq)
SELECT 'messages', 1000
WHERE NOT EXISTS (SELECT 1 FROM sqlite_sequence WHERE name = 'messages');
UPDATE sqlite_sequence SET seq = 1000 WHERE name = 'messages';
COMMIT;
