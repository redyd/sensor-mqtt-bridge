from core.mqtt_client import MqttClient
from core.command_receiver import CommandReceiver
from core.sensors_exporter import SensorsExporter
from sensors.bme280_sensor import Bme280Sensor
from sensors.ltr559_sensor import Ltr559Sensor
from sensors.sph0645_sensor import Sph0645Sensor
from sensors.pms5003_sensor import Pms5003Sensor
from sensors.scd30_sensor import Scd30Sensor
from fakes.mock_sensor import MockSensor
import time


def init_sensor(sensor_class, fallback):
    try:
        return sensor_class()
    except BaseException as error:
        print(f"{sensor_class.__name__} indisponible ({error}), capteur factice utilisé.")
        return fallback


mock = MockSensor()
bme280_sensor = init_sensor(Bme280Sensor, mock)
light_sensor = init_sensor(Ltr559Sensor, mock)
microphone_sensor = init_sensor(Sph0645Sensor, mock)
particulate_matter_sensor = init_sensor(Pms5003Sensor, mock)
co2_sensor = init_sensor(Scd30Sensor, mock)

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

mqtt_client = MqttClient("192.168.1.46", 1883, command_receiver)

try:
    while True:
        data = sensors_exporter.export()
        print("Données exportées")
        mqtt_client.send_data("capteurs/donnees", data)
        print("Données envoyées")
        print("En attente...")
        time.sleep(2)
except KeyboardInterrupt:
    print("Terminaison du programme...")
    mqtt_client.close()
