import datetime
from collections.abc import Sequence

from core.air_quality_score import calculate_scores
from core.sensors_definitions import (
    Co2Sensor,
    HumiditySensor,
    LightSensor,
    MicrophoneSensor,
    ParticulateMatterSensor,
    PressureSensor,
    SensorReading,
    TemperatureSensor,
)
from core.sensors_writer import DEFAULT_PATH, SensorsCsvWriter


class SensorsExporter:
    """Aggregate sensor readings and export one JSON payload."""

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
        writer: SensorsCsvWriter | None = None,
        write_every: int = 1,  # write to CSV every N exports
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

        self._writer = writer or SensorsCsvWriter(path)
        self._write_every = write_every
        self._export_count = 0

    def export(self) -> dict:
        payload = {
            "timestamp": datetime.datetime.now().isoformat(),
            "values": {},
        }

        self._set_value(
            payload["values"],
            "temperature",
            self._aggregate_readings([sensor.get_temperature() for sensor in self._temperature_sensors]),
        )
        self._set_value(
            payload["values"],
            "pressure",
            self._aggregate_readings([sensor.get_pressure() for sensor in self._pressure_sensors]),
        )
        self._set_value(
            payload["values"],
            "humidity",
            self._aggregate_readings([sensor.get_humidity() for sensor in self._humidity_sensors]),
        )
        self._set_value(
            payload["values"],
            "light",
            self._aggregate_readings([sensor.get_light() for sensor in self._light_sensors]),
        )
        self._set_value(
            payload["values"],
            "sound_level",
            self._aggregate_readings([sensor.get_sound_level() for sensor in self._microphone_sensors]),
        )
        self._set_value(
            payload["values"],
            "particulate_matter",
            self._aggregate_readings([
                sensor.get_particulate_matter()
                for sensor in self._particulate_matter_sensors
            ]),
        )
        self._set_value(
            payload["values"],
            "co2",
            self._aggregate_readings([sensor.get_co2() for sensor in self._co2_sensors]),
        )

        self._add_scores(payload)

        self._export_count += 1
        if self._export_count % self._write_every == 0:
            self._writer.write(payload)

        return payload

    def _set_value(self, values: dict, key: str, reading: SensorReading | None) -> None:
        if reading is None:
            return

        raw, smooth = reading
        values[key] = {
            "raw": raw,
            "smooth": smooth,
        }

    def _aggregate_readings(self, readings: Sequence[SensorReading]) -> SensorReading | None:
        if not readings:
            return None

        if len(readings) == 1:
            return readings[0]

        raw_values = [reading[0] for reading in readings]
        smooth_values = [reading[1] for reading in readings]
        return self._average(raw_values), self._average(smooth_values)

    def _add_scores(self, payload: dict) -> None:
        # scores are only computed when all four required metrics are present
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

    @staticmethod
    def _average(values: Sequence[float]) -> float:
        return sum(values) / len(values)
