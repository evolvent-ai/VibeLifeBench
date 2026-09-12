# rail_booking_mock

FastMCP mock server for China rail search and booking scenarios. It is intentionally small:
it supports train search, offer pricing, booking, cancellation, booking lists, train status,
and student passenger profiles for quota/verification checks.

Runtime data is loaded from `/env-seed/init.sql` into a fresh SQLite database on startup.
