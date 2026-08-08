from ltr559 import LTR559

from core.sensors_definitions import LightSensor


class Ltr559Sensor(LightSensor):
    """LTR559 : lumière ambiante."""

    def __init__(self):
        self._sensor = LTR559()

    def get_light(self) -> float:
        self._sensor.update_sensor()
        return self._sensor.get_lux()
