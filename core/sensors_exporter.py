from core.sensors_definitions import *

import csv
import datetime
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sensors.csv")


class SensorsExporter:
    """Export sensor data to a single CSV file with raw and smoothed values."""

    TEMPERATURE_SENSOR: TemperatureSensor
    PRESSURE_SENSOR: PressureSensor
    HUMIDITY_SENSOR: HumiditySensor
    LIGHT_SENSOR: LightSensor
    MICROPHONE_SENSOR: MicrophoneSensor
    PARTICULE_MATTER_SENSOR: ParticulateMatterSensor
    CO2_CENSOR: Co2Sensor

    CSV_FIELDNAMES = [
        "timestamp",
        "temperature",
        "temperature_smooth",
        "pressure",
        "pressure_smooth",
        "humidity",
        "humidity_smooth",
        "light",
        "light_smooth",
        "sound_level",
        "sound_level_smooth",
        "particulate_matter",
        "particulate_matter_smooth",
        "co2",
        "co2_smooth",
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
        directory = os.path.dirname(self._path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        self._write_every = write_every
        self._export_count = 0

    def export(self) -> dict:
        now = datetime.datetime.now().isoformat()

        temperature_raw, temperature_smooth = self.TEMPERATURE_SENSOR.get_temperature()
        pressure_raw, pressure_smooth = self.PRESSURE_SENSOR.get_pressure()
        humidity_raw, humidity_smooth = self.HUMIDITY_SENSOR.get_humidity()
        light_raw, light_smooth = self.LIGHT_SENSOR.get_light()
        sound_raw, sound_smooth = self.MICROPHONE_SENSOR.get_sound_level()
        particulate_raw, particulate_smooth = self.PARTICULE_MATTER_SENSOR.get_particulate_matter()
        co2_raw, co2_smooth = self.CO2_CENSOR.get_co2()

        raw_data = {
            "timestamp": now,
            "temperature": temperature_raw,
            "pressure": pressure_raw,
            "humidity": humidity_raw,
            "light": light_raw,
            "sound_level": sound_raw,
            "particulate_matter": particulate_raw,
            "co2": co2_raw,
        }

        smooth_data = {
            "timestamp": now,
            "temperature": temperature_smooth,
            "pressure": pressure_smooth,
            "humidity": humidity_smooth,
            "light": light_smooth,
            "sound_level": sound_smooth,
            "particulate_matter": particulate_smooth,
            "co2": co2_smooth,
        }

        data = {
            "raw": raw_data,
            "smooth": smooth_data,
        }

        self._export_count += 1
        if self._export_count % self._write_every == 0:
            self._write_row(raw_data, smooth_data)

        return data

    def _write_row(self, raw_data: dict, smooth_data: dict):
        file_exists = os.path.isfile(self._path)

        with open(self._path, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_FIELDNAMES)
            if not file_exists:
                writer.writeheader()

            row = {
                "timestamp": raw_data["timestamp"],
                "temperature": raw_data["temperature"],
                "temperature_smooth": smooth_data["temperature"],
                "pressure": raw_data["pressure"],
                "pressure_smooth": smooth_data["pressure"],
                "humidity": raw_data["humidity"],
                "humidity_smooth": smooth_data["humidity"],
                "light": raw_data["light"],
                "light_smooth": smooth_data["light"],
                "sound_level": raw_data["sound_level"],
                "sound_level_smooth": smooth_data["sound_level"],
                "particulate_matter": raw_data["particulate_matter"],
                "particulate_matter_smooth": smooth_data["particulate_matter"],
                "co2": raw_data["co2"],
                "co2_smooth": smooth_data["co2"],
            }
            writer.writerow(row)
