"""Initialization utilities for configuration and sensors."""

import json
import os
import sys
from fakes.mock_sensor import MockSensor
from sensors.bme280_sensor import Bme280Sensor
from sensors.ltr559_sensor import Ltr559Sensor
from sensors.sph0645_sensor import Sph0645Sensor
from sensors.pms5003_sensor import Pms5003Sensor
from sensors.scd30_sensor import Scd30Sensor
from sensors.lmt84_sensor import Lmt84Sensor


def load_config():
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


def init_sensor(sensor_class, enabled=True):
    if not enabled:
        print(f"! {sensor_class.__name__} disabled in configuration.")
        return MockSensor()
    
    try:
        sensor = sensor_class()
        print(f"{sensor_class.__name__} initialized successfully.")
        return sensor
    except BaseException as error:
        print(f"\nFATAL ERROR: {sensor_class.__name__} is ENABLED but unavailable!")
        print(f"Error details: {error}")
        print("\nTo fix this issue:")
        print(f"  1. Disable this sensor in config.json by setting '{sensor_class.__name__.lower()}': false")
        print("  2. Or check that your hardware is properly connected and drivers are installed")
        sys.exit(1)


def init_all_sensors(config):
    enabled = config["enabled_sensors"]
    
    print("\n=== Sensor Initialization ===\n")
    
    sensors = {
        "bme280": init_sensor(Bme280Sensor, enabled["bme280"]),
        "ltr559": init_sensor(Ltr559Sensor, enabled["ltr559"]),
        "sph0645": init_sensor(Sph0645Sensor, enabled["sph0645"]),
        "pms5003": init_sensor(Pms5003Sensor, enabled["pms5003"]),
        "scd30": init_sensor(Scd30Sensor, enabled["scd30"]),
        "lmt84": init_sensor(Lmt84Sensor, enabled["lmt84"])
    }
    
    print("\n=== All sensors initialized ===\n")
    
    return sensors
