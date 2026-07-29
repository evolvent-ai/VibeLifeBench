# Changelog

All notable changes to the public VibeLifeBench release are documented here.

## [1.1.1] - 2026-07-29

### Fixed

- Corrected task rubric and environment issues across the 20-task open subset, including career audit loading, Weather location matching, and task-specific backend checks.
- Preserved nested Hotel and Flight MCP input schemas so agents receive structured guest, passenger, and payment fields.
- Made `scripts/run_eval.py --models-json` accept repository-relative and external absolute paths without raising `Path.relative_to()` errors.
- Replaced Hotel mock-server tests' dependency on a removed private `train_set` seed with a self-contained public SQL fixture.
- Preserved Hotel currencies through search, availability, reservation, retrieval, and cancellation responses.
- Fixed Hotel rate-plan ID round-tripping for valid seed-defined hotel prefixes such as `hotel_*` and `prov_*`.
- Exposed seeded future-dated Banking payments through a user-scoped, filterable `list_pending_payments` tool.
- Added deterministic one-stop Flight offer synthesis so seeded connecting routes are searchable and bookable.
- Made Hotel scenario-clock operations deterministic and removed the Python 3.12 `datetime.utcnow()` deprecation warning.

### Added

- Repository-level pytest development dependencies and release regression tests.
- Hotel and Flight MCP schema contract tests.
- A minimal continuous-integration gate for locked dependency sync, environment materialization, compilation, tests, and package builds.

### Removed

- Internal task-repair reports and stale task-local test suites that referenced private paths or conflicted during repository-wide pytest collection.
