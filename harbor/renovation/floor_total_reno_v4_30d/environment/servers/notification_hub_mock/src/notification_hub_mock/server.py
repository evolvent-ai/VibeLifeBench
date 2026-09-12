"""notification_hub_mock MCP server entry point (streamable-HTTP transport only)."""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import (
    AlertService,
    NotificationService,
    OfficialAccountService,
    SubscriptionService,
)
from .tools import (
    register_account_tools,
    register_alert_tools,
    register_notification_tools,
    register_subscription_tools,
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

    subscription_service = SubscriptionService(conn)
    notification_service = NotificationService(conn)
    alert_service = AlertService(conn)
    account_service = OfficialAccountService(conn)

    MCP = FastMCP("notification-hub-mock", host="0.0.0.0")
    register_subscription_tools(MCP, subscription_service)
    register_notification_tools(MCP, notification_service)
    register_alert_tools(MCP, alert_service)
    register_account_tools(MCP, account_service)
    return MCP


def main() -> None:
    parser = argparse.ArgumentParser(
        description="notification_hub_mock MCP server (streamable-HTTP)"
    )
    parser.add_argument("--env", type=str, default=os.environ.get("XHS_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $XHS_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .MCP.json debugging")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8005)
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
        MCP = build_server(db_path=str(db_file), init_sql=init_sql_path)
        if args.transport == "stdio":
            logger.info("Starting notification-hub-mock on stdio (env=%s)", env_dir)
            MCP.run(transport="stdio")
        else:
            MCP.settings.host = args.host
            MCP.settings.port = args.port
            logger.info(
                "Starting notification-hub-mock on http://%s:%d/MCP (env=%s)",
                args.host, args.port, env_dir,
            )
            MCP.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception("Server startup failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
