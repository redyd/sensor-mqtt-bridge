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
  "timestamp": "2026-08-17T12:00:00.000000",
  "values": {
    "temperature": {
      "raw": 22.4,
      "smooth": 22.1,
      "score": 10
    },
    "pressure": {
      "raw": 1012.8,
      "smooth": 1012.4
    },
    "humidity": {
      "raw": 48.0,
      "smooth": 47.6,
      "score": 10
    },
    "light": {
      "raw": 300.0,
      "smooth": 295.0
    },
    "sound_level": {
      "raw": 0.03,
      "smooth": 0.02
    },
    "particulate_matter": {
      "raw": 8.0,
      "smooth": 7.5,
      "score": 10
    },
    "co2": {
      "raw": 620.0,
      "smooth": 610.0,
      "score": 10
    }
  },
  "score": 10
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
- score

Only smoothed values are written to the CSV file, plus the global score:

```csv
timestamp,temperature,pressure,humidity,light,sound_level,particulate_matter,co2,score
2026-08-17T12:00:00.000000,22.1,1012.4,47.6,295.0,0.02,7.5,610.0,10
```

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
```²

Add user to I2C bus

```bash
sudo usermod -aG i2c $USER
```

Start !

```bash
python main.py
```


Plusieurs gros changement structurels sont à faire. Actuellement, l'extraction de données se fait via des sensors avec protocole. Tous n'implémentent pas encore les bonnes méthode: commence par ça, ainsi que de nettoyer/fix les classes en erreurs.
Ensuite, on va changer la manière dont on va envoyer les données: les sensors seront tous utilisés dans une classe, qui contiendra un set de chaque Protocole, le but étant de faire la moyenne arithmétique d'un ensemble de capteur afin d'avoir des valeurs plus cohérentes et des valeurs à exporter unique (plus de plusieurs température etc); si le set ne contient qu'un seul élement, alors on garde la valeur, et on passe les objets en "DI like" comme actuellement, sous forme de tableau depuis le main. 
Cette nouvelle classe va permettre d'exporter les valeurs comme qui suit:

[
    {
        "<type de valeur (temperature etc)>":
            "raw": <valeur brute>,
            "smooth": <valeur lissé>,
            "score": <score associé, optionnel>
    },
    ...
    "score": <score global>
]

Voici la manière de calculer le score:
def calcul_score(temperature, humidite, co2, particules):

    # -------------------------
    # 1. SCORE HUMIDITE
    # -------------------------
    if 70 < humidite < 80:
        hscore = 80 - humidite

    elif 30 <= humidite <= 70:
        hscore = 10

    elif 20 < humidite < 30:
        hscore = humidite - 20

    else:
        hscore = 0


    # -------------------------
    # 2. SCORE CO2
    # -------------------------
    if 0 <= co2 < 2500:
        CO2score = 10

    elif 2500 <= co2 <= 4500:
        CO2score = (co2 - 4500) / -200

    else:
        CO2score = 0


    # -------------------------
    # 3. SCORE TEMPERATURE
    # -------------------------
    if 20 <= temperature <= 25:
        Tscore = 10

    elif 15 < temperature < 20:
        Tscore = 2 * (temperature - 15)

    elif 25 < temperature < 35:
        Tscore = 35 - temperature

    else:
        Tscore = 0


    # -------------------------
    # 4. SCORE PARTICULES
    # -------------------------
    if 0 <= particules < 25:
        Pscore = 10

    elif 25 <= particules < 35:
        Pscore = 35 - particules

    else:
        Pscore = 0


    # -------------------------
    # 5. SCORE FINAL
    # -------------------------
    indice_air = (
        (Tscore  0.8)
        + (CO2score  1)
        + (Pscore  1)
        + (hscore  0.8)
    ) / (0.8 + 1 + 1 + 0.8)

    return indice_air

Le but est d'ensuite envoyer les données via MQTT, et de les sauvegarder en JSON.
Je veux ABSOLUMENT que le code soit prore, clean architecture et pas de spaghetti. inspire toi de ce que j'ai déjà fait.

NB:
- Moyenne arithmétic en cas de multiple capteurs
- Score de l'humidité, particule, température, CO2
