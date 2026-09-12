from . import helpers as h

def check_s11_underlier_trace(env):
    return h.used_all(env,11,[("email","search_emails"),("email","read_email"),("brokerage","list_funds")])

def check_s11_note_block_backend(env):
    return h.has_record(env,"due_diligence_log.json",stage=11,object_id="pb_note_12pct",decision="blocked") and h.has_record(env,"risk_register.json",stage=11,object_id="subordinated_property_receivable",decision="blocked") and h.no_new_broker_filled_orders(env)

CHECKS = [
    ('s11_underlier_trace', check_s11_underlier_trace, 1.25),
    ('s11_note_block_backend', check_s11_note_block_backend, 2.0),
]
