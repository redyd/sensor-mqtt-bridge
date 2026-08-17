from core.sensors_definitions import *


class CommandReceiver:
    """Dispatch of received MQTT commands."""

    # number corresponds to delivery guarantee:
    # 0 = very fast but unreliable, 1 = fast and moderately reliable, 2 = slow but very reliable
    SUBSCRIPTIONS = [
        ("commands/interval", 2),
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
        tension_temperature_sensor: TensionTemperatureSensor,
        relative_temperature_sensor: RelativeTemperatureSensor,
        pressure_sensor: PressureSensor,
        humidity_sensor: HumiditySensor,
        light_sensor: LightSensor,
        microphone_sensor: MicrophoneSensor,
        particulate_matter_sensor: ParticulateMatterSensor,
        co2_sensor: Co2Sensor,
        update_interval_callback=None,
    ):
        self.TENSION_TEMPERATURE_SENSOR = tension_temperature_sensor
        self.RELATIVE_TEMPERATURE_SENSOR = relative_temperature_sensor
        self.PRESSURE_SENSOR = pressure_sensor
        self.HUMIDITY_SENSOR = humidity_sensor
        self.LIGHT_SENSOR = light_sensor
        self.MICROPHONE_SENSOR = microphone_sensor
        self.PARTICULE_MATTER_SENSOR = particulate_matter_sensor
        self.CO2_CENSOR = co2_sensor
        self._update_interval_callback = update_interval_callback

        self._handlers = {
            "commands/interval": {
                "set_interval": self._handle_set_interval,
            },
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

        print(f"Interval updated to {interval}s")

    def _handle_unknown(self, payload):
        print(f"Unknown command: {payload}")