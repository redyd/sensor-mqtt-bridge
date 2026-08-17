import csv
import datetime
import os
from collections.abc import Callable, Sequence

from core.air_quality_score import calculate_scores
from core.sensors_definitions import (
    Co2Sensor,
    HumiditySensor,
    LightSensor,
    MicrophoneSensor,
    ParticulateMatterSensor,
    PressureSensor,
    TemperatureSensor,
)

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sensors.csv")

SensorReading = tuple[float, float]


class SensorsExporter:
    """Aggregate sensor readings and export one JSON payload."""

    CSV_FIELDNAMES = [
        "timestamp",
        "temperature",
        "pressure",
        "humidity",
        "light",
        "sound_level",
        "particulate_matter",
        "co2",
        "score",
    ]

    def __init__(
        self,
        temperature_sensors: Sequence[TemperatureSensor] | None = None,
        pressure_sensors: Sequence[PressureSensor] | None = None,
        humidity_sensors: Sequence[HumiditySensor] | None = None,
        light_sensors: Sequence[LightSensor] | None = None,
        microphone_sensors: Sequence[MicrophoneSensor] | None = None,
        particulate_matter_sensors: Sequence[ParticulateMatterSensor] | None = None,
        co2_sensors: Sequence[Co2Sensor] | None = None,
        path: str = DEFAULT_PATH,
        write_every: int = 1,
    ):
        if write_every <= 0:
            raise ValueError("write_every must be greater than zero")

        self._temperature_sensors = list(temperature_sensors or [])
        self._pressure_sensors = list(pressure_sensors or [])
        self._humidity_sensors = list(humidity_sensors or [])
        self._light_sensors = list(light_sensors or [])
        self._microphone_sensors = list(microphone_sensors or [])
        self._particulate_matter_sensors = list(particulate_matter_sensors or [])
        self._co2_sensors = list(co2_sensors or [])

        self._path = path
        directory = os.path.dirname(self._path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        self._write_every = write_every
        self._export_count = 0

    def export(self) -> dict:
        payload = {
            "timestamp": datetime.datetime.now().isoformat(),
            "values": {},
        }

        self._add_value(payload["values"], "temperature", self._temperature_sensors, "get_temperature")
        self._add_value(payload["values"], "pressure", self._pressure_sensors, "get_pressure")
        self._add_value(payload["values"], "humidity", self._humidity_sensors, "get_humidity")
        self._add_value(payload["values"], "light", self._light_sensors, "get_light")
        self._add_value(payload["values"], "sound_level", self._microphone_sensors, "get_sound_level")
        self._add_value(payload["values"], "particulate_matter", self._particulate_matter_sensors, "get_particulate_matter")
        self._add_value(payload["values"], "co2", self._co2_sensors, "get_co2")

        self._add_scores(payload)

        self._export_count += 1
        if self._export_count % self._write_every == 0:
            self._write_payload(payload)

        return payload

    def _add_value(
        self,
        values: dict,
        key: str,
        sensors: Sequence,
        method_name: str,
    ) -> None:
        reading = self._aggregate(sensors, lambda sensor: getattr(sensor, method_name)())
        if reading is None:
            return

        raw, smooth = reading
        values[key] = {
            "raw": raw,
            "smooth": smooth,
        }

    def _aggregate(
        self,
        sensors: Sequence,
        read: Callable[[object], SensorReading],
    ) -> SensorReading | None:
        if not sensors:
            return None

        readings = [read(sensor) for sensor in sensors]
        if len(readings) == 1:
            return readings[0]

        raw_values = [reading[0] for reading in readings]
        smooth_values = [reading[1] for reading in readings]
        return self._average(raw_values), self._average(smooth_values)

    def _add_scores(self, payload: dict) -> None:
        values = payload["values"]
        required_keys = ("temperature", "humidity", "co2", "particulate_matter")
        if not all(key in values for key in required_keys):
            return

        scores = calculate_scores(
            temperature=values["temperature"]["smooth"],
            humidity=values["humidity"]["smooth"],
            co2=values["co2"]["smooth"],
            particulate_matter=values["particulate_matter"]["smooth"],
        )

        for key in required_keys:
            values[key]["score"] = scores[key]
        payload["score"] = scores["global"]

    def _write_payload(self, payload: dict) -> None:
        file_exists = os.path.isfile(self._path)
        file_is_empty = not file_exists or os.path.getsize(self._path) == 0

        with open(self._path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_FIELDNAMES)
            if file_is_empty:
                writer.writeheader()
            writer.writerow(self._build_csv_row(payload))

    def _build_csv_row(self, payload: dict) -> dict:
        values = payload["values"]
        row = {
            "timestamp": payload["timestamp"],
            "score": payload.get("score"),
        }

        for key in self.CSV_FIELDNAMES:
            if key in ("timestamp", "score"):
                continue
            reading = values.get(key)
            row[key] = reading["smooth"] if reading is not None else None

        return row

    @staticmethod
    def _average(values: Sequence[float]) -> float:
        return sum(values) / len(values)
