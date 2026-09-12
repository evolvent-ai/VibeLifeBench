BEGIN TRANSACTION;
INSERT INTO entry_requirements (origin_nationality,destination,purpose,visa_required,allowed_stay_days,passport_validity_months,docs_needed_json,notes,updated_at) VALUES
('CN','JP','business',1,90,6,'["passport","business invitation","itinerary","employment evidence"]','A Japanese business visa or other valid entry permission is required unless the traveler independently qualifies for a published exemption.','2026-06-25T00:00:00Z'),
('CN','JP','tourism',1,90,6,'["passport","application","itinerary","financial evidence"]','Verify the visa product and current consular instructions before travel.','2026-06-25T00:00:00Z'),
('CN','HK','transit',0,7,6,'["valid passport","confirmed onward ticket","destination entry documents"]','Transit eligibility depends on a genuine onward journey and immigration inspection; this record does not guarantee admission.','2026-06-25T00:00:00Z'),
('CN','KR','transit',0,1,6,'["valid passport","confirmed through itinerary"]','Airside transit without entering Korea may be possible; re-check airline and airport conditions for the exact itinerary.','2026-06-25T00:00:00Z'),
('CN','TW','transit',1,NULL,6,'["valid mainland travel and entry permissions","confirmed onward ticket"]','Do not assume airside transit permission for a PRC passport holder without current official confirmation.','2026-06-25T00:00:00Z');
INSERT INTO visa_products (product_id,destination,nationality,name,processing_time_days,fee_amount,fee_currency,delivery,form_schema_json) VALUES
('visa_jp_cn_business','JP','CN','Japan short-stay business visa',7,400,'CNY','consular','{"required":["passport","business invitation","employment evidence","itinerary"]}');
INSERT INTO advisories (country_code,level,text,updated_at) VALUES
('JP',1,'Exercise normal precautions and monitor transport disruptions.','2026-06-25T00:00:00Z'),
('HK',1,'For transit, carry confirmed onward travel and destination documents and follow airport and immigration instructions.','2026-06-25T00:00:00Z'),
('KR',1,'Confirm airside transit conditions with the operating airlines and airport.','2026-06-25T00:00:00Z'),
('TW',2,'Travel-document requirements for PRC passport holders require specific current verification.','2026-06-25T00:00:00Z');
INSERT INTO _counters (name,value) VALUES ('application_seq',9000),('document_seq',9000),('subscription_seq',9000),('notification_seq',9000);
COMMIT;

-- REAL-SOURCE ANCHOR (reviewed 2026-07-29): official process context, not a visa decision.
BEGIN TRANSACTION;
UPDATE entry_requirements
SET notes = notes || ' Official procedures context: https://www.mofa.go.jp/j_info/visit/visa/topics/china.html'
WHERE origin_nationality = 'CN' AND destination = 'JP' AND purpose = 'business';
COMMIT;
