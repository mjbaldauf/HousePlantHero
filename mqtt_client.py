import paho.mqtt.client as mqtt
import json


class MQTTPublisher:

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883)
        self.client.loop_start()

    def publish(self, topic, payload=dict()):

        if isinstance(payload, dict):
            payload = json.dumps(payload)

        self.client.publish(topic, payload)

        print(f"Published to {topic}: {payload}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()