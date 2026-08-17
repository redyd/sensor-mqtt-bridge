import importlib
import tempfile
import unittest

from core.sensors_exporter import SensorsExporter


class FixedSensor:
    def __init__(self, **readings):
        self._readings = readings

    def get_temperature(self):
        return self._readings["temperature"]

    def get_pressure(self):
        return self._readings["pressure"]

    def get_humidity(self):
        return self._readings["humidity"]

    def get_light(self):
        return self._readings["light"]

    def get_sound_level(self):
        return self._readings["sound_level"]

    def get_particulate_matter(self):
        return self._readings["particulate_matter"]

    def get_co2(self):
        return self._readings["co2"]


class SensorsExporterTest(unittest.TestCase):
    def test_imports_do_not_raise(self):
        importlib.import_module("core.sensors_exporter")
        importlib.import_module("fakes.mock_sensor")

    def test_single_sensor_value_is_preserved(self):
        sensor = FixedSensor(temperature=(21.5, 21.0))

        payload = SensorsExporter(
            temperature_sensors=[sensor],
            path=self._temporary_path(),
        ).export()

        self.assertEqual(payload["values"]["temperature"], {"raw": 21.5, "smooth": 21.0})

    def test_multiple_sensors_are_averaged_arithmetically(self):
        first = FixedSensor(temperature=(20.0, 19.0))
        second = FixedSensor(temperature=(24.0, 23.0))

        payload = SensorsExporter(
            temperature_sensors=[first, second],
            path=self._temporary_path(),
        ).export()

        self.assertEqual(payload["values"]["temperature"]["raw"], 22.0)
        self.assertEqual(payload["values"]["temperature"]["smooth"], 21.0)

    def test_smooth_value_is_not_rounded_on_export(self):
        first = FixedSensor(temperature=(20.0, 19.1111))
        second = FixedSensor(temperature=(24.0, 23.2222))

        payload = SensorsExporter(
            temperature_sensors=[first, second],
            path=self._temporary_path(),
        ).export()

        self.assertEqual(payload["values"]["temperature"]["smooth"], 21.16665)

    def test_particulate_matter_exports_only_pm2_5_numeric_value(self):
        sensor = FixedSensor(particulate_matter=(8.0, 7.5))

        payload = SensorsExporter(
            particulate_matter_sensors=[sensor],
            path=self._temporary_path(),
        ).export()

        self.assertEqual(payload["values"]["particulate_matter"], {"raw": 8.0, "smooth": 7.5})

    def test_payload_contains_scores_when_required_values_are_present(self):
        sensor = FixedSensor(
            temperature=(22.5, 22.0),
            humidity=(45.0, 50.0),
            co2=(620.0, 600.0),
            particulate_matter=(8.0, 10.0),
        )

        payload = SensorsExporter(
            temperature_sensors=[sensor],
            humidity_sensors=[sensor],
            co2_sensors=[sensor],
            particulate_matter_sensors=[sensor],
            path=self._temporary_path(),
        ).export()

        self.assertIn("timestamp", payload)
        self.assertEqual(payload["score"], 10)
        for key in ("temperature", "humidity", "co2", "particulate_matter"):
            self.assertEqual(payload["values"][key]["score"], 10)

    def test_payload_omits_global_score_without_required_values(self):
        sensor = FixedSensor(temperature=(22.5, 22.0))

        payload = SensorsExporter(
            temperature_sensors=[sensor],
            path=self._temporary_path(),
        ).export()

        self.assertNotIn("score", payload)
        self.assertNotIn("score", payload["values"]["temperature"])

    def test_export_writes_csv_with_smooth_values_and_global_score(self):
        sensor = FixedSensor(
            temperature=(22.5, 22.0),
            pressure=(1013.0, 1012.5),
            humidity=(45.0, 50.0),
            light=(300.0, 295.0),
            sound_level=(0.03, 0.02),
            particulate_matter=(8.0, 10.0),
            co2=(620.0, 600.0),
        )

        with tempfile.NamedTemporaryFile(mode="r+") as file:
            payload = SensorsExporter(
                temperature_sensors=[sensor],
                pressure_sensors=[sensor],
                humidity_sensors=[sensor],
                light_sensors=[sensor],
                microphone_sensors=[sensor],
                particulate_matter_sensors=[sensor],
                co2_sensors=[sensor],
                path=file.name,
            ).export()

            file.seek(0)
            rows = file.readlines()

        self.assertEqual(rows[0], "timestamp,temperature,pressure,humidity,light,sound_level,particulate_matter,co2,score\n")
        self.assertEqual(len(rows), 2)
        self.assertIn(payload["timestamp"], rows[1])
        self.assertIn(",22.0,1012.5,50.0,295.0,0.02,10.0,600.0,10.0\n", rows[1])

    def _temporary_path(self):
        return tempfile.NamedTemporaryFile().name


if __name__ == "__main__":
    unittest.main()
