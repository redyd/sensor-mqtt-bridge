# Sensor MQTT Bridge

> A Python application that reads environmental sensors, publishes live data over MQTT, and logs smoothed measurements to CSV — designed for Raspberry Pi.

```
   ___     ___    _  _     ___     ___     ___              ___     ___     ___     ___     ___     ___
  / __|   | __|  | \| |   / __|   / _ \   | _ \     o O O  | _ )   | _ \   |_ _|   |   \   / __|   | __|
  \__ \   | _|   | .` |   \__ \  | (_) |  |   /    o       | _ \   |   /    | |    | |) | | (_ |   | _|
  |___/   |___|  |_|\_|   |___/   \___/   |_|_\   TS__[O]  |___/   |_|_\   |___|   |___/   \___|   |___|
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
```

---

## What it does

Each cycle, the bridge:

1. **Reads** all enabled sensors (temperature, pressure, humidity, light, sound, particulate matter, CO₂)
2. **Smooths** each reading with a sliding average to reduce noise
3. **Scores** air quality on a 0–10 scale from the four key metrics
4. **Publishes** a structured JSON payload to `sensors/data` over MQTT
5. **Logs** smoothed values and the global score to `data/sensors.csv`
6. **Listens** for MQTT commands to adjust the interval or pause collection

The terminal shows a live table with raw, smoothed, and score values for every sensor.

---

## Supported sensors

| Sensor | Measures | Interface |
|---|---|---|
| **BME280** | Temperature · Pressure · Humidity | I²C |
| **LTR559** | Ambient light | I²C |
| **SPH0645** | Sound level (RMS) | I²S / sounddevice |
| **PMS5003** | Particulate matter PM2.5 | UART |
| **SCD30** | CO₂ · Temperature · Humidity | I²C |
| **LMT84** | Temperature (analog) | SPI via MCP3008 |

Any disabled sensor is replaced by a **MockSensor** that generates random values in plausible ranges, so the app always runs — even on Windows or without hardware.

---

## Air quality score

Each key metric is scored individually from 0 to 10, then combined into a global score:

| Metric | Optimal range | Score |
|---|---|---|
| Temperature | 20–25 °C | 10 |
| Humidity | 30–70 % | 10 |
| CO₂ | < 2500 ppm | 10 |
| PM2.5 | < 25 µg/m³ | 10 |

**Global score** = weighted average of the four individual scores (temperature × 0.8, humidity × 0.8, CO₂ × 1, PM2.5 × 1), normalised to 10.

---

## MQTT payload

Published to `sensors/data` on every cycle:

```json
{
  "timestamp": "2026-08-17T12:00:00.123456",
  "values": {
    "temperature": { "raw": 22.4,  "smooth": 22.1,  "score": 10.0 },
    "pressure":    { "raw": 1013.2, "smooth": 1013.0 },
    "humidity":    { "raw": 48.0,  "smooth": 47.6,  "score": 10.0 },
    "light":       { "raw": 312.5, "smooth": 308.1 },
    "sound_level": { "raw": 0.031, "smooth": 0.028 },
    "particulate_matter": { "raw": 8.0, "smooth": 7.5, "score": 10.0 },
    "co2":         { "raw": 620.0, "smooth": 610.0, "score": 10.0 }
  },
  "score": 10.0
}
```

`score` fields only appear when all four required metrics (temperature, humidity, CO₂, PM2.5) are enabled.

---

## MQTT commands

Send JSON to these topics to control the bridge at runtime:

| Topic | Payload | Effect |
|---|---|---|
| `commands/interval` | `{"command": "set_interval", "interval": 5}` | Change the read/publish interval (seconds) |
| `commands/pause` | `{"command": "toggle", "toggle": true}` | Pause or resume data collection |

Both topics use **QoS 2** (exactly-once delivery).

---

## Node-RED dashboard

A `flows.json` is included for a ready-to-import Node-RED dashboard. It subscribes to `sensors/data` and displays live charts and gauges for all metrics, plus a pause button and an interval slider that publish to the command topics.

Import it via **Node-RED → Import → Select file**.

---

## Installation

### Raspberry Pi (recommended)

Install system dependencies first:

```bash
sudo apt update
sudo apt install -y python3-dev python3-venv i2c-tools libatlas-base-dev portaudio19-dev
sudo usermod -aG i2c $USER
# reconnect your session after this
```

Then set up the Python environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Windows (mock mode)

Hardware drivers are skipped automatically on Windows — all sensors run as MockSensors.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## Configuration

Edit `config.json` before running:

```json
{
  "enabled_sensors": {
    "bme280": true,
    "ltr559": true,
    "sph0645": true,
    "pms5003": true,
    "scd30": true,
    "lmt84": true
  },
  "mqtt_broker": "192.168.1.46",
  "mqtt_port": 1883,
  "update_interval": 2
}
```

If a sensor is set to `true` but is unreachable (not connected, missing driver), **the app exits immediately** with a clear error message and instructions to fix it.

---

## Running

```bash
source .venv/bin/activate
python main.py
```

Stop with **Ctrl+C** — the MQTT connection is closed cleanly.

---

## Tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers the scoring functions, sensor exporter aggregation logic, CSV output, and the initializer fallback behaviour — no hardware required.

---

## Project structure

```
SensorMqttBridge/
├── main.py                   # Entry point and terminal display
├── config.json               # Runtime configuration
├── flows.json                # Node-RED dashboard flows
├── core/
│   ├── air_quality_score.py  # Scoring functions (0–10 scale)
│   ├── command_receiver.py   # MQTT command dispatcher
│   ├── mqtt_client.py        # MQTT connection and publishing
│   ├── sensors_definitions.py# Protocol interfaces for all sensor types
│   ├── sensors_exporter.py   # Aggregation, scoring, and payload assembly
│   └── sensors_writer.py     # CSV logging
├── sensors/                  # Hardware sensor drivers
├── fakes/                    # MockSensor for testing and Windows
├── utils/
│   ├── initializer.py        # Config loading and sensor init
│   └── sliding_average.py    # Fixed-window sliding average
└── data/
    └── sensors.csv           # Written at runtime
```
