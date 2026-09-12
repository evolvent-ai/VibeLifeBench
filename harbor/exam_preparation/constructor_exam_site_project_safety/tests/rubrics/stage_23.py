from ._helpers import response_check_id, structured_check_id

def s23_final_notion_handover(env) -> bool:
    return response_check_id(env, 's23_final_notion_handover')

def s23_final_email_draft(env) -> bool:
    return response_check_id(env, 's23_final_email_draft')

CHECKS = [
    ('s23_final_notion_handover', s23_final_notion_handover, 1.0),
    ('s23_final_email_draft', s23_final_email_draft, 1.0),
]
