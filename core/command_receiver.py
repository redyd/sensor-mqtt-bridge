from core.sensors_definitions import *


class CommandReceiver:
    """Dispatch of received MQTT commands."""

    # number corresponds to delivery guarantee:
    # 0 = very fast but unreliable, 1 = fast and moderately reliable, 2 = slow but very reliable
    SUBSCRIPTIONS = [
        ("commands/interval", 2),
        ("commands/pause", 2),
    ]

    TENSION_TEMPERATURE_SENSOR: TensionTemperatureSensor
    RELATIVE_TEMPERATURE_SENSOR: RelativeTemperatureSensor
    PRESSURE_SENSOR: PressureSensor
    HUMIDITY_SENSOR: HumiditySensor
    LIGHT_SENSOR: LightSensor
    MICROPHONE_SENSOR: MicrophoneSensor
    PARTICULE_MATTER_SENSOR: ParticulateMatterSensor
    CO2_CENSOR: Co2Sensor

    def __init__(
        self,
        update_interval_callback=None,
        toggle_pause_callback=None
    ):
        self._update_interval_callback = update_interval_callback
        self._toggle_pause_callback = toggle_pause_callback

        self._handlers = {
            "commands/interval": {
                "set_interval": self._handle_set_interval,
            },
            "commands/pause": {
                "toggle": self._toggle_pause,
            }
        }

    def handle(self, topic, payload):
        command = payload.get("command")
        topic_handlers = self._handlers.get(topic, {})
        handler = topic_handlers.get(command, self._handle_unknown)
        handler(payload)

    def _handle_set_interval(self, payload):
        interval = payload.get("interval")

        if not isinstance(interval, (int, float)):
            print(f"Invalid interval value: {payload}")
            return

        if interval <= 0:
            print(f"Interval must be greater than zero: {interval}")
            return

        if self._update_interval_callback is not None:
            self._update_interval_callback(interval)

        
    def _toggle_pause(self, payload):
        toggle = payload.get("toggle")

        if not isinstance(toggle, bool):
            print(f"Invalid pause value: {payload}")
            return

        if self._toggle_pause_callback is not None:
            self._toggle_pause_callback(toggle)

    def _handle_unknown(self, payload):
        print(f"Unknown command: {payload}")