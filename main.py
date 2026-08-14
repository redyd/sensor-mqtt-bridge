from core.mqtt_client import MqttClient
from core.command_receiver import CommandReceiver
from core.sensors_exporter import SensorsExporter
from utils.initializer import load_config, init_all_sensors
import time
import json


config = load_config()
sensors = init_all_sensors(config)

bme280_sensor = sensors["bme280"]
light_sensor = sensors["ltr559"]
microphone_sensor = sensors["sph0645"]
particulate_matter_sensor = sensors["pms5003"]
co2_sensor = sensors["scd30"]

command_receiver = CommandReceiver(
    temperature_sensor=bme280_sensor,
    pressure_sensor=bme280_sensor,
    humidity_sensor=bme280_sensor,
    light_sensor=light_sensor,
    microphone_sensor=microphone_sensor,
    particulate_matter_sensor=particulate_matter_sensor,
    co2_sensor=co2_sensor,
)

sensors_exporter = SensorsExporter(
    temperature_sensor=bme280_sensor,
    pressure_sensor=bme280_sensor,
    humidity_sensor=bme280_sensor,
    light_sensor=light_sensor,
    microphone_sensor=microphone_sensor,
    particulate_matter_sensor=particulate_matter_sensor,
    co2_sensor=co2_sensor,
)

MQTT_CLIENT = MqttClient(config["mqtt_broker"], config["mqtt_port"], command_receiver)
FETCH_INTERVAL_SECOND = config["update_interval"]

try:
    while True:
        data = sensors_exporter.export()
        
        print("\n" + "="*60)
        print("Sensor Data:")
        print("="*60)
        print(json.dumps(data, indent=2))
        print("="*60 + "\n")
        
        MQTT_CLIENT.send_data("sensors/data", data)
        print("Data sent to MQTT broker")
        print(f"Waiting {FETCH_INTERVAL_SECOND} seconds...\n")
        
        time.sleep(FETCH_INTERVAL_SECOND)
except KeyboardInterrupt:
    print("\n⛔ Terminating program...")
    MQTT_CLIENT.close()
