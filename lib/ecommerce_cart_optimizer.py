from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from itertools import combinations, product
import json
from pathlib import Path
import re
import sqlite3
from typing import Iterable


_SEED_TABLE = re.compile(
    r"\bINSERT(?:\s+OR\s+\w+)?\s+INTO\s+(products|skus|stocks|coupons)\b",
    re.IGNORECASE,
)

_MINIMAL_SCHEMA = """
CREATE TABLE products (
  product_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  brand TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT NOT NULL,
  rating REAL NOT NULL,
  rating_count INTEGER NOT NULL,
  sales_count INTEGER NOT NULL,
  base_price_minor INTEGER NOT NULL,
  return_policy TEXT NOT NULL
);
CREATE TABLE skus (
  sku_id TEXT PRIMARY KEY,
  product_id TEXT NOT NULL,
  attrs_json TEXT NOT NULL,
  price_minor INTEGER NOT NULL
);
CREATE TABLE stocks (
  sku_id TEXT PRIMARY KEY,
  quantity INTEGER NOT NULL
);
CREATE TABLE coupons (
  code TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  value_bp_or_minor INTEGER NOT NULL,
  min_spend_minor INTEGER NOT NULL,
  valid_from TEXT NOT NULL,
  valid_until TEXT NOT NULL,
  category_restriction TEXT,
  max_uses INTEGER NOT NULL,
  used_count INTEGER NOT NULL,
  active INTEGER NOT NULL
);
"""


@dataclass(frozen=True)
class CartPlan:
    sku_ids: frozenset[str]
    product_titles: frozenset[str]
    coupon_codes: frozenset[str]
    subtotal_minor: int
    total_minor: int


def _complete_statements(sql: str) -> Iterable[str]:
    buffer = ""
    for line in sql.splitlines(keepends=True):
        buffer += line
        if sqlite3.complete_statement(buffer):
            statement = buffer.strip()
            buffer = ""
            if statement:
                yield statement
    if buffer.strip():
        raise ValueError("incomplete SQL statement in ecommerce seed")


def _load_seed(init_sql_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(_MINIMAL_SCHEMA)
    try:
        sql = init_sql_path.read_text(encoding="utf-8")
        for statement in _complete_statements(sql):
            if _SEED_TABLE.search(statement):
                conn.execute(statement)
    except Exception:
        conn.close()
        raise
    return conn


def _coupon_subsets(rows: list[sqlite3.Row]) -> Iterable[tuple[sqlite3.Row, ...]]:
    for size in range(len(rows) + 1):
        yield from combinations(rows, size)


def _coupon_discount(
    coupon: sqlite3.Row,
    selected_skus: tuple[sqlite3.Row, ...],
) -> int | None:
    restriction = coupon["category_restriction"]
    eligible_subtotal = sum(
        int(row["price_minor"])
        for row in selected_skus
        if not restriction or row["category"] == restriction
    )
    if restriction and eligible_subtotal == 0:
        return None
    if int(coupon["min_spend_minor"]) > eligible_subtotal:
        return None

    kind = str(coupon["kind"])
    value = int(coupon["value_bp_or_minor"])
    if kind == "percent_off":
        return (eligible_subtotal * value) // 10_000
    if kind == "flat_off":
        return min(value, eligible_subtotal)
    if kind == "free_shipping":
        return 0
    return None


def optimal_cart_plans(
    init_sql_path: Path,
    pool_prefix: str,
    as_of_date: date,
) -> tuple[CartPlan, ...]:
    """Return every minimum-total cart using the ecommerce mock's pricing rules."""
    conn = _load_seed(Path(init_sql_path))
    try:
        sku_rows = conn.execute(
            """
            SELECT s.sku_id, s.product_id, s.attrs_json, s.price_minor,
                   p.title, p.category
            FROM skus AS s
            JOIN products AS p ON p.product_id = s.product_id
            JOIN stocks AS st ON st.sku_id = s.sku_id
            WHERE s.sku_id LIKE ? AND st.quantity > 0
            ORDER BY s.sku_id
            """,
            (f"{pool_prefix}%",),
        ).fetchall()
        if not sku_rows:
            raise ValueError(f"no in-stock SKUs for pool prefix {pool_prefix!r}")

        by_need: dict[str, list[sqlite3.Row]] = {}
        for row in sku_rows:
            try:
                attrs = json.loads(str(row["attrs_json"] or "{}"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed attrs_json for {row['sku_id']}") from exc
            need = str(attrs.get("need") or "").strip()
            if not need:
                raise ValueError(f"missing need attribute for {row['sku_id']}")
            by_need.setdefault(need, []).append(row)

        coupon_rows = [
            row
            for row in conn.execute("SELECT * FROM coupons ORDER BY code").fetchall()
            if int(row["active"])
            and str(row["valid_from"]) <= as_of_date.isoformat() <= str(row["valid_until"])
            and not (
                int(row["max_uses"]) > 0
                and int(row["used_count"]) >= int(row["max_uses"])
            )
        ]

        plans: set[CartPlan] = set()
        for selected in product(*(by_need[need] for need in sorted(by_need))):
            selected_tuple = tuple(selected)
            subtotal = sum(int(row["price_minor"]) for row in selected_tuple)
            for subset in _coupon_subsets(coupon_rows):
                discounts: list[int] = []
                for coupon in subset:
                    discount = _coupon_discount(coupon, selected_tuple)
                    if discount is None:
                        break
                    discounts.append(discount)
                else:
                    plans.add(
                        CartPlan(
                            sku_ids=frozenset(str(row["sku_id"]) for row in selected_tuple),
                            product_titles=frozenset(str(row["title"]) for row in selected_tuple),
                            coupon_codes=frozenset(str(row["code"]) for row in subset),
                            subtotal_minor=subtotal,
                            total_minor=max(0, subtotal - sum(discounts)),
                        )
                    )

        if not plans:
            raise ValueError(f"no cart plans for pool prefix {pool_prefix!r}")
        minimum = min(plan.total_minor for plan in plans)
        return tuple(
            sorted(
                (plan for plan in plans if plan.total_minor == minimum),
                key=lambda plan: (
                    tuple(sorted(plan.sku_ids)),
                    tuple(sorted(plan.coupon_codes)),
                ),
            )
        )
    finally:
        conn.close()


def money_terms(total_minor: int) -> tuple[str, ...]:
    terms = [str(int(total_minor)), f"{int(total_minor) / 100:.2f}"]
    if int(total_minor) % 100 == 0:
        terms.append(str(int(total_minor) // 100))
    return tuple(dict.fromkeys(terms))
