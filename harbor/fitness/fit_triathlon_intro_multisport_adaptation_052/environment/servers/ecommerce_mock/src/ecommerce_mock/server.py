"""ecommerce-mock entry point.

Boots a FastMCP server that speaks ONLY streamable-http. The server has
no simulated clock and no admin CLI; the v3 orchestrator drives all
stage-level state changes through `mutation` events.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .backends import apply_init_sql, get_conn, init_schema
from .services import (
    CartService,
    CatalogService,
    CouponService,
    OrderService,
    RefundService,
)
from .tools import (
    register_cart_tools,
    register_catalog_tools,
    register_coupon_tools,
    register_order_tools,
    register_refund_tools,
)


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def build_server(db_path: str, init_sql: str | None, host: str, port: int) -> FastMCP:
    """Create the FastMCP server: init the DB, optionally apply init_sql,
    construct services, and register all tools.
    """
    conn = get_conn(db_path)
    init_schema(conn)
    if init_sql:
        apply_init_sql(conn, init_sql)

    catalog_service = CatalogService(conn)
    coupon_service = CouponService(conn)
    cart_service = CartService(conn, coupon_service=coupon_service)
    # cyclic injection (cart needs coupon for view; coupon needs cart to
    # return refreshed view to the agent on apply/remove).
    coupon_service.cart_service = cart_service
    order_service = OrderService(conn, cart_service=cart_service, coupon_service=coupon_service)
    refund_service = RefundService(conn)

    mcp = FastMCP(
        "ecommerce-mock",
        host=host,
        port=int(port),
        streamable_http_path="/mcp",
    )
    register_catalog_tools(mcp, catalog_service)
    register_cart_tools(mcp, cart_service)
    register_coupon_tools(mcp, coupon_service)
    register_order_tools(mcp, order_service)
    register_refund_tools(mcp, refund_service)
    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="ecommerce-mock MCP server (streamable-http)")
    parser.add_argument("--env", type=str, default=os.environ.get("XHS_ENV"),
                        help="Path to envs/<server>/<env_name>/ directory (falls back to $XHS_ENV)")
    parser.add_argument("--transport", choices=["streamable-http", "stdio"],
                        default="streamable-http",
                        help="streamable-http for Terrarium/containers; stdio for local .mcp.json debugging")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8004)
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
            logger.info("ecommerce-mock starting on stdio (env=%s)", env_dir)
            mcp.run(transport="stdio")
        else:
            logger.info(
                "ecommerce-mock starting on http://%s:%d/mcp (env=%s)",
                args.host, args.port, env_dir,
            )
            mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("server shutdown requested")
    except Exception as exc:  # noqa: BLE001
        logger.exception("server startup failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
