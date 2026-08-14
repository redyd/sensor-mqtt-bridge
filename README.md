# 🌡️ Sensor MQTT Bridge

Un pont d'intégration intelligent pour collecter, exporter et contrôler des capteurs environnementaux via MQTT. Parfait pour les projets IoT, la domotique et le monitoring d'environnement.

## ✨ Caractéristiques

- **🔌 Multi-capteurs** : Support de 7 types de capteurs différents
- **📡 Communication MQTT** : Intégration fluide avec les brokers MQTT
- **📊 Enregistrement des données** : Journalisation automatique en CSV
- **🎯 Commandes à distance** : Recevez et traitez les commandes via MQTT
- **🔄 Fallback automatique** : Bascule sur capteurs de test si un capteur échoue
- **⚙️ Architecture modulaire** : Facile à étendre avec de nouveaux capteurs

## 📦 Capteurs supportés

| Capteur | Type | Mesures |
|---------|------|---------|
| **BME280** | Température, Pression, Humidité | °C, hPa, % |
| **LTR559** | Luminosité | Lux |
| **SPH0645** | Microphone | dB |
| **PMS5003** | Particules fines | PM1.0, PM2.5, PM10 |
| **SCD30** | CO₂ | ppm |
| **Mock** | Capteur de test | Valeurs aléatoires |

## 🚀 Démarrage rapide

### Prérequis

- Python 3.7+
- `paho-mqtt` pour la communication MQTT
- Dépendances des capteurs (I2C, GPIO, etc.)

### Installation

```bash
# Cloner le projet
git clone <repo-url>
cd sensor-mqtt-bridge

# Installer les dépendances
pip install -r requirements.txt
```

**Alternative - Installation manuelle :**
```bash
pip install paho-mqtt bme280 smbus2 ltr559 pms5003 scd30-i2c numpy sounddevice
```

### Configuration

Modifiez l'adresse du broker MQTT dans `main.py` :

```python
mqtt_client = MqttClient("192.168.1.46", 1883, command_receiver)
```

### Lancement

```bash
python main.py
```

## 📋 Architecture

### Structure du projet

```
sensor-mqtt-bridge/
├── main.py                 # Point d'entrée principal
├── core/
│   ├── mqtt_client.py     # Gestion de la connexion MQTT
│   ├── command_receiver.py # Traitement des commandes
│   ├── sensors_exporter.py # Export et journalisation des données
│   └── sensors_definitions.py # Définitions des interfaces capteurs
├── sensors/               # Implémentations spécifiques des capteurs
│   ├── bme280_sensor.py
│   ├── ltr559_sensor.py
│   ├── sph0645_sensor.py
│   ├── pms5003_sensor.py
│   ├── scd30_sensor.py
│   └── lmt84_sensor.py
├── fakes/
│   └── mock_sensor.py     # Capteur de test pour développement
├── utils/
│   └── sliding_average.py # Utilitaires de traitement
└── data/
    └── sensors.csv        # Journal des mesures

```

## 🔄 Flux de données

```
┌─────────────────────────────────────────────────────────┐
│               Capteurs Physiques                         │
│  (BME280, LTR559, SPH0645, PMS5003, SCD30)              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  CommandReceiver       │
        │  (Collecte données)    │
        └────────┬───────────────┘
                 │
        ┌────────┴────────┬──────────────┐
        ▼                 ▼              ▼
    SensorsExporter   MqttClient   sensors.csv
    (Traitement)   (Transmission)  (Historique)
        │                 │
        └────────┬────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │   Broker MQTT        │
      │  (192.168.1.46:1883) │
      └──────────────────────┘
```

## 📡 Topics MQTT

### Publication

- **`capteurs/donnees`** : Données de tous les capteurs (JSON)
  ```json
  {
    "timestamp": "2026-08-14T10:30:45.123456",
    "temperature": 22.5,
    "pressure": 1013.25,
    "humidity": 45.6,
    "light": 450.2,
    "sound_level": 35.5,
    "particulate_matter": {"pm1_0": 5, "pm2_5": 8, "pm10": 12},
    "co2": 520.4
  }
  ```

### Souscription

Les topics de commande sont définis dans `CommandReceiver` pour un contrôle à distance.

## 🛠️ Extension

### Ajouter un nouveau capteur

1. Créer une nouvelle classe dans `sensors/mon_capteur.py` :

```python
class MonCapteur:
    def get_ma_mesure(self) -> float:
        # Implémentation
        return valeur
```

2. Ajouter le protocole dans `core/sensors_definitions.py`
3. Intégrer dans `main.py` et `SensorsExporter`

## 📊 Données enregistrées

Les données sont automatiquement journalisées en CSV avec les colonnes :
- `timestamp` : Date/heure ISO
- `temperature` : °C
- `pressure` : hPa
- `humidity` : %
- `light` : Lux
- `sound_level` : dB
- `particulate_matter` : JSON avec PM1.0, PM2.5, PM10
- `co2` : ppm

## 🔧 Configuration avancée

### Fréquence d'envoi

Modifiez le délai en secondes dans `main.py` :

```python
time.sleep(2)  # Intervalle de 2 secondes
```

### Chemin d'export CSV

Personnalisez dans `SensorsExporter` :

```python
sensors_exporter = SensorsExporter(
    # ...capteurs...
    path="/mon/chemin/custom.csv",
    write_every=1  # Écrire à chaque mesure
)
```

## 📝 Gestion des erreurs

Le système bascule automatiquement sur des capteurs de test si un capteur réel échoue :

```
BME280 indisponible (I2C error), capteur factice utilisé.
```

Cela permet au système de continuer à fonctionner même avec des capteurs défaillants.

## 🔗 Dépendances

Toutes les dépendances sont listées dans [`requirements.txt`](requirements.txt) :

| Paquet | Version | Description |
|--------|---------|-------------|
| `paho-mqtt` | 1.6.1 | Client MQTT |
| `bme280` | 0.0.6 | Capteur BME280 |
| `smbus2` | 0.4.1 | Communication I2C |
| `ltr559` | 1.0.5 | Capteur LTR559 |
| `pms5003` | 1.1 | Capteur PMS5003 |
| `scd30-i2c` | 0.0.18 | Capteur SCD30 |
| `numpy` | 1.24.3 | Calcul numérique |
| `sounddevice` | 0.4.5 | Capture audio SPH0645 |

## 📜 Licence

À définir selon vos préférences

## 👤 Auteur

Développé pour le monitoring intelligent d'environnement

---

**💡 Conseil** : Utilisez un dashboard MQTT comme Node-RED ou Grafana pour visualiser les données en temps réel !
