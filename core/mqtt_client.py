import paho.mqtt.client as mqtt

from core.command_receiver import CommandReceiver

import json


class MqttClient:
    """Gère la connexion ouverte sur le broker MQTT."""

    def __init__(self, broker, port, command_receiver: CommandReceiver):
        self._command_receiver = command_receiver

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(broker, port)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connecté au broker, code: {rc}")
        client.subscribe(CommandReceiver.SUBSCRIPTIONS)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            self._command_receiver.handle(msg.topic, payload)
        except json.JSONDecodeError:
            print("Message MQTT invalide, ignoré.")

    def send_data(self, topic, data):
        self._client.publish(topic, json.dumps(data))

    def close(self):
        self._client.loop_stop()
        self._client.disconnect()
        print("Connexion au MQTT fermée.")
