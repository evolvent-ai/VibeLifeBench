-- emails-mcp zhao_meng_litigation — init.sql
-- Snapshot of Zhao Meng's personal email, for a food safety online shopping contract dispute (consumer suing seller for a refund plus tenfold compensation). Reference frame: 2026-05-20.
-- The emails contain key facts of the case (basis for implicit constraints) and must never directly state legal conclusions. This case is a "counterintuitive minefield":
-- The emails preserve the parties' original statements and uncertain understandings, which must be cross-checked against other materials.
--
-- Core traps (each has email factual support + a legal_search case anchor):
-- ① Compensation-multiplier trap: Zhao Meng thought food also involved "refund plus three"; the correct rule is the Food Safety Law's "refund plus ten," with a 1000-yuan minimum (art_fsl_148/case_f01).
--   ② Knowingly buying despite known defects trap: Zhao Meng worries that placing an order after reading negative reviews still counts as "knowingly buying despite known defects" and means she cannot seek compensation; in the food sector, this does not affect the claim (art_interp_03/case_f04).
--   ③ Jurisdiction trap: The seller is in Hangzhou, so Zhao Meng assumes she must go to Hangzhou to file suit; the place where an online purchase is received (Shanghai) is the place of contract performance, so suit may be filed where the goods are received (case_f10).
--   ④ Label defect vs. substantive nonconformity: No Chinese label/expired products/illegal additives = substantive nonconformity eligible for compensation at ten times the price; minor defects that do not affect safety are not compensable (art_interp_15/case_f07).
--   ⑤ Proper defendant: Choose either the producer or the seller; if the platform cannot provide the seller's information, it may make advance compensation (art_fsl_148/art_cpl_c_44/case_f05/f08).
--   Purchase 2026-04-18 / Receipt 2026-04-22 / Price: one can of imported infant formula ¥680 + imported substitute tea ¥1200 / no Chinese label + one product tested positive for illegal additives /
--   The seller "Global Select" is domiciled in Hangzhou, Zhejiang / e-commerce platform "Youxian Gou". The ordinary limitation period is 3 years, and the claim is well within the limitation period.
-- body_text only. id manually specified for reproducibility.

BEGIN;

DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'zhao.meng@gmail.com', 'Zhao Meng (Zhao Meng)', '2026-01-01T00:00:00Z');

DELETE FROM folders;
INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam'),
  (6, 'Family'),
  (7, 'Order');

-- =========================================================================
-- INBOX (folder_id = 1)
-- =========================================================================

-- E-commerce platform: order confirmation (critical!) — product/goods price/seller name/platform/delivery location
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20260418-order@youxiangou.com>', '[Youxiangou] Order confirmation NO.YX20260418', 'Youxiangu Shopping Mall <order@youxiangou.com>', '["zhao.meng@gmail.com"]',
   '2026-04-18T20:20:00Z',
   'Dear Zhao Meng, your order from the "Huanqiu Youxuan" store on Youxianggou Mall has been confirmed: ① 1 can of imported infant formula ¥680; ② 1 box of imported substitute tea (health tea) ¥1200. Total: ¥1880. Seller: Huanqiu Youxuan (operator: Hangzhou Huanqiu Youxuan Food Co., Ltd., registered address: XX Road, Yuhang District, Hangzhou, Zhejiang Province). Delivery address: No. XX, XX Road, Pudong New Area, Shanghai (Zhao Meng). Platform: Youxianggou Mall.',
   1, 1, '{}', 320, '2026-04-18T20:20:00Z');

-- Payment voucher
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (2, 1, '<20260418-pay@youxiangou.com>', '[Youxiangou] Payment successful', 'pay@youxiangou.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T20:25:00Z',
   'Your order YX20260418 has been paid successfully. Amount paid: ¥1880 (WeChat Pay). Thank you for your purchase.',
   1, 0, '{}', 160, '2026-04-18T20:25:00Z');

-- Receipt + discovery of an issue (critical! No Chinese label + suspected illegal additives) — clue indicating noncompliance with food safety standards
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (3, 1, '<20260422-recv@zhao-meng>', '[Backup] Issues Discovered After Receiving the Goods', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-22T19:00:00Z',
   'The goods were received on April 22. Problem documentation (unboxing videos and photos were all preserved): ① The entire can of imported infant formula had only foreign-language text (German), with no Chinese label or Chinese instructions at all, so it was impossible to understand the ingredients, expiration date, or information about the domestic agent; ② The product page for that box of “health-preserving substitute tea” claimed that it could “lower blood pressure and blood sugar and improve sleep,” but it was merely an ordinary food and had no health-food approval number. After drinking it for two days, I experienced heart palpitations, and after looking into it, suspected that it contained something that should not have been added. I sealed and preserved both items as they were and did not continue using them.',
   1, 1, '{}', 320, '2026-04-22T19:00:00Z');

-- Seller's customer service (distraction + misleading: "At most, we can offer you a return and refund" + "If you bought it after seeing the negative reviews, you knowingly bought a fake, so you cannot receive compensation")
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (4, 1, '<20260425-seller@huanqiu.com>', 'Reply: Regarding Your Return Request', 'Huanqiu Youxuan customer service <kefu@huanqiu-youxuan.com>', '["zhao.meng@gmail.com"]',
   '2026-04-25T11:00:00Z',
   'Ms. Zhao, regarding the issue you reported, the most we can do is accept a return and issue a refund; compensation is impossible. Moreover, we saw that before placing your order, you had already read negative reviews in the comments section stating that there was “no Chinese label.” You knew about the situation and still purchased the product, which constitutes knowingly purchasing counterfeit or substandard goods and professional anti-counterfeiting activity. The law will not support your claim for compensation. We suggest that you accept the refund and stop pursuing the matter.',
   1, 1, '{}', 240, '2026-04-25T11:00:00Z');

-- Mother (distractor + misleading: "refund one and compensate three" + "it’s not worth suing over a thousand-plus yuan")
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (5, 1, '<20260510-mom@family.local>', 'Don''t be so particular over such a small amount of money', 'Zhao''s Mother <zhao.mom@163.com>', '["zhao.meng@gmail.com"]',
   '2026-05-10T19:30:00Z',
   'Mengmeng, it’s only a little over a thousand yuan. I’ve heard that if you buy a counterfeit product, at most you can “get a refund plus three times the purchase price.” Even if you got triple that thousand-plus yuan, it wouldn’t amount to much. Is it really worth suing someone and spending so much time and energy over this? Why not just have him refund the money and let it go? — Mom',
   1, 0, '{}', 180, '2026-05-10T19:30:00Z');

