BEGIN IMMEDIATE;

UPDATE cards
SET unbilled_balance_minor = unbilled_balance_minor + 48600,
    available_credit_minor = MAX(0, available_credit_minor - 48600)
WHERE card_id = 'card_cmb_family';

INSERT INTO unbilled_transactions
    (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind)
VALUES
    ('ub_dar_interest_20260812', 'card_cmb_family', '2026-08-12T08:00:00+08:00',
     48600, 'Revolving interest adjustment', '6012', 'Finance', 'interest');

COMMIT;
