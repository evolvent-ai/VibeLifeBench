"""job_board_mock MCP server entry point (streamable-HTTP transport only)."""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import (
    CatalogService,
    ChatService,
    SeekerService,
)
from .tools import (
    register_catalog_tools,
    register_chat_tools,
    register_seeker_tools,
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

    catalog_service = CatalogService(conn)
    seeker_service = SeekerService(conn)
    chat_service = ChatService(conn)

    mcp = FastMCP("job-board-mock", host="0.0.0.0")
    register_catalog_tools(mcp, catalog_service)
    register_seeker_tools(mcp, seeker_service)
    register_chat_tools(mcp, chat_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="job_board_mock MCP server (streamable-HTTP)")
    parser.add_argument("--env", type=str, default=os.environ.get("VLB_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $VLB_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8018)
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
            logger.info("Starting job-board-mock on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting job-board-mock on http://%s:%d/mcp (env=%s)",
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
