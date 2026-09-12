"""hotel_booking_mock MCP server entry point (streamable-HTTP transport only)."""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import get_conn, init_schema
from .services import (
    AvailabilityService,
    CatalogService,
    GuestService,
    ReservationService,
)
from .tools import (
    register_availability_tools,
    register_catalog_tools,
    register_guest_tools,
    register_reservation_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def build_server(env_dir: Path) -> FastMCP:
    """Cold-boot the DB from <env>/init.sql and register agent-facing tools."""
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    for sidecar in (env_dir / "runtime.db-wal", env_dir / "runtime.db-shm"):
        if sidecar.exists():
            sidecar.unlink()

    conn = get_conn(str(db_file))
    init_schema(conn)

    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        conn.executescript(init_sql.read_text(encoding="utf-8"))

    catalog_service = CatalogService(conn)
    availability_service = AvailabilityService(conn)
    reservation_service = ReservationService(conn)
    guest_service = GuestService(conn)

    mcp = FastMCP("hotel-booking-mock", host="0.0.0.0")
    register_catalog_tools(mcp, catalog_service)
    register_availability_tools(mcp, availability_service)
    register_reservation_tools(mcp, reservation_service)
    register_guest_tools(mcp, guest_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(
        description="hotel_booking_mock MCP server (streamable-HTTP)"
    )
    parser.add_argument("--env", type=str, default=os.environ.get("XHS_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $XHS_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    if not args.env:
        parser.error("--env is required (pass --env <dir> or set $XHS_ENV)")

    try:
        mcp = build_server(Path(args.env))
        if args.transport == "stdio":
            logger.info("Starting hotel-booking-mock on stdio (env=%s)", args.env)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting hotel-booking-mock on http://%s:%d/mcp (env=%s)",
                args.host, args.port, args.env,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception("Server startup failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
