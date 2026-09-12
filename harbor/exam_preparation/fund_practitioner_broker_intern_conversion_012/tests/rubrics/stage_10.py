from ._helpers import *

def s10_photo_privacy_official_only(env) -> bool:
    return h_s10_photo_privacy_official_only(env)

CHECKS = [
    ("s10_photo_privacy_official_only", s10_photo_privacy_official_only, 2.0),
]
