# Changelog

All notable changes to the public VibeLifeBench release are documented here.

## [1.0.0] - 2026-07-31

### Added

- Initial public release of the 20-task open subset across 10 life-admin domains.
- Long-horizon task timelines with 20–33 stages, silent world updates, authorization boundaries, and cross-service dependencies.
- Task-local synthetic environments for 21 services, plus 22 runnable mock-server packages and the Terrarium capability layer.
- Check-level scoring over authoritative backend state, agent-visible tool evidence, workspace deliverables, and cross-stage consistency.
- Reproducible evaluation tooling, locked dependencies, CI release gates, and public regression tests.

### Validated

- All task metadata, README metadata, and package metadata use release version `1.0.0`.
- Rubric checks bind evidence to the correct backend object and reject narration-only, wrong-object, stale-state, and write-as-read shortcuts.
- No backend-gate wrapper architecture or generated backend-gate modules are included in the release.
