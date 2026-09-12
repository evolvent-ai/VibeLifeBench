from . import helpers as h

def check_s3_legal_mail_trace(env):
    return h.used_all(env,3,[("email","search_emails"),("email","read_email")])

def check_s3_divorce_record(env):
    return h.has_record(env,"risk_register.json",stage=3,object_id="divorce_disclosure",decision="pending_counsel") or h.has_record(env,"due_diligence_log.json",stage=3,object_id="divorce_disclosure",decision="pending_counsel")

CHECKS = [
    ('s3_legal_mail_trace', check_s3_legal_mail_trace, 1.25),
    ('s3_divorce_record', check_s3_divorce_record, 1.5),
]
