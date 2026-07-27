"""FastMCP entry point for rail_booking_mock."""

import argparse
import json
import logging
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS train_offers (
  offer_id TEXT PRIMARY KEY,
  train_no TEXT NOT NULL,
  date TEXT NOT NULL,
  train_type TEXT NOT NULL,
  origin_city TEXT NOT NULL,
  dest_city TEXT NOT NULL,
  origin_station TEXT NOT NULL,
  dest_station TEXT NOT NULL,
  depart_at TEXT NOT NULL,
  arrive_at TEXT NOT NULL,
  seat_class TEXT NOT NULL,
  adult_fare REAL NOT NULL,
  student_fare REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CNY',
  adult_seats_remaining INTEGER NOT NULL,
  ordinary_student_seats_remaining INTEGER NOT NULL,
  graduation_student_seats_remaining INTEGER NOT NULL,
  student_discount_available INTEGER NOT NULL DEFAULT 0,
  refundability TEXT NOT NULL,
  route_notes TEXT,
  source_url TEXT
);

CREATE INDEX IF NOT EXISTS idx_train_route_date
  ON train_offers(origin_city, dest_city, date);

CREATE TABLE IF NOT EXISTS student_profiles (
  user_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  ordinary_quota_remaining INTEGER NOT NULL DEFAULT 0,
  graduation_quota_remaining INTEGER NOT NULL DEFAULT 0,
  xuexin_status TEXT NOT NULL DEFAULT 'pending',
  school_proof_status TEXT NOT NULL DEFAULT 'pending',
  discount_zone TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS train_bookings (
  booking_ref TEXT PRIMARY KEY,
  user_id TEXT,
  offer_id TEXT NOT NULL REFERENCES train_offers(offer_id),
  status TEXT NOT NULL,
  total_paid REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CNY',
  created_at TEXT NOT NULL,
  contact_json TEXT NOT NULL,
  passengers_json TEXT NOT NULL,
  tickets_json TEXT NOT NULL,
  history_json TEXT NOT NULL DEFAULT '[]'
);

CREATE INDEX IF NOT EXISTS idx_train_bookings_user ON train_bookings(user_id);

CREATE TABLE IF NOT EXISTS train_status (
  train_no TEXT NOT NULL,
  date TEXT NOT NULL,
  status TEXT NOT NULL,
  delay_min INTEGER NOT NULL DEFAULT 0,
  platform TEXT,
  gate TEXT,
  last_updated TEXT NOT NULL,
  PRIMARY KEY (train_no, date)
);

CREATE TABLE IF NOT EXISTS _counters (
  name TEXT PRIMARY KEY,
  value INTEGER NOT NULL
);
"""


ALIASES = {
    "hangzhou": "杭州",
    "hangzhou east": "杭州东",
    "杭州": "杭州",
    "杭州东": "杭州东",
    "changsha": "长沙",
    "changsha south": "长沙南",
    "长沙": "长沙",
    "长沙南": "长沙南",
    "nanjing": "南京",
    "nanjing south": "南京南",
    "南京": "南京",
    "南京南": "南京南",
    "beijing": "北京",
    "beijing south": "北京南",
    "beijing west": "北京西",
    "北京": "北京",
    "北京南": "北京南",
    "北京西": "北京西",
    "xian": "西安",
    "xi'an": "西安",
    "xian north": "西安北",
    "xi'an north": "西安北",
    "西安": "西安",
    "西安北": "西安北",
    "xining": "西宁",
    "西宁": "西宁",
    "lhasa": "拉萨",
    "拉萨": "拉萨",
    "kunming": "昆明",
    "kunming south": "昆明南",
    "昆明": "昆明",
    "昆明南": "昆明南",
    "dali": "大理",
    "大理": "大理",
}

STUDENT_SEAT_CLASSES = {"second_class", "hard_seat"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _setup_logging(debug: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def _connect(env_dir: Path) -> sqlite3.Connection:
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    for sidecar in (env_dir / "runtime.db-wal", env_dir / "runtime.db-shm"):
        if sidecar.exists():
            sidecar.unlink()
    conn = sqlite3.connect(db_file, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA_SQL)
    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        conn.executescript(init_sql.read_text(encoding="utf-8"))
    return conn


def _row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}


def _norm_values(value: str) -> set[str]:
    raw = " ".join(str(value or "").strip().split())
    lower = raw.lower()
    vals = {raw, lower}
    if lower in ALIASES:
        vals.add(ALIASES[lower])
    if raw in ALIASES:
        vals.add(ALIASES[raw])
    return {v for v in vals if v}


def _next_counter(conn: sqlite3.Connection, name: str) -> int:
    conn.execute(
        "INSERT INTO _counters(name, value) VALUES (?, 0) "
        "ON CONFLICT(name) DO NOTHING",
        (name,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE name = ?", (name,))
    row = conn.execute("SELECT value FROM _counters WHERE name = ?", (name,)).fetchone()
    return int(row["value"])


def _booking_ref(conn: sqlite3.Connection) -> str:
    seq = _next_counter(conn, "booking_seq")
    return f"RB{seq:06d}"


class RailService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def search_trains(
        self,
        origin: str,
        dest: str,
        date: str,
        passengers: list[dict[str, Any]] | None = None,
        seat_class: str | None = None,
        max_results: int = 20,
    ) -> dict[str, Any]:
        origin_vals = list(_norm_values(origin))
        dest_vals = list(_norm_values(dest))
        where = [
            "date = ?",
            f"(origin_city IN ({','.join('?' for _ in origin_vals)}) "
            f"OR origin_station IN ({','.join('?' for _ in origin_vals)}))",
            f"(dest_city IN ({','.join('?' for _ in dest_vals)}) "
            f"OR dest_station IN ({','.join('?' for _ in dest_vals)}))",
        ]
        params: list[Any] = [date, *origin_vals, *origin_vals, *dest_vals, *dest_vals]
        if seat_class:
            where.append("seat_class = ?")
            params.append(seat_class)
        rows = self.conn.execute(
            f"SELECT * FROM train_offers WHERE {' AND '.join(where)} ORDER BY depart_at LIMIT ?",
            (*params, max(1, min(int(max_results), 50))),
        ).fetchall()
        offers = [self._offer_out(row, passengers or []) for row in rows]
        return {"offers": offers, "total": len(offers), "returned": len(offers)}

    def get_train_offer(self, offer_id: str) -> dict[str, Any]:
        row = self._offer_row(offer_id)
        return self._offer_out(row, [])

    def price_train_offer(
        self,
        offer_id: str,
        passengers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        row = self._offer_row(offer_id)
        tickets = self._price_tickets(row, passengers)
        total = round(sum(t["fare"] for t in tickets), 2)
        return {
            "offer_id": offer_id,
            "train_no": row["train_no"],
            "date": row["date"],
            "currency": row["currency"],
            "total_price": {"amount": total, "currency": row["currency"]},
            "tickets": tickets,
        }

    def create_train_booking(
        self,
        offer_id: str,
        passengers: list[dict[str, Any]],
        contact: dict[str, Any],
        payment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not passengers:
            return {"error": "passengers_required"}
        row = self._offer_row(offer_id)
        tickets = self._price_tickets(row, passengers)
        adult_count = sum(1 for t in tickets if t["fare_type"] == "adult")
        ordinary_count = sum(
            1 for t in tickets
            if t["fare_type"] == "student" and t.get("student_quota_source") == "ordinary"
        )
        graduation_count = sum(
            1 for t in tickets
            if t["fare_type"] == "student" and t.get("student_quota_source") == "graduation-trip"
        )
        if adult_count > int(row["adult_seats_remaining"]):
            return {"error": "inventory_gone", "reason": "not enough adult seats"}
        if ordinary_count > int(row["ordinary_student_seats_remaining"]):
            return {"error": "inventory_gone", "reason": "not enough ordinary student seats"}
        if graduation_count > int(row["graduation_student_seats_remaining"]):
            return {"error": "inventory_gone", "reason": "not enough graduation student seats"}

        total = round(sum(t["fare"] for t in tickets), 2)
        booking_ref = _booking_ref(self.conn)
        now = _now_iso()
        user_id = (
            contact.get("user_id")
            or passengers[0].get("user_id")
            or contact.get("email")
            or "unknown"
        )
        history = [{"at": now, "event": "CREATED", "detail": f"offer={offer_id}"}]
        self.conn.execute(
            """
            INSERT INTO train_bookings (
              booking_ref, user_id, offer_id, status, total_paid, currency,
              created_at, contact_json, passengers_json, tickets_json, history_json
            ) VALUES (?, ?, ?, 'ticketed', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                booking_ref,
                user_id,
                offer_id,
                total,
                row["currency"],
                now,
                json.dumps(contact, ensure_ascii=False),
                json.dumps(passengers, ensure_ascii=False),
                json.dumps(tickets, ensure_ascii=False),
                json.dumps(history, ensure_ascii=False),
            ),
        )
        self.conn.execute(
            """
            UPDATE train_offers
            SET adult_seats_remaining = adult_seats_remaining - ?,
                ordinary_student_seats_remaining = ordinary_student_seats_remaining - ?,
                graduation_student_seats_remaining = graduation_student_seats_remaining - ?
            WHERE offer_id = ?
            """,
            (adult_count, ordinary_count, graduation_count, offer_id),
        )
        for ticket in tickets:
            profile_id = ticket.get("user_id")
            if not profile_id or ticket["fare_type"] != "student":
                continue
            if ticket.get("student_quota_source") == "ordinary":
                self.conn.execute(
                    "UPDATE student_profiles SET ordinary_quota_remaining = MAX(0, ordinary_quota_remaining - 1) WHERE user_id = ?",
                    (profile_id,),
                )
            elif ticket.get("student_quota_source") == "graduation-trip":
                self.conn.execute(
                    "UPDATE student_profiles SET graduation_quota_remaining = MAX(0, graduation_quota_remaining - 1) WHERE user_id = ?",
                    (profile_id,),
                )
        return {
            "booking_ref": booking_ref,
            "status": "ticketed",
            "total_paid": {"amount": total, "currency": row["currency"]},
            "tickets": tickets,
            "created_at": now,
        }

    def list_train_bookings(self, user_id: str | None = None) -> dict[str, Any]:
        if user_id:
            rows = self.conn.execute(
                "SELECT * FROM train_bookings WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM train_bookings ORDER BY created_at DESC"
            ).fetchall()
        bookings = [self._booking_out(row, include_detail=True) for row in rows]
        return {"bookings": bookings, "count": len(bookings)}

    def cancel_train_booking(self, booking_ref: str, reason: str | None = None) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM train_bookings WHERE booking_ref = ?",
            (booking_ref,),
        ).fetchone()
        if not row:
            return {"error": "booking_not_found"}
        if row["status"] == "cancelled":
            return {"error": "already_cancelled", "booking_ref": booking_ref}
        offer = self._offer_row(row["offer_id"])
        tickets = json.loads(row["tickets_json"])
        adult_count = sum(1 for t in tickets if t["fare_type"] == "adult")
        ordinary_count = sum(
            1 for t in tickets
            if t["fare_type"] == "student" and t.get("student_quota_source") == "ordinary"
        )
        graduation_count = sum(
            1 for t in tickets
            if t["fare_type"] == "student" and t.get("student_quota_source") == "graduation-trip"
        )
        self.conn.execute(
            """
            UPDATE train_offers
            SET adult_seats_remaining = adult_seats_remaining + ?,
                ordinary_student_seats_remaining = ordinary_student_seats_remaining + ?,
                graduation_student_seats_remaining = graduation_student_seats_remaining + ?
            WHERE offer_id = ?
            """,
            (adult_count, ordinary_count, graduation_count, offer["offer_id"]),
        )
        for ticket in tickets:
            profile_id = ticket.get("user_id")
            if not profile_id or ticket["fare_type"] != "student":
                continue
            if ticket.get("student_quota_source") == "ordinary":
                self.conn.execute(
                    "UPDATE student_profiles SET ordinary_quota_remaining = ordinary_quota_remaining + 1 WHERE user_id = ?",
                    (profile_id,),
                )
            elif ticket.get("student_quota_source") == "graduation-trip":
                self.conn.execute(
                    "UPDATE student_profiles SET graduation_quota_remaining = graduation_quota_remaining + 1 WHERE user_id = ?",
                    (profile_id,),
                )
        history = json.loads(row["history_json"])
        history.append({"at": _now_iso(), "event": "CANCELLED", "detail": reason or ""})
        self.conn.execute(
            "UPDATE train_bookings SET status = 'cancelled', history_json = ? WHERE booking_ref = ?",
            (json.dumps(history, ensure_ascii=False), booking_ref),
        )
        refund = round(float(row["total_paid"]) * 0.9, 2)
        return {
            "booking_ref": booking_ref,
            "status": "cancelled",
            "refund": {"amount": refund, "currency": row["currency"]},
            "penalty": {"amount": round(float(row["total_paid"]) - refund, 2), "currency": row["currency"]},
        }

    def get_train_status(self, train_no: str, date: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM train_status WHERE train_no = ? AND date = ?",
            (train_no, date),
        ).fetchone()
        if row:
            return _row_dict(row) or {}
        return {
            "train_no": train_no,
            "date": date,
            "status": "SCHEDULED",
            "delay_min": 0,
            "last_updated": _now_iso(),
        }

    def get_student_profile(self, user_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM student_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return _row_dict(row) or {"error": "student_profile_not_found", "user_id": user_id}

    def update_student_verification(
        self,
        user_id: str,
        xuexin_status: str | None = None,
        school_proof_status: str | None = None,
        discount_zone: str | None = None,
        note: str | None = None,
    ) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM student_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if not row:
            return {"error": "student_profile_not_found", "user_id": user_id}
        self.conn.execute(
            """
            UPDATE student_profiles
            SET xuexin_status = COALESCE(?, xuexin_status),
                school_proof_status = COALESCE(?, school_proof_status),
                discount_zone = COALESCE(?, discount_zone),
                notes = COALESCE(?, notes)
            WHERE user_id = ?
            """,
            (xuexin_status, school_proof_status, discount_zone, note, user_id),
        )
        return self.get_student_profile(user_id)

    def _offer_row(self, offer_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM train_offers WHERE offer_id = ?",
            (offer_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"offer_not_found: {offer_id}")
        return row

    def _profile_for_passenger(self, passenger: dict[str, Any]) -> sqlite3.Row | None:
        user_id = passenger.get("user_id")
        if user_id:
            row = self.conn.execute(
                "SELECT * FROM student_profiles WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            if row:
                return row
        name = passenger.get("name") or passenger.get("display_name")
        if name:
            return self.conn.execute(
                "SELECT * FROM student_profiles WHERE display_name = ?",
                (name,),
            ).fetchone()
        return None

    def _student_eligibility(
        self,
        offer: sqlite3.Row,
        profile: sqlite3.Row | None,
        remaining_ordinary_seats: int,
        remaining_graduation_seats: int,
    ) -> tuple[bool, str | None, str]:
        if int(offer["student_discount_available"]) != 1:
            return False, None, "no_student_discount_inventory"
        if offer["seat_class"] not in STUDENT_SEAT_CLASSES:
            return False, None, "seat_class_not_supported"
        if profile is None:
            return False, None, "student_profile_not_found"
        if int(profile["ordinary_quota_remaining"]) > 0 and remaining_ordinary_seats > 0:
            return True, "ordinary", ""
        proof_ok = profile["xuexin_status"] == "verified" or profile["school_proof_status"] == "verified"
        if int(profile["graduation_quota_remaining"]) > 0 and not proof_ok:
            return False, None, "graduation_proof_pending"
        if int(profile["graduation_quota_remaining"]) > 0 and remaining_graduation_seats > 0:
            return True, "graduation-trip", ""
        if remaining_ordinary_seats <= 0 and remaining_graduation_seats <= 0:
            return False, None, "student_discount_seats_sold_out"
        return False, None, "student_quota_exhausted"

    def _price_tickets(
        self,
        offer: sqlite3.Row,
        passengers: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        ordinary_left = int(offer["ordinary_student_seats_remaining"])
        graduation_left = int(offer["graduation_student_seats_remaining"])
        tickets: list[dict[str, Any]] = []
        for idx, passenger in enumerate(passengers):
            profile = self._profile_for_passenger(passenger)
            wants_adult = passenger.get("fare_type") == "adult"
            eligible, quota_source, reason = self._student_eligibility(
                offer,
                profile,
                ordinary_left,
                graduation_left,
            )
            if eligible and not wants_adult:
                fare_type = "student"
                fare = float(offer["student_fare"])
                if quota_source == "ordinary":
                    ordinary_left -= 1
                elif quota_source == "graduation-trip":
                    graduation_left -= 1
                ineligibility_reason = ""
            else:
                fare_type = "adult"
                fare = float(offer["adult_fare"])
                ineligibility_reason = "" if wants_adult else reason
                quota_source = None
            user_id = profile["user_id"] if profile else passenger.get("user_id")
            tickets.append(
                {
                    "pax_idx": idx,
                    "user_id": user_id,
                    "passenger_name": passenger.get("name") or passenger.get("display_name") or user_id,
                    "train_no": offer["train_no"],
                    "date": offer["date"],
                    "origin_station": offer["origin_station"],
                    "dest_station": offer["dest_station"],
                    "seat_class": offer["seat_class"],
                    "fare_type": fare_type,
                    "fare": round(fare, 2),
                    "currency": offer["currency"],
                    "student_quota_source": quota_source,
                    "student_eligibility_status": "eligible" if fare_type == "student" else "not_used",
                    "student_ineligibility_reason": ineligibility_reason,
                    "xuexin_verification_status": profile["xuexin_status"] if profile else "unknown",
                    "school_graduation_proof_status": profile["school_proof_status"] if profile else "unknown",
                    "discount_zone": profile["discount_zone"] if profile else None,
                }
            )
        return tickets

    def _offer_out(
        self,
        row: sqlite3.Row,
        passengers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        out = {
            "offer_id": row["offer_id"],
            "train_no": row["train_no"],
            "date": row["date"],
            "train_type": row["train_type"],
            "origin_city": row["origin_city"],
            "dest_city": row["dest_city"],
            "origin_station": row["origin_station"],
            "dest_station": row["dest_station"],
            "depart_at": row["depart_at"],
            "arrive_at": row["arrive_at"],
            "seat_class": row["seat_class"],
            "adult_fare": row["adult_fare"],
            "student_fare": row["student_fare"],
            "currency": row["currency"],
            "adult_seats_remaining": row["adult_seats_remaining"],
            "ordinary_student_seats_remaining": row["ordinary_student_seats_remaining"],
            "graduation_student_seats_remaining": row["graduation_student_seats_remaining"],
            "student_discount_available": bool(row["student_discount_available"]),
            "refundability": row["refundability"],
            "route_notes": row["route_notes"],
            "source_url": row["source_url"],
        }
        if passengers:
            out["pricing_preview"] = self.price_train_offer(row["offer_id"], passengers)
        return out

    def _booking_out(self, row: sqlite3.Row, include_detail: bool) -> dict[str, Any]:
        offer = self._offer_row(row["offer_id"])
        out = {
            "booking_ref": row["booking_ref"],
            "status": row["status"],
            "user_id": row["user_id"],
            "train_no": offer["train_no"],
            "date": offer["date"],
            "route": f"{offer['origin_station']}->{offer['dest_station']}",
            "total_paid": {"amount": row["total_paid"], "currency": row["currency"]},
            "created_at": row["created_at"],
        }
        if include_detail:
            out["contact"] = json.loads(row["contact_json"])
            out["passengers"] = json.loads(row["passengers_json"])
            out["tickets"] = json.loads(row["tickets_json"])
            out["history"] = json.loads(row["history_json"])
        return out


def build_server(env_dir: Path) -> FastMCP:
    conn = _connect(env_dir)
    service = RailService(conn)
    mcp = FastMCP("rail-booking-mock", host="0.0.0.0")

    @mcp.tool()
    async def search_trains(
        origin: str,
        dest: str,
        date: str,
        passengers: list[dict[str, Any]] | None = None,
        seat_class: str | None = None,
        max_results: int = 20,
    ) -> dict[str, Any]:
        """Search train offers by origin, destination, and date."""
        return service.search_trains(origin, dest, date, passengers, seat_class, max_results)

    @mcp.tool()
    async def get_train_offer(offer_id: str) -> dict[str, Any]:
        """Fetch a previously returned train offer."""
        return service.get_train_offer(offer_id)

    @mcp.tool()
    async def price_train_offer(
        offer_id: str,
        passengers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Price an offer for passengers, applying eligible student discounts."""
        return service.price_train_offer(offer_id, passengers)

    @mcp.tool()
    async def create_train_booking(
        offer_id: str,
        passengers: list[dict[str, Any]],
        contact: dict[str, Any],
        payment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a ticketed rail booking."""
        return service.create_train_booking(offer_id, passengers, contact, payment)

    @mcp.tool()
    async def list_train_bookings(user_id: str | None = None) -> dict[str, Any]:
        """List train bookings, optionally filtered by user_id."""
        return service.list_train_bookings(user_id)

    @mcp.tool()
    async def cancel_train_booking(
        booking_ref: str,
        reason: str | None = None,
    ) -> dict[str, Any]:
        """Cancel a rail booking and return a mock refund."""
        return service.cancel_train_booking(booking_ref, reason)

    @mcp.tool()
    async def get_train_status(train_no: str, date: str) -> dict[str, Any]:
        """Return train status for a train_no and date."""
        return service.get_train_status(train_no, date)

    @mcp.tool()
    async def get_student_profile(user_id: str) -> dict[str, Any]:
        """Return student ticket quota and verification state for a passenger."""
        return service.get_student_profile(user_id)

    @mcp.tool()
    async def update_student_verification(
        user_id: str,
        xuexin_status: str | None = None,
        school_proof_status: str | None = None,
        discount_zone: str | None = None,
        note: str | None = None,
    ) -> dict[str, Any]:
        """Update mock student verification state after proof review."""
        return service.update_student_verification(
            user_id,
            xuexin_status=xuexin_status,
            school_proof_status=school_proof_status,
            discount_zone=discount_zone,
            note=note,
        )

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="rail_booking_mock MCP server")
    parser.add_argument("--env", required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    _setup_logging(args.debug)
    try:
        mcp = build_server(Path(args.env))
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("shutdown requested")
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).exception("server startup failed: %s", exc)
        sys.exit(1)
