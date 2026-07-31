"""Configuration dataclass for the flight booking mock server."""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfig:
    env: str
    host: str
    port: int
    debug: bool
    transport: str


def parse_args(argv: Optional[list[str]] = None) -> AppConfig:
    parser = argparse.ArgumentParser(
        description="flight-booking-mock MCP server (streamable-HTTP)"
    )
    parser.add_argument("--env", type=str, default=os.environ.get("VLB_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $VLB_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8009)
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")

    args = parser.parse_args(argv)
    if not args.env:
        parser.error("--env is required (pass --env <dir> or set $VLB_ENV)")
    return AppConfig(
        env=args.env,
        host=args.host,
        port=args.port,
        debug=args.debug,
        transport=args.transport,
    )
