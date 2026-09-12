from . import helpers as h

def check_s23_card_trace(env):
    return h.used_all(env,23,[("credit_card","get_card"),("credit_card","list_unbilled")])

def check_s23_card_backend(env):
    return h.highrisk_unbilled_seen(env) and (h.card_is_frozen(env,"card_tang_chengyu_black") or h.has_record(env,"security_incidents.json",stage=23,object_id="card_tang_chengyu_black",status="escalated"))

CHECKS = [
    ('s23_card_trace', check_s23_card_trace, 1.25),
    ('s23_card_backend', check_s23_card_backend, 1.75),
]
