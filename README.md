# Sensor MQTT Bridge

A Python application for collecting environmental sensor data and publishing it via MQTT protocol.

## Overview

This project collects data from multiple environmental sensors, logs it to CSV, and publishes it to an MQTT broker for real-time monitoring and integration with other systems.

## Project Structure

```
sensor-mqtt-bridge/
├── main.py                    # Application entry point
├── config.json                # Configuration file
├── requirements.txt           # Python dependencies
├── core/
│   ├── mqtt_client.py         # MQTT broker connection
│   ├── command_receiver.py    # MQTT command handler
│   ├── sensors_exporter.py    # Data collection and CSV logging
│   └── sensors_definitions.py # Sensor interface protocols
├── sensors/                   # Sensor implementations
│   ├── bme280_sensor.py       # Temperature, Pressure, Humidity
│   ├── ltr559_sensor.py       # Light sensor
│   ├── sph0645_sensor.py      # Microphone
│   ├── pms5003_sensor.py      # Particulate matter
│   ├── scd30_sensor.py        # CO2
│   └── lmt84_sensor.py        # Additional sensor
├── fakes/
│   └── mock_sensor.py         # Test sensor for development
├── utils/
│   ├── initializer.py         # Sensor initialization logic
│   └── sliding_average.py     # Data processing utilities
└── data/
    └── sensors.csv            # Sensor data log
```

## Supported Sensors

| Sensor | Measurement | Unit |
|--------|-------------|------|
| BME280 | Temperature, Pressure, Humidity | °C, hPa, % |
| LTR559 | Light | Lux |
| SPH0645 | Sound Level | dB |
| PMS5003 | Particulate Matter | µg/m³ |
| SCD30 | CO2 | ppm |

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sensor-mqtt-bridge
```

2. Start venv & install dependencies:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

The `requirements.txt` includes:
- paho-mqtt: MQTT client library
- bme280: BME280 sensor driver
- smbus2: I2C communication
- ltr559: LTR559 sensor driver
- pms5003: PMS5003 sensor driver
- scd30-i2c: SCD30 sensor driver
- numpy: Numerical computations
- sounddevice: Audio capture for microphone

## Configuration

Edit `config.json` to configure the application:

```json
{
  "enabled_sensors": {
    "bme280": true,
    "ltr559": true,
    "sph0645": false,
    "pms5003": true,
    "scd30": true
  },
  "mqtt_broker": "192.168.1.46",
  "mqtt_port": 1883,
  "update_interval": 2
}
```

Parameters:
- `enabled_sensors`: Enable/disable individual sensors
- `mqtt_broker`: IP address or hostname of MQTT broker
- `mqtt_port`: MQTT broker port
- `update_interval`: Seconds between sensor readings

### Important Notes

- If a sensor is enabled but unavailable, the application will exit with an error
- The SPH0645 microphone sensor may interfere with Bluetooth audio; disable it if not needed
- All enabled sensors must be functional or properly configured as unavailable

## Usage

Start the application:

```bash
python main.py
```

The application will:
1. Initialize all enabled sensors
2. Connect to the MQTT broker
3. Continuously collect sensor data
4. Publish data to `sensors/data` topic in JSON format
5. Log data to CSV file

Data format published to MQTT:
```json
{
  "timestamp": "2026-08-14T16:13:06.586810",
  "temperature": 22.5,
  "pressure": 1013.25,
  "humidity": 45.6,
  "light": 450.2,
  "sound_level": 35.5,
  "particulate_matter": {
    "pm1_0": 5,
    "pm2_5": 8,
    "pm10": 12
  },
  "co2": 520.4
}
```

## MQTT Topics

### Published Topics

- `sensors/data`: Sensor measurements (JSON format)

### Subscribed Topics

- `commands/status`: Status requests (expects `{"command": "get_status"}`)

## Error Handling

If an enabled sensor fails to initialize, the application will display:
```
FATAL ERROR: <SensorName> is ENABLED but unavailable!
Error details: <error message>

To fix this issue:
1. Disable this sensor in config.json
2. Or check hardware connection and drivers
```

The application will then exit with code 1.

## Logging

Sensor data is automatically logged to `data/sensors.csv` with the following columns:
- timestamp
- temperature
- pressure
- humidity
- light
- sound_level
- particulate_matter
- co2

## Development

For testing without physical sensors, disable all sensors in `config.json`. The application will use mock sensors that generate random values.

## On Raspberry

```bash
sudo apt update
sudo apt install -y python3-dev python3-venv i2c-tools libatlas-base-dev portaudio19-dev
```

Clone repo & classic installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Add user to I2C bus

```bash
sudo usermod -aG i2c $USER
```

Start !

```bash
python main.py
```

## TODO

- [ ] Vérifier la conformité des types et formats de données avec le cahier des charges
- [ ] Définir tous les topics MQTT et commandes: fréquences, bouton pause, bouton reset
- [ ] Définir et implémenter le gestionnaire de réponses pour tous les topics et commandes
- [ ] Intégrer au système de dashboard (interface de visualisation et de contrôle des données)
- [ ] Deux capteurs mesure la température (BME280 & LMT84) ?: utiliser les deux