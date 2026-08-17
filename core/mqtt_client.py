import paho.mqtt.client as mqtt

from core.command_receiver import CommandReceiver

import json


class MqttClient:
    """Manages the open connection to the MQTT broker."""

    def __init__(self, broker, port, command_receiver: CommandReceiver):
        self._command_receiver = command_receiver

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(broker, port)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to broker, code: {rc}")
        client.subscribe(CommandReceiver.SUBSCRIPTIONS)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            self._command_receiver.handle(msg.topic, payload)
            print(f"received {msg}")
        except json.JSONDecodeError:
            print("Invalid MQTT message, ignored.")
        except (TypeError, ValueError):
            print(f"Invalid MQTT payload for topic {msg.topic}, ignored.")

    def send_data(self, topic, data):
        if not self._client.is_connected():
            return False

        message_info = self._client.publish(topic, json.dumps(data))

        try:
            message_info.wait_for_publish(timeout=2)
        except (RuntimeError, ValueError):
            return False

        return message_info.rc == mqtt.MQTT_ERR_SUCCESS

    def close(self):
        self._client.loop_stop()
        self._client.disconnect()
        print("MQTT connection closed.")
