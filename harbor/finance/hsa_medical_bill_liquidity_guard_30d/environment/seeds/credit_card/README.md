# HSA Medical Bill Liquidity Guard - 30-Day Plan

This task-local `credit_card` seed contains synthetic offline account, transaction,
payee, recurring-payment, and pending-payment records for user `usr_fin`.

The SQLite database is initialized from `init.sql` before the scenario starts.
It represents the state before any timeline mutation. Later changes are applied
only by the ordered world-controller releases.

The protected account is `acct_protected`; the ordinary checking account is
`acct_checking_main`; and the bill-pay sweep is `acct_billpay`. Values are
minor USD units. All records are synthetic and require no network access.
