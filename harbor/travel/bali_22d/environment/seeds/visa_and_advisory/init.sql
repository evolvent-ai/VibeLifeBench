BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS entry_requirements (
    origin_nationality TEXT,
    destination TEXT,
    purpose TEXT,
    visa_required INTEGER,
    allowed_stay_days INTEGER,
    passport_validity_months INTEGER DEFAULT 6,
    docs_needed_json TEXT DEFAULT '[]',
    notes TEXT DEFAULT '',
    updated_at TEXT,
    PRIMARY KEY (origin_nationality, destination, purpose)
);

CREATE TABLE IF NOT EXISTS visa_products (
    product_id TEXT PRIMARY KEY,
    destination TEXT,
    nationality TEXT,
    name TEXT,
    processing_time_days INTEGER,
    fee_amount INTEGER,
    fee_currency TEXT,
    delivery TEXT,
    form_schema_json TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS advisories (
    country_code TEXT PRIMARY KEY,
    level INTEGER,
    text TEXT,
    updated_at TEXT
);

INSERT INTO entry_requirements (origin_nationality, destination, purpose, visa_required, allowed_stay_days, passport_validity_months, docs_needed_json, notes, updated_at) VALUES
('CN', 'ID', 'tourism', 1, 30, 6, '["passport","return_ticket","hotel_booking","sufficient_funds"]', 'Visa on Arrival (VOA) available at airport. IDR 500,000. Passport must have >=6 months validity from entry date.', '2026-05-01T00:00:00Z'),
('CN', 'ID', 'business', 1, 30, 6, '["passport","invitation_letter","company_letter","return_ticket"]', 'Business VOA or e-Visa. Processing 3-5 days for e-Visa.', '2026-05-01T00:00:00Z'),
('CN', 'ID', 'transit', 0, 1, 6, '["passport","onward_ticket"]', 'Transit without visa for <24h if not leaving airport.', '2026-05-01T00:00:00Z');

INSERT INTO visa_products (product_id, destination, nationality, name, processing_time_days, fee_amount, fee_currency, delivery, form_schema_json) VALUES
('vp_id_voa_cn', 'ID', 'CN', 'Indonesia Visa on Arrival (VOA) - 30 days', 0, 500000, 'IDR', 'on_arrival', '{"required_docs": ["passport_bio_page","return_ticket","accommodation_proof"]}'),
('vp_id_evisa_cn_tourist', 'ID', 'CN', 'Indonesia e-Visa B1 (Tourism) - 60 days', 5, 1500000, 'IDR', 'electronic', '{"required_docs": ["passport_bio_page","photo_4x6","return_ticket","bank_statement","hotel_booking"]}'),
('vp_id_evisa_cn_business', 'ID', 'CN', 'Indonesia e-Visa B2 (Business) - 60 days', 5, 2000000, 'IDR', 'electronic', '{"required_docs": ["passport_bio_page","photo_4x6","invitation_letter","company_letter"]}');

INSERT INTO advisories (country_code, level, text, updated_at) VALUES
('ID', 1, 'Indonesia: exercise normal travel precautions. Routine mosquito-bite prevention is recommended in tropical regions. Mount Agung (Bali) is at Level 1 (Normal).', '2026-05-20T00:00:00Z'),
('CN', 1, 'China: Normal precautions. No specific travel advisory.', '2026-05-01T00:00:00Z'),
('SG', 1, 'Singapore: Normal precautions. Transit hub.', '2026-05-01T00:00:00Z');


-- Closed historical applications for unrelated users provide normal account history.
INSERT INTO visa_applications (
  application_id, user_id, product_id, status, applicant_json, answers_json,
  decision_day, decision_note, evisa_doc_ref, history_json, created_at, updated_at
) VALUES
('VA-ID-240603-3P4F57C', 'usr_ayu_pratama', 'vp_id_evisa_cn_tourist', 'approved',
 '{"full_name":"Ayu Pratama","passport_country":"CN","passport_last4":"4821"}',
 '{"arrival_month":"2024-08","lodging_city":"Jakarta","sponsor":"self"}',
 4, 'Issued after accommodation proof was added.', 'EVI-RNXEGAJMMT7GC',
 '[{"at":"2024-06-03T09:20:00Z","status":"submitted"},{"at":"2024-06-07T07:45:00Z","status":"approved"}]',
 '2024-06-03T09:20:00Z', '2024-06-07T07:45:00Z'),
('VA-ID-240912-MS5SL2X', 'usr_zhou_nan', 'vp_id_evisa_cn_business', 'withdrawn',
 '{"full_name":"Zhou Nan","passport_country":"CN","passport_last4":"1906"}',
 '{"host_company":"Nusantara Design PT","meeting_city":"Surabaya"}',
 NULL, 'Applicant cancelled the meeting before adjudication.', NULL,
 '[{"at":"2024-09-12T02:10:00Z","status":"draft"},{"at":"2024-09-15T10:30:00Z","status":"withdrawn"}]',
 '2024-09-12T02:10:00Z', '2024-09-15T10:30:00Z'),
('VA-ID-250108-J56SXIQ', 'usr_song_yan', 'vp_id_evisa_cn_tourist', 'rejected',
 '{"full_name":"Song Yan","passport_country":"CN","passport_last4":"7330"}',
 '{"arrival_month":"2025-02","lodging_city":"Yogyakarta","sponsor":"self"}',
 7, 'Bank statement pages were incomplete at the decision cutoff.', NULL,
 '[{"at":"2025-01-08T05:40:00Z","status":"submitted"},{"at":"2025-01-15T08:05:00Z","status":"rejected"}]',
 '2025-01-08T05:40:00Z', '2025-01-15T08:05:00Z'),
('VA-ID-250421-VOJK64P', 'usr_he_jun', 'vp_id_evisa_cn_business', 'approved',
 '{"full_name":"He Jun","passport_country":"CN","passport_last4":"2518"}',
 '{"host_company":"Bumi Robotics","meeting_city":"Bandung"}',
 5, 'Invitation and employer letters matched the declared visit.', 'EVI-HP4DKKNWDA5CC',
 '[{"at":"2025-04-21T06:15:00Z","status":"submitted"},{"at":"2025-04-26T03:30:00Z","status":"approved"}]',
 '2025-04-21T06:15:00Z', '2025-04-26T03:30:00Z'),
('VA-ID-250830-5PTQ66Q', 'usr_tang_ning', 'vp_id_evisa_cn_tourist', 'withdrawn',
 '{"full_name":"Tang Ning","passport_country":"CN","passport_last4":"6042"}',
 '{"arrival_month":"2025-11","lodging_city":"Medan","sponsor":"relative"}',
 NULL, 'Travel dates moved beyond the product window.', NULL,
 '[{"at":"2025-08-30T11:00:00Z","status":"draft"},{"at":"2025-09-02T04:25:00Z","status":"withdrawn"}]',
 '2025-08-30T11:00:00Z', '2025-09-02T04:25:00Z');

INSERT INTO application_documents (doc_id, application_id, kind, ref, uploaded_at) VALUES
('doc_ayu_passport', 'VA-ID-240603-3P4F57C', 'passport_bio_page', 'vault://casefiles/ayu/passport-redacted.pdf', '2024-06-03T09:25:00Z'),
('doc_ayu_lodging', 'VA-ID-240603-3P4F57C', 'accommodation_proof', 'vault://casefiles/ayu/jakarta-stay.pdf', '2024-06-06T01:10:00Z'),
('doc_zhou_invite', 'VA-ID-240912-MS5SL2X', 'invitation_letter', 'vault://casefiles/zhou/host-letter.pdf', '2024-09-12T02:18:00Z'),
('doc_song_bank', 'VA-ID-250108-J56SXIQ', 'bank_statement', 'vault://casefiles/song/bank-partial.pdf', '2025-01-08T05:52:00Z'),
('doc_he_invite', 'VA-ID-250421-VOJK64P', 'invitation_letter', 'vault://casefiles/he/bumi-invite.pdf', '2025-04-21T06:22:00Z'),
('doc_he_company', 'VA-ID-250421-VOJK64P', 'company_letter', 'vault://casefiles/he/employer-letter.pdf', '2025-04-22T03:00:00Z'),
('doc_tang_photo', 'VA-ID-250830-5PTQ66Q', 'photo_4x6', 'vault://casefiles/tang/photo.jpg', '2025-08-30T11:08:00Z');

INSERT INTO advisory_subscriptions (sub_id, country_code, sink, created_at) VALUES
('SUB-ID-240310-XTMSQW', 'ID', 'email:archive.reader@example.com', '2024-03-10T02:20:00Z'),
('SUB-SG-241102-FFUOYZ', 'SG', 'push:device-9c21', '2024-11-02T15:35:00Z'),
('SUB-CN-250218-CJJQWL', 'CN', 'email:zhou.nan@example.com', '2025-02-18T08:10:00Z'),
('SUB-ID-251204-N5ZCNP', 'ID', 'push:device-1aa7', '2025-12-04T05:45:00Z');

INSERT INTO notifications (id, created_at, channel, payload_json) VALUES
('NTF-ID-250617-PTRJZT', '2025-06-17T01:20:00Z', 'email', '{"country_code":"ID","topic":"regional_health_notice","delivery":"sent"}'),
('NTF-SG-251211-WJXMIU', '2025-12-11T09:40:00Z', 'push', '{"country_code":"SG","topic":"airport_service_update","delivery":"opened"}');

COMMIT;
