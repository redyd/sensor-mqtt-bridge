import unittest
from unittest.mock import patch

from fakes.mock_sensor import MockSensor
from utils import initializer


class InitializerTest(unittest.TestCase):
    def test_disabled_sensor_does_not_load_hardware_dependency(self):
        with patch("utils.initializer.load_sensor_class") as load_sensor_class:
            sensor = initializer.init_sensor("bme280", enabled=False)

        self.assertIsInstance(sensor, MockSensor)
        load_sensor_class.assert_not_called()

    def test_windows_uses_mock_sensor_without_loading_hardware_dependency(self):
        with patch("utils.initializer.platform.system", return_value="Windows"):
            with patch("utils.initializer.load_sensor_class") as load_sensor_class:
                sensor = initializer.init_sensor("bme280", enabled=True)

        self.assertIsInstance(sensor, MockSensor)
        load_sensor_class.assert_not_called()


if __name__ == "__main__":
    unittest.main()
