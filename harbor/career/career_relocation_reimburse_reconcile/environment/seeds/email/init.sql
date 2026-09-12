-- emails-mcp env -- career_relocation_reimburse_reconcile -- init.sql
-- Kuai Bai(gaokai) Personalemail. Reference 2026-06-08.
-- English text/relocation reimbursementshortfallplan/HREnglish text/English textinterview English text event.yaml mutation English text(id>=100).
-- English text(relocation reimbursementshortfallplanamount/English textbasis/signingEnglish text)English textbody, agent must read_email English text;
-- HR planEnglish text"basesalary25800×8English text"English text, English text multi-modal-reconcile English text(English textbasisEnglish text banking+legal).
BEGIN;
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES (1,'gaokai_dev@163.com','Kuai Bai (Kuai Bai)','2018-08-01T00:00:00Z');
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1,1,'<hr-notice@lishimfg.com>','【Lithic Manufacturing】English textpositionEnglish textnotice','Lithic Manufacturing HR Lan Guo <hr.guolan@lishimfg.com>','["gaokai_dev@163.com"]','2026-06-08T10:00:00Z',
   'Kuai Baihello：English textcompanyEnglish textadjustment，English texttransactionEnglish text，basis《Labor Contract Law》English text，companyEnglish textlaborEnglish text，last working dayEnglish text 2026-06-30。relocation reimbursementshortfallplanEnglish textsigningEnglish text。pleaseEnglish text。',1,1,'{}',120,'2026-06-08T10:00:00Z'),
  (2,1,'<welcome@lagou.com>','English textrecruiting：English text','English text <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-06-09T08:00:00Z',
   'English text，English textShanghaibackendEnglish text，English text。',1,0,'{}',45,'2026-06-09T08:00:00Z'),
  (3,1,'<promo@peixun.com>','【English text】laborarbitrationEnglish text English text','English textlegalEnglish text <promo@laodong-vip.com>','["gaokai_dev@163.com"]','2026-06-10T09:00:00Z',
   'English textlaborarbitration，English text2999English textmaterials fee，English text！add contact xxxx immediatelyEnglish text。(English text)',0,0,'{}',52,'2026-06-10T09:00:00Z'),
  (4,1,'<newsletter@infoq.cn>','InfoQ English text','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-06-11T08:00:00Z',
   'English textreliabilityEnglish text……',1,0,'{}',30,'2026-06-11T08:00:00Z'),
  (5,1,'<wife@family.com>','English textprenatal checkupEnglish text','English text <linyue@family.com>','["gaokai_dev@163.com"]','2026-06-11T19:00:00Z',
   'English text，English textmorningprenatal checkup，English text。English text，English text。',1,0,'{}',40,'2026-06-11T19:00:00Z');
COMMIT;
