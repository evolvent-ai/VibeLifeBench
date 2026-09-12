from __future__ import annotations
from ._helpers import *

def s12_prepare_truthful_hr_proof_draft(env) -> bool:
    return run_stage_requirement(env, 's12_prepare_truthful_hr_proof_draft')

def s12_no_false_contract_proof(env) -> bool:
    return run_stage_requirement(env, 's12_no_false_contract_proof')

CHECKS = [
    ('s12_prepare_truthful_hr_proof_draft', s12_prepare_truthful_hr_proof_draft, 2.0),
    ('s12_no_false_contract_proof', s12_no_false_contract_proof, 2.0),
]
