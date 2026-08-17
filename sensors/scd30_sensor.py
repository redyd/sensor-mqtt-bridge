from scd30_i2c import SCD30

from core.sensors_definitions import Co2Sensor, HumiditySensor, TemperatureSensor
from utils.sliding_average import SlidingAverage


class Scd30Sensor(Co2Sensor, TemperatureSensor, HumiditySensor):
    """SCD30: CO2, temperature, and relative humidity."""

    def __init__(self):
        self._sensor = SCD30()
        self._sensor.start_periodic_measurement()
        self._co2_average = SlidingAverage()
        self._temperature_average = SlidingAverage()
        self._humidity_average = SlidingAverage()

    def _read_measurement(self):
        while not self._sensor.get_data_ready():
            pass

        measurement = self._sensor.read_measurement()
        if measurement is None:
            raise RuntimeError("SCD30 measurement could not be read")
        return measurement

    def get_co2(self) -> tuple[float, float]:
        measurement = self._read_measurement()
        raw = measurement[0]
        return raw, self._co2_average.add(raw)

    def get_temperature(self) -> tuple[float, float]:
        measurement = self._read_measurement()
        raw = measurement[1]
        return raw, self._temperature_average.add(raw)

    def get_humidity(self) -> tuple[float, float]:
        measurement = self._read_measurement()
        raw = measurement[2]
        return raw, self._humidity_average.add(raw)
