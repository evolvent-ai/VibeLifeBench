from __future__ import annotations
from ._helpers import derived_text, has_exact_number, severance_deposit_minor, text_has, used_tool

def s17_severance_paid_backend(env) -> bool:
    return used_tool(env, 'list_transactions', stage=17, arg_substr='acct_gk_checking') and s17_paid_amount_reconciled(env)

def s17_paid_amount_reconciled(env) -> bool:
    raw = derived_text(env)
    if not raw.strip():
        return False
    dim_paid = severance_deposit_minor(env, stage=17) == 20080000 and has_exact_number(raw, 200800)
    dim_gap = text_has(raw, [['shortfall-alternative-27', 'reduced', 'refund', 'receive', 'deposited', 'payment', 'calculated', 'low', 'very', 'remaining-alternative-28', 'standard-alternative-29', 'withholding-alternative-30', 'reduced-alternative-31', 'than', 'below', 'under', 'only', 'reached', 'recently', 'full', 'nearly', 'using', 'base', 'contractual', 'reduced-alternative-32', 'under-alternative-33', 'payment-alternative-34', 'than-alternative-35', 'below-alternative-36', 'short', 'shortfall-alternative-37', 'reduced-alternative-38']])
    dim_fix = text_has(raw, [['amount', 'need', 'must', 'difference', 'remaining-alternative-39', 'remaining-alternative-40', 'complete', 'back', 'recover', 'recovering', 'yet', 'paid-alternative-41', 'still', 'further', 'supplemental', 'remaining-alternative-42', 'remaining-alternative-43', 'request-alternative-44', 'negotiated-alternative-45', 'claims', 'pursue-alternative-46', 'apply', 'lawful-alternative-47', 'not paid in full alternative 5623982', 'payable', 'payable-alternative-48', 'remaining-alternative-49', 'supplemental-alternative-50', 'supplement', 'should pay']])
    return dim_paid and dim_gap and dim_fix
CHECKS = [('s17_severance_paid_backend', s17_severance_paid_backend, 1.5), ('s17_paid_amount_reconciled', s17_paid_amount_reconciled, 3.0)]
