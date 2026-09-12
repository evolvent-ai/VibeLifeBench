"""credit_card_mock MCP server entry point (streamable-HTTP transport only)."""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import (
    CardService,
    DisputeService,
    PaymentService,
    RewardsService,
    StatementService,
)
from .tools import (
    register_card_tools,
    register_dispute_tools,
    register_payment_tools,
    register_rewards_tools,
    register_statement_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def build_server(db_path: str, init_sql: str | None, host: str, port: int) -> FastMCP:
    conn = get_conn(db_path)
    init_schema(conn)
    if init_sql:
        apply_init_sql(conn, init_sql)

    card_service = CardService(conn)
    statement_service = StatementService(conn)
    payment_service = PaymentService(conn)
    dispute_service = DisputeService(conn)
    rewards_service = RewardsService(conn)

    mcp = FastMCP("credit-card-mock", host=host, port=port)
    register_card_tools(mcp, card_service)
    register_statement_tools(mcp, statement_service)
    register_payment_tools(mcp, payment_service)
    register_dispute_tools(mcp, dispute_service)
    register_rewards_tools(mcp, rewards_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Credit Card MCP Mock Server (streamable-HTTP)")
    parser.add_argument("--env", type=str, default=os.environ.get("XHS_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $XHS_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8002)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    if not args.env:
        parser.error("--env is required (pass --env <dir> or set $XHS_ENV)")
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
        mcp = build_server(
            db_path=str(db_file),
            init_sql=init_sql_path,
            host=args.host,
            port=args.port,
        )
        if args.transport == "stdio":
            logger.info("Starting credit_card_mock on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            logger.info(
                "Starting credit_card_mock on http://%s:%d/mcp (env=%s)",
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
