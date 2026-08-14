from pms5003 import PMS5003

from core.sensors_definitions import ParticulateMatterSensor


class Pms5003Sensor(ParticulateMatterSensor):
    """PMS5003 : particules fines."""

    def __init__(self):
        self._sensor = PMS5003()

    def get_particulate_matter(self) -> dict:
        reading = self._sensor.read()
        return {
            "pm1_0": reading.pm_ug_per_m3(1.0),
            "pm2_5": reading.pm_ug_per_m3(2.5),
            "pm10": reading.pm_ug_per_m3(10),
        }
