from . import _helpers as h

def s11_counselor_integrity_mail_read(env):
    return h.s11_counselor_integrity_mail_read(env)

CHECKS = [
    ("s11_counselor_integrity_mail_read", s11_counselor_integrity_mail_read, 1.5),
]
