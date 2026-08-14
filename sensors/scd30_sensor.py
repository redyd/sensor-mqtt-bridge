from scd30_i2c import SCD30

from core.sensors_definitions import Co2Sensor


class Scd30Sensor(Co2Sensor):
    """SCD30: CO2."""

    def __init__(self):
        self._sensor = SCD30()
        self._sensor.start_periodic_measurement()

    def get_co2(self) -> float:
        while not self._sensor.get_data_ready():
            pass
        co2, _temperature, _humidity = self._sensor.read_measurement()
        return co2
