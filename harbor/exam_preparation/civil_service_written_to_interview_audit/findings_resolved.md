# Resolved Findings

This environment window records the historical findings resolved by the current
task bundle. Line numbers refer to the delivered files after the repair.

- Round 4 QC collector `NameError`: `environment/evidence-collector/collector.py:285-317` now defines `_session_mcp_calls` before the `main()` entrypoint at line 320 and includes a regression-safe empty-log path at lines 163-165, so event-000 produces metadata and a parseable empty trace.
- Round 5 collector follow-up: `environment/evidence-collector/collector.py:320-323` keeps the `__main__` guard immediately after `main()` and removes the stale duplicate helper that had followed the guard; the single helper definition at `environment/evidence-collector/collector.py:285-317` is therefore the bound implementation used by the executable entrypoint. `/data/pipeline/tools/test_collector_trace.py` passes the positive MCP extraction test, and an empty-trajectory regression creates `metadata.json`, `trace.json`, `response.txt`, and `trajectory.json`.
- Round 5 smoke recheck: the required runtime nop smoke completed all 25 steps with every main collector and world-controller snapshot successful; the previously reported maps dependency failure did not reproduce after the current vendored server and seed bundle were started from a clean compose project.
- Round 3 oracle stage-18 and stage-21 checks: the stage-18/21 handlers are already present in the upstream task steps and the current environment preserves the required email and confirmation state without altering `steps/`.
- Round 2 oracle checks: the current bundle preserves all stage-specific service seeds, workspace records, and ordered releases in `environment/world-controller/releases/`, with release application controlled by the complete `controller.py`.
- Round 1 smoke maps startup: `environment/servers/maps_mock/` is vendored from the canonical server and its seed is mounted read-only at `environment/docker-compose.yaml:121-142`; the maps service has the same healthcheck and world-clock contract as the other mocks.
- Round 3/4 smoke environment failures: `environment/docker-compose.yaml` uses task-local `build:` contexts for every service, maps all nine runtime volumes, and injects `WORLD_CLOCK_FILE` into every clock-reading mock.
- Round 1-5 verify language and lexicon findings: all delivered environment files are English-only (`environment/` has zero Han characters), while glossary-aligned domain terms remain in seeds, workspace records, and release values.
