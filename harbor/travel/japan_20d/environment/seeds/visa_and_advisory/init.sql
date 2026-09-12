-- visa_products catalog seed.
-- form_schema_json is the full §3.3 structure: {fields: [...], required_docs: [...]}.
-- Fee is stored in MAJOR units in the currency listed (e.g. 230 CNY, 185 USD, 127 GBP, 80 EUR).

BEGIN TRANSACTION;

-- ---------- JAPAN ----------

INSERT OR REPLACE INTO visa_products VALUES
('vp_jp_tourist_single_cn','JP','CN',
 'Japan Single-Entry Tourist Visa (CN nationals)',
 5, 230, 'CNY', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"emergency_contact","type":"string","required":false}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_jp_tourist_multi_3y_cn','JP','CN',
 'Japan Multi-Entry Tourist Visa 3-Year (CN nationals)',
 7, 440, 'CNY', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"prior_jp_entries","type":"string","required":false},{"name":"emergency_contact","type":"string","required":false}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_jp_evisa_tourist_cn','JP','CN',
 'Japan eVisa Tourist (CN residents via accredited agency)',
 5, 240, 'CNY', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"emergency_contact","type":"string","required":true}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_jp_transit_cn','JP','CN',
 'Japan Transit Visa (CN nationals)',
 3, 140, 'CNY', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"onward_destination","type":"string","required":true},{"name":"onward_flight_no","type":"string","required":true},{"name":"photo_ref","type":"string","required":true}],"required_docs":["passport","itinerary"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_jp_business_single_cn','JP','CN',
 'Japan Single-Entry Business Visa (CN nationals)',
 5, 230, 'CNY', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"host_company_jp","type":"string","required":true},{"name":"invitation_letter_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"emergency_contact","type":"string","required":false}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_jp_business_multi_cn','JP','CN',
 'Japan Multi-Entry Business Visa (CN nationals)',
 7, 440, 'CNY', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"host_company_jp","type":"string","required":true},{"name":"invitation_letter_ref","type":"string","required":true},{"name":"prior_jp_entries","type":"string","required":false},{"name":"photo_ref","type":"string","required":true}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

-- ---------- UNITED STATES ----------

INSERT OR REPLACE INTO visa_products VALUES
('vp_us_b1b2_cn','US','CN',
 'US B1/B2 Visitor Visa 10-Year (CN nationals)',
 30, 185, 'USD', 'embassy',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"ds160_confirmation","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"interview_location","type":"string","required":true}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_us_esta','US','*',
 'US ESTA (VWP travel authorisation)',
 1, 21, 'USD', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"emergency_contact","type":"string","required":true}],"required_docs":["passport"]}');

-- ---------- UNITED KINGDOM ----------

INSERT OR REPLACE INTO visa_products VALUES
('vp_uk_standard_visitor_cn','GB','CN',
 'UK Standard Visitor Visa 6-Month (CN nationals)',
 15, 127, 'GBP', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"tb_certificate_ref","type":"string","required":true}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_uk_eta','GB','*',
 'UK Electronic Travel Authorisation (ETA)',
 1, 16, 'GBP', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"emergency_contact","type":"string","required":false}],"required_docs":["passport","photo"]}');

-- ---------- SCHENGEN / EU ----------

INSERT OR REPLACE INTO visa_products VALUES
('vp_schengen_short_stay_cn','DE','CN',
 'Schengen Short-Stay C Visa (CN nationals - via Germany consulate)',
 15, 80, 'EUR', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"purpose","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"insurance_cert_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true},{"name":"emergency_contact","type":"string","required":false}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_etias','DE','*',
 'ETIAS Schengen Travel Authorisation',
 1, 7, 'EUR', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"first_schengen_entry","type":"string","required":true}],"required_docs":["passport"]}');

-- ---------- ASIA OTHER ----------

INSERT OR REPLACE INTO visa_products VALUES
('vp_kr_keta','KR','*',
 'K-ETA (Korea Electronic Travel Authorisation)',
 1, 10000, 'KRW', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"accommodation","type":"string","required":true},{"name":"photo_ref","type":"string","required":true}],"required_docs":["passport","photo"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_kr_tourist_c3_cn','KR','CN',
 'Korea C-3 Tourist Visa (CN nationals)',
 7, 60, 'USD', 'paper',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_vn_evisa','VN','*',
 'Vietnam e-Visa (90 days single/multi)',
 3, 25, 'USD', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"port_of_entry","type":"string","required":true},{"name":"photo_ref","type":"string","required":true}],"required_docs":["passport","photo"]}');

-- ---------- AUSTRALIA / CANADA ----------

INSERT OR REPLACE INTO visa_products VALUES
('vp_au_evisitor','AU','*',
 'Australia eVisitor (subclass 651)',
 1, 0, 'AUD', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true}],"required_docs":["passport"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_au_visitor_600_cn','AU','CN',
 'Australia Visitor Visa subclass 600 (CN nationals)',
 30, 190, 'AUD', 'embassy',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true},{"name":"itinerary","type":"string","required":true},{"name":"financial_proof_ref","type":"string","required":true},{"name":"employment_letter_ref","type":"string","required":true},{"name":"photo_ref","type":"string","required":true}],"required_docs":["passport","photo","itinerary","bank_statement"]}');

INSERT OR REPLACE INTO visa_products VALUES
('vp_ca_eta','CA','*',
 'Canada eTA (electronic travel authorisation)',
 1, 7, 'CAD', 'evisa',
 '{"fields":[{"name":"applicant_name","type":"string","required":true},{"name":"passport_no","type":"string","required":true},{"name":"passport_expiry","type":"date","required":true},{"name":"date_of_birth","type":"date","required":true},{"name":"nationality","type":"string","required":true}],"required_docs":["passport"]}');

COMMIT;
-- entry_requirements seed matrix.
-- 14 nationalities x 15 destinations, tourism primary + select business/transit rows.
-- Task-relevant JP rows were manually reviewed on 2026-07-30 against MOFA/MHLW
-- sources in docs/audits/artifacts/2026-07-29-japan_20d-real-world-sources.json.
-- Other catalog rows are historical search distractors and must be re-verified
-- before use; they are not presented as permanently current policy.
-- Columns: origin_nationality, destination, purpose, visa_required,
--          allowed_stay_days, passport_validity_months, docs_needed_json,
--          notes, updated_at.

BEGIN TRANSACTION;

