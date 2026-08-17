import random

from core.sensors_definitions import *
from utils.sliding_average import SlidingAverage


class MockSensor(
    TensionTemperatureSensor,
    RelativeTemperatureSensor,
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

    def get_tension_temperature(self) -> tuple[float, float]:
        raw = round(random.uniform(18, 28), 1)
        return raw, self._temperature_average.add(raw)
    
    def get_relative_temperature(self) -> tuple[float, float]:
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
        pm1_0 = round(random.uniform(1, 15), 1)
        pm2_5 = round(random.uniform(pm1_0, max(pm1_0 * 1.5, 20)), 1)
        pm10 = round(random.uniform(pm2_5, max(pm2_5 * 1.3, 50)), 1)
        
        raw = {"pm1_0": pm1_0, "pm2_5": pm2_5, "pm10": pm10}
        smooth = {
            key: self._particulate_average[key].add(value)
            for key, value in raw.items()
        }
        return raw, smooth

    def get_co2(self) -> tuple[float, float]:
        raw = round(random.uniform(400, 800), 1)
        return raw, self._co2_average.add(raw)
