"""Initialization utilities for configuration and sensors."""

import json
import os
import platform
import sys

from fakes.mock_sensor import MockSensor

SENSOR_DEPENDENCIES: dict[str, tuple[str, str]] = {
    "bme280": ("sensors.bme280_sensor", "Bme280Sensor"),
    "ltr559": ("sensors.ltr559_sensor", "Ltr559Sensor"),
    "sph0645": ("sensors.sph0645_sensor", "Sph0645Sensor"),
    "pms5003": ("sensors.pms5003_sensor", "Pms5003Sensor"),
    "scd30": ("sensors.scd30_sensor", "Scd30Sensor"),
    "lmt84": ("sensors.lmt84_sensor", "Lmt84Sensor"),
}


def load_config() -> dict:
    """Load configuration from config.json or use default values."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {
        "enabled_sensors": {
            "bme280": True,
            "ltr559": True,
            "sph0645": True,
            "pms5003": True,
            "scd30": True,
            "lmt84": True
        },
        "mqtt_broker": "192.168.1.46",
        "mqtt_port": 1883,
        "update_interval": 2,
    }


def load_sensor_class(sensor_key: str) -> type:
    module_name, class_name = SENSOR_DEPENDENCIES[sensor_key]
    module = __import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)


def init_sensor(sensor_key: str, enabled: bool = True) -> object:
    module_name, class_name = SENSOR_DEPENDENCIES[sensor_key]

    if not enabled:
        print(f"! {class_name} disabled in configuration.")
        return MockSensor()

    if platform.system() == "Windows":
        print(f"! {class_name} uses hardware dependencies unavailable on Windows. Using MockSensor.")
        return MockSensor()

    try:
        sensor_class = load_sensor_class(sensor_key)
        sensor = sensor_class()
        print(f"{sensor_class.__name__} initialized successfully.")
        return sensor
    except BaseException as error:  # catch hardware errors (ImportError, OSError, etc.)
        print(f"\nFATAL ERROR: {class_name} is ENABLED but unavailable!")
        print(f"Error details: {error}")
        print("\nTo fix this issue:")
        print(f"  1. Disable this sensor in config.json by setting '{sensor_key}': false")
        print("  2. Or check that your hardware is properly connected and drivers are installed")
        sys.exit(1)


def init_all_sensors(config: dict) -> dict[str, object]:
    enabled = config["enabled_sensors"]

    print("\n=== Sensor Initialization ===\n")

    sensors = {
        "bme280": init_sensor("bme280", enabled["bme280"]),
        "ltr559": init_sensor("ltr559", enabled["ltr559"]),
        "sph0645": init_sensor("sph0645", enabled["sph0645"]),
        "pms5003": init_sensor("pms5003", enabled["pms5003"]),
        "scd30": init_sensor("scd30", enabled["scd30"]),
        "lmt84": init_sensor("lmt84", enabled["lmt84"])
    }

    print("\n=== All sensors initialized ===\n")

    return sensors
