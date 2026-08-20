from pms5003 import PMS5003

from core.sensors_definitions import ParticulateMatterSensor
from utils.sliding_average import SlidingAverage


class Pms5003Sensor(ParticulateMatterSensor):
    """PMS5003: fine particulate matter."""

    def __init__(self) -> None:
        self._sensor = PMS5003()
        self._particulate_average = SlidingAverage()

    def get_particulate_matter(self) -> tuple[float, float]:
        reading = self._sensor.read()
        raw = reading.pm_ug_per_m3(2.5)  # PM2.5 concentration in µg/m³
        return raw, self._particulate_average.add(raw)
