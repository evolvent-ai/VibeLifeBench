"""FastMCP server entrypoint - streamable-http only.

v3: single ``--env`` flag. The env directory may contain an ``init.sql``
that is executed against a brand-new SQLite file on every cold start.
There is no clock, no admin path, no bundled seed.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import AccountService, FundService, MarketService, OrderService
from .tools import (
    register_account_tools,
    register_fund_tools,
    register_market_tools,
    register_order_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def build_server(env_dir: Path) -> FastMCP:
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
    for sidecar in (
        db_file.with_suffix(db_file.suffix + "-wal"),
        db_file.with_suffix(db_file.suffix + "-shm"),
    ):
        if sidecar.exists():
            sidecar.unlink()

    conn = get_conn(str(db_file))
    init_schema(conn)

    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        apply_init_sql(conn, str(init_sql))
    else:
        logger.info("No init.sql in %s; starting with empty tables", env_dir)

    market_service = MarketService(conn)
    account_service = AccountService(conn, market_service)
    order_service = OrderService(conn, market_service)
    fund_service = FundService(conn)

    mcp = FastMCP("brokerage-mock", host="0.0.0.0")
    register_account_tools(mcp, account_service)
    register_market_tools(mcp, market_service)
    register_order_tools(mcp, order_service)
    register_fund_tools(mcp, fund_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Brokerage MCP Mock Server")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8003)
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
        mcp = build_server(env_dir=Path(args.env))
        if args.transport == "stdio":
            logger.info("Starting brokerage_mock MCP server on stdio")
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting brokerage_mock MCP server on http://%s:%d/mcp (streamable-http)",
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
