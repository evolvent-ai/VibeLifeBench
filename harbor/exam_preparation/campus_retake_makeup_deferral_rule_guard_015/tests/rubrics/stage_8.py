from . import _helpers as h

def s8_initial_room_tentative(env):
    return h.s8_initial_room_tentative(env)

CHECKS = [
    ("s8_initial_room_tentative", s8_initial_room_tentative, 1.25),
]
