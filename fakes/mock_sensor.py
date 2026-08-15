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

    def get_temperature(self) -> tuple[float, float]:
        raw = round(random.uniform(18, 28), 1)
        return raw, self._temperature_average.add(raw)

    def get_pressure(self) -> tuple[float, float]:
        raw = round(random.uniform(990, 1025), 1)
        return raw, self._pressure_average.add(raw)

    def get_humidity(self) -> tuple[float, float]:
        raw = round(random.uniform(30, 70), 1)
        return raw, self._humidity_average.add(raw)

    def get_light(self) -> tuple[float, float]:
        raw = round(random.uniform(0, 1000), 1)
        return raw, self._light_average.add(raw)

    def get_sound_level(self) -> tuple[float, float]:
        raw = round(random.uniform(30, 80), 1)
        return raw, self._sound_level_average.add(raw)

    def get_particulate_matter(self) -> tuple[dict, dict]:
        raw = {"pm1_0": 5, "pm2_5": 8, "pm10": 12}
        smooth = {
            key: self._particulate_average[key].add(value)
            for key, value in raw.items()
        }
        return raw, smooth

    def get_co2(self) -> tuple[float, float]:
        raw = round(random.uniform(400, 800), 1)
        return raw, self._co2_average.add(raw)
