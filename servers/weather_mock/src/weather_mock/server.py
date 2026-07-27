"""weather_mock MCP server entry point (streamable-HTTP transport only)."""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import SQLiteBackend
from .services import (
    AlertsService,
    AQIService,
    TyphoonService,
    WeatherService,
)
from .tools import (
    register_alert_tools,
    register_aqi_tools,
    register_typhoon_tools,
    register_weather_tools,
)


def _setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Weather Mock MCP Server (streamable-HTTP)")
    ap.add_argument("--env", type=str, default=os.environ.get("XHS_ENV"),
                    help="Path to envs/<server>/<env_name>/ directory (falls back to $XHS_ENV)")
    ap.add_argument("--transport", choices=["streamable-http", "stdio"],
                    default="streamable-http",
                    help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8011)
    ap.add_argument("--debug", action="store_true")
    return ap.parse_args(argv)


def build_server(env_dir: Path) -> tuple[FastMCP, SQLiteBackend]:
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    for sidecar in (env_dir / "runtime.db-wal", env_dir / "runtime.db-shm"):
        if sidecar.exists():
            sidecar.unlink()

    be = SQLiteBackend(str(db_file))

    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        be.apply_init_sql(str(init_sql))

    workspace_root = os.environ.get("AGENT_WORKSPACE")
    alerts = AlertsService(be, workspace_root=workspace_root)
    aqi = AQIService(be)
    typhoons = TyphoonService(be)
    weather = WeatherService(be)

    mcp = FastMCP("weather-mock", host="0.0.0.0")
    register_weather_tools(mcp, weather)
    register_alert_tools(mcp, alerts)
    register_aqi_tools(mcp, aqi)
    register_typhoon_tools(mcp, typhoons)

    return mcp, be


def main() -> None:
    args = _parse_args()
    _setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    if not args.env:
        raise SystemExit("--env is required (pass --env <dir> or set $XHS_ENV)")

    be = None
    try:
        mcp, be = build_server(Path(args.env))
        if args.transport == "stdio":
            logger.info("Starting weather-mock on stdio (env=%s)", args.env)
            mcp.run(transport="stdio")
        else:
            mcp.settings.host = args.host
            mcp.settings.port = args.port
            logger.info(
                "Starting weather-mock on http://%s:%d/mcp (env=%s)",
                args.host, args.port, args.env,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("shutdown requested")
    except Exception as e:
        logger.error("server startup failed: %s", e, exc_info=True)
        sys.exit(1)
    finally:
        try:
            if be is not None:
                be.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
