# bilingual-city-culture-day Harbor environment

This environment is task-local and self-contained. It starts six MCP mock
services, a one-shot workspace initializer, and a world-controller. Seed SQL
is copied into this directory before build and is mounted read-only at
`/env-seed`; each mock service copies it into its own writable runtime volume.

The world-controller is the only component allowed to apply silent world
mutations **and the only writer of authoritative evaluation evidence**. It
shares the six runtime SQLite volumes, a read-only workspace source, and the
private writable `eval-evidence` volume. The main/agent service mounts the same
evidence at `/harbor/evidence:ro`; no other service has a writable evidence
mount. The agent reaches the mock services through MCP and never receives
controller credentials or release fixtures.

Before each turn, the step setup advances the shared historical-simulation
clock to the instruction timestamp and applies every release assigned to that
turn. The agent and all six mocks therefore observe the same frozen "now" and
the same complete pre-turn world. After the turn, Harbor uploads
`/logs/agent/trajectory.json`; the trusted main-service collector replaces
`/workspace/.harbor-stage/current` with only that turn's parsed
trajectory/response/trace. The world-controller then validates the step
metadata, captures the world through MCP, copies only non-hidden business files
with allowed suffixes, and atomically publishes append-only
`/evidence/stages/stage-N`. No mutation is applied between agent completion and
snapshot capture. Verifiers read only those stage directories.

Service MCP endpoints:

- `job-board` -> `http://job-board:8000/mcp`
- `email` -> `http://email:8000/mcp`
- `calendar` -> `http://calendar:8000/mcp`
- `legal-search` -> `http://legal-search:8000/mcp`
- `notion` -> `http://notion:8000/mcp`
- `notification-hub` -> `http://notification-hub:8000/mcp`

The six MCP mocks build from source vendored under `servers/<name>_mock/`;
compose declares `build:` for all nine services and pulls nothing beyond the
public `python:3.12-slim` base. The former `vibe-agent-benchmark/*_mock:latest`
tags were local-only and could not be pulled by a recipient. Credentials are
injected only by the runner; no credential appears in this task directory.
