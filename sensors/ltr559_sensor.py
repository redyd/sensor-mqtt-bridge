from ltr559 import LTR559

from core.sensors_definitions import LightSensor
from utils.sliding_average import SlidingAverage


class Ltr559Sensor(LightSensor):
    """LTR559: ambient light."""

    def __init__(self) -> None:
        self._sensor = LTR559()
        self._light_average = SlidingAverage()

    def get_light(self) -> tuple[float, float]:
        self._sensor.update_sensor()  # triggers a new sensor reading before fetching lux
        raw = self._sensor.get_lux()
        return raw, self._light_average.add(raw)