-- ==================================================================
-- ORIGIN: CN (China PRC)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('CN','JP','tourism',1,30,0,
 '["ordinary_passport","photo","application_form","itinerary","hotel_booking","return_ticket","financial_proof","employment_letter","accredited_agency_submission"]',
 'Chinese nationals residing in China use the competent Japanese overseas establishment and its accredited-agency channel for short-term tourism applications. The official eVisa page describes 15-day or 30-day single-entry stays and does not publish a universal six-month passport minimum. Verify passport acceptance and transit rules for the actual itinerary.',
 '2026-07-30T11:23:05+08:00'),

('CN','JP','business',1,NULL,6,
 '["passport","photo","application_form","invitation_letter","company_letter","itinerary","financial_proof"]',
 'Single/multi-entry business visa. Requires invitation letter from JP host company on letterhead with purpose and duration.',
 '2026-02-27T00:00:00Z'),

('CN','JP','transit',1,NULL,6,
 '["passport","onward_ticket","visa_for_next_country"]',
 'Transit visa for airside stays >24h or landside connections; 72h TWOV may apply at some airports subject to onward ticket.',
 '2026-01-12T00:00:00Z'),

('CN','US','tourism',1,NULL,6,
 '["passport","photo","ds160_confirmation","application_fee_receipt","interview_appointment","itinerary","financial_proof","employment_letter"]',
 'B1/B2 visa via embassy interview. 10-year multi-entry common. Admission is I-94 determined, typically up to 6 months per entry.',
 '2026-03-01T00:00:00Z'),

('CN','GB','tourism',1,NULL,6,
 '["passport","photo","application_form","financial_proof","employment_letter","itinerary","hotel_booking","tb_certificate"]',
 'Standard Visitor visa. TB test certificate required for applicants residing in mainland China for >6 months.',
 '2026-02-14T00:00:00Z'),

('CN','DE','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","itinerary","schengen_insurance","financial_proof","employment_letter","return_ticket"]',
 'Schengen Short-Stay C visa (<=90 days/180). Passport must be valid >=3 months beyond planned departure AND issued within last 10 years.',
 '2026-03-05T00:00:00Z'),

('CN','FR','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","itinerary","schengen_insurance","financial_proof","employment_letter","return_ticket"]',
 'Schengen Short-Stay via France consulate or VFS. Insurance with >=EUR30,000 coverage required.',
 '2026-03-05T00:00:00Z'),

('CN','IT','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","itinerary","schengen_insurance","financial_proof","employment_letter","return_ticket"]',
 'Schengen Short-Stay. Italy consulates apply the 3-month-beyond-departure rule strictly.',
 '2026-03-05T00:00:00Z'),

('CN','ES','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","itinerary","schengen_insurance","financial_proof","return_ticket"]',
 'Schengen Short-Stay via Spain VFS. Biometrics collection required in person.',
 '2026-03-05T00:00:00Z'),

('CN','KR','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof","employment_letter","return_ticket"]',
 'Tourist C-3 visa required for mainland CN. Incheon/Busan regional group visa programs exist. K-ETA exemption has not applied to CN PRC nationals.',
 '2026-03-22T00:00:00Z'),

('CN','TH','tourism',0,30,6,
 '["passport","return_ticket","proof_of_funds_20000THB"]',
 'Visa exemption extended indefinitely from 2024-03; 30 days per entry, up to 60 days consecutive via in-country extension.',
 '2026-02-19T00:00:00Z'),

('CN','VN','tourism',0,15,6,
 '["passport","return_ticket","hotel_booking"]',
 '15-day visa exemption for CN tourists entering via designated ports; e-visa available for up to 90 days.',
 '2025-12-04T00:00:00Z'),

('CN','SG','tourism',0,30,6,
 '["passport","return_ticket","hotel_booking","sg_arrival_card"]',
 '30-day mutual visa exemption (effective 2024-02). SG Arrival Card (SGAC) required within 72h before arrival.',
 '2026-01-30T00:00:00Z'),

('CN','AU','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof","employment_letter","health_declaration"]',
 'Visitor visa subclass 600 required. Frequent-traveller 3-year or 10-year multi-entry possible for qualifying applicants.',
 '2026-03-10T00:00:00Z'),

('CN','CA','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof","employment_letter","biometrics_receipt"]',
 'Temporary Resident Visa (TRV). Biometrics required and reusable for 10 years.',
 '2026-02-26T00:00:00Z'),

('CN','TW','tourism',1,NULL,6,
 '["mainland_travel_permit","entry_exit_permit","itinerary"]',
 'Mainland CN residents require both a Mainland Travel Permit and an Entry/Exit Permit issued by Taiwan MAC. Individual tourism suspended since 2019; limited group/visits.',
 '2026-03-15T00:00:00Z'),

('CN','HK','tourism',1,NULL,6,
 '["ep_eep_permit","photo"]',
 'Mainland residents travel to HK on Exit-Entry Permit for Travelling to and from HK & Macao (EEP) with endorsement; not a visa but permit-gated.',
 '2026-02-01T00:00:00Z');

-- CN transit through common hubs
INSERT OR REPLACE INTO entry_requirements VALUES
('CN','KR','transit',0,1,6,
 '["passport","onward_ticket","boarding_pass"]',
 'Up to 24h TWOV at ICN/GMP/PUS with onward ticket to third country; extension to 30 days via group-transit tour programs.',
 '2026-01-08T00:00:00Z'),

('CN','SG','transit',0,4,6,
 '["passport","onward_ticket"]',
 '96-hour Visa-Free Transit Facility (VFTF) for sterile-side onward travel; standard 30-day visa-free for tourism applies instead if admitted.',
 '2026-01-08T00:00:00Z'),

('CN','DE','transit',0,1,3,
 '["passport","onward_ticket"]',
 'Airside Schengen transit for CN nationals generally requires Airport Transit Visa (ATV type A) unless onward ticket to third country via one EU airport only.',
 '2025-12-14T00:00:00Z');

-- ==================================================================
-- ORIGIN: HK (Hong Kong SAR passport)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('HK','JP','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa-free 90 days on HKSAR passport for tourism/business short-stay.',
 '2026-03-18T00:00:00Z'),

('HK','US','tourism',1,NULL,6,
 '["passport","photo","ds160_confirmation","interview_appointment","itinerary"]',
 'HKSAR passport holders are NOT in the Visa Waiver Program. B1/B2 interview at US consulate required.',
 '2026-03-01T00:00:00Z'),

