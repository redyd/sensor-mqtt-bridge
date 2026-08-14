import random

from core.sensors_definitions import *


class MockSensor(
    TemperatureSensor,
    PressureSensor,
    HumiditySensor,
    LightSensor,
    MicrophoneSensor,
    ParticulateMatterSensor,
    Co2Sensor,
):
    """Dummy sensor used for testing"""

    def get_temperature(self) -> float:
        return round(random.uniform(18, 28), 1)

    def get_pressure(self) -> float:
        return round(random.uniform(990, 1025), 1)

    def get_humidity(self) -> float:
        return round(random.uniform(30, 70), 1)

    def get_light(self) -> float:
        return round(random.uniform(0, 1000), 1)

    def get_sound_level(self) -> float:
        return round(random.uniform(30, 80), 1)

    def get_particulate_matter(self) -> dict:
        return {"pm1_0": 5, "pm2_5": 8, "pm10": 12}

    def get_co2(self) -> float:
        return round(random.uniform(400, 800), 1)
