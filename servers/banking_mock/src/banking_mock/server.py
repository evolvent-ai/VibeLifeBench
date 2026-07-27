"""banking_mock MCP server entry point (streamable-HTTP transport only)."""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import (
    AccountService,
    PayeeService,
    RecurringService,
    TransferService,
)
from .tools import (
    register_account_tools,
    register_payee_tools,
    register_recurring_tools,
    register_transfer_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def build_server(db_path: str, init_sql: str | None) -> FastMCP:
    """Open the DB, optionally apply init_sql, register tools, return FastMCP."""
    conn = get_conn(db_path)
    init_schema(conn)
    if init_sql:
        apply_init_sql(conn, init_sql)

    account_service = AccountService(conn)
    transfer_service = TransferService(conn)
    payee_service = PayeeService(conn)
    recurring_service = RecurringService(conn)

    mcp = FastMCP("banking-mock", host="0.0.0.0")
    register_account_tools(mcp, account_service)
    register_transfer_tools(mcp, transfer_service)
    register_payee_tools(mcp, payee_service)
    register_recurring_tools(mcp, recurring_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="banking_mock MCP server")
    parser.add_argument("--env", type=str, default=os.environ.get("VLB_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory "
                             "(falls back to $VLB_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; "
                             "stdio for local .mcp.json debugging")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    if not args.env:
        parser.error("--env is required (pass --env <dir> or set $VLB_ENV)")
    env_dir = Path(args.env)
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    for sidecar in (str(db_file) + "-wal", str(db_file) + "-shm"):
        if os.path.exists(sidecar):
            os.remove(sidecar)

    init_sql = env_dir / "init.sql"
    init_sql_path = str(init_sql) if init_sql.exists() else None

    try:
        mcp = build_server(db_path=str(db_file), init_sql=init_sql_path)
        if args.transport == "stdio":
            logger.info("Starting banking-mock on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting banking-mock on http://%s:%d/mcp (env=%s)",
                args.host, args.port, env_dir,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception("Server startup failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
