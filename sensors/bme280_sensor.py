import bme280
import smbus2

from core.sensors_definitions import HumiditySensor, PressureSensor, RelativeTemperatureSensor
from utils.sliding_average import SlidingAverage


class Bme280Sensor(RelativeTemperatureSensor, PressureSensor, HumiditySensor):
    """BME280: temperature, pressure, and relative humidity."""

    def __init__(self, port=1, address=0x76):
        self._bus = smbus2.SMBus(port)
        self._calibration_params = bme280.load_calibration_params(self._bus, address)
        self._address = address
        self._temperature_average = SlidingAverage()
        self._pressure_average = SlidingAverage()
        self._humidity_average = SlidingAverage()

    def _read(self):
        return bme280.sample(self._bus, self._address, self._calibration_params)

    def get_relative_temperature(self) -> tuple[float, float]:
        raw = self._read().temperature
        return raw, self._temperature_average.add(raw)

    def get_pressure(self) -> tuple[float, float]:
        raw = self._read().pressure
        return raw, self._pressure_average.add(raw)

    def get_humidity(self) -> tuple[float, float]:
        raw = self._read().humidity
        return raw, self._humidity_average.add(raw)