-- Draft of the "accounts to pursue together" that Zhao Meng herself listed (factual basis for the claim-screening matrix)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (6, 1, '<20260519-claims-bak@zhao-meng>', '[Backup] Several Charges I Want to Request from the Seller', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-19T22:00:00Z',
   'For this claim, I want to recover everything I can: ① First, refund the 1880 yuan purchase price; ② for the imported milk powder can with no Chinese label and the box of tea suspected of containing an unauthorized additive, I want a refund plus tenfold compensation; ③ I experienced heart palpitations after drinking the tea, went to the hospital emergency department, and spent more than 300 yuan, so I also want to claim the registration and examination fees; ④ I also want the seller to pay me 20,000 yuan in damages for mental distress, just to vent my anger; ⑤ if the seller disappears and cannot be found, can I make the Youxiangu platform pay? ⑥ I did see the negative reviews before placing the order—will that prevent me from recovering compensation? First, ask the assistant how to handle these issues, whether I can claim them, and whom I should sue.',
   1, 0, '{}', 360, '2026-05-19T22:00:00Z');

-- Zhao Meng's own memorandum on the "budget for finding a testing institution" (basis for the hard constraints on selecting and engaging a testing institution)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (7, 1, '<20260516-budget-bak@zhao-meng>', '[Backup] Budget and Requirements for Finding a Food Testing Agency', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-16T22:00:00Z',
   'The lawyer said that to determine whether that box of tea contains any illegal additives and whether the milk powder label complies with the regulations, it would be best to obtain a test report from a legitimate food inspection agency, which the court will recognize. My bottom lines are: ① I can pay at most 3000 yuan (¥3000) for the testing fee; I cannot afford to pay more. I only need to test label compliance and one or two illegal additives, not a full-panel package; ② the agency must have CMA qualifications for food inspection (preferably CNAS as well), and the report must be capable of being accepted by the Shanghai courts; ③ it must be independent and objective, with no affiliation or financial dealings with the seller''s company; ④ do not choose one that "guarantees it will find noncompliance and charges based on the result"—the court will not recognize such a report. First, help me screen the reliable and affordable agencies in the inspection-agency directory on that legal services platform.',
   1, 0, '{}', 360, '2026-05-16T22:00:00Z');

-- Emergency-room receipt (clue to actual losses: medical expenses)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (8, 1, '<20260424-clinic@zhao-meng>', '[Backup] Medical Expenses After Drinking the Tea', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-24T21:00:00Z',
   'Note: On April 23, after drinking that wellness tea, I experienced heart palpitations and hand tremors. I went to the emergency department of the community hospital, and the registration, ECG, and examinations cost 320 yuan in total. I kept the receipt and medical records. The doctor said it appeared to have been caused by ingesting some kind of stimulant.',
   1, 0, '{}', 180, '2026-04-24T21:00:00Z');

-- Evidence of prior knowledge (saw negative reviews before placing the order — factual basis for the knowingly-buying-counterfeit-goods defense, but irrelevant in the food sector)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (9, 1, '<20260418-review@zhao-meng>', '[Backup] Negative Review Seen Before Ordering', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T19:00:00Z',
   'For the record: Before I ordered that imported infant formula, someone in the comments did indeed say, "The entire can has no Chinese label, so I can''t understand it." At the time, I thought it was cheap, and I bought it to try it out and to preserve evidence in case I needed to assert my rights. The seller later used this to claim that I "knowingly bought a fake." I kept the screenshot.',
   1, 0, '{}', 180, '2026-04-18T19:00:00Z');

-- =========================================================================
-- Sent (folder_id = 2)
-- =========================================================================
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (20, 2, '<20260428-sent-seller@zhao-meng>', 'Letter Regarding Refunds and Food Safety Compensation', 'zhao.meng@gmail.com', '["kefu@huanqiu-youxuan.com"]',
   '2026-04-28T09:00:00Z',
   'Huanqiu Youxuan: On 2026-04-18, I purchased imported infant formula and substitute tea from your store for a total of 1880 yuan. Upon receipt, I discovered that the imported infant formula had no Chinese label, while the substitute tea was suspected of containing illegal additives and making unlawful efficacy claims; both therefore failed to meet food safety standards. I now demand a refund of the purchase price and, pursuant to Article 148 of the Food Safety Law, compensation equal to ten times the purchase price. Please handle this within ten days of receiving this letter; otherwise, I will pursue my rights through litigation. — Zhao Meng',
   1, 0, '{}', 300, '2026-04-28T09:00:00Z');

-- =========================================================================
-- Order folder (folder_id = 7) — Seller/platform information + product page archive
-- =========================================================================
-- Seller and platform information (place of residence/place of delivery, for determining online-shopping jurisdiction + platform liability)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (30, 7, '<20260418-sellerinfo@zhao-meng>', 'Seller and platform information (for reference)', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T20:40:00Z',
   'For reference: Seller "Huanqiu Youxuan"; operator: Hangzhou Huanqiu Youxuan Food Co., Ltd.; address: Yuhang District, Hangzhou, Zhejiang Province. Sales platform: Youxiangu Mall (platform operator: Shanghai Youxiangu Network Technology Co., Ltd.). My delivery location: Pudong New District, Shanghai.',
   1, 0, '{}', 180, '2026-04-18T20:40:00Z');

-- Archived product page (unlawful efficacy claims for substitute tea + no health food approval number)
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (31, 7, '<20260418-page@zhao-meng>', '[Backup] Product Page Screenshot Description', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-04-18T21:00:00Z',
   'For the record: The product details page for that box of "health-preserving substitute tea" said it could "specifically treat high blood pressure, lower blood sugar, and completely cure insomnia," but it was merely an ordinary food product (the ingredient list said tea leaves and herbs) and had no health food approval number (and no "Blue Hat" mark). It is itself a violation for an ordinary food product to make claims about treating diseases. I kept all the screenshots.',
   1, 0, '{}', 200, '2026-04-18T21:00:00Z');



INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1000, 1, '<inbox-bg-001@mail.local>', 'Administrative System Reminder #001', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-03T09:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 181, '2026-01-03T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1001, 1, '<inbox-bg-002@mail.local>', 'Property Bill Reminder #002', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-04T10:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 182, '2026-01-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1002, 1, '<inbox-bg-003@mail.local>', 'Platform Promotional Update #003', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-05T11:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 183, '2026-01-05T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1003, 1, '<inbox-bg-004@mail.local>', 'Delivery arrival notification #004', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-06T12:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 184, '2026-01-06T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1004, 1, '<inbox-bg-005@mail.local>', 'Colleague Meeting Minutes #005', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-07T13:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   0, 0, '{}', 185, '2026-01-07T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1005, 1, '<inbox-bg-006@mail.local>', 'Health Examination Center Reminder #006', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-08T14:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 186, '2026-01-08T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1006, 1, '<inbox-bg-007@mail.local>', 'Bank statement reminder #007', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-09T15:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 187, '2026-01-09T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1007, 1, '<inbox-bg-008@mail.local>', 'Community event announcement #008', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-10T16:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 188, '2026-01-10T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1008, 1, '<inbox-bg-009@mail.local>', 'Administrative System Reminder #009', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-11T08:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 189, '2026-01-11T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1009, 1, '<inbox-bg-010@mail.local>', 'Property Bill Reminder #010', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-12T09:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 190, '2026-01-12T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1010, 1, '<inbox-bg-011@mail.local>', 'Platform Promotional Update #011', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-13T10:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 191, '2026-01-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1011, 1, '<inbox-bg-012@mail.local>', 'Express Delivery Arrival Notification #012', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-14T11:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 192, '2026-01-14T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1012, 1, '<inbox-bg-013@mail.local>', 'Colleague Meeting Minutes #013', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-15T12:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 193, '2026-01-15T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1013, 1, '<inbox-bg-014@mail.local>', 'Health Examination Center Reminder #014', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-16T13:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 194, '2026-01-16T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1014, 1, '<inbox-bg-015@mail.local>', 'Bank Reconciliation Reminder #015', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-17T14:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   0, 0, '{}', 195, '2026-01-17T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1015, 1, '<inbox-bg-016@mail.local>', 'Community event announcement #016', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-18T15:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 196, '2026-01-18T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1016, 1, '<inbox-bg-017@mail.local>', 'Administrative System Reminder #017', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-19T16:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 1, '{}', 197, '2026-01-19T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1017, 1, '<inbox-bg-018@mail.local>', 'Property Bill Reminder #018', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-20T08:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 198, '2026-01-20T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1018, 1, '<inbox-bg-019@mail.local>', 'Platform Promotional Update #019', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-21T09:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 199, '2026-01-21T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1019, 1, '<inbox-bg-020@mail.local>', 'Express Delivery Arrival Notification #020', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-22T10:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   0, 0, '{}', 200, '2026-01-22T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1020, 1, '<inbox-bg-021@mail.local>', 'Colleague Meeting Minutes #021', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-23T11:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 201, '2026-01-23T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1021, 1, '<inbox-bg-022@mail.local>', 'Health Examination Center Reminder #022', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-24T12:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 202, '2026-01-24T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1022, 1, '<inbox-bg-023@mail.local>', 'Bank Reconciliation Reminder #023', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-25T13:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 203, '2026-01-25T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1023, 1, '<inbox-bg-024@mail.local>', 'Community event announcement #024', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-26T14:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 204, '2026-01-26T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1024, 1, '<inbox-bg-025@mail.local>', 'Administrative System Reminder #025', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-27T15:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 205, '2026-01-27T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1025, 1, '<inbox-bg-026@mail.local>', 'Property Bill Reminder #026', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-28T16:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 206, '2026-01-28T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1026, 1, '<inbox-bg-027@mail.local>', 'Platform Promotional Update #027', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-29T08:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 207, '2026-01-29T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1027, 1, '<inbox-bg-028@mail.local>', 'Express Delivery Arrival Notification #028', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-30T09:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 208, '2026-01-30T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1028, 1, '<inbox-bg-029@mail.local>', 'Colleague Meeting Minutes #029', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-01-31T10:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 209, '2026-01-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1029, 1, '<inbox-bg-030@mail.local>', 'Health Examination Center Reminder #030', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-01T11:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   0, 0, '{}', 210, '2026-02-01T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1030, 1, '<inbox-bg-031@mail.local>', 'Bank Reconciliation Reminder #031', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-02T12:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 211, '2026-02-02T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1031, 1, '<inbox-bg-032@mail.local>', 'Community event announcement #032', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-03T13:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 212, '2026-02-03T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1032, 1, '<inbox-bg-033@mail.local>', 'Administrative System Reminder #033', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-04T14:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 213, '2026-02-04T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1033, 1, '<inbox-bg-034@mail.local>', 'Property Bill Reminder #034', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-05T15:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 1, '{}', 214, '2026-02-05T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1034, 1, '<inbox-bg-035@mail.local>', 'Platform Promotional Update #035', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-06T16:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 215, '2026-02-06T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1035, 1, '<inbox-bg-036@mail.local>', 'Express Delivery Arrival Notification #036', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-07T08:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 216, '2026-02-07T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1036, 1, '<inbox-bg-037@mail.local>', 'Colleague Meeting Minutes #037', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-08T09:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 217, '2026-02-08T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1037, 1, '<inbox-bg-038@mail.local>', 'Health Examination Center Reminder #038', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-09T10:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 218, '2026-02-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1038, 1, '<inbox-bg-039@mail.local>', 'Bank Reconciliation Reminder #039', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-10T11:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 219, '2026-02-10T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1039, 1, '<inbox-bg-040@mail.local>', 'Community event announcement #040', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-11T12:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   0, 0, '{}', 220, '2026-02-11T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1040, 1, '<inbox-bg-041@mail.local>', 'Administrative System Reminder #041', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-12T13:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 221, '2026-02-12T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1041, 1, '<inbox-bg-042@mail.local>', 'Property Bill Reminder #042', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-13T14:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 222, '2026-02-13T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1042, 1, '<inbox-bg-043@mail.local>', 'Platform Promotional Update #043', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-14T15:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 223, '2026-02-14T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1043, 1, '<inbox-bg-044@mail.local>', 'Express Delivery Arrival Notification #044', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-15T16:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 224, '2026-02-15T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1044, 1, '<inbox-bg-045@mail.local>', 'Colleague Meeting Minutes #045', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-16T08:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   0, 0, '{}', 225, '2026-02-16T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1045, 1, '<inbox-bg-046@mail.local>', 'Health Examination Center Reminder #046', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-17T09:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 226, '2026-02-17T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1046, 1, '<inbox-bg-047@mail.local>', 'Bank Reconciliation Reminder #047', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-18T10:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 227, '2026-02-18T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1047, 1, '<inbox-bg-048@mail.local>', 'Community Event Notice #048', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-19T11:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 228, '2026-02-19T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1048, 1, '<inbox-bg-049@mail.local>', 'Administrative System Reminder #049', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-20T12:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 229, '2026-02-20T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1049, 1, '<inbox-bg-050@mail.local>', 'Property Bill Reminder #050', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-21T13:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 230, '2026-02-21T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1050, 1, '<inbox-bg-051@mail.local>', 'Platform Promotional Update #051', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-22T14:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 1, '{}', 231, '2026-02-22T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1051, 1, '<inbox-bg-052@mail.local>', 'Express Delivery Arrival Notification #052', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-23T15:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 232, '2026-02-23T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1052, 1, '<inbox-bg-053@mail.local>', 'Colleague Meeting Minutes #053', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-24T16:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 233, '2026-02-24T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1053, 1, '<inbox-bg-054@mail.local>', 'Health Examination Center Reminder #054', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-25T08:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 234, '2026-02-25T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1054, 1, '<inbox-bg-055@mail.local>', 'Bank Reconciliation Reminder #055', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-26T09:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   0, 0, '{}', 235, '2026-02-26T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1055, 1, '<inbox-bg-056@mail.local>', 'Community Event Notice #056', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-27T10:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 236, '2026-02-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1056, 1, '<inbox-bg-057@mail.local>', 'Administrative System Reminder #057', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-02-28T11:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 237, '2026-02-28T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1057, 1, '<inbox-bg-058@mail.local>', 'Property Bill Reminder #058', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-01T12:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 238, '2026-03-01T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1058, 1, '<inbox-bg-059@mail.local>', 'Platform Promotional Update #059', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-02T13:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 239, '2026-03-02T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1059, 1, '<inbox-bg-060@mail.local>', 'Express Delivery Arrival Notification #060', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-03T14:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   0, 0, '{}', 240, '2026-03-03T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1060, 1, '<inbox-bg-061@mail.local>', 'Colleague Meeting Minutes #061', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-04T15:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 241, '2026-03-04T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1061, 1, '<inbox-bg-062@mail.local>', 'Health Examination Center Reminder #062', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-05T16:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 242, '2026-03-05T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1062, 1, '<inbox-bg-063@mail.local>', 'Bank Reconciliation Reminder #063', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-06T08:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 243, '2026-03-06T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1063, 1, '<inbox-bg-064@mail.local>', 'Community Event Notice #064', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-07T09:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 244, '2026-03-07T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1064, 1, '<inbox-bg-065@mail.local>', 'Administrative system reminder #065', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-08T10:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 245, '2026-03-08T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1065, 1, '<inbox-bg-066@mail.local>', 'Property Bill Reminder #066', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-09T11:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 246, '2026-03-09T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1066, 1, '<inbox-bg-067@mail.local>', 'Platform Promotional Update #067', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-10T12:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 247, '2026-03-10T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1067, 1, '<inbox-bg-068@mail.local>', 'Express Delivery Arrival Notification #068', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-11T13:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 1, '{}', 248, '2026-03-11T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1068, 1, '<inbox-bg-069@mail.local>', 'Colleague Meeting Minutes #069', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-12T14:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 249, '2026-03-12T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1069, 1, '<inbox-bg-070@mail.local>', 'Health Examination Center Reminder #070', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-13T15:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   0, 0, '{}', 180, '2026-03-13T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1070, 1, '<inbox-bg-071@mail.local>', 'Bank Reconciliation Reminder #071', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-14T16:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 181, '2026-03-14T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1071, 1, '<inbox-bg-072@mail.local>', 'Community Event Notice #072', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-15T08:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 182, '2026-03-15T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1072, 1, '<inbox-bg-073@mail.local>', 'Administrative system reminder #073', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-16T09:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 183, '2026-03-16T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1073, 1, '<inbox-bg-074@mail.local>', 'Property bill reminder #074', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-17T10:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 184, '2026-03-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1074, 1, '<inbox-bg-075@mail.local>', 'Platform Promotional Information #075', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-18T11:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 185, '2026-03-18T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1075, 1, '<inbox-bg-076@mail.local>', 'Express Delivery Arrival Notification #076', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-19T12:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 186, '2026-03-19T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1076, 1, '<inbox-bg-077@mail.local>', 'Colleague Meeting Minutes #077', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-20T13:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 187, '2026-03-20T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1077, 1, '<inbox-bg-078@mail.local>', 'Health Examination Center Reminder #078', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-21T14:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 188, '2026-03-21T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1078, 1, '<inbox-bg-079@mail.local>', 'Bank Reconciliation Reminder #079', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-22T15:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 189, '2026-03-22T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1079, 1, '<inbox-bg-080@mail.local>', 'Community Event Notice #080', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-23T16:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   0, 0, '{}', 190, '2026-03-23T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1080, 1, '<inbox-bg-081@mail.local>', 'Administrative system reminder #081', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-24T08:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 191, '2026-03-24T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1081, 1, '<inbox-bg-082@mail.local>', 'Property bill reminder #082', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-25T09:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 192, '2026-03-25T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1082, 1, '<inbox-bg-083@mail.local>', 'Platform Promotional Information #083', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-26T10:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 193, '2026-03-26T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1083, 1, '<inbox-bg-084@mail.local>', 'Express Delivery Arrival Notification #084', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-27T11:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 194, '2026-03-27T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1084, 1, '<inbox-bg-085@mail.local>', 'Colleague Meeting Minutes #085', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-28T12:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   0, 1, '{}', 195, '2026-03-28T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1085, 1, '<inbox-bg-086@mail.local>', 'Health Examination Center Reminder #086', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-29T13:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 196, '2026-03-29T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1086, 1, '<inbox-bg-087@mail.local>', 'Bank Reconciliation Reminder #087', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-30T14:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 197, '2026-03-30T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1087, 1, '<inbox-bg-088@mail.local>', 'Community Event Notice #088', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-03-31T15:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 198, '2026-03-31T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1088, 1, '<inbox-bg-089@mail.local>', 'Administrative system reminder #089', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-01T16:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 199, '2026-04-01T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1089, 1, '<inbox-bg-090@mail.local>', 'Property bill reminder #090', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-02T08:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 200, '2026-04-02T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1090, 1, '<inbox-bg-091@mail.local>', 'Platform Promotional Information #091', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-03T09:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 201, '2026-04-03T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1091, 1, '<inbox-bg-092@mail.local>', 'Express delivery arrival notification #092', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-04T10:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 202, '2026-04-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1092, 1, '<inbox-bg-093@mail.local>', 'Colleague Meeting Minutes #093', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-05T11:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 203, '2026-04-05T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1093, 1, '<inbox-bg-094@mail.local>', 'Health Examination Center Reminder #094', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-06T12:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 204, '2026-04-06T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1094, 1, '<inbox-bg-095@mail.local>', 'Bank Reconciliation Reminder #095', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-07T13:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   0, 0, '{}', 205, '2026-04-07T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1095, 1, '<inbox-bg-096@mail.local>', 'Community Event Notice #096', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-08T14:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 206, '2026-04-08T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1096, 1, '<inbox-bg-097@mail.local>', 'Administrative system reminder #097', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-09T15:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 207, '2026-04-09T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1097, 1, '<inbox-bg-098@mail.local>', 'Property bill reminder #098', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-10T16:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 208, '2026-04-10T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1098, 1, '<inbox-bg-099@mail.local>', 'Platform Promotional Information #099', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-11T08:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 209, '2026-04-11T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1099, 1, '<inbox-bg-100@mail.local>', 'Express delivery arrival notification #100', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-12T09:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   0, 0, '{}', 210, '2026-04-12T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1100, 1, '<inbox-bg-101@mail.local>', 'Colleague Meeting Minutes #101', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-13T10:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 211, '2026-04-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1101, 1, '<inbox-bg-102@mail.local>', 'Health Examination Center Reminder #102', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-14T11:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 1, '{}', 212, '2026-04-14T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1102, 1, '<inbox-bg-103@mail.local>', 'Bank Reconciliation Reminder #103', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-15T12:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 213, '2026-04-15T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1103, 1, '<inbox-bg-104@mail.local>', 'Community Event Notice #104', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-16T13:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 214, '2026-04-16T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1104, 1, '<inbox-bg-105@mail.local>', 'Administrative system reminder #105', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-17T14:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 215, '2026-04-17T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1105, 1, '<inbox-bg-106@mail.local>', 'Property bill reminder #106', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-18T15:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 216, '2026-04-18T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1106, 1, '<inbox-bg-107@mail.local>', 'Platform Promotional Information #107', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-19T16:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 217, '2026-04-19T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1107, 1, '<inbox-bg-108@mail.local>', 'Express delivery arrival notification #108', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-20T08:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 218, '2026-04-20T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1108, 1, '<inbox-bg-109@mail.local>', 'Colleague Meeting Minutes #109', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-21T09:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 219, '2026-04-21T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1109, 1, '<inbox-bg-110@mail.local>', 'Health Examination Center Reminder #110', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-22T10:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   0, 0, '{}', 220, '2026-04-22T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1110, 1, '<inbox-bg-111@mail.local>', 'Bank Reconciliation Reminder #111', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-23T11:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 221, '2026-04-23T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1111, 1, '<inbox-bg-112@mail.local>', 'Community Event Notice #112', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-24T12:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   1, 0, '{}', 222, '2026-04-24T12:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1112, 1, '<inbox-bg-113@mail.local>', 'Administrative system reminder #113', 'Administrative Service Desk <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-25T13:00:00Z', 'This week''s administrative matters are pending confirmation, including expense reimbursements, office supplies, and meeting room changes. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 223, '2026-04-25T13:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1113, 1, '<inbox-bg-114@mail.local>', 'Property bill reminder #114', 'Pudong Property Management Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-26T14:00:00Z', 'This month''s property management and parking fee bills have been issued. Please complete the reconciliation before the end of the month. Please check the relevant items by email subject and follow up as needed.',
   1, 0, '{}', 224, '2026-04-26T14:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1114, 1, '<inbox-bg-115@mail.local>', 'Platform Promotional Information #115', 'Youxiangu Shopping Mall <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-27T15:00:00Z', 'Routine platform promotions, including discounts on grains, cooking oils, snacks, cleaning supplies, and mother-and-baby products. Please check the relevant items by email subject and follow up as needed.',
   0, 0, '{}', 225, '2026-04-27T15:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1115, 1, '<inbox-bg-116@mail.local>', 'Express delivery arrival notification #116', 'Shunlian Express <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-28T16:00:00Z', 'Your package is about to be delivered. Please keep your phone available and watch for the delivery time. Please check the relevant details against the email subject and follow up if necessary.',
   1, 0, '{}', 226, '2026-04-28T16:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1116, 1, '<inbox-bg-117@mail.local>', 'Colleague Meeting Minutes #117', 'Administrative Department colleague <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-29T08:00:00Z', 'Attached are the minutes of the department''s regular meeting, covering the meeting room renovation, office supplies, and supplier arrangements. Please review the relevant matters against the email subject and follow up as needed.',
   1, 0, '{}', 227, '2026-04-29T08:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1117, 1, '<inbox-bg-118@mail.local>', 'Health Examination Center Reminder #118', 'Pudong Physical Examination Center <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-04-30T09:00:00Z', 'The annual physical examination appointment window is now open. Please confirm the time in the system. Check the relevant matters against the email subject line and follow up as needed.',
   1, 0, '{}', 228, '2026-04-30T09:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1118, 1, '<inbox-bg-119@mail.local>', 'Bank Reconciliation Reminder #119', 'Shanghai Pudong Development Bank <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-05-01T10:00:00Z', 'Your credit card statement is ready. Please review the transaction details for the most recent billing cycle. Please check the relevant details against the email subject and follow up if necessary.',
   1, 1, '{}', 229, '2026-05-01T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1119, 1, '<inbox-bg-120@mail.local>', 'Community Event Notice #120', 'Neighborhood Residents'' Committee <auto@mail.local>', '["zhao.meng@gmail.com"]',
   '2026-05-02T11:00:00Z', 'There will be a community activity and used-item collection event this weekend; everyone is welcome to participate as needed. Please check the relevant details against the email subject and follow up as needed.',
   0, 0, '{}', 230, '2026-05-02T11:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1120, 6, '<family-bg-001@family.local>', 'Shall we eat together this weekend?', 'Zhao''s Mother <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-04T19:00:00Z', 'Come home for dinner this weekend, and bring back some fruit while you''re at it. (Family 001)', 1, 0, '{}', 151, '2026-02-04T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1121, 6, '<family-bg-002@family.local>', 'Family Group Photos', 'Older female cousin <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-07T19:00:00Z', 'Sending you photos from the last gathering as a keepsake—when you have time, pick out a few to send to the family. (Family 002)', 1, 0, '{}', 152, '2026-02-07T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1122, 6, '<family-bg-003@family.local>', 'Dad''s medical examination report', 'Zhao''s Father <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-10T19:00:00Z', 'The medical checkup report is in the drawer. Remember to remind me when it’s time for my follow-up examination. (Family 003)', 1, 0, '{}', 153, '2026-02-10T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1123, 6, '<family-bg-004@family.local>', 'Ideas for summer vacation travel', 'Maternal Aunt <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-13T19:00:00Z', 'Everyone wants to find somewhere a little closer to unwind during the summer vacation. (Family 004)', 1, 0, '{}', 154, '2026-02-13T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1124, 6, '<family-bg-005@family.local>', 'Shall we eat together this weekend?', 'Zhao''s Mother <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-16T19:00:00Z', 'Come home for dinner this weekend, and bring back some fruit while you''re at it. (Family 005)', 1, 0, '{}', 155, '2026-02-16T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1125, 6, '<family-bg-006@family.local>', 'Family Group Photos', 'Older female cousin <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-19T19:00:00Z', 'Sending you photos from the last gathering as a keepsake—when you have time, pick out a few to send to the family. (Family 006)', 1, 0, '{}', 156, '2026-02-19T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1126, 6, '<family-bg-007@family.local>', 'Dad''s medical examination report', 'Zhao''s Father <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-22T19:00:00Z', 'The medical checkup report is in the drawer. Remember to remind me when it’s time for my follow-up examination. (Family 007)', 1, 0, '{}', 157, '2026-02-22T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1127, 6, '<family-bg-008@family.local>', 'Ideas for summer vacation travel', 'Maternal Aunt <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-25T19:00:00Z', 'Everyone wants to find somewhere a little closer to unwind during the summer vacation. (Family 008)', 1, 0, '{}', 158, '2026-02-25T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1128, 6, '<family-bg-009@family.local>', 'Shall we eat together this weekend?', 'Zhao''s Mother <family@local>', '["zhao.meng@gmail.com"]',
   '2026-02-28T19:00:00Z', 'Come home for dinner this weekend, and bring back some fruit while you''re at it. (Family 009)', 1, 0, '{}', 159, '2026-02-28T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1129, 6, '<family-bg-010@family.local>', 'Family Group Photos', 'Older female cousin <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-03T19:00:00Z', 'Sending you photos from the last gathering as a keepsake—when you have time, pick out a few to send to the family. (Family 010)', 1, 0, '{}', 160, '2026-03-03T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1130, 6, '<family-bg-011@family.local>', 'Dad''s medical examination report', 'Zhao''s Father <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-06T19:00:00Z', 'The medical checkup report is in the drawer. Remember to remind me when it’s time for my follow-up examination. (Family 011)', 1, 0, '{}', 161, '2026-03-06T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1131, 6, '<family-bg-012@family.local>', 'Ideas for summer vacation travel', 'Maternal Aunt <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-09T19:00:00Z', 'Everyone wants to find somewhere a little closer to unwind during the summer vacation. (Family 012)', 1, 0, '{}', 162, '2026-03-09T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1132, 6, '<family-bg-013@family.local>', 'Shall we eat together this weekend?', 'Zhao''s Mother <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-12T19:00:00Z', 'Come home for dinner this weekend, and bring back some fruit while you''re at it. (Family 013)', 1, 0, '{}', 163, '2026-03-12T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1133, 6, '<family-bg-014@family.local>', 'Family Group Photos', 'Older female cousin <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-15T19:00:00Z', 'Sending you photos from the last gathering as a keepsake—when you have time, pick out a few to send to the family. (Family 014)', 1, 0, '{}', 164, '2026-03-15T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1134, 6, '<family-bg-015@family.local>', 'Dad''s medical examination report', 'Zhao''s Father <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-18T19:00:00Z', 'The medical checkup report is in the drawer. Remember to remind me when it’s time for my follow-up examination. (Family 015)', 1, 0, '{}', 165, '2026-03-18T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1135, 6, '<family-bg-016@family.local>', 'Ideas for summer vacation travel', 'Maternal Aunt <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-21T19:00:00Z', 'Everyone wants to find somewhere a little closer to unwind during summer vacation. (Family 016)', 1, 0, '{}', 166, '2026-03-21T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1136, 6, '<family-bg-017@family.local>', 'Shall we eat together this weekend?', 'Zhao''s Mother <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-24T19:00:00Z', 'Go home for a meal this weekend, and bring back some fruit while you''re at it. (Family 017)', 1, 0, '{}', 167, '2026-03-24T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1137, 6, '<family-bg-018@family.local>', 'Family Group Photos', 'Older female cousin <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-27T19:00:00Z', 'Sending you photos from the last gathering as a keepsake—when you have time, pick out a few to send to the family. (Family 018)', 1, 0, '{}', 168, '2026-03-27T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1138, 6, '<family-bg-019@family.local>', 'Dad''s medical examination report', 'Zhao''s Father <family@local>', '["zhao.meng@gmail.com"]',
   '2026-03-30T19:00:00Z', 'The medical examination report is in the drawer; remember to remind me of the follow-up examination time. (Family 019)', 1, 0, '{}', 169, '2026-03-30T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1139, 6, '<family-bg-020@family.local>', 'Ideas for summer vacation travel', 'Maternal Aunt <family@local>', '["zhao.meng@gmail.com"]',
   '2026-04-02T19:00:00Z', 'Everyone wants to find somewhere a little closer to unwind during summer vacation. (Family 020)', 1, 0, '{}', 170, '2026-04-02T19:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1140, 7, '<order-bg-001@orders.local>', '[Order] Daily necessities shipped #001', 'Lifestyle Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-07T10:00:00Z', 'The household items you purchased, such as tissues and laundry detergent, have been shipped. (Order 001)', 1, 0, '{}', 171, '2026-01-07T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1141, 7, '<order-bg-002@orders.local>', '[Order] Office Supplies Confirmation #002', 'Office Bulk Purchasing <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-09T10:00:00Z', 'The ordered folders, label paper, and notebooks have been confirmed. (Order 002)', 1, 0, '{}', 172, '2026-01-09T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1142, 7, '<order-bg-003@orders.local>', '[After-sales] Refund progress reminder #003', 'Mall After-Sales <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-11T10:00:00Z', 'Your after-sales request is being processed. Please watch for further notifications. (Order 003)', 1, 0, '{}', 173, '2026-01-11T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1143, 7, '<order-bg-004@orders.local>', '[Order] Milk and cereal delivery #004', 'Community Home Delivery <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-13T10:00:00Z', 'Breakfast supplies will be delivered tonight; please watch for them. (Order 004)', 1, 0, '{}', 174, '2026-01-13T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1144, 7, '<order-bg-005@orders.local>', '[Order] Small Household Appliances Order Placed Successfully #005', 'Appliance Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-15T10:00:00Z', 'Small appliance order confirmed; estimated delivery within two days. (Order 005)', 1, 0, '{}', 175, '2026-01-15T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1145, 7, '<order-bg-006@orders.local>', '[Order] Daily necessities shipped #006', 'Lifestyle Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-17T10:00:00Z', 'The household items you purchased, such as tissues and laundry detergent, have been shipped. (Order 006)', 1, 0, '{}', 176, '2026-01-17T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1146, 7, '<order-bg-007@orders.local>', '[Order] Office Supplies Confirmation #007', 'Office Bulk Purchasing <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-19T10:00:00Z', 'The ordered folders, label paper, and notebooks have been confirmed. (Order 007)', 1, 0, '{}', 177, '2026-01-19T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1147, 7, '<order-bg-008@orders.local>', '[After-sales] Refund progress reminder #008', 'Mall After-Sales <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-21T10:00:00Z', 'Your after-sales request is being processed. Please watch for further notifications. (Order 008)', 1, 0, '{}', 178, '2026-01-21T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1148, 7, '<order-bg-009@orders.local>', '[Order] Milk and cereal delivery #009', 'Community Home Delivery <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-23T10:00:00Z', 'Breakfast supplies will be delivered tonight; please watch for them. (Order 009)', 1, 0, '{}', 179, '2026-01-23T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1149, 7, '<order-bg-010@orders.local>', '[Order] Small Household Appliances Order Placed Successfully #010', 'Appliance Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-25T10:00:00Z', 'Small appliance order confirmed; estimated delivery within two days. (Order 010)', 1, 0, '{}', 180, '2026-01-25T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1150, 7, '<order-bg-011@orders.local>', '[Order] Daily necessities shipped #011', 'Lifestyle Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-27T10:00:00Z', 'The household items you purchased, such as tissues and laundry detergent, have been shipped. (Order 011)', 1, 0, '{}', 181, '2026-01-27T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1151, 7, '<order-bg-012@orders.local>', '[Order] Office Supplies Confirmation #012', 'Office Bulk Purchasing <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-29T10:00:00Z', 'The ordered folders, label paper, and notebooks have been confirmed. (Order 012)', 1, 0, '{}', 182, '2026-01-29T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1152, 7, '<order-bg-013@orders.local>', '[After-sales] Refund progress reminder #013', 'Mall After-Sales <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-01-31T10:00:00Z', 'Your after-sales request is being processed. Please watch for further notifications. (Order 013)', 1, 1, '{}', 183, '2026-01-31T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1153, 7, '<order-bg-014@orders.local>', '[Order] Milk and cereal delivery #014', 'Community Home Delivery <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-02T10:00:00Z', 'Breakfast supplies will be delivered tonight; please watch for them. (Order 014)', 1, 0, '{}', 184, '2026-02-02T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1154, 7, '<order-bg-015@orders.local>', '[Order] Small Household Appliances Order Placed Successfully #015', 'Appliance Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-04T10:00:00Z', 'Small appliance order confirmed; estimated delivery within two days. (Order 015)', 1, 0, '{}', 185, '2026-02-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1155, 7, '<order-bg-016@orders.local>', '[Order] Daily necessities shipped #016', 'Lifestyle Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-06T10:00:00Z', 'The household items you purchased, such as tissues and laundry detergent, have been shipped. (Order 016)', 1, 0, '{}', 186, '2026-02-06T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1156, 7, '<order-bg-017@orders.local>', '[Order] Office Supplies Confirmation #017', 'Office Bulk Purchasing <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-08T10:00:00Z', 'The ordered folders, label paper, and notebooks have been confirmed. (Order 017)', 1, 0, '{}', 187, '2026-02-08T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1157, 7, '<order-bg-018@orders.local>', '[After-sales] Refund progress reminder #018', 'Mall After-Sales <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-10T10:00:00Z', 'Your after-sales request is being processed. Please watch for further notifications. (Order 018)', 1, 0, '{}', 188, '2026-02-10T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1158, 7, '<order-bg-019@orders.local>', '[Order] Milk and Cereal Delivery #019', 'Community Home Delivery <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-12T10:00:00Z', 'The breakfast supplies will be delivered tonight. Please watch for them. (Order 019)', 1, 0, '{}', 189, '2026-02-12T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1159, 7, '<order-bg-020@orders.local>', '[Order] Small Household Appliances Order Placed Successfully #020', 'Appliance Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-14T10:00:00Z', 'Small appliance order confirmed; estimated delivery within two days. (Order 020)', 1, 0, '{}', 190, '2026-02-14T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1160, 7, '<order-bg-021@orders.local>', '[Order] Daily necessities shipped #021', 'Lifestyle Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-16T10:00:00Z', 'The household items you purchased, such as tissues and laundry detergent, have been shipped. (Order 021)', 1, 0, '{}', 191, '2026-02-16T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1161, 7, '<order-bg-022@orders.local>', '[Order] Office Supplies Confirmation #022', 'Office Bulk Purchasing <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-18T10:00:00Z', 'The ordered folders, label paper, and notebooks have been confirmed. (Order 022)', 1, 0, '{}', 192, '2026-02-18T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1162, 7, '<order-bg-023@orders.local>', '[After-Sales] Refund Progress Reminder #023', 'Mall After-Sales <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-20T10:00:00Z', 'Your after-sales request is being processed. Please watch for further notifications. (Order 023)', 1, 0, '{}', 193, '2026-02-20T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1163, 7, '<order-bg-024@orders.local>', '[Order] Milk and Cereal Delivery #024', 'Community Home Delivery <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-22T10:00:00Z', 'The breakfast supplies will be delivered tonight. Please watch for them. (Order 024)', 1, 0, '{}', 194, '2026-02-22T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1164, 7, '<order-bg-025@orders.local>', '[Order] Small Household Appliances Order Placed Successfully #025', 'Appliance Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-24T10:00:00Z', 'Small appliance order confirmed; estimated delivery within two days. (Order 025)', 1, 0, '{}', 195, '2026-02-24T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1165, 7, '<order-bg-026@orders.local>', '[Order] Daily necessities shipped #026', 'Lifestyle Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-26T10:00:00Z', 'The tissues, laundry detergent, and other daily necessities you purchased have been shipped. (Order 026)', 1, 1, '{}', 196, '2026-02-26T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1166, 7, '<order-bg-027@orders.local>', '[Order] Office Supplies Confirmation #027', 'Office Bulk Purchasing <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-02-28T10:00:00Z', 'The ordered folders, label paper, and notebooks have been confirmed. (Order 027)', 1, 0, '{}', 197, '2026-02-28T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1167, 7, '<order-bg-028@orders.local>', '[After-Sales] Refund Progress Reminder #028', 'Mall After-Sales <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-03-02T10:00:00Z', 'Your after-sales request is being processed. Please watch for further notifications. (Order 028)', 1, 0, '{}', 198, '2026-03-02T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1168, 7, '<order-bg-029@orders.local>', '[Order] Milk and Cereal Delivery #029', 'Community Home Delivery <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-03-04T10:00:00Z', 'The breakfast supplies will be delivered tonight. Please watch for them. (Order 029)', 1, 0, '{}', 199, '2026-03-04T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1169, 7, '<order-bg-030@orders.local>', '[Order] Small household appliances order placed successfully #030', 'Appliance Store <order@mall.local>', '["zhao.meng@gmail.com"]',
   '2026-03-06T10:00:00Z', 'Small appliance order confirmed; estimated delivery within two days. (Order 030)', 1, 0, '{}', 200, '2026-03-06T10:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1170, 2, '<sent-bg-001@zhao-meng>', 'Meeting Confirmation #001', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-03-05T09:30:00Z', 'Received. Please proceed with this version for now; I’ll add more this afternoon. (Sent 001)', 1, 0, '{}', 141, '2026-03-05T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1171, 2, '<sent-bg-002@zhao-meng>', 'Data Upload #002', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-03-09T09:30:00Z', 'The attachment has been received; I will review everything together later. (Sent 002)', 1, 0, '{}', 142, '2026-03-09T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1172, 2, '<sent-bg-003@zhao-meng>', 'Family Reply #003', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-03-13T09:30:00Z', 'I''ll go back this weekend and bring you some medicine while I''m at it. (Sent 003)', 1, 0, '{}', 143, '2026-03-13T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1173, 2, '<sent-bg-004@zhao-meng>', 'Meeting Confirmation #004', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-03-17T09:30:00Z', 'Received. Please proceed with this version for now; I’ll add more this afternoon. (Sent 004)', 1, 0, '{}', 144, '2026-03-17T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1174, 2, '<sent-bg-005@zhao-meng>', 'Data Upload #005', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-03-21T09:30:00Z', 'The attachment has been received; I will review everything together later. (Sent 005)', 1, 0, '{}', 145, '2026-03-21T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1175, 2, '<sent-bg-006@zhao-meng>', 'Family Reply #006', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-03-25T09:30:00Z', 'I''ll go back this weekend and bring you some medicine while I''m at it. (Sent 006)', 1, 0, '{}', 146, '2026-03-25T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1176, 2, '<sent-bg-007@zhao-meng>', 'Meeting Confirmation #007', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-03-29T09:30:00Z', 'Received. Please proceed with this version for now; I’ll add more this afternoon. (Sent 007)', 1, 0, '{}', 147, '2026-03-29T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1177, 2, '<sent-bg-008@zhao-meng>', 'Data Upload #008', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-04-02T09:30:00Z', 'The attachment has been received; I will review everything together later. (Sent 008)', 1, 0, '{}', 148, '2026-04-02T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1178, 2, '<sent-bg-009@zhao-meng>', 'Family Reply #009', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-04-06T09:30:00Z', 'I''ll go back this weekend and bring you some medicine while I''m at it. (Sent 009)', 1, 0, '{}', 149, '2026-04-06T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1179, 2, '<sent-bg-010@zhao-meng>', 'Meeting Confirmation #010', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-04-10T09:30:00Z', 'Received. Please proceed with this version for now; I’ll add more this afternoon. (Sent 010)', 1, 0, '{}', 150, '2026-04-10T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1180, 2, '<sent-bg-011@zhao-meng>', 'Data Upload #011', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-04-14T09:30:00Z', 'Attachments received; I’ll review them all together later. (Sent 011)', 1, 0, '{}', 151, '2026-04-14T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1181, 2, '<sent-bg-012@zhao-meng>', 'Family Reply #012', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-04-18T09:30:00Z', 'I''ll go back this weekend and bring you some medicine while I''m at it. (Sent 012)', 1, 0, '{}', 152, '2026-04-18T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1182, 2, '<sent-bg-013@zhao-meng>', 'Meeting Confirmation #013', 'zhao.meng@gmail.com', '["ops@example.com"]',
   '2026-04-22T09:30:00Z', 'Received. Please proceed with this version for now; I’ll add more this afternoon. (Sent 013)', 1, 0, '{}', 153, '2026-04-22T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1183, 2, '<sent-bg-014@zhao-meng>', 'Data Upload #014', 'zhao.meng@gmail.com', '["vendor@example.com"]',
   '2026-04-26T09:30:00Z', 'Attachments received; I’ll review them all together later. (Sent 014)', 1, 0, '{}', 154, '2026-04-26T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1184, 2, '<sent-bg-015@zhao-meng>', 'Family Reply #015', 'zhao.meng@gmail.com', '["mom@local"]',
   '2026-04-30T09:30:00Z', 'I''ll go back this weekend and bring you some medicine while I''m at it. (Sent 015)', 1, 0, '{}', 155, '2026-04-30T09:30:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1185, 3, '<draft-bg-001@zhao-meng>', 'Draft: Pending Item 1', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-02T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-02T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1186, 3, '<draft-bg-002@zhao-meng>', 'Draft: Pending Item 2', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-03T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-03T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1187, 3, '<draft-bg-003@zhao-meng>', 'Draft: Pending Item 3', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-04T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-04T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1188, 3, '<draft-bg-004@zhao-meng>', 'Draft: Pending Item 4', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-05T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-05T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1189, 3, '<draft-bg-005@zhao-meng>', 'Draft: Pending Item 5', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-06T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-06T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1190, 3, '<draft-bg-006@zhao-meng>', 'Draft: Pending Item 6', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-07T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-07T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1191, 3, '<draft-bg-007@zhao-meng>', 'Draft: Pending Item 7', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-08T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-08T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1192, 3, '<draft-bg-008@zhao-meng>', 'Draft: Pending Item 8', 'zhao.meng@gmail.com', '["zhao.meng@gmail.com"]',
   '2026-05-09T22:00:00Z', 'This is an unsent personal draft intended to create a realistic email structure.', 0, 0, '{}', 120, '2026-05-09T22:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1193, 5, '<spam-bg-001@spam.local>', 'Limited-time offer/Unusual login alert 1', 'Unknown sender <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-02-26T06:00:00Z', 'A typical spam sample, used to enrich email noise.', 0, 0, '{}', 110, '2026-02-26T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1194, 5, '<spam-bg-002@spam.local>', 'Limited-time offer/Unusual login alert 2', 'Unknown sender <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-03-09T06:00:00Z', 'A typical spam sample, used to enrich email noise.', 0, 0, '{}', 110, '2026-03-09T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1195, 5, '<spam-bg-003@spam.local>', 'Limited-time offer/Unusual login alert 3', 'Unknown sender <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-03-20T06:00:00Z', 'A typical spam sample, used to enrich email noise.', 0, 0, '{}', 110, '2026-03-20T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1196, 5, '<spam-bg-004@spam.local>', 'Limited-time offer/Unusual login alert 4', 'Unknown sender <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-03-31T06:00:00Z', 'A typical spam sample, used to enrich email noise.', 0, 0, '{}', 110, '2026-03-31T06:00:00Z');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1197, 5, '<spam-bg-005@spam.local>', 'Limited-time offer/Unusual login alert 5', 'Unknown sender <spam@spam.local>', '["zhao.meng@gmail.com"]',
   '2026-04-11T06:00:00Z', 'A typical spam sample, used to enrich email noise.', 0, 0, '{}', 110, '2026-04-11T06:00:00Z');

-- Refresh denormalised folder counts.

UPDATE folders SET
  message_count = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id),
  unread_count  = (SELECT COUNT(*) FROM messages WHERE messages.folder_id = folders.id AND messages.is_read = 0);

INSERT INTO _counters (key, value) VALUES
  ('msg_seq', 500);

COMMIT;
