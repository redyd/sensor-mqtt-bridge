from core.sensors_definitions import *

import csv
import datetime
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sensors.csv")


class SensorsExporter:
    """Export sensor data to a single CSV file with raw and smoothed values."""

    TENSION_TEMPERATURE_SENSOR: TensionTemperatureSensor
    PRESSURE_SENSOR: PressureSensor
    HUMIDITY_SENSOR: HumiditySensor
    LIGHT_SENSOR: LightSensor
    MICROPHONE_SENSOR: MicrophoneSensor
    PARTICULE_MATTER_SENSOR: ParticulateMatterSensor
    CO2_CENSOR: Co2Sensor

    CSV_FIELDNAMES = [
        "timestamp",
        "relative_temperature",
        "relative_temperature_smooth",
        "tension_temperature",
        "tension_temperature_smooth",
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
        tension_temperature_sensor: TensionTemperatureSensor,
        relative_temperature_sensor: RelativeTemperatureSensor,
        pressure_sensor: PressureSensor,
        humidity_sensor: HumiditySensor,
        light_sensor: LightSensor,
        microphone_sensor: MicrophoneSensor,
        particulate_matter_sensor: ParticulateMatterSensor,
        co2_sensor: Co2Sensor,
        path: str = DEFAULT_PATH,
        write_every: int = 1,
    ):
        self.TENSION_TEMPERATURE_SENSOR = tension_temperature_sensor
        self.RELATIVE_TEMPERATURE_SENSOR = relative_temperature_sensor
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

        tension_temperature_raw, tension_temperature_smooth = self.TENSION_TEMPERATURE_SENSOR.get_tension_temperature()
        relative_temperature_raw, relative_temperature_smooth = self.RELATIVE_TEMPERATURE_SENSOR.get_relative_temperature()
        pressure_raw, pressure_smooth = self.PRESSURE_SENSOR.get_pressure()
        humidity_raw, humidity_smooth = self.HUMIDITY_SENSOR.get_humidity()
        light_raw, light_smooth = self.LIGHT_SENSOR.get_light()
        sound_raw, sound_smooth = self.MICROPHONE_SENSOR.get_sound_level()
        particulate_raw, particulate_smooth = self.PARTICULE_MATTER_SENSOR.get_particulate_matter()
        co2_raw, co2_smooth = self.CO2_CENSOR.get_co2()

        raw_data = {
            "timestamp": now,
            "relative_temperature": relative_temperature_raw,
            "tension_temperature": tension_temperature_raw,
            "pressure": pressure_raw,
            "humidity": humidity_raw,
            "light": light_raw,
            "sound_level": sound_raw,
            "particulate_matter": particulate_raw,
            "co2": co2_raw,
        }

        smooth_data = {
            "timestamp": now,
            "tension_temperature": tension_temperature_smooth,
            "relative_temperature": relative_temperature_smooth,
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

    def _build_row(self, raw_data: dict, smooth_data: dict) -> dict:
        row = {"timestamp": raw_data["timestamp"]}
        for key in (
            "relative_temperature",
            "tension_temperature",
            "pressure",
            "humidity",
            "light",
            "sound_level",
            "particulate_matter",
            "co2",
        ):
            row[f"{key}"] = raw_data[key]
            row[f"{key}_smooth"] = smooth_data[key]
        return row

    def _write_row(self, raw_data: dict, smooth_data: dict):
        file_exists = os.path.isfile(self._path)

        with open(self._path, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_FIELDNAMES)
            if not file_exists:
                writer.writeheader()

            row = self._build_row(raw_data, smooth_data)
            writer.writerow({fieldname: row.get(fieldname) for fieldname in self.CSV_FIELDNAMES})
