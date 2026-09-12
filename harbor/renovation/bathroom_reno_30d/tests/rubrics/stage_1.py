"""Stage 1: source/time/status discipline and night-use risks."""
from .checks import s1_servers, s1_args, s1_result
CHECKS = [
    ("s1_servers", s1_servers, 0.25),
    ("s1_args", s1_args, 0.25),
    ("s1_result", s1_result, 1.5),
]
