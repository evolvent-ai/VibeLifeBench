"""FastMCP server entry-point for delivery_logistics_mock.

Wires the SQLite backend, the service layer, and the agent-facing tools
onto a FastMCP instance and runs it on streamable-http transport. Takes
a single ``--env <path>`` flag (v3 contract): a fresh runtime DB is
created inside ``<env>/runtime.db`` on every cold start, the bundled
schema is applied, then any ``<env>/init.sql`` is executed.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import get_conn, init_schema
from .services import (
    IssueService,
    PickupService,
    ShipmentService,
    SubscriptionService,
    TrackingService,
)
from .tools import (
    register_issue_tools,
    register_pickup_tools,
    register_shipment_tools,
    register_subscription_tools,
    register_tracking_tools,
)

DEFAULT_PORT = 8005


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def build_server(
    env_dir: Path,
    *,
    host: str = "0.0.0.0",
    port: int = DEFAULT_PORT,
) -> FastMCP:
    """Create the FastMCP server, initialise the DB, and register all tools."""
    logger = logging.getLogger(__name__)

    db_file = env_dir / "runtime.db"
    for sidecar in (db_file, db_file.with_suffix(db_file.suffix + "-wal"),
                    db_file.with_suffix(db_file.suffix + "-shm")):
        if sidecar.exists():
            sidecar.unlink()

    conn = get_conn(str(db_file))
    init_schema(conn)
    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        logger.info("Applying init_sql from %s", init_sql)
        conn.executescript(init_sql.read_text(encoding="utf-8"))

    tracking = TrackingService(conn)
    shipments = ShipmentService(conn)
    pickups = PickupService(conn)
    issues = IssueService(conn)
    subs = SubscriptionService(conn)

    mcp = FastMCP(
        "delivery-logistics-mock",
        host=host,
        port=port,
        streamable_http_path="/mcp",
    )
    register_tracking_tools(mcp, tracking)
    register_shipment_tools(mcp, shipments)
    register_pickup_tools(mcp, pickups)
    register_issue_tools(mcp, issues)
    register_subscription_tools(mcp, subs)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Delivery Logistics MCP Mock Server")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--env", type=str, default=os.environ.get("VLB_ENV"),
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
    env_dir = Path(args.env).resolve()
    if not env_dir.is_dir():
        logger.error("env path is not a directory: %s", env_dir)
        sys.exit(2)

    try:
        mcp = build_server(env_dir, host=args.host, port=args.port)
        if args.transport == "stdio":
            logger.info("Starting delivery_logistics_mock on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            logger.info(
                "Starting delivery_logistics_mock on streamable-http %s:%d (env=%s)",
                args.host,
                args.port,
                env_dir,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception(f"Server startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
