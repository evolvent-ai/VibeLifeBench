"""Stage 7: partial-refund offer and elderly-safety rights impact."""
from .checks import s7_servers, s7_args, s7_result
CHECKS = [
    ("s7_servers", s7_servers, 0.25),
    ("s7_args", s7_args, 0.25),
    ("s7_result", s7_result, 1.5),
]
