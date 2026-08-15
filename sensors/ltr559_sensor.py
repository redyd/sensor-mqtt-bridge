from ltr559 import LTR559

from core.sensors_definitions import LightSensor
from utils.sliding_average import SlidingAverage


class Ltr559Sensor(LightSensor):
    """LTR559: ambient light."""

    def __init__(self):
        self._sensor = LTR559()
        self._light_average = SlidingAverage()

    def get_light(self) -> float:
        self._sensor.update_sensor()
        return self._sensor.get_lux()

    def get_average_light(self) -> float:
        return self._light_average.add(self.get_light())
