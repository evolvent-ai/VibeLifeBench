# Resolved Findings

- Previous env smoke setup failure (HTTP proxy sent internal controller calls to the proxy and returned 502): added controller readiness polling and explicit `NO_PROXY`/`no_proxy` entries in all step setup scripts, for example `steps/event-000/workdir/setup.sh:7-14` and the corresponding lines in `steps/event-001` through `steps/event-023`.
- Release-bound smoke failure (release requests returned HTTP 403): corrected the release token headers to match the authoritative release JSON tokens, for example `steps/event-004/workdir/setup.sh:15` and the corresponding release-bound setup scripts.
- Release mutation failure (attached service databases reported WAL mode): retained the DELETE journal contract in all vendored mock database backends and invalidated stale image layers with the explicit contract comment, for example `environment/servers/calendar_mock/src/calendar_mock/backends/db.py:17` and the corresponding seven backend files.
