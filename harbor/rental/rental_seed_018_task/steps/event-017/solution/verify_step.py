#!/usr/bin/env python3
from pathlib import Path

trajectory = Path("/logs/agent/trajectory.json")
assert trajectory.exists(), "oracle trajectory is missing"
print("verified event-000")
