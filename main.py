from core.mqtt_client import MqttClient
from core.command_receiver import CommandReceiver
from core.sensors_exporter import SensorsExporter
from utils.initializer import load_config, init_all_sensors
import time
import os
import platform


BANNER = r'''                                                                            
   ___     ___    _  _     ___     ___     ___              ___     ___     ___     ___     ___     ___   
  / __|   | __|  | \| |   / __|   / _ \   | _ \     o O O  | _ )   | _ \   |_ _|   |   \   / __|   | __|  
  \__ \   | _|   | .` |   \__ \  | (_) |  |   /    o       | _ \   |   /    | |    | |) | | (_ |   | _|   
  |___/   |___|  |_|\_|   |___/   \___/   |_|_\   TS__[O]  |___/   |_|_\   |___|   |___/   \___|   |___|  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"

WIDTH = 58
SENSOR_KEYS = [
    "temperature",
    "pressure",
    "humidity",
    "light",
    "sound_level",
    "particulate_matter",
    "co2",
]


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def print_header(interval, broker, port):
    print(BANNER)
    print(f"{DIM}interval: {interval}s | broker: {broker}:{port}{RESET}")
    print(f"{CYAN}{'-' * WIDTH}{RESET}")


def print_sensors_table(raw_data, smooth_data):
    print(f"{BOLD}{'SENSOR':<20}{'RAW':>19}{'SMOOTH':>19}{RESET}")
    print(f"{CYAN}{'-' * WIDTH}{RESET}")

    for key in SENSOR_KEYS:
        raw_value = raw_data.get(key, "-")
        smooth_value = smooth_data.get(key, "-")

        if isinstance(raw_value, dict) or isinstance(smooth_value, dict):
            print(f"{key:<20}")
            sub_keys = raw_value.keys() if isinstance(raw_value, dict) else smooth_value.keys()
            for sub_key in sub_keys:
                sub_raw = raw_value.get(sub_key, "-") if isinstance(raw_value, dict) else "-"
                sub_smooth = smooth_value.get(sub_key, "-") if isinstance(smooth_value, dict) else "-"
                print(f"  {sub_key:<18}{str(sub_raw):>19}{str(sub_smooth):>19}")
        else:
            print(f"{key:<20}{str(raw_value):>19}{str(smooth_value):>19}")

    print(f"{CYAN}{'-' * WIDTH}{RESET}")


def print_send_status(send_ok):
    status_color = GREEN if send_ok else RED
    print(f"MQTT send: {status_color}{'OK' if send_ok else 'FAIL'}{RESET}")


def print_log(log_queue):
    print(f"\n{BOLD}LOG{RESET}")
    print(f"{CYAN}{'-' * WIDTH}{RESET}")
    for i, log in enumerate(log_queue):
        prefix = ">" if i == len(log_queue) - 1 else " "
        print(f" {prefix} {log}")


def send_sensor_data(mqtt_client, raw_data, smooth_data):
    result1 = mqtt_client.send_data("sensors/raw_data", raw_data)
    result2 = mqtt_client.send_data("sensors/smooth_data", smooth_data)
    return result1 and result2


config = load_config()
sensors = init_all_sensors(config)

bme280_sensor = sensors["bme280"]
light_sensor = sensors["ltr559"]
microphone_sensor = sensors["sph0645"]
particulate_matter_sensor = sensors["pms5003"]
co2_sensor = sensors["scd30"]
lmt84 = sensors["lmt84"]

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
    tension_temperature_sensor=lmt84,
    relative_temperature_sensor=bme280_sensor,
    pressure_sensor=bme280_sensor,
    humidity_sensor=bme280_sensor,
    light_sensor=light_sensor,
    microphone_sensor=microphone_sensor,
    particulate_matter_sensor=particulate_matter_sensor,
    co2_sensor=co2_sensor,
)

MQTT_CLIENT = MqttClient(config["mqtt_broker"], config["mqtt_port"], command_receiver)
FETCH_INTERVAL_SECOND = config["update_interval"]
log_queue = ["---", "---", "---"]

try:
    while True:
        data = sensors_exporter.export()
        raw_data = data["raw"]
        smooth_data = data["smooth"]

        clear_screen()
        print_header(FETCH_INTERVAL_SECOND, config["mqtt_broker"], config["mqtt_port"])
        print_sensors_table(raw_data, smooth_data)

        send_ok = send_sensor_data(MQTT_CLIENT, raw_data, smooth_data)
        print_send_status(send_ok)

        timestamp = time.strftime("%H:%M:%S")
        log_queue.pop(0)
        log_queue.append(f"Data sent at {timestamp}" if send_ok else f"Send failed at {timestamp}")

        print_log(log_queue)

        time.sleep(FETCH_INTERVAL_SECOND)
except KeyboardInterrupt:
    print("\nTerminating program...")
    MQTT_CLIENT.close()
    print("Done.")