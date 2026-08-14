from core.sensors_definitions import *


class CommandReceiver:
    """Dispatch of received MQTT commands."""

    # number corresponds to delivery guarantee:
    # 0 = very fast but unreliable, 1 = fast and moderately reliable, 2 = slow but very reliable
    SUBSCRIPTIONS = [
        ("commands/status", 0),
    ]
    
    TEMPERATURE_SENSOR: TemperatureSensor
    PRESSURE_SENSOR: PressureSensor
    HUMIDITY_SENSOR: HumiditySensor
    LIGHT_SENSOR: LightSensor
    MICROPHONE_SENSOR: MicrophoneSensor
    PARTICULE_MATTER_SENSOR: ParticulateMatterSensor
    CO2_CENSOR: Co2Sensor

    def __init__(
        self,
        temperature_sensor: TemperatureSensor,
        pressure_sensor: PressureSensor,
        humidity_sensor: HumiditySensor,
        light_sensor: LightSensor,
        microphone_sensor: MicrophoneSensor,
        particulate_matter_sensor: ParticulateMatterSensor,
        co2_sensor: Co2Sensor,
    ):
        self.TEMPERATURE_SENSOR = temperature_sensor
        self.PRESSURE_SENSOR = pressure_sensor
        self.HUMIDITY_SENSOR = humidity_sensor
        self.LIGHT_SENSOR = light_sensor
        self.MICROPHONE_SENSOR = microphone_sensor
        self.PARTICULE_MATTER_SENSOR = particulate_matter_sensor
        self.CO2_CENSOR = co2_sensor
        
        self._handlers = {
            "commands/status": {
                "get_status": self._handle_get_status,
            },
        }

    def handle(self, topic, payload):
        command = payload.get("command")
        topic_handlers = self._handlers.get(topic, {})
        handler = topic_handlers.get(command, self._handle_unknown)
        handler(payload)

    def _handle_get_status(self, payload):
        status = {
            "temperature": self.TEMPERATURE_SENSOR.get_temperature(),
            "pressure": self.PRESSURE_SENSOR.get_pressure(),
            "humidity": self.HUMIDITY_SENSOR.get_humidity(),
            "light": self.LIGHT_SENSOR.get_light(),
            "sound_level": self.MICROPHONE_SENSOR.get_sound_level(),
            "particulate_matter": self.PARTICULE_MATTER_SENSOR.get_particulate_matter(),
            "co2": self.CO2_CENSOR.get_co2(),
        }
        print(f"Status: {status}")

    def _handle_unknown(self, payload):
        print(f"Unknown command: {payload}")