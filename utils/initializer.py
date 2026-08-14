"""Utilitaires d'initialisation pour la configuration et les capteurs."""

import json
import os
from fakes.mock_sensor import MockSensor
from sensors.bme280_sensor import Bme280Sensor
from sensors.ltr559_sensor import Ltr559Sensor
from sensors.sph0645_sensor import Sph0645Sensor
from sensors.pms5003_sensor import Pms5003Sensor
from sensors.scd30_sensor import Scd30Sensor


def load_config():
    """Charge la configuration depuis config.json ou utilise les valeurs par défaut."""
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
        },
        "mqtt_broker": "192.168.1.46",
        "mqtt_port": 1883,
        "update_interval": 2,
    }


def init_sensor(sensor_class, fallback, enabled=True):
    """Initialise un capteur si activé, sinon retourne le fallback."""
    if not enabled:
        print(f"{sensor_class.__name__} désactivé dans la configuration.")
        return fallback
    try:
        return sensor_class()
    except BaseException as error:
        print(f"{sensor_class.__name__} indisponible ({error}), capteur factice utilisé.")
        return fallback


def init_all_sensors(config):
    """Initialise tous les capteurs selon la configuration."""
    enabled = config["enabled_sensors"]
    mock = MockSensor()
    
    return {
        "bme280": init_sensor(Bme280Sensor, mock, enabled["bme280"]),
        "ltr559": init_sensor(Ltr559Sensor, mock, enabled["ltr559"]),
        "sph0645": init_sensor(Sph0645Sensor, mock, enabled["sph0645"]),
        "pms5003": init_sensor(Pms5003Sensor, mock, enabled["pms5003"]),
        "scd30": init_sensor(Scd30Sensor, mock, enabled["scd30"]),
        "mock": mock,
    }
