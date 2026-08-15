import random

from core.sensors_definitions import *
from utils.sliding_average import SlidingAverage


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

    def __init__(self):
        self._temperature_average = SlidingAverage()
        self._pressure_average = SlidingAverage()
        self._humidity_average = SlidingAverage()
        self._light_average = SlidingAverage()
        self._sound_level_average = SlidingAverage()
        self._particulate_average = {
            "pm1_0": SlidingAverage(),
            "pm2_5": SlidingAverage(),
            "pm10": SlidingAverage(),
        }
        self._co2_average = SlidingAverage()

    def get_temperature(self) -> float:
        return round(random.uniform(18, 28), 1)

    def get_average_temperature(self) -> float:
        return self._temperature_average.add(self.get_temperature())

    def get_pressure(self) -> float:
        return round(random.uniform(990, 1025), 1)

    def get_average_pressure(self) -> float:
        return self._pressure_average.add(self.get_pressure())

    def get_humidity(self) -> float:
        return round(random.uniform(30, 70), 1)

    def get_average_humidity(self) -> float:
        return self._humidity_average.add(self.get_humidity())

    def get_light(self) -> float:
        return round(random.uniform(0, 1000), 1)

    def get_average_light(self) -> float:
        return self._light_average.add(self.get_light())

    def get_sound_level(self) -> float:
        return round(random.uniform(30, 80), 1)

    def get_average_sound_level(self) -> float:
        return self._sound_level_average.add(self.get_sound_level())

    def get_particulate_matter(self) -> dict:
        return {"pm1_0": 5, "pm2_5": 8, "pm10": 12}

    def get_average_particulate_matter(self) -> dict:
        current = self.get_particulate_matter()
        return {
            key: self._particulate_average[key].add(value)
            for key, value in current.items()
        }

    def get_co2(self) -> float:
        return round(random.uniform(400, 800), 1)

    def get_average_co2(self) -> float:
        return self._co2_average.add(self.get_co2())
