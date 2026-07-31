"""Date / time helpers.

v3: no simulated clock. ``DEFAULT_WRITE_TIME`` is the fixed timestamp the
server stamps on writes when init.sql has not supplied one. Tasks that
care about per-stage timestamps set them via event-yaml mutations.
"""

DEFAULT_WRITE_TIME = "2026-01-01T00:00:00.000Z"
