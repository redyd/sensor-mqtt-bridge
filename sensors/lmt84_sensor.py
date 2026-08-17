from gpiozero import MCP3008

from core.sensors_definitions import TemperatureSensor
from utils.sliding_average import SlidingAverage


class Lmt84Sensor(TemperatureSensor):
    """LMT84 : température (capteur analogique, lu via ADC MCP3008)."""

    # Vout = -5.50 mV/°C x T + 1035 mV (datasheet LMT84)
    _SLOPE_MV_PER_C = -5.50
    _OFFSET_MV = 1035

    def __init__(self, channel=0, reference_voltage=3.3):
        self._adc = MCP3008(channel=channel)
        self._reference_voltage = reference_voltage
        self._temperature_average = SlidingAverage()

    def get_temperature(self) -> tuple[float, float]:
        raw = self._adc.value * self._reference_voltage * 1000
        raw_temperature = (raw - self._OFFSET_MV) / self._SLOPE_MV_PER_C
        return raw_temperature, self._temperature_average.add(raw_temperature)
