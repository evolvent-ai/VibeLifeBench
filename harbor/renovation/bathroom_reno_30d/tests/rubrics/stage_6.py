"""Stage 6: engineering-document card transaction reconciliation."""
from .checks import s6_servers, s6_args, s6_result
CHECKS = [
    ("s6_servers", s6_servers, 0.25),
    ("s6_args", s6_args, 0.25),
    ("s6_result", s6_result, 2.0),
]
