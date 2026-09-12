# car_rental_mock

FastMCP mock server for self-drive rental-car scenarios. Runtime state is loaded
from an env directory's `init.sql` into a fresh SQLite database on startup.

The server is data-driven: vehicle models, pickup/return locations, insurance
plans, return rules, energy assumptions, and seeded offers all live in env SQL.

