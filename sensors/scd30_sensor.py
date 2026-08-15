from scd30_i2c import SCD30

from core.sensors_definitions import Co2Sensor
from utils.sliding_average import SlidingAverage


class Scd30Sensor(Co2Sensor):
    """SCD30: CO2."""

    def __init__(self):
        self._sensor = SCD30()
        self._sensor.start_periodic_measurement()
        self._co2_average = SlidingAverage()

    def get_co2(self) -> tuple[float, float]:
        while not self._sensor.get_data_ready():
            pass

        measurement = self._sensor.read_measurement()
        if measurement is None:
            raise RuntimeError("SCD30 measurement could not be read")

        raw = measurement[0]
        return raw, self._co2_average.add(raw)
