import paho.mqtt.publish as publish
import time
import random
import json
from datetime import datetime, timedelta

values = [
    95, 92, 90, 86, 82,
]

def publish_toy_soil_values():
    for soil in values:
        payload = {
            "soil": soil,
            "temperature": 22 + random.uniform(-1,1),
            "humidity": 40 + random.uniform(-3,3),
            "fake_time": (datetime.now() - timedelta(hours=24)).isoformat()

        }

        publish.single(
            "soilmonitor/climate",
            json.dumps(payload),
            hostname="localhost"
        )

        print(payload)
        time.sleep(10)