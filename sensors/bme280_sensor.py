import bme280
import smbus2

from core.sensors_definitions import HumiditySensor, PressureSensor, TemperatureSensor


class Bme280Sensor(TemperatureSensor, PressureSensor, HumiditySensor):
    """BME280 : température, pression et humidité relative."""

    def __init__(self, port=1, address=0x76):
        self._bus = smbus2.SMBus(port)
        self._calibration_params = bme280.load_calibration_params(self._bus, address)
        self._address = address

    def _read(self):
        return bme280.sample(self._bus, self._address, self._calibration_params)

    def get_temperature(self) -> float:
        return self._read().temperature

    def get_pressure(self) -> float:
        return self._read().pressure

    def get_humidity(self) -> float:
        return self._read().humidity
