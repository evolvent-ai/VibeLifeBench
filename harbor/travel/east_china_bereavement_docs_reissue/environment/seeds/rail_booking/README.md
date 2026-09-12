# rail_booking task-local seed

This offline synthetic rail_booking environment supports the East China bereavement travel and document reissue scenario. The scenario window is 2026-04-03 through 2026-04-27 in Asia/Shanghai.

`init.sql` defines the stage-zero SQLite state. Any `mutation_*.sql` files are retained as source references; the world-controller applies their equivalent structured operations at the mapped release boundary. Data is synthetic and contains no real personal information.
