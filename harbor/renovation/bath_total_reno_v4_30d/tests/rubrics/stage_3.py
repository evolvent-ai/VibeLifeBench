"""Stage 3: quality claim intake; no artificial server call ordering."""
from .checks import s3_servers, s3_args, s3_result
CHECKS = [
    ("s3_servers", s3_servers, 0.25),
    ("s3_args", s3_args, 0.25),
    ("s3_result", s3_result, 3.0),
]
