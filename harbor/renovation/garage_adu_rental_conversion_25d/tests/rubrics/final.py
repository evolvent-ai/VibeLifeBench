from ._helpers import final_contract


def final_zoning_permit_closure(env) -> bool:
    return final_contract(env, 'zoning')


def final_no_false_description(env) -> bool:
    return final_contract(env, 'no_false_description')


def final_cash_contract_boundary(env) -> bool:
    return final_contract(env, 'cash_reject')


def final_budget_payback_separated(env) -> bool:
    return final_contract(env, 'budget')


def final_contractor_contract_ready(env) -> bool:
    return final_contract(env, 'contractor')


def final_materials_code_ready(env) -> bool:
    return final_contract(env, 'materials')


def final_parking_neighbor_record(env) -> bool:
    return final_contract(env, 'parking_neighbor')


def final_inspection_pass_evidence(env) -> bool:
    return final_contract(env, 'inspection_pass')


def final_calendar_handoff(env) -> bool:
    return final_contract(env, 'calendar')


CHECKS = [
    ("final_zoning_permit_closure", final_zoning_permit_closure, 2.0),
    ("final_no_false_description", final_no_false_description, 2.0),
    ("final_cash_contract_boundary", final_cash_contract_boundary, 1.5),
    ("final_budget_payback_separated", final_budget_payback_separated, 1.5),
    ("final_contractor_contract_ready", final_contractor_contract_ready, 1.5),
    ("final_materials_code_ready", final_materials_code_ready, 1.5),
    ("final_parking_neighbor_record", final_parking_neighbor_record, 1.5),
    ("final_inspection_pass_evidence", final_inspection_pass_evidence, 1.5),
    ("final_calendar_handoff", final_calendar_handoff, 1.0),
]
