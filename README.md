# Sensor MQTT Bridge

Application Python de collecte de mesures environnementales, avec publication MQTT et journalisation CSV.

## Fonctionnement

L'application initialise les capteurs activés dans `config.json`, agrège les mesures disponibles, calcule un score de qualité d'air quand les données nécessaires sont présentes, puis:

- publie le payload JSON sur `sensors/data`;
- écrit les valeurs lissées dans `data/sensors.csv`;
- écoute des commandes MQTT pour modifier l'intervalle ou mettre la collecte en pause.

Capteurs pris en charge: BME280, LTR559, SPH0645, PMS5003, SCD30 et LMT84.

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Sur Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Sur Raspberry Pi, installer aussi les dépendances système utiles:

```bash
sudo apt update
sudo apt install -y python3-dev python3-venv i2c-tools libatlas-base-dev portaudio19-dev
sudo usermod -aG i2c $USER
```

Reconnecter la session après l'ajout au groupe `i2c`.

## Configuration

Modifier `config.json`:

```json
{
  "enabled_sensors": {
    "bme280": false,
    "ltr559": false,
    "sph0645": false,
    "pms5003": false,
    "scd30": false,
    "lmt84": false
  },
  "mqtt_broker": "192.168.1.46",
  "mqtt_port": 1883,
  "update_interval": 2
}
```

Si un capteur activé est indisponible ou mal branché, l'application s'arrête avec une erreur explicite. Avec tous les capteurs désactivés, des capteurs mock sont utilisés.

## Lancement

```bash
python main.py
```

Payload MQTT publié sur `sensors/data`:

```json
{
  "timestamp": "2026-08-17T12:00:00",
  "values": {
    "temperature": { "raw": 22.4, "smooth": 22.1, "score": 10 },
    "humidity": { "raw": 48.0, "smooth": 47.6, "score": 10 },
    "co2": { "raw": 620.0, "smooth": 610.0, "score": 10 }
  },
  "score": 10
}
```

## Commandes MQTT

- `commands/interval`: `{"command": "set_interval", "interval": 5}`
- `commands/pause`: `{"command": "toggle", "toggle": true}`

## Tests

```bash
pytest
```
