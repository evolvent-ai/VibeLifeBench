from . import _helpers as h

def s3_unofficial_room_downgraded(env):
    return h.s3_unofficial_room_downgraded(env)

CHECKS = [
    ("s3_unofficial_room_downgraded", s3_unofficial_room_downgraded, 1.5),
]
