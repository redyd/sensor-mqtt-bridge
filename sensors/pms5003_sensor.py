from pms5003 import PMS5003

from core.sensors_definitions import ParticulateMatterSensor
from utils.sliding_average import SlidingAverage


class Pms5003Sensor(ParticulateMatterSensor):
    """PMS5003: fine particulate matter."""

    def __init__(self):
        self._sensor = PMS5003()
        self._particulate_average = {
            "pm1_0": SlidingAverage(),
            "pm2_5": SlidingAverage(),
            "pm10": SlidingAverage(),
        }

    def get_particulate_matter(self) -> tuple[dict, dict]:
        reading = self._sensor.read()
        raw = {
            "pm1_0": reading.pm_ug_per_m3(1.0),
            "pm2_5": reading.pm_ug_per_m3(2.5),
            "pm10": reading.pm_ug_per_m3(10),
        }
        smooth = {
            key: self._particulate_average[key].add(value)
            for key, value in raw.items()
        }
        return raw, smooth
