#! /usr/bin/env python3

import requests
from datetime import datetime, timedelta, timezone

BASE = "https://homeassistant.ckn.li"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI1YjY0ZWE5N2FiMzM0NTQ0OGMyNjhmZTIxYzAxZTE1MSIsImlhdCI6MTc1NjAzOTAxNCwiZXhwIjoyMDcxMzk5MDE0fQ.X-sQli-NTpCjeXpn19zf-maPRDldkSeTuhKZua1k8uM"
ENTITY = "sensor.hue_outdoor_motion_sensor_2_temperature"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

begin = datetime(2025, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
current = begin
now = datetime.now(timezone.utc)

while current < now:
    current += timedelta(hours=1)
    resp = requests.get(
        f"{BASE}/api/history/period/{current.isoformat()}",
        params={
            "end_time": current.isoformat(),
            "filter_entity_id": ENTITY
        },
        headers=HEADERS,
        timeout=15,
    )
    print(current, resp.json())
