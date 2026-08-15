import bme280
import smbus2

from core.sensors_definitions import HumiditySensor, PressureSensor, TemperatureSensor
from utils.sliding_average import SlidingAverage


class Bme280Sensor(TemperatureSensor, PressureSensor, HumiditySensor):
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

    def get_temperature(self) -> float:
        return self._read().temperature

    def get_average_temperature(self) -> float:
        return self._temperature_average.add(self.get_temperature())

    def get_pressure(self) -> float:
        return self._read().pressure

    def get_average_pressure(self) -> float:
        return self._pressure_average.add(self.get_pressure())

    def get_humidity(self) -> float:
        return self._read().humidity

    def get_average_humidity(self) -> float:
        return self._humidity_average.add(self.get_humidity())
