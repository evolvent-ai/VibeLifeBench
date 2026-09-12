# Old-home renovation rental — banking data

The initial banking state contains six user accounts, seventeen payees, twenty-nine historical transactions, and five recurring-payment records. Payees cover utilities, property services, insurance, repairs, the renovation company, the air-testing laboratory, and personal collection requests that require source verification.

The transaction history spans rent collection, deposit return, tax, utilities, repairs, cleaning, storage, and household maintenance. Later task actions must preserve the distinction between a verified company payee and a personal transfer request.

`init.sql` is deterministic and uses synthetic financial identifiers.
