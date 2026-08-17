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
        self._particulate_average = SlidingAverage()
        self._co2_average = SlidingAverage()

    def get_temperature(self) -> tuple[float, float]:
        raw = round(random.uniform(10, 40), 1)
        return raw, self._temperature_average.add(raw)
    
    def get_pressure(self) -> tuple[float, float]:
        raw = round(random.uniform(990, 1025), 1)
        return raw, self._pressure_average.add(raw)

    def get_humidity(self) -> tuple[float, float]:
        raw = round(random.uniform(10, 90), 1)
        return raw, self._humidity_average.add(raw)

    def get_light(self) -> tuple[float, float]:
        raw = round(random.uniform(0, 1000), 1)
        return raw, self._light_average.add(raw)

    def get_sound_level(self) -> tuple[float, float]:
        raw = round(random.uniform(30, 80), 1)
        return raw, self._sound_level_average.add(raw)


    def get_particulate_matter(self) -> tuple[float, float]:
        raw = round(random.uniform(0, 80), 1)
        return raw, self._particulate_average.add(raw)

    def get_co2(self) -> tuple[float, float]:
        raw = round(random.uniform(400, 5000), 1)
        return raw, self._co2_average.add(raw)
