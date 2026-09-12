"""notion_mock MCP server entry point (streamable-HTTP transport only).

v3 CLI: a single ``--env <path>`` flag. The env directory:

* holds the optional ``init.sql`` applied to a fresh sqlite DB,
* is also where the server writes its scratch ``runtime.db`` (wiped on
  every cold start).

No admin module, no clock advancement. Stage mutations go through
direct sqlite writes to ``<env>/runtime.db`` from the orchestrator.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import (
    BlockService,
    DatabaseService,
    PageService,
    SearchService,
    UserService,
)
from .tools import (
    register_block_tools,
    register_database_tools,
    register_page_tools,
    register_search_tools,
    register_stub_tools,
    register_user_tools,
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
    """Open a fresh runtime DB, apply schema + init.sql, return FastMCP."""
    db_file = env_dir / "runtime.db"
    for path in (db_file, db_file.with_suffix(".db-wal"), db_file.with_suffix(".db-shm")):
        if path.exists():
            path.unlink()

    conn = get_conn(str(db_file))
    init_schema(conn)

    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        apply_init_sql(conn, str(init_sql))

    page_service = PageService(conn)
    block_service = BlockService(conn)
    database_service = DatabaseService(conn)
    search_service = SearchService(conn)
    user_service = UserService(conn)

    mcp = FastMCP("notion-mock", host="0.0.0.0")
    register_page_tools(mcp, page_service)
    register_block_tools(mcp, block_service)
    register_database_tools(mcp, database_service)
    register_search_tools(mcp, search_service)
    register_user_tools(mcp, user_service)
    register_stub_tools(mcp)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(
        description="notion_mock MCP server (streamable-HTTP)"
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8008)
    parser.add_argument("--env", type=str, default=os.environ.get("XHS_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $XHS_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    if not args.env:
        parser.error("--env is required (pass --env <dir> or set $XHS_ENV)")
    env_dir = Path(args.env)
    if not env_dir.is_dir():
        logger.error("--env path is not a directory: %s", env_dir)
        sys.exit(2)

    try:
        mcp = build_server(env_dir)
        if args.transport == "stdio":
            logger.info("Starting notion-mock on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting notion-mock on http://%s:%d/mcp (env=%s)",
                args.host,
                args.port,
                env_dir,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception("Server startup failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