('HK','GB','tourism',0,180,6,
 '["passport","return_ticket","eta_approval"]',
 'Visa-free 6 months as Standard Visitor; UK ETA required for all visa-exempt nationals since 2024.',
 '2026-02-22T00:00:00Z'),

('HK','DE','tourism',0,90,3,
 '["passport","return_ticket","hotel_booking","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS travel authorisation applies to HKSAR passport from 2025.',
 '2026-03-05T00:00:00Z'),

('HK','FR','tourism',0,90,3,
 '["passport","return_ticket","hotel_booking","etias_approval"]',
 'Schengen visa-free 90/180 via France. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('HK','IT','tourism',0,90,3,
 '["passport","return_ticket","etias_approval"]',
 'Schengen visa-free. ETIAS required from 2025.',
 '2026-03-05T00:00:00Z'),

('HK','ES','tourism',0,90,3,
 '["passport","return_ticket","etias_approval"]',
 'Schengen visa-free. ETIAS required from 2025.',
 '2026-03-05T00:00:00Z'),

('HK','KR','tourism',0,90,6,
 '["passport","keta_approval","return_ticket"]',
 'Visa-free 90 days; K-ETA required for air arrivals since 2021 (HK currently in K-ETA temporary exemption list through 2025 - verify annually).',
 '2026-02-04T00:00:00Z'),

('HK','TH','tourism',0,30,6,
 '["passport","return_ticket","proof_of_funds_10000THB"]',
 'Visa-exempt 30 days for tourism.',
 '2026-01-19T00:00:00Z'),

('HK','VN','tourism',0,14,6,
 '["passport","return_ticket"]',
 'HKSAR passport: 14 days visa-free per entry, with 30-day gap between stays. E-visa up to 90 days available.',
 '2025-11-28T00:00:00Z'),

('HK','SG','tourism',0,30,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 30 days. SGAC submission required within 72h before arrival.',
 '2026-01-30T00:00:00Z'),

('HK','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651","return_ticket"]',
 'eVisitor (subclass 651) free authorisation for HKSAR passports; 3-month stays, 12-month multi-entry.',
 '2026-03-10T00:00:00Z'),

('HK','CA','tourism',0,180,6,
 '["passport","eta_approval","return_ticket"]',
 'eTA required for air travel; visa-free stay up to 6 months.',
 '2026-02-26T00:00:00Z'),

('HK','TW','tourism',0,30,6,
 '["passport","online_travel_authority"]',
 'Online Travel Authority Certificate required for HKSAR passport holders; free, issued online.',
 '2026-03-15T00:00:00Z');

-- ==================================================================
-- ORIGIN: TW (Taiwan)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('TW','JP','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa-free 90 days on Taiwan passport with national ID number printed.',
 '2026-03-18T00:00:00Z'),

('TW','US','tourism',0,90,6,
 '["passport","esta_approval","return_ticket"]',
 'Visa Waiver Program; ESTA required. Passport must have national ID number.',
 '2026-03-01T00:00:00Z'),

('TW','GB','tourism',0,180,6,
 '["passport","eta_approval","return_ticket"]',
 'Visa-free 6 months; UK ETA required from 2025 for TW passport.',
 '2026-02-22T00:00:00Z'),

