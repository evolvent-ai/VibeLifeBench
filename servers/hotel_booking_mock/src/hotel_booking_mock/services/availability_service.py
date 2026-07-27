import sqlite3
from typing import List, Optional, Tuple

from ..utils.dates import compact, from_compact, iter_nights
from ..utils.exceptions import BadDateRangeError, HotelNotFoundError
from ..utils.ids import slugify


class AvailabilityService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_room_availability(
        self,
        hotel_id: str,
        check_in: str,
        check_out: str,
        guests: int,
    ) -> List[dict]:
        try:
            nights = iter_nights(check_in, check_out)
        except ValueError:
            raise BadDateRangeError("check_out must be after check_in")
        if len(nights) > 30:
            raise BadDateRangeError("stay exceeds 30 nights")

        row = self.conn.execute("SELECT hotel_id FROM hotels WHERE hotel_id = ?", (hotel_id,)).fetchone()
        if not row:
            raise HotelNotFoundError("hotel not found")

        rp_rows = self.conn.execute(
            """
            SELECT rate_plan_row_id, date, room_type, flavor, nightly_price, currency,
                   inventory_remaining, inventory_capacity, cancellation_policy, refundable_until,
                   breakfast_included, max_occupancy
            FROM rate_plans
            WHERE hotel_id = ? AND date IN (%s)
            """ % (",".join(["?"] * len(nights))),
            [hotel_id, *nights],
        ).fetchall()

        # group by (room_type, flavor)
        combos: dict = {}
        for r in rp_rows:
            if int(r["max_occupancy"]) < int(guests):
                continue
            combos.setdefault((r["room_type"], r["flavor"]), {})[r["date"]] = r

        out: List[dict] = []
        for (room_type, flavor), date_map in combos.items():
            if not all(n in date_map for n in nights):
                continue
            if any(int(date_map[n]["inventory_remaining"]) <= 0 for n in nights):
                continue

            currencies = {str(date_map[n]["currency"]) for n in nights}
            if len(currencies) != 1:
                continue
            currency = next(iter(currencies))
            nightly_prices = [int(date_map[n]["nightly_price"]) for n in nights]
            price_total = sum(nightly_prices)
            min_inventory = min(int(date_map[n]["inventory_remaining"]) for n in nights)
            refundable_until = date_map[nights[0]]["refundable_until"]
            # refundable_until for the plan = the MOST CONSERVATIVE (earliest) if any night has one
            all_refundable_untils = [date_map[n]["refundable_until"] for n in nights if date_map[n]["refundable_until"]]
            if all_refundable_untils and len(all_refundable_untils) == len(nights):
                refundable_until = min(all_refundable_untils)
                refundable = True
            else:
                refundable_until = None
                refundable = False

            cancellation_policy = date_map[nights[0]]["cancellation_policy"]
            breakfast = bool(date_map[nights[0]]["breakfast_included"])

            rate_plan_id = make_rate_plan_id(hotel_id, room_type, flavor, check_in, check_out)
            notes = "Weekend surcharge applies Fri/Sat"

            out.append({
                "rate_plan_id": rate_plan_id,
                "room_type": room_type,
                "max_occupancy": int(date_map[nights[0]]["max_occupancy"]),
                "nights": len(nights),
                "nightly_prices": nightly_prices,
                "price_total": price_total,
                "currency": currency,
                "cancellation_policy": cancellation_policy,
                "refundable": refundable,
                "refundable_until": refundable_until,
                "breakfast_included": breakfast,
                "inventory_remaining": min_inventory,
                "flavor": flavor,
                "notes": notes,
            })

        # sort: cheapest first
        out.sort(key=lambda x: x["price_total"])
        return out


def make_rate_plan_id(hotel_id: str, room_type: str, flavor: str, check_in: str, check_out: str) -> str:
    slug = slugify(room_type)
    return f"rp_{hotel_id}_{slug}_{flavor}_{compact(check_in)}_{compact(check_out)}"


def parse_rate_plan_id(rate_plan_id: str) -> Tuple[str, str, str, str, str]:
    """Parse back (hotel_id, room_type_slug, flavor, check_in, check_out).

    rate_plan_id format: rp_<hotel_id>_<room_type_slug>_<flavor>_<YYYYMMDD>_<YYYYMMDD>
    hotel_id always starts with 'htl_' and the last two tokens are compact dates.
    room_type_slug may contain hyphens ('-') but no underscores.
    """
    if not rate_plan_id.startswith("rp_"):
        raise ValueError("rate_plan_id must start with 'rp_'")
    body = rate_plan_id[3:]
    parts = body.split("_")
    if len(parts) < 5:
        raise ValueError("rate_plan_id has too few segments")
    try:
        check_in = from_compact(parts[-2])
        check_out = from_compact(parts[-1])
    except Exception as e:
        raise ValueError(f"bad compact dates: {e}")
    flavor = parts[-3]
    if flavor not in ("flex", "semi", "prepaid"):
        raise ValueError(f"bad flavor: {flavor}")
    rest = parts[:-3]
    if len(rest) < 2:
        raise ValueError("rate_plan_id missing hotel_id or room slug")
    # Room slug is the single last token (slugify produces hyphens, never underscores).
    slug = rest[-1]
    hotel_tokens = rest[:-1]
    if hotel_tokens[0] != "htl":
        raise ValueError("rate_plan_id hotel segment must start with 'htl'")
    hotel_id = "_".join(hotel_tokens)
    return hotel_id, slug, flavor, check_in, check_out


def resolve_room_type(conn: sqlite3.Connection, hotel_id: str, slug: str) -> Optional[str]:
    """Given a slugified room name, find the canonical room_type string by looking up rate_plans for that hotel."""
    rows = conn.execute(
        "SELECT DISTINCT room_type FROM rate_plans WHERE hotel_id = ?",
        (hotel_id,),
    ).fetchall()
    for r in rows:
        if slugify(r["room_type"]) == slug:
            return r["room_type"]
    return None
