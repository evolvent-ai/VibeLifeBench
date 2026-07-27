"""calendar_mock MCP server entry point (streamable-HTTP transport only)."""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import get_conn, init_schema
from .services import CalendarService, EventService
from .tools import register_calendar_tools, register_event_tools


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def build_server(env_dir: Path) -> FastMCP:
    """Open a fresh runtime DB inside the env, apply schema + init.sql, return FastMCP."""
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

    calendar_service = CalendarService(conn)
    event_service = EventService(conn)

    mcp = FastMCP("calendar-mock", host="0.0.0.0")
    register_calendar_tools(mcp, calendar_service)
    register_event_tools(mcp, event_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="calendar_mock MCP server (streamable-HTTP)")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8007)
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
        mcp = build_server(env_dir)
        if args.transport == "stdio":
            logger.info("Starting calendar-mock on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting calendar-mock on http://%s:%d/mcp (streamable-http, env=%s)",
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
