from dataclasses import dataclass
from typing import Optional


@dataclass
class RoadEvent:
    event_id: str
    road_id: str
    start_dt: str
    end_dt: str
    kind: str          # closure | heavy_traffic | accident
    magnitude: Optional[float] = None
    note: Optional[str] = None
    active: bool = False


@dataclass
class TransitEvent:
    event_id: str
    line_id: Optional[str]
    stop_id: Optional[str]
    start_dt: str
    end_dt: str
    kind: str          # suspended | delayed
    note: Optional[str] = None
    active: bool = False


@dataclass
class Notification:
    id: int
    created_at: str
    channel: str
    payload_json: str
