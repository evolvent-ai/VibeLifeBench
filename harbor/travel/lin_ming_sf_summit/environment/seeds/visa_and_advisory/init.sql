BEGIN TRANSACTION;
INSERT INTO entry_requirements VALUES ('CN', 'US', 'business', 1, 180, 0, '["passport", "B1/B2_visa", "EVUS_if_10_year_visitor_visa"]', 'Temporary business travel uses the B-1 or combined B1/B2 visitor-visa framework. PRC nationals traveling on a 10-year B1/B2 visa must have a current EVUS enrollment. The passport must remain valid for the actual trip; because this synthetic passport expires soon after return, obtain carrier/CBP confirmation rather than assuming EVUS replaces either document.', '2026-03-14T18:00:00+08:00');
INSERT INTO visa_products VALUES ('US_B1B2_CN', 'US', 'CN', 'US B1/B2 Visitor Visa', 5, 185, 'USD', 'stamp', '{"fields": ["passport_number", "passport_expiry", "purpose"]}');
INSERT INTO advisories VALUES ('US', 1, 'A valid visa permits travel to a U.S. port of entry but does not guarantee admission; preserve the separate passport, visa and EVUS readiness checks.', '2026-03-14T18:00:00+08:00');

CREATE TABLE IF NOT EXISTS passports (
    passport_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL,
    nationality TEXT,
    passport_number TEXT,
    issue_date TEXT,
    expiry_date TEXT,
    status TEXT,
    notes TEXT
);
INSERT OR IGNORE INTO passports VALUES (
    'PP001', 'liming@company.com', 'CN', 'E12345678', '2016-05-30', '2026-05-30', 'active',
    'Passport expires 2026-05-30.'
);

CREATE TABLE IF NOT EXISTS visas (
    visa_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL,
    country TEXT,
    visa_type TEXT,
    issue_date TEXT,
    expiry_date TEXT,
    entries TEXT,
    status TEXT
);
INSERT OR IGNORE INTO visas VALUES (
    'VS001', 'liming@company.com', 'US', 'B1/B2', '2021-06-15', '2031-06-14', 'multiple', 'active'
);

CREATE TABLE IF NOT EXISTS evus (
    evus_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL,
    enrollment_number TEXT,
    status TEXT,
    expiry_date TEXT,
    last_updated TEXT
);
INSERT OR IGNORE INTO evus VALUES (
    'EV001', 'liming@company.com', 'EN1234567890', 'active', '2026-03-25', '2024-03-25'
);

-- EVUS renewal is intentionally left in a pre-action draft state at Stage 0.
-- The source object is visible and queryable, but no future approval is pre-seeded;
-- a valid renewal must be created or completed through the formal tool path.
INSERT OR REPLACE INTO visa_applications
  (application_id,user_id,product_id,status,applicant_json,answers_json,decision_day,decision_note,evisa_doc_ref,history_json,created_at,updated_at) VALUES
  ('APP_EVUS_LIMING','liming@company.com','US_B1B2_CN','draft',
   '{"name":"Li Ming","email":"liming@company.com","passport_number":"E12345678"}',
   '{"kind":"EVUS_renewal","prior_enrollment_number":"EN1234567890","prior_expiry":"2026-03-25","evus_status":"needs_renewal"}',
   NULL,'Renewal not yet submitted; current enrollment expires before the planned outbound flight',NULL,
   '[{"day":0,"event":"draft_created","note":"Travel assistant must verify and complete EVUS before departure"}]',
   '2026-03-15T09:00:00','2026-03-15T09:00:00');
INSERT OR REPLACE INTO application_documents (doc_id,application_id,kind,ref,uploaded_at) VALUES
  ('DOC_EVUS_LIMING','APP_EVUS_LIMING','HISTORICAL_EVUS','EVUS-EN1234567890-expires-2026-03-25','2026-03-15T09:00:00');

INSERT INTO _counters VALUES ('application', 1), ('document', 4), ('subscription', 0), ('notification', 0);
COMMIT;
