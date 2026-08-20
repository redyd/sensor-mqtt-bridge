import json

import paho.mqtt.client as mqtt

from core.command_receiver import CommandReceiver


class MqttClient:
    """Manages the open connection to the MQTT broker."""

    def __init__(self, broker: str, port: int, command_receiver: CommandReceiver) -> None:
        self._command_receiver = command_receiver

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(broker, port)
        self._client.loop_start()  # runs the network loop in a background thread

    # paho callback signatures are fixed by the library
    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to broker, code: {rc}")
        client.subscribe(CommandReceiver.SUBSCRIPTIONS)

    # paho callback signatures are fixed by the library
    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            self._command_receiver.handle(msg.topic, payload)
        except json.JSONDecodeError:
            print("Invalid MQTT message, ignored.")
        except (TypeError, ValueError):
            print(f"Invalid MQTT payload for topic {msg.topic}, ignored.")

    def send_data(self, topic: str, data: dict[str, str | float | dict[str, str | float]]) -> bool:
        if not self._client.is_connected():
            return False

        message_info = self._client.publish(topic, json.dumps(data))

        try:
            message_info.wait_for_publish(timeout=2)
        except (RuntimeError, ValueError):
            return False

        return message_info.rc == mqtt.MQTT_ERR_SUCCESS

    def close(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()
        print("MQTT connection closed.")