('TW','DE','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180 for TW passports with ID number. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('TW','FR','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('TW','IT','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('TW','ES','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('TW','KR','tourism',0,90,6,
 '["passport","keta_approval","return_ticket"]',
 'Visa-free 90 days; K-ETA generally required, with rolling short exemption lists.',
 '2026-02-04T00:00:00Z'),

('TW','TH','tourism',0,30,6,
 '["passport","return_ticket"]',
 'Visa exemption scheme (renewed annually); 30-day stays.',
 '2026-01-19T00:00:00Z'),

('TW','VN','tourism',1,NULL,6,
 '["passport","photo","evisa_application","itinerary"]',
 'Taiwanese passports require Vietnam e-visa (up to 90 days) or visa-on-arrival via approved agency.',
 '2025-12-04T00:00:00Z'),

('TW','SG','tourism',0,30,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 30 days. SGAC required pre-arrival.',
 '2026-01-30T00:00:00Z'),

('TW','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651"]',
 'eVisitor (subclass 651) online authorisation, free.',
 '2026-03-10T00:00:00Z'),

('TW','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel; visa-free up to 6 months.',
 '2026-02-26T00:00:00Z'),

('TW','HK','tourism',0,30,6,
 '["passport","online_preregistration"]',
 'Pre-arrival Registration for Taiwan Residents (iPermit) valid 2 months, two entries 30 days each.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: US
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('US','JP','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa-free 90 days; JP does not enforce 6-month rule but passport must be valid for stay duration.',
 '2026-03-18T00:00:00Z'),

('US','JP','business',0,90,6,
 '["passport","return_ticket","business_letter"]',
 'Short-stay business trips (meetings, conferences) permitted under visa-free entry; no employment.',
 '2026-02-15T00:00:00Z'),

('US','GB','tourism',0,180,6,
 '["passport","eta_approval","return_ticket"]',
 'Standard Visitor 6 months visa-free; UK ETA required for all US travellers since Jan 2025.',
 '2026-02-22T00:00:00Z'),

('US','DE','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required from 2025.',
 '2026-03-05T00:00:00Z'),

('US','FR','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required from 2025.',
 '2026-03-05T00:00:00Z'),

('US','IT','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('US','ES','tourism',0,90,3,
 '["passport","etias_approval","return_ticket"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('US','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days; K-ETA required (rolling exemption for US through 2025 ends 2026).',
 '2026-02-04T00:00:00Z'),

('US','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption extended to 60 days in 2024.',
 '2026-01-19T00:00:00Z'),

('US','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days per entry (policy extended through 2028).',
 '2025-12-04T00:00:00Z'),

('US','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days. SGAC required within 72h before arrival.',
 '2026-01-30T00:00:00Z'),

('US','AU','tourism',0,90,6,
 '["passport","eta_subclass601"]',
 'ETA subclass 601 (small fee) for US passport holders; 3-month stays, 12-month multi-entry.',
 '2026-03-10T00:00:00Z'),

('US','CA','tourism',0,180,6,
 '["passport"]',
 'Visa-free 6 months; eTA not required for US citizens (but required for US permanent residents arriving by air).',
 '2026-02-26T00:00:00Z'),

('US','TW','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa-free 90 days for US passports.',
 '2026-03-15T00:00:00Z'),

('US','HK','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: JP
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('JP','JP','tourism',0,0,6,
 '["passport"]',
 'Home country; no entry requirement needed.',
 '2026-01-01T00:00:00Z'),

('JP','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required (25 USD).',
 '2026-03-01T00:00:00Z'),

('JP','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('JP','DE','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('JP','FR','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('JP','IT','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('JP','ES','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('JP','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days. K-ETA exemption historically granted to JP passports.',
 '2026-02-04T00:00:00Z'),

('JP','TH','tourism',0,30,6,
 '["passport","return_ticket"]',
 'Visa exemption 30 days.',
 '2026-01-19T00:00:00Z'),

('JP','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days per entry.',
 '2025-12-04T00:00:00Z'),

('JP','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('JP','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651"]',
 'eVisitor (subclass 651) free online authorisation.',
 '2026-03-10T00:00:00Z'),

('JP','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel; visa-free up to 6 months.',
 '2026-02-26T00:00:00Z'),

('JP','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('JP','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- Extra tourism row: JP <-> CN reinstatement (2024-11-30 policy)
INSERT OR REPLACE INTO entry_requirements VALUES
('JP','CN','tourism',0,15,6,
 '["passport","return_ticket","hotel_booking"]',
 'Visa-free 15-day tourism policy reinstated 2024-11-30. Longer stays require C-visa.',
 '2026-02-02T00:00:00Z');

-- ==================================================================
-- ORIGIN: GB (United Kingdom)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('GB','JP','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa-free 90 days for UK passport (Temporary Visitor).',
 '2026-03-18T00:00:00Z'),

('GB','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required.',
 '2026-03-01T00:00:00Z'),

('GB','DE','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180 (post-Brexit). ETIAS required from 2025.',
 '2026-03-05T00:00:00Z'),

('GB','FR','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('GB','IT','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('GB','ES','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('GB','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days. K-ETA may be required; rolling exemption list.',
 '2026-02-04T00:00:00Z'),

('GB','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption 60 days (2024 extension).',
 '2026-01-19T00:00:00Z'),

('GB','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days (policy extended through 2028).',
 '2025-12-04T00:00:00Z'),

('GB','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('GB','AU','tourism',0,90,6,
 '["passport","eta_subclass601"]',
 'ETA subclass 601 for UK passport; fee-based online authorisation.',
 '2026-03-10T00:00:00Z'),

('GB','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel; visa-free up to 6 months.',
 '2026-02-26T00:00:00Z'),

('GB','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('GB','HK','tourism',0,180,6,
 '["passport"]',
 'Visa-free 180 days (longest among HK waivers) for British National passports.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: DE (Germany)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('DE','JP','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days (Temporary Visitor status).',
 '2026-03-18T00:00:00Z'),

('DE','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required.',
 '2026-03-01T00:00:00Z'),

('DE','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('DE','FR','tourism',0,90,0,
 '["passport_or_eu_id"]',
 'EU/Schengen free movement. National ID card suffices; no passport validity minimum.',
 '2026-03-05T00:00:00Z'),

('DE','IT','tourism',0,90,0,
 '["passport_or_eu_id"]',
 'EU/Schengen free movement.',
 '2026-03-05T00:00:00Z'),

('DE','ES','tourism',0,90,0,
 '["passport_or_eu_id"]',
 'EU/Schengen free movement.',
 '2026-03-05T00:00:00Z'),

('DE','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days. K-ETA applies per current rules.',
 '2026-02-04T00:00:00Z'),

('DE','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption 60 days (2024 extension).',
 '2026-01-19T00:00:00Z'),

('DE','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days.',
 '2025-12-04T00:00:00Z'),

('DE','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('DE','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651"]',
 'eVisitor (subclass 651) free online authorisation.',
 '2026-03-10T00:00:00Z'),

('DE','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel.',
 '2026-02-26T00:00:00Z'),

('DE','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('DE','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: FR (France) — mirrors DE for EU/Schengen nationals
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('FR','JP','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-18T00:00:00Z'),

('FR','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required.',
 '2026-03-01T00:00:00Z'),

('FR','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('FR','DE','tourism',0,90,0,
 '["passport_or_eu_id"]',
 'EU/Schengen free movement.',
 '2026-03-05T00:00:00Z'),

('FR','IT','tourism',0,90,0,
 '["passport_or_eu_id"]',
 'EU/Schengen free movement.',
 '2026-03-05T00:00:00Z'),

('FR','ES','tourism',0,90,0,
 '["passport_or_eu_id"]',
 'EU/Schengen free movement.',
 '2026-03-05T00:00:00Z'),

('FR','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days. K-ETA per current rules.',
 '2026-02-04T00:00:00Z'),

('FR','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption 60 days.',
 '2026-01-19T00:00:00Z'),

('FR','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days.',
 '2025-12-04T00:00:00Z'),

('FR','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('FR','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651"]',
 'eVisitor free online authorisation.',
 '2026-03-10T00:00:00Z'),

('FR','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel.',
 '2026-02-26T00:00:00Z'),

('FR','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('FR','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: KR (Korea)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('KR','JP','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-18T00:00:00Z'),

('KR','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required.',
 '2026-03-01T00:00:00Z'),

('KR','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('KR','DE','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('KR','FR','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('KR','IT','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('KR','ES','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('KR','TH','tourism',0,90,6,
 '["passport","return_ticket"]',
 'Visa exemption 90 days (KR-TH bilateral).',
 '2026-01-19T00:00:00Z'),

('KR','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days.',
 '2025-12-04T00:00:00Z'),

('KR','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('KR','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651"]',
 'eVisitor subclass 651 online authorisation.',
 '2026-03-10T00:00:00Z'),

('KR','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel.',
 '2026-02-26T00:00:00Z'),

('KR','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('KR','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: SG (Singapore)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('SG','JP','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-18T00:00:00Z'),

('SG','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required.',
 '2026-03-01T00:00:00Z'),

('SG','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('SG','DE','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('SG','FR','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('SG','IT','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('SG','ES','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('SG','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days. K-ETA per current rules.',
 '2026-02-04T00:00:00Z'),

('SG','TH','tourism',0,30,6,
 '["passport"]',
 'Visa exemption 30 days.',
 '2026-01-19T00:00:00Z'),

('SG','VN','tourism',0,30,6,
 '["passport"]',
 'Visa exemption 30 days (ASEAN bilateral).',
 '2025-12-04T00:00:00Z'),

('SG','AU','tourism',0,90,6,
 '["passport","evisitor_subclass651"]',
 'eVisitor free online authorisation.',
 '2026-03-10T00:00:00Z'),

('SG','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel.',
 '2026-02-26T00:00:00Z'),

('SG','TW','tourism',0,30,6,
 '["passport"]',
 'Visa-free 30 days.',
 '2026-03-15T00:00:00Z'),

('SG','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: IN (India) — broadly visa-required
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('IN','JP','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof","employment_letter","hotel_booking"]',
 'Tourist visa required via JP embassy/VFS; multi-entry variants exist for frequent travellers.',
 '2026-03-18T00:00:00Z'),

('IN','US','tourism',1,NULL,6,
 '["passport","photo","ds160_confirmation","interview_appointment","itinerary","financial_proof"]',
 'B1/B2 visa via embassy interview. 10-year multi-entry common.',
 '2026-03-01T00:00:00Z'),

('IN','GB','tourism',1,NULL,6,
 '["passport","photo","application_form","financial_proof","employment_letter","itinerary"]',
 'Standard Visitor visa required.',
 '2026-02-22T00:00:00Z'),

('IN','DE','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","schengen_insurance","financial_proof","return_ticket"]',
 'Schengen Short-Stay visa.',
 '2026-03-05T00:00:00Z'),

('IN','FR','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","schengen_insurance","financial_proof","return_ticket"]',
 'Schengen Short-Stay visa.',
 '2026-03-05T00:00:00Z'),

('IN','IT','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","schengen_insurance","financial_proof","return_ticket"]',
 'Schengen Short-Stay visa.',
 '2026-03-05T00:00:00Z'),

('IN','ES','tourism',1,NULL,3,
 '["passport","photo","application_form","hotel_booking","schengen_insurance","financial_proof","return_ticket"]',
 'Schengen Short-Stay visa.',
 '2026-03-05T00:00:00Z'),

('IN','KR','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof"]',
 'C-3 tourist visa required.',
 '2026-02-04T00:00:00Z'),

('IN','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption up to 60 days extended to Indian nationals from late 2024.',
 '2026-01-19T00:00:00Z'),

('IN','VN','tourism',1,NULL,6,
 '["passport","photo","evisa_application","itinerary"]',
 'Vietnam e-visa up to 90 days.',
 '2025-12-04T00:00:00Z'),

('IN','SG','tourism',0,30,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 30 days for select Indian passport holders meeting criteria; check SG ICA before travel.',
 '2026-01-30T00:00:00Z'),

('IN','AU','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof"]',
 'Visitor visa subclass 600 required.',
 '2026-03-10T00:00:00Z'),

('IN','CA','tourism',1,NULL,6,
 '["passport","photo","application_form","biometrics_receipt","itinerary","financial_proof"]',
 'TRV visitor visa required; biometrics.',
 '2026-02-26T00:00:00Z'),

('IN','TW','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary"]',
 'TW e-visa or visitor visa required for Indian nationals (limited exemptions).',
 '2026-03-15T00:00:00Z'),

('IN','HK','tourism',0,14,6,
 '["passport","online_preregistration"]',
 '14-day visa-free stay with online pre-arrival registration for Indian nationals.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: AU (Australia)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('AU','JP','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-18T00:00:00Z'),

('AU','US','tourism',0,90,6,
 '["passport","esta_approval"]',
 'Visa Waiver Program; ESTA required.',
 '2026-03-01T00:00:00Z'),

('AU','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('AU','DE','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('AU','FR','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('AU','IT','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('AU','ES','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('AU','KR','tourism',0,90,6,
 '["passport","keta_approval"]',
 'Visa-free 90 days. K-ETA per current rules.',
 '2026-02-04T00:00:00Z'),

('AU','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption 60 days.',
 '2026-01-19T00:00:00Z'),

('AU','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days.',
 '2025-12-04T00:00:00Z'),

('AU','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('AU','CA','tourism',0,180,6,
 '["passport","eta_approval"]',
 'eTA required for air travel.',
 '2026-02-26T00:00:00Z'),

('AU','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('AU','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: CA (Canada)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('CA','JP','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-18T00:00:00Z'),

('CA','US','tourism',0,180,6,
 '["passport"]',
 'Bilateral visa-free 6 months; no ESTA for Canadian citizens. Canadian PRs follow their nationality rules.',
 '2026-03-01T00:00:00Z'),

('CA','GB','tourism',0,180,6,
 '["passport","eta_approval"]',
 'Visa-free 6 months. UK ETA required from 2025.',
 '2026-02-22T00:00:00Z'),

('CA','DE','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180. ETIAS required.',
 '2026-03-05T00:00:00Z'),

('CA','FR','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('CA','IT','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('CA','ES','tourism',0,90,3,
 '["passport","etias_approval"]',
 'Schengen visa-free 90/180.',
 '2026-03-05T00:00:00Z'),

('CA','KR','tourism',0,180,6,
 '["passport","keta_approval"]',
 'Bilateral 180 days visa-free (unique to CA). K-ETA per current rules.',
 '2026-02-04T00:00:00Z'),

('CA','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption 60 days.',
 '2026-01-19T00:00:00Z'),

('CA','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days.',
 '2025-12-04T00:00:00Z'),

('CA','SG','tourism',0,90,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 90 days.',
 '2026-01-30T00:00:00Z'),

('CA','AU','tourism',0,90,6,
 '["passport","eta_subclass601"]',
 'ETA subclass 601 (fee-based online authorisation).',
 '2026-03-10T00:00:00Z'),

('CA','TW','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-03-15T00:00:00Z'),

('CA','HK','tourism',0,90,6,
 '["passport"]',
 'Visa-free 90 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- ORIGIN: RU (Russia)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('RU','JP','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","hotel_booking","financial_proof"]',
 'Tourist visa required. Post-2022 processing slower and more scrutinised.',
 '2026-03-18T00:00:00Z'),

('RU','US','tourism',1,NULL,6,
 '["passport","photo","ds160_confirmation","interview_appointment","itinerary","financial_proof"]',
 'B1/B2 visa; RU nationals often routed to third-country consulates (Warsaw, Astana) due to Moscow embassy drawdown.',
 '2026-03-01T00:00:00Z'),

('RU','GB','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof"]',
 'Standard Visitor visa required; enhanced vetting since 2022.',
 '2026-02-22T00:00:00Z'),

('RU','DE','tourism',1,NULL,3,
 '["passport","photo","application_form","schengen_insurance","hotel_booking","financial_proof","return_ticket"]',
 'Schengen visa with heightened scrutiny. Some DE consulates limit tourist-visa issuance.',
 '2026-03-05T00:00:00Z'),

('RU','FR','tourism',1,NULL,3,
 '["passport","photo","application_form","schengen_insurance","hotel_booking","financial_proof","return_ticket"]',
 'Schengen Short-Stay; France has suspended standard tourist visas from Russia for extended periods - verify consulate status.',
 '2026-03-05T00:00:00Z'),

('RU','IT','tourism',1,NULL,3,
 '["passport","photo","application_form","schengen_insurance","hotel_booking","financial_proof"]',
 'Schengen Short-Stay visa.',
 '2026-03-05T00:00:00Z'),

('RU','ES','tourism',1,NULL,3,
 '["passport","photo","application_form","schengen_insurance","hotel_booking","financial_proof"]',
 'Schengen Short-Stay visa.',
 '2026-03-05T00:00:00Z'),

('RU','KR','tourism',0,60,6,
 '["passport","keta_approval","return_ticket"]',
 'Bilateral visa exemption 60 days; K-ETA per current rules.',
 '2026-02-04T00:00:00Z'),

('RU','TH','tourism',0,60,6,
 '["passport","return_ticket"]',
 'Visa exemption 60 days (2024 extension, high RU tourism volume).',
 '2026-01-19T00:00:00Z'),

('RU','VN','tourism',0,45,6,
 '["passport","return_ticket"]',
 'Visa exemption 45 days.',
 '2025-12-04T00:00:00Z'),

('RU','SG','tourism',0,30,6,
 '["passport","sg_arrival_card"]',
 'Visa-free 30 days (bilateral).',
 '2026-01-30T00:00:00Z'),

('RU','AU','tourism',1,NULL,6,
 '["passport","photo","application_form","itinerary","financial_proof"]',
 'Visitor visa subclass 600 required.',
 '2026-03-10T00:00:00Z'),

('RU','CA','tourism',1,NULL,6,
 '["passport","photo","application_form","biometrics_receipt","itinerary"]',
 'TRV visitor visa required; sanctions-related scrutiny.',
 '2026-02-26T00:00:00Z'),

('RU','TW','tourism',0,14,6,
 '["passport","return_ticket"]',
 '14-day visa-free pilot programme for RU passports (extended annually).',
 '2026-03-15T00:00:00Z'),

('RU','HK','tourism',0,14,6,
 '["passport","return_ticket"]',
 'Visa-free 14 days.',
 '2026-02-01T00:00:00Z');

-- ==================================================================
-- Extra business-purpose rows for scenario (JP focus)
-- ==================================================================

INSERT OR REPLACE INTO entry_requirements VALUES
('US','JP','transit',0,1,6,
 '["passport","onward_ticket"]',
 'Airside transit up to 24h under visa-free status.',
 '2026-01-14T00:00:00Z'),

('GB','JP','business',0,90,6,
 '["passport","business_letter"]',
 'Short-stay business visits allowed under visa-free entry.',
 '2026-02-15T00:00:00Z'),

('DE','JP','business',0,90,6,
 '["passport","business_letter"]',
 'Short-stay business visits allowed under visa-free entry.',
 '2026-02-15T00:00:00Z'),

('IN','JP','business',1,NULL,6,
 '["passport","photo","application_form","invitation_letter","company_letter","itinerary"]',
 'Business visa via JP embassy; invitation letter required.',
 '2026-02-15T00:00:00Z');

COMMIT;
-- advisories seed — 2026-Q2 snapshot.
-- Levels: 1=normal, 2=caution, 3=reconsider, 4=do not travel.
-- updated_at chosen within 30 days of 2026-04-17.

BEGIN TRANSACTION;

INSERT OR REPLACE INTO advisories VALUES
('JP', 1,
 'Exercise normal precautions. Japan is generally safe for travel with low violent-crime rates. Be prepared for earthquakes: download the JMA Safety Tips app and identify evacuation routes at hotels. Typhoon season affects southern and western Japan between June and October; monitor JMA warnings and expect rail and air disruptions in Kyushu, Shikoku and Kansai during that window.',
 '2026-04-01T08:00:00Z'),

('US', 2,
 'Exercise increased caution. Firearm-related violence occurs across the country including in tourist districts; keep situational awareness and avoid demonstrations. Healthcare is world-class but extremely expensive without insurance; travellers should carry proof of coverage ideally >USD 100,000 and use urgent-care clinics rather than ERs where possible.',
 '2026-04-02T00:00:00Z'),

('CN', 2,
 'Exercise increased caution. Arbitrary enforcement of local laws — including exit bans on foreign nationals — has been reported, particularly for travellers with business or research ties. Carry identification at all times and avoid photographing government facilities, military sites, or protests.',
 '2026-03-25T00:00:00Z'),

('RU', 4,
 'Do not travel. Armed conflict continues in neighbouring Ukraine, and sanctions have severed most banking, flight, and consular services. The US, UK, EU, Japan, and Canada have all downgraded their diplomatic presence and cannot reliably assist citizens. Risk of wrongful detention of foreign nationals is high.',
 '2026-04-05T00:00:00Z'),

('UA', 4,
 'Do not travel. Full-scale armed conflict with Russia is ongoing. Missile and drone strikes can occur anywhere in the country with little warning, including Kyiv and Lviv. Air travel is suspended and consular assistance is extremely limited.',
 '2026-04-05T00:00:00Z'),

('IL', 3,
 'Reconsider travel due to the ongoing regional conflict, rocket fire from Gaza and Lebanon, and risk of terrorism. Travel near Gaza border areas, the West Bank outside major tourist sites, and northern border zones should be avoided entirely; Tel Aviv and Jerusalem operate but sirens and shelter instructions are possible at any time.',
 '2026-04-03T00:00:00Z'),

('LB', 4,
 'Do not travel. Active conflict in southern Lebanon and ongoing economic collapse have severely disrupted public services. US and several EU governments have issued mandatory departure notices for non-essential staff. Commercial air service is intermittent.',
 '2026-04-04T00:00:00Z'),

('IR', 4,
 'Do not travel. Risk of arbitrary arrest, detention, and wrongful imprisonment of foreign and dual nationals is very high. Ongoing regional hostilities and US-sanctions environment preclude normal consular support. Dual nationals are specifically at risk and may not be permitted to leave.',
 '2026-04-04T00:00:00Z'),

('KP', 4,
 'Do not travel. The US, UK and most Western governments prohibit or strongly advise against all travel to the DPRK. Foreign visitors face severe risk of arbitrary arrest and prolonged detention with no consular access. Tourism infrastructure is state-controlled.',
 '2026-03-30T00:00:00Z'),

('TH', 2,
 'Exercise increased caution. Civil unrest and insurgent activity persist in the southernmost provinces of Yala, Pattani, Narathiwat, and Songkhla (south of Hat Yai) — avoid unless essential. Bangkok and major tourist areas (Phuket, Chiang Mai, Koh Samui) remain generally safe, but watch for pickpocketing and scams around Khao San Road and tuk-tuk touts.',
 '2026-04-06T00:00:00Z'),

('GB', 1,
 'Exercise normal precautions. The UK is generally safe; London and other urban centres see standard petty-crime patterns. UK terror threat level stays at SUBSTANTIAL — attacks possible but infrequent. Monitor the National Rail website during industrial-action weeks, which can disrupt domestic transport.',
 '2026-04-07T00:00:00Z'),

('DE', 1,
 'Exercise normal precautions. Germany is safe for travel. Be alert to pickpocketing at major transit hubs (Frankfurt Hbf, Berlin Hbf, Munich Hbf) and large public events such as Oktoberfest. Klimakleber climate-protest disruptions may delay ground travel on short notice in major cities.',
 '2026-04-07T00:00:00Z'),

('FR', 2,
 'Exercise increased caution due to terrorism and civil unrest. France is under the Vigipirate "urgence attentat" elevated posture with security operations around transit hubs and places of worship. Large-scale demonstrations in Paris and Marseille can become disorderly with short notice. Pickpocketing in Métro and around major monuments remains common.',
 '2026-04-06T00:00:00Z'),

('IT', 1,
 'Exercise normal precautions. Italy is generally safe. Pickpocketing and bag-slashing are common around the Colosseum, Termini station, Venice vaporetti, and the Duomo in Milan; keep bags closed and wallets in front pockets. Summer heatwaves can reach extreme levels in the south — check weather before day trips.',
 '2026-04-08T00:00:00Z'),

('ES', 1,
 'Exercise normal precautions. Spain is safe for travellers. Pickpocketing and bag-snatching are frequent in Barcelona''s Las Ramblas, Metro Line 3, and Madrid''s Puerta del Sol. Beach towns see heavier summer petty-crime volume; keep valuables in hotel safes.',
 '2026-04-08T00:00:00Z'),

('KR', 1,
 'Exercise normal precautions. South Korea has one of the lowest violent-crime rates among OECD economies. Tensions with the DPRK can prompt occasional alerts but rarely affect travellers. Seoul protests around government complexes in Gwanghwamun are peaceful but can disrupt transit.',
 '2026-04-08T00:00:00Z'),

('SG', 1,
 'Exercise normal precautions. Singapore has very low crime rates. Local laws on drugs, vandalism, and public disorder are strictly enforced with severe penalties including caning and the death penalty for drug trafficking; transit passengers are not exempt.',
 '2026-04-09T00:00:00Z'),

('AU', 1,
 'Exercise normal precautions. Australia is safe for travel. Bushfire season (Oct–Apr) affects rural regions; monitor state emergency-service apps and respect road closures. Coastal areas carry rip-current risk — swim between the flags at patrolled beaches.',
 '2026-04-09T00:00:00Z'),

('CA', 1,
 'Exercise normal precautions. Canada is safe. Wildfire smoke can degrade air quality in western and central provinces during summer; AQI can reach hazardous levels in Vancouver and the Prairies. Bear-country rules apply in national parks — carry bear spray where posted.',
 '2026-04-09T00:00:00Z'),

('NZ', 1,
 'Exercise normal precautions. New Zealand is safe. Outdoor risks dominate: check Department of Conservation alpine and flood advisories before multi-day tramps, and be aware of rip currents on west-coast beaches. Earthquake activity is ongoing — know drop-cover-hold drill.',
 '2026-04-09T00:00:00Z'),

('TW', 2,
 'Exercise increased caution. Taiwan remains safe for tourists but cross-strait tensions with the PRC can escalate on short notice, occasionally disrupting flights and ferries. Typhoon season (July–October) can cause sudden cancellations. Earthquake activity has increased post-Hualien 2024.',
 '2026-04-05T00:00:00Z'),

('HK', 2,
 'Exercise increased caution. Hong Kong is generally safe for tourism, but the National Security Law is enforced aggressively; avoid political activity, protest photography, or social-media posts that authorities could interpret as endangering national security. Exit bans on foreign nationals have been reported.',
 '2026-04-05T00:00:00Z'),

('IN', 2,
 'Exercise increased caution due to crime, terrorism, and civil unrest. Specific regions carry higher risk: all travel to Jammu & Kashmir outside Ladakh is discouraged; the India-Pakistan border area and parts of the central-eastern Maoist/Naxal belt (Chhattisgarh, Jharkhand, Odisha) should be avoided. Delhi, Mumbai, Bengaluru, Jaipur, and Kerala are routine for tourists.',
 '2026-04-03T00:00:00Z'),

('ID', 2,
 'Exercise increased caution due to terrorism and natural disasters. Bali, Jakarta, and Yogyakarta are popular and generally safe but bag-snatching is common. Avoid Papua (West Papua province) due to separatist violence. Volcanic activity (Merapi, Semeru, Marapi) disrupts flights and inland travel with little warning.',
 '2026-04-04T00:00:00Z'),

('VN', 1,
 'Exercise normal precautions. Vietnam is safe for travellers. Motorbike-traffic crossings in Hanoi and HCMC are chaotic but generally predictable — walk steadily and don''t stop. Bag-snatch thefts from moving motorbikes occur; keep bags away from the roadside.',
 '2026-04-08T00:00:00Z'),

('PH', 2,
 'Exercise increased caution due to crime, terrorism, and kidnapping. All travel to the Sulu Archipelago and Marawi City (Mindanao) is discouraged. Manila, Cebu, Palawan, and Boracay are generally safe for tourism. Typhoons strike frequently between June and December — check PAGASA before island transfers.',
 '2026-04-06T00:00:00Z'),

('MX', 3,
 'Reconsider travel. Violence from organised crime varies sharply by state. Multiple northern and pacific states (Tamaulipas, Sinaloa, Zacatecas, Guerrero, Colima, Michoacán) are designated "do not travel". Cancún, Mexico City, Oaxaca, and Puerto Vallarta remain on "exercise increased caution" with careful planning.',
 '2026-04-03T00:00:00Z');

-- ==================================================================
-- Scheduled advisory change for D11 (typhoon Kansai).
-- Pre-staged as a 'pending_advisory' row in notifications payload.
-- The row below is the target state (JP level 2) but left COMMENTED-OUT here.
-- The advisory_raise event is actually stored in pending_events_seed.sql and
-- fired by the harness via admin_advance_day on day_index=11 so that the mock
-- server produces the fan-out notifications correctly.
-- Target state on D11 would be:
--   ('JP', 2, '... typhoon remnants, Kansai rail/air disruption ...',
--     '2026-04-27T07:00:00Z')
-- ==================================================================

COMMIT;
-- pending_events_seed.sql
--
-- Scripted admin_advance_day intrusions for the japan_20d task.
-- SPEC §3.11 / §5 accepts events inline on each admin_advance_day call; the
-- harness reads rows from this helper table to decide what to feed in when it
-- advances the clock. This table is NOT part of SPEC §4 and lives only in the
-- benchmark seed, so we create it conditionally here.

CREATE TABLE IF NOT EXISTS scripted_events (
    seq               INTEGER PRIMARY KEY AUTOINCREMENT,
    scheduled_day     INTEGER NOT NULL,
    scheduled_time    TEXT,               -- HH:MM reference, advisory only
    event_json        TEXT NOT NULL,      -- exact payload shape for admin_advance_day.events[]
    active            INTEGER NOT NULL DEFAULT 1,
    note              TEXT
);

CREATE INDEX IF NOT EXISTS idx_scripted_events_day
    ON scripted_events (scheduled_day, active);

BEGIN TRANSACTION;

-- ------------------------------------------------------------------
-- D1: channel/fraud review for the Japan tourist-visa application route.
-- events.yaml id=D1_visa_channel_review, day=1, time=08:30.
-- This row preserves the event count while replacing the invented senior-only
-- form with a distinct operational fact: China-resident applicants use the
-- competent overseas establishment and accredited-agency channel, and MOFA
-- warns against fraudulent look-alike eVisa sites.
-- ------------------------------------------------------------------
INSERT INTO scripted_events (scheduled_day, scheduled_time, event_json, active, note) VALUES
(1, '08:30',
 '{"type":"policy_change","origin":"CN","destination":"JP","purpose":"tourism","visa_required":true,"allowed_stay_days":30,"submission_channel":"accredited_agency","note":"MOFA channel review: Chinese nationals residing in China use the competent overseas establishment and accredited agencies for the tourist eVisa route. Reject look-alike payment sites and confirm current documentary requirements through the official portal."}',
 1,
 'D1 channel review per events.yaml D1_visa_channel_review');

-- ------------------------------------------------------------------
-- D11: advisory_raise on JP, level 1 -> 2, tied to typhoon MAYA.
-- events.yaml id=D10_typhoon_watch_alert seeds the weather-side narrative
-- on day 10; D11_typhoon_track_update on day 11 upgrades to Typhoon,
-- and the visa/advisory side raises the JP advisory level at that point
-- so fan-out lands before Li Wei departs on day 14.
-- ------------------------------------------------------------------
INSERT INTO scripted_events (scheduled_day, scheduled_time, event_json, active, note) VALUES
(11, '09:00',
 '{"type":"advisory_raise","country":"JP","level":2,"text":"Exercise increased caution in western and central Japan. JMA has upgraded tropical storm MAYA (T2602) to typhoon status, with landfall expected in Kyushu/Kansai on 2026-05-11 to 2026-05-12. Expect rail cancellations (Shinkansen reduced schedule), air disruptions at KIX/ITM/FUK, and widespread flood-prone alerts inland. Reconfirm accommodations and have a contingency day planned if you are transiting during the window."}',
 1,
 'D11 JP advisory bump tied to typhoon MAYA; scheduled_activate_day=11');

-- ------------------------------------------------------------------
-- Document-review hook for the mother''s passport. The expiry remains a useful
-- operational constraint because it leaves limited margin for airline, transit
-- and consular handling, but it is not encoded as an automatic Japanese
-- six-month-rule rejection.
-- ------------------------------------------------------------------

COMMIT;
-- seed_applications_sample.sql
--
-- No visa_applications rows are pre-seeded — the agent must drive the full
-- draft->upload->submit flow at runtime (see SPEC §3.4-§3.8).
--
-- Instead, we pre-populate a lightweight 'traveler_profiles' lookup table
-- (benchmark-only, not in SPEC §4) that agents can read to fetch the three
-- household passport numbers, DOB, and nationality. Task PERSONA.md says
-- these details are the user-side source of truth; the lookup table keeps
-- them consistent whether the agent reads them from persona files,
-- filesystem mock, or asks the user.

CREATE TABLE IF NOT EXISTS traveler_profiles (
    user_id           TEXT PRIMARY KEY,
    full_name         TEXT NOT NULL,
    full_name_native  TEXT,
    nationality       TEXT NOT NULL,
    passport_no       TEXT NOT NULL,
    passport_expiry   TEXT NOT NULL,      -- ISO date
    date_of_birth     TEXT NOT NULL,      -- ISO date
    age_on_2026_04_17 INTEGER,
    notes             TEXT
);

BEGIN TRANSACTION;

INSERT OR REPLACE INTO traveler_profiles VALUES
('li_wei',
 'Li Wei', 'Li Wei',
 'CN', 'G41382056',
 '2029-10-22',
 '1993-08-15', 32,
 'Primary traveller. Shanghai hukou, SaaS PM. Passport remains valid well beyond the trip. Verify the actual visa channel and any transit-country rule.');

INSERT OR REPLACE INTO traveler_profiles VALUES
('li_jianguo',
 'Li Jianguo', 'Li Jianguo',
 'CN', 'G17925638',
 '2028-06-30',
 '1960-11-22', 65,
 'Father. Type-II diabetic and insulin-dependent. Medication quantity, cold-chain and current Japan import-confirmation guidance require review. Age alone does not trigger an invented visa form.');

INSERT OR REPLACE INTO traveler_profiles VALUES
('zhang_lan',
 'Zhang Lan', 'Zhang Lan',
 'CN', 'G29476801',
 '2026-11-08',
 '1963-04-03', 62,
 'Mother. Passport expires 2026-11-08 and remains valid through the 2026-05-16 return. The short remaining margin should be surfaced for airline, visa-channel and transit confirmation without claiming an automatic Japanese six-month-rule rejection.');

COMMIT;
