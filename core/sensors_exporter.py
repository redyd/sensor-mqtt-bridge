from core.sensors_definitions import *

import csv
import datetime
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sensors.csv")


class SensorsExporter:
    """Exporte les données des capteurs et les journalise dans un fichier CSV."""

    TEMPERATURE_SENSOR: TemperatureSensor
    PRESSURE_SENSOR: PressureSensor
    HUMIDITY_SENSOR: HumiditySensor
    LIGHT_SENSOR: LightSensor
    MICROPHONE_SENSOR: MicrophoneSensor
    PARTICULE_MATTER_SENSOR: ParticulateMatterSensor
    CO2_CENSOR: Co2Sensor

    FIELDNAMES = [
        "timestamp",
        "temperature",
        "pressure",
        "humidity",
        "light",
        "sound_level",
        "particulate_matter",
        "co2",
    ]

    def __init__(
        self,
        temperature_sensor: TemperatureSensor,
        pressure_sensor: PressureSensor,
        humidity_sensor: HumiditySensor,
        light_sensor: LightSensor,
        microphone_sensor: MicrophoneSensor,
        particulate_matter_sensor: ParticulateMatterSensor,
        co2_sensor: Co2Sensor,
        path: str = DEFAULT_PATH,
        write_every: int = 1,
    ):
        self.TEMPERATURE_SENSOR = temperature_sensor
        self.PRESSURE_SENSOR = pressure_sensor
        self.HUMIDITY_SENSOR = humidity_sensor
        self.LIGHT_SENSOR = light_sensor
        self.MICROPHONE_SENSOR = microphone_sensor
        self.PARTICULE_MATTER_SENSOR = particulate_matter_sensor
        self.CO2_CENSOR = co2_sensor

        self._path = path
        self._write_every = write_every
        self._export_count = 0

    def export(self) -> dict:
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "temperature": self.TEMPERATURE_SENSOR.get_temperature(),
            "pressure": self.PRESSURE_SENSOR.get_pressure(),
            "humidity": self.HUMIDITY_SENSOR.get_humidity(),
            "light": self.LIGHT_SENSOR.get_light(),
            "sound_level": self.MICROPHONE_SENSOR.get_sound_level(),
            "particulate_matter": self.PARTICULE_MATTER_SENSOR.get_particulate_matter(),
            "co2": self.CO2_CENSOR.get_co2(),
        }

        self._export_count += 1
        if self._export_count % self._write_every == 0:
            self._write(data)

        return data

    def _write(self, data: dict):
        file_exists = os.path.isfile(self._path)
        directory = os.path.dirname(self._path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self._path, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
