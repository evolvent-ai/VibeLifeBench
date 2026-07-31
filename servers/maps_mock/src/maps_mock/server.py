"""maps_mock MCP server entry point (streamable-HTTP transport only).

v3: single ``--env`` flag. The env directory may contain an ``init.sql``
that is executed against a brand-new SQLite file on every cold start.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import (
    SqliteBackend,
    apply_init_sql,
    ensure_db,
)
from .services import (
    DirectionsService,
    GeocodeService,
    PlacesService,
    TrafficService,
    TransitService,
)
from .tools import (
    register_directions_tools,
    register_geocode_tools,
    register_places_tools,
    register_transit_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def build_server(env_dir: Path) -> tuple[FastMCP, SqliteBackend]:
    """Cold-start the server from an env directory.

    - ``env_dir/runtime.db`` is unlinked if present, then re-created.
    - The package schema is applied.
    - ``env_dir/init.sql`` is executed if it exists.
    """
    logger = logging.getLogger(__name__)
    env_dir = Path(env_dir)
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    for sidecar in (db_file.with_suffix(db_file.suffix + "-wal"),
                    db_file.with_suffix(db_file.suffix + "-shm")):
        if sidecar.exists():
            sidecar.unlink()

    backend = ensure_db(str(db_file))

    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        logger.info("Applying init_sql from %s", init_sql)
        apply_init_sql(backend, str(init_sql))

    geocode = GeocodeService(backend)
    places = PlacesService(backend)
    traffic = TrafficService(backend)
    transit = TransitService(backend, geocode)
    directions = DirectionsService(backend, geocode, traffic, transit)

    mcp = FastMCP("maps-mock", host="0.0.0.0")
    register_geocode_tools(mcp, geocode)
    register_places_tools(mcp, places)
    register_directions_tools(mcp, directions)
    register_transit_tools(mcp, transit, traffic, directions)
    return mcp, backend


def main() -> None:
    parser = argparse.ArgumentParser(
        description="maps_mock MCP server (streamable-HTTP)"
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8012)
    parser.add_argument(
        "--env",
        type=str,
        default=os.environ.get("VLB_ENV"),
        help="Path to envs/<server>/<env_name>/ directory (falls back to $VLB_ENV)",
    )
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    if not args.env:
        parser.error("--env is required (pass --env <dir> or set $VLB_ENV)")

    try:
        mcp, _backend = build_server(env_dir=Path(args.env))
        if args.transport == "stdio":
            logger.info("Starting maps-mock on stdio")
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting maps-mock on http://%s:%d/mcp (streamable-http)",
                args.host,
                args.port,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception("Server startup failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
