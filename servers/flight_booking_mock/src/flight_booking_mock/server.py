"""FastMCP entry point for flight-booking-mock (streamable-HTTP only)."""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends.sqlite_backend import SQLiteBackend
from .config import AppConfig, parse_args
from .services import (
    BookingService,
    PricingService,
    SearchService,
    StatusService,
)
from .tools import (
    register_booking_tools,
    register_pricing_tools,
    register_search_tools,
    register_status_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def build_server(cfg: AppConfig) -> tuple[FastMCP, SQLiteBackend]:
    """Cold-boot the DB from <env>/init.sql and wire up MCP tools."""
    env_dir = Path(cfg.env)
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    # Drop stale wal/shm sidecars too — sqlite leaves them behind on crash.
    for sidecar in (env_dir / "runtime.db-wal", env_dir / "runtime.db-shm"):
        if sidecar.exists():
            sidecar.unlink()

    backend = SQLiteBackend(str(db_file))

    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        backend.apply_init_sql(str(init_sql))

    search_service = SearchService(backend)
    pricing_service = PricingService(backend)
    booking_service = BookingService(backend)
    status_service = StatusService(backend)

    mcp = FastMCP("flight-booking-mock", host="0.0.0.0")
    register_search_tools(mcp, search_service)
    register_pricing_tools(mcp, pricing_service)
    register_booking_tools(mcp, booking_service)
    register_status_tools(mcp, status_service)
    return mcp, backend


def main() -> None:
    cfg = parse_args()
    setup_logging(cfg.debug)
    logger = logging.getLogger(__name__)

    try:
        mcp, _backend = build_server(cfg)
        if cfg.transport == "stdio":
            logger.info("Starting flight-booking-mock on stdio (env=%s)", cfg.env)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = cfg.host
            mcp.settings.port = cfg.port
            logger.info(
                "Starting flight-booking-mock on http://%s:%d/mcp (env=%s)",
                cfg.host, cfg.port, cfg.env,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Server startup failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
