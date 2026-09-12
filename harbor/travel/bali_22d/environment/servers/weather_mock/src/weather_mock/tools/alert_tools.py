from __future__ import annotations

import json
from typing import Any, Union

from mcp.server.fastmcp import FastMCP

from ..services.alerts_service import AlertsService
from ..utils.exceptions import (
    InvalidGeo,
    SinkOutsideWorkspace,
    WeatherNotFound,
)


def _dumps(obj: Any) -> str:
    return json.dumps(obj, default=str, ensure_ascii=False)


def register_alert_tools(mcp: FastMCP, service: AlertsService) -> None:

    @mcp.tool()
    async def get_alerts(geo: Union[dict, str]) -> str:
        """Return the list of currently-active severe weather alerts for ``geo``.

        Args:
            geo: supported city name or {lat,lng}.
        """
        try:
            rows = service.get_active_alerts_for_geo(geo)
            return _dumps(rows)
        except WeatherNotFound as e:
            return _dumps({"error": str(e)})
        except InvalidGeo as e:
            return _dumps({"error": f"invalid_geo: {e}"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})

    @mcp.tool()
    async def subscribe_alerts(geo: Union[dict, str], sink: str) -> str:
        """Create a push-subscription for alerts covering ``geo``.

        Supported ``sink`` schemes:
          - file:///abs/path/to/notifications.log — appends one JSON line per
            alert. The path must live under the agent workspace.
          - memory://<channel_id> — enqueues in-process for local consumers.
        """
        try:
            result = service.create_subscription(geo, sink)
            return _dumps(result)
        except SinkOutsideWorkspace:
            return _dumps({"error": "sink_outside_workspace"})
        except WeatherNotFound as e:
            return _dumps({"error": str(e)})
        except InvalidGeo as e:
            return _dumps({"error": f"invalid_geo: {e}"})
        except Exception as e:
            return _dumps({"error": f"internal_error: {e}"})
