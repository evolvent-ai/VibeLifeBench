"""Stage 0: baseline sources, three lines and elderly-safety setup."""
from .checks import s0_servers, s0_args, s0_result, s0_files
CHECKS = [
    ("s0_servers", s0_servers, 0.25),
    ("s0_args", s0_args, 0.25),
    ("s0_result", s0_result, 1.5),
    ("s0_files", s0_files, 1.5),
]
